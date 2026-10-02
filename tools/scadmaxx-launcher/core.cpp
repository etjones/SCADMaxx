#include "core.h"
#include <QCoreApplication>
#include <QDir>
#include <QDirIterator>
#include <QFile>
#include <QFileInfo>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QRegularExpression>
#include <QSaveFile>
#include <QSet>
#include <QSettings>
#include <QStandardPaths>
#include <QThread>
#include <algorithm>
#ifdef Q_OS_WIN
#define NOMINMAX
#include <windows.h>
#include <shlwapi.h>
#include <shlobj.h>
#endif

QString normalizedExtension(QString value) {
    value = value.trimmed().toLower();
    if (!value.startsWith('.')) value.prepend('.');
    static const QRegularExpression pattern("^\\.[a-z0-9][a-z0-9_-]*$");
    return pattern.match(value).hasMatch() ? value : QString();
}

QString pathKey(const QString &path) {
    if (path.isEmpty()) return {};
    QFileInfo file(path);
    QString result = file.exists() ? file.canonicalFilePath() : file.absoluteFilePath();
    result = QDir::cleanPath(result);
#ifdef Q_OS_WIN
    result = result.toCaseFolded();
#endif
    return result;
}

bool validExecutable(const QString &path, const QString &self) {
    QFileInfo info(path);
    return info.isAbsolute() && info.isFile() && info.suffix().compare("exe", Qt::CaseInsensitive) == 0
        && pathKey(path) != pathKey(self) && info.isReadable();
}

Build describeBuild(const QString &path) {
    QFileInfo info(path);
    Build build{info.absoluteFilePath(), info.dir().dirName() + " / " + info.fileName(), {}};
#ifdef Q_OS_WIN
    const auto native = QDir::toNativeSeparators(build.path).toStdWString();
    DWORD unused = 0;
    const DWORD size = GetFileVersionInfoSizeW(native.c_str(), &unused);
    if (size > 0 && size < 16 * 1024 * 1024) {
        QByteArray data(static_cast<qsizetype>(size), '\0');
        if (GetFileVersionInfoW(native.c_str(), 0, size, data.data())) {
            VS_FIXEDFILEINFO *version = nullptr; UINT length = 0;
            if (VerQueryValueW(data.data(), L"\\", reinterpret_cast<void **>(&version), &length)
                && length >= sizeof(VS_FIXEDFILEINFO) && version->dwSignature == 0xfeef04bd) {
                build.version = QString("%1.%2.%3.%4").arg(HIWORD(version->dwFileVersionMS))
                    .arg(LOWORD(version->dwFileVersionMS)).arg(HIWORD(version->dwFileVersionLS))
                    .arg(LOWORD(version->dwFileVersionLS));
            }
        }
    }
#endif
    return build;
}

bool excludedCollectionFolder(const QString &folder) {
    const QString name = QFileInfo(folder).fileName().toLower();
    static const QSet<QString> excluded{"artifacts", "runs", "source", "src", "build", "out",
        "vcpkg", "vcpkg_installed", "deptools", "dependencies", "vendor", "openscad-master", "scadmaxx", ".git"};
    return excluded.contains(name) || name.startsWith("wt-") || name.startsWith("test-vcpkg")
        || QFileInfo::exists(QDir(folder).filePath(".git"));
}

static QVector<Build> discoverDirectories(const QStringList &directories) {
    QVector<Build> result; QSet<QString> seen;
    for (const auto &folder : directories) {
        QDirIterator it(folder, QDir::Files | QDir::NoSymLinks);
        while (it.hasNext()) {
            it.next();
            if (QThread::currentThread()->isInterruptionRequested()) return result;
            const auto info = it.fileInfo();
            const QString name = info.fileName().toLower();
            if (name != "openscad.exe" && name != "scadmaxx.exe" && name != "scadmax.exe") continue;
            const auto key = pathKey(info.absoluteFilePath());
            if (!seen.contains(key)) { seen.insert(key); result.append(describeBuild(info.absoluteFilePath())); }
        }
    }
    std::sort(result.begin(), result.end(), [](const Build &a, const Build &b){ return a.path < b.path; });
    return result;
}

QVector<Build> discover(const QStringList &folders) {
    QStringList directories;
    for (const auto &folder : folders) {
        if (excludedCollectionFolder(folder)) continue;
        directories.append(folder);
        const auto children = QDir(folder).entryInfoList(QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
        for (const auto &child : children)
            if (!excludedCollectionFolder(child.absoluteFilePath())) directories.append(child.absoluteFilePath());
    }
    return discoverDirectories(directories);
}

QVector<Build> discoverInstalled(const QString &folder) {
    // An explicitly chosen installation may be inside an otherwise excluded workspace folder.
    return discoverDirectories({folder, QDir(folder).filePath("bin")});
}

bool applyBuildReview(Config &config, const QVector<Build> &candidates, const QStringList &selected,
                      const QStringList &protectedPaths, QString &error) {
    QSet<QString> selectedKeys, protectedKeys;
    for (const auto &path : selected) selectedKeys.insert(pathKey(path));
    for (const auto &path : protectedPaths) if (!path.isEmpty()) protectedKeys.insert(pathKey(path));
    for (const auto &path : config.mappings) if (!path.isEmpty()) protectedKeys.insert(pathKey(path));
    for (const auto &b : candidates) {
        if (!selectedKeys.contains(pathKey(b.path)) && protectedKeys.contains(pathKey(b.path))) {
            error = "Change the extension mapping before excluding its selected build."; return false;
        }
    }
    Config next = config;
    for (const auto &b : candidates) {
        const auto key = pathKey(b.path);
        next.excludedBuilds.removeAll(key);
        if (selectedKeys.contains(key)) mergeBuilds(next, {b});
        else {
            next.excludedBuilds.append(key);
            next.builds.erase(std::remove_if(next.builds.begin(), next.builds.end(),
                [&](const Build &current){return pathKey(current.path) == key;}), next.builds.end());
        }
    }
    config = next; return true;
}

void mergeBuilds(Config &config, const QVector<Build> &found) {
    for (const auto &build : found) {
        auto it = std::find_if(config.builds.begin(), config.builds.end(), [&](const Build &b){
            return pathKey(b.path) == pathKey(build.path);
        });
        if (it == config.builds.end()) config.builds.append(build);
        else it->version = build.version;
    }
}

bool readConfig(const QString &file, Config &config, QString &error) {
    if (!QFileInfo::exists(file)) { config = Config(); return true; }
    QFile input(file);
    if (!input.open(QIODevice::ReadOnly)) { error = input.errorString(); return false; }
    QJsonParseError parse;
    const auto doc = QJsonDocument::fromJson(input.readAll(), &parse);
    if (parse.error != QJsonParseError::NoError || !doc.isObject()) {
        error = "Cannot read settings: " + parse.errorString(); return false;
    }
    const auto obj = doc.object();
    if (obj.value("schema").toInt() != 1 || !obj.value("mappings").isObject()
        || !obj.value("builds").isArray() || !obj.value("folders").isArray()) {
        error = "Unsupported or incomplete settings file. Original file has been preserved."; return false;
    }
    Config next; next.mappings.clear();
    const auto mappings = obj.value("mappings").toObject();
    for (auto it = mappings.begin(); it != mappings.end(); ++it) {
        if (normalizedExtension(it.key()) != it.key() || !it.value().isString()) {
            error = "Invalid extension mapping in settings."; return false;
        }
        next.mappings.insert(it.key(), it.value().toString());
    }
    for (const auto &value : obj.value("builds").toArray()) {
        auto b = value.toObject();
        if (!QFileInfo(b.value("path").toString()).isAbsolute()) { error = "Invalid build path."; return false; }
        next.builds.append({b.value("path").toString(), b.value("name").toString(), b.value("version").toString()});
    }
    for (const auto &value : obj.value("folders").toArray()) {
        if (!value.isString() || !QFileInfo(value.toString()).isAbsolute()) { error = "Invalid search folder."; return false; }
        next.folders.append(value.toString());
    }
    next.tray = obj.value("tray").toBool(true);
    next.startup = obj.value("startup").toBool(false);
    next.scanOnStartup = obj.value("scanOnStartup").toBool(false);
    if (obj.contains("excludedBuilds") && !obj.value("excludedBuilds").isArray()) {
        error = "Invalid excluded builds list."; return false;
    }
    for (const auto &value : obj.value("excludedBuilds").toArray()) {
        if (!value.isString() || !QFileInfo(value.toString()).isAbsolute()) { error = "Invalid excluded build path."; return false; }
        next.excludedBuilds.append(pathKey(value.toString()));
    }
    config = next; return true;
}

bool writeConfig(const QString &file, const Config &config, QString &error) {
    QJsonObject mappings; QJsonArray builds, folders, excluded;
    for (auto it = config.mappings.begin(); it != config.mappings.end(); ++it) mappings.insert(it.key(), it.value());
    for (const auto &b : config.builds) builds.append(QJsonObject{{"path", b.path}, {"name", b.name}, {"version", b.version}});
    for (const auto &f : config.folders) folders.append(f);
    for (const auto &path : config.excludedBuilds) excluded.append(path);
    const QJsonObject obj{{"schema", 1}, {"mappings", mappings}, {"builds", builds}, {"folders", folders},
                         {"tray", config.tray}, {"startup", config.startup}, {"scanOnStartup", config.scanOnStartup},
                         {"excludedBuilds", excluded}};
    if (!QDir().mkpath(QFileInfo(file).absolutePath())) { error = "Cannot create settings directory."; return false; }
    QSaveFile output(file);
    if (!output.open(QIODevice::WriteOnly)) { error = output.errorString(); return false; }
    const auto bytes = QJsonDocument(obj).toJson();
    if (output.write(bytes) != bytes.size() || !output.commit()) { error = output.errorString(); return false; }
    return true;
}

bool resolveOpen(const Config &config, const QString &file, const QString &self,
                 QString &program, QStringList &arguments, QString &error) {
    const QFileInfo info(file);
    if (!info.isFile()) { error = "File not found: " + file; return false; }
    const auto ext = "." + info.suffix().toLower();
    program = config.mappings.value(ext);
    if (!validExecutable(program, self)) {
        error = "Choose an available build for " + ext + " in SCADMaxx Launcher.\nSelected path: "
            + (program.isEmpty() ? "(none)" : program); return false;
    }
    arguments = QStringList{info.absoluteFilePath()}; return true;
}

QString configLocation() {
    return QStandardPaths::writableLocation(QStandardPaths::AppLocalDataLocation) + "/settings.json";
}

bool setStartup(bool enabled, const QString &executable, QString &error) {
#ifdef Q_OS_WIN
    QSettings run("HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", QSettings::NativeFormat);
    if (enabled) run.setValue("SCADMaxxLauncher", '"' + QDir::toNativeSeparators(executable) + "\" --tray");
    else run.remove("SCADMaxxLauncher");
    run.sync();
    if (run.status() != QSettings::NoError) { error = "Could not update sign-in startup."; return false; }
    return true;
#else
    Q_UNUSED(enabled); Q_UNUSED(executable); error = "Windows is required."; return false;
#endif
}

bool registerHandlers(const Config &config, const QString &executable, QString &error) {
#ifdef Q_OS_WIN
    QSettings registry("HKEY_CURRENT_USER\\Software", QSettings::NativeFormat);
    const QString exe = QDir::toNativeSeparators(executable);
    const QString capabilities = "SCADMaxx/Launcher/Capabilities";
    registry.setValue(capabilities + "/ApplicationName", "SCADMaxx Launcher");
    registry.setValue(capabilities + "/ApplicationDescription", "Open SCAD files with your selected build");
    registry.remove(capabilities + "/FileAssociations");
    for (auto it = config.mappings.begin(); it != config.mappings.end(); ++it) {
        const QString progId = "SCADMaxx.Launcher" + it.key();
        const QString base = "Classes/" + progId;
        registry.setValue(base + "/.", "SCAD source (" + it.key() + ")");
        registry.setValue(base + "/DefaultIcon/.", '"' + exe + "\",0");
        registry.setValue(base + "/shell/open/command/.", '"' + exe + "\" --open \"%1\"");
        registry.setValue("Classes/" + it.key() + "/OpenWithProgids/" + progId, QString());
        registry.setValue(capabilities + "/FileAssociations/" + it.key(), progId);
    }
    registry.setValue("RegisteredApplications/SCADMaxx Launcher", "Software\\SCADMaxx\\Launcher\\Capabilities");
    registry.sync();
    if (registry.status() != QSettings::NoError) { error = "Could not register file handlers for this user."; return false; }
    SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, nullptr, nullptr);
    return true;
#else
    Q_UNUSED(config); Q_UNUSED(executable); error = "Windows is required."; return false;
#endif
}

bool isDefaultHandler(const QString &extension, const QString &executable) {
#ifdef Q_OS_WIN
    DWORD count = 32768; QVector<wchar_t> value(count);
    const auto ext = extension.toStdWString();
    if (SUCCEEDED(AssocQueryStringW(ASSOCF_NONE, ASSOCSTR_EXECUTABLE, ext.c_str(), L"open", value.data(), &count)))
        return pathKey(QString::fromWCharArray(value.constData())) == pathKey(executable);
#else
    Q_UNUSED(extension); Q_UNUSED(executable);
#endif
    return false;
}
