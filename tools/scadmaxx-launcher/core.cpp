#include "core.h"
#include <QtCore>
#include <algorithm>
#ifdef Q_OS_WIN
#define NOMINMAX
#include <windows.h>
#include <shlwapi.h>
#include <shlobj.h>
#endif

Config::Config() {
    FileType scad; scad.id = "scad"; scad.name = "OpenSCAD"; scad.extensions = {".scad"};
    FileType maxx; maxx.id = "scadmaxx"; maxx.name = "SCADMaxx"; maxx.extensions = {".scadmaxx"};
    types = {scad, maxx};
}
QString normalizedExtension(QString value) {
    value = value.trimmed().toLower(); if (!value.startsWith('.')) value.prepend('.');
    static const QRegularExpression re("^\\.[a-z0-9][a-z0-9_-]*$");
    return re.match(value).hasMatch() ? value : QString();
}
QString pathKey(const QString &path) {
    if (path.isEmpty()) return {};
    QFileInfo f(path); QString result = QDir::cleanPath(f.exists() ? f.canonicalFilePath() : f.absoluteFilePath());
#ifdef Q_OS_WIN
    result = result.toCaseFolded();
#endif
    return result;
}
bool validExecutableName(const QString &name) {
    static const QRegularExpression re("^[^<>:\"/\\\\|?*]+\\.exe$", QRegularExpression::CaseInsensitiveOption);
    return name == name.trimmed() && re.match(name).hasMatch();
}
bool validExecutable(const QString &path, const QString &self) {
    QFileInfo info(path);
    return info.isAbsolute() && info.isFile() && info.isReadable() && info.size() > 0
        && info.suffix().compare("exe", Qt::CaseInsensitive) == 0 && pathKey(path) != pathKey(self);
}
bool excludedCollectionFolder(const QString &folder) {
    QString name = QFileInfo(folder).fileName().toLower();
    static const QSet<QString> excluded{"artifacts", ".artifacts", "runs", "source", "src", "build", "out", ".git",
        "vcpkg", "vcpkg_installed", "deptools", "dependencies", "vendor", "openscad-master"};
    return excluded.contains(name) || name.startsWith("wt-") || name.startsWith("test-vcpkg")
        || QFileInfo::exists(QDir(folder).filePath(".git"));
}
QString orderLabel(const QString &order) {
    if (order == "version") return "Version";
    if (order == "modified") return "Executable modified time";
    return "Build name / date";
}
int naturalCompare(QString a, QString b) {
    static const QRegularExpression tokens("[0-9]+|[^0-9]+");
    auto left = tokens.globalMatch(a.toCaseFolded()), right = tokens.globalMatch(b.toCaseFolded());
    while (left.hasNext() && right.hasNext()) {
        QString x = left.next().captured(), y = right.next().captured();
        if (x[0].isDigit() && y[0].isDigit()) {
            while (x.size() > 1 && x[0] == '0') x.remove(0, 1);
            while (y.size() > 1 && y[0] == '0') y.remove(0, 1);
            if (x.size() != y.size()) return x.size() < y.size() ? -1 : 1;
        }
        int cmp = QString::compare(x, y); if (cmp) return cmp;
    }
    return left.hasNext() ? 1 : right.hasNext() ? -1 : 0;
}
static QRegularExpression versionPattern("^([0-9]+(?:\\.[0-9]+)*)(?:[- ]?(dev|alpha|beta|rc)([0-9]*))?(?:[+-].*)?$",
    QRegularExpression::CaseInsensitiveOption);
bool knownVersion(const QString &version) { return versionPattern.match(version.trimmed()).hasMatch(); }
int versionCompare(const QString &a, const QString &b) {
    auto x = versionPattern.match(a.trimmed()), y = versionPattern.match(b.trimmed());
    if (!x.hasMatch() || !y.hasMatch()) return int(x.hasMatch()) - int(y.hasMatch());
    auto xn = x.captured(1).split('.'), yn = y.captured(1).split('.');
    for (int i = 0; i < qMax(xn.size(), yn.size()); ++i) {
        int cmp = naturalCompare(i < xn.size() ? xn[i] : "0", i < yn.size() ? yn[i] : "0");
        if (cmp) return cmp;
    }
    const QStringList stages{"dev", "alpha", "beta", "rc", ""};
    int cmp = stages.indexOf(x.captured(2).toLower()) - stages.indexOf(y.captured(2).toLower());
    return cmp ? cmp : naturalCompare(x.captured(3).isEmpty() ? "0" : x.captured(3), y.captured(3).isEmpty() ? "0" : y.captured(3));
}
static QString sidecarVersion(const QString &path) {
    QFile f(path); if (!f.open(QIODevice::ReadOnly) || f.size() > 1024 * 1024) return {};
    QXmlStreamReader xml(&f); QStringList stack; QMap<QString, QString> fields;
    while (!xml.atEnd()) {
        xml.readNext();
        if (xml.isDTD()) return {};
        if (xml.isStartElement()) {
            const auto tag = xml.name().toString();
            if (stack == QStringList{"version", "current"} &&
                QStringList{"major_version", "minor_version", "patchlevel", "identifier"}.contains(tag)) {
                if (fields.contains(tag)) return {};
                fields[tag] = xml.readElementText();
            } else stack.append(tag);
        } else if (xml.isEndElement() && !stack.isEmpty()) stack.removeLast();
    }
    if (xml.hasError() || fields.size() != 4) return {};
    QString version = fields["major_version"] + "." + fields["minor_version"] + "." + fields["patchlevel"];
    if (!fields["identifier"].isEmpty()) version += "-" + fields["identifier"];
    return knownVersion(version) ? version : QString();
}
static QString executableVersion(const QString &path) {
#ifdef Q_OS_WIN
    const auto native = QDir::toNativeSeparators(path).toStdWString(); DWORD unused = 0;
    DWORD size = GetFileVersionInfoSizeW(native.c_str(), &unused);
    if (size > 0 && size < 16 * 1024 * 1024) {
        QByteArray data(size, '\0');
        if (GetFileVersionInfoW(native.c_str(), 0, size, data.data())) {
            struct Translation { WORD language, codepage; }; Translation *tr = nullptr; UINT length = 0;
            if (VerQueryValueW(data.data(), L"\\VarFileInfo\\Translation", reinterpret_cast<void **>(&tr), &length)) {
                for (UINT i = 0; i < length / sizeof(Translation); ++i) {
                    const auto key = QString("\\StringFileInfo\\%1%2\\ProductVersion")
                        .arg(tr[i].language, 4, 16, QChar('0')).arg(tr[i].codepage, 4, 16, QChar('0')).toStdWString();
                    wchar_t *text = nullptr; UINT count = 0;
                    if (VerQueryValueW(data.data(), key.c_str(), reinterpret_cast<void **>(&text), &count) && count) {
                        const auto value = QString::fromWCharArray(text).trimmed(); if (knownVersion(value)) return value;
                    }
                }
            }
            VS_FIXEDFILEINFO *v = nullptr;
            if (VerQueryValueW(data.data(), L"\\", reinterpret_cast<void **>(&v), &length)
                && length >= sizeof(VS_FIXEDFILEINFO) && v->dwSignature == 0xfeef04bd)
                return QString("%1.%2.%3.%4").arg(HIWORD(v->dwFileVersionMS)).arg(LOWORD(v->dwFileVersionMS))
                    .arg(HIWORD(v->dwFileVersionLS)).arg(LOWORD(v->dwFileVersionLS));
        }
    }
#else
    Q_UNUSED(path);
#endif
    return {};
}
BuildCache::BuildCache(QString file) : file(std::move(file)) {
    QFile f(this->file); if (f.open(QIODevice::ReadOnly) && f.size() < 8 * 1024 * 1024)
        entries = QJsonDocument::fromJson(f.readAll()).object();
}
Build BuildCache::describe(const QString &path) {
    QFileInfo info(path); QDir folder = info.dir(); if (folder.dirName().compare("bin", Qt::CaseInsensitive) == 0) folder.cdUp();
    if (folder.dirName().compare("staging", Qt::CaseInsensitive) == 0) folder.cdUp();
    QString buildName = folder.dirName();
    if (buildName.startsWith("attempt-", Qt::CaseInsensitive)) {
        QDir release = folder; if (release.cdUp()) buildName = release.dirName() + " / " + buildName;
    }
    Build b{info.absoluteFilePath(), buildName + " / " + info.fileName(), {}, info.lastModified().toMSecsSinceEpoch()};
    const QString sidecar = info.dir().filePath("version.xml"); QFileInfo xml(sidecar);
    const QString fingerprint = QString("%1:%2:%3:%4").arg(info.size()).arg(b.modified).arg(xml.size()).arg(xml.lastModified().toMSecsSinceEpoch());
    const auto key = pathKey(path); const auto cached = entries.value(key).toObject();
    if (cached["fingerprint"].toString() == fingerprint && cached["version"].isString()) b.version = cached["version"].toString();
    else {
        ++metadataReads; b.version = sidecarVersion(sidecar); if (b.version.isEmpty()) b.version = executableVersion(path);
        entries[key] = QJsonObject{{"fingerprint", fingerprint}, {"version", b.version}};
    }
    return b;
}
void BuildCache::save() {
    if (file.isEmpty() || !QDir().mkpath(QFileInfo(file).absolutePath())) return;
    QLockFile lock(file + ".lock"); if (!lock.tryLock(0)) return;
    // Cache writes are best-effort and independent from configuration writes.
    while (entries.size() > 4096) entries.erase(entries.begin());
    QSaveFile out(file); if (out.open(QIODevice::WriteOnly)) {
        const auto bytes = QJsonDocument(entries).toJson(QJsonDocument::Compact);
        if (out.write(bytes) == bytes.size()) out.commit();
    }
}
ScanResult scanType(const FileType &type, BuildCache &cache, const QString &self) {
    ScanResult result; QSet<QString> seen, excluded;
    for (const auto &p : type.excludedBuilds) excluded.insert(pathKey(p));
    auto add = [&](const QString &p, QVector<Build> *source) {
        const auto key = pathKey(p);
        if (excluded.contains(key) || !validExecutable(p, self)) return;
        auto build = cache.describe(p);
        if (source) {
            bool duplicate = false; for (const auto &b : *source) duplicate |= pathKey(b.path) == key;
            if (!duplicate) source->append(build);
        }
        if (!seen.contains(key)) { seen.insert(key); result.builds.append(build); }
    };
    for (const auto &source : type.sources) {
        auto &builds = result.sources[source.id];
        if (!QDir(source.folder).exists()) { result.warnings.append("Folder unavailable: " + source.folder); continue; }
        QStringList dirs{source.folder};
        if (source.collection) {
            const auto children = QDir(source.folder).entryInfoList(QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
            for (const auto &child : children) if (!excludedCollectionFolder(child.absoluteFilePath())) dirs.append(child.absoluteFilePath());
        }
        const auto roots = dirs;
        for (const auto &dir : roots) {
            const auto bin = QDir(dir).filePath("bin");
            if (!QFileInfo(bin).isSymLink()) dirs.append(bin);
            const auto staging = QDir(dir).filePath("staging");
            if (QFileInfo(staging).isDir() && !QFileInfo(staging).isSymLink()) {
                dirs.append(staging);
                const auto stagingBin = QDir(staging).filePath("bin");
                if (!QFileInfo(stagingBin).isSymLink()) dirs.append(stagingBin);
            }
        }
        for (const auto &dir : dirs) {
            const auto candidate = QDir(dir).filePath(source.executable);
            if (!QFileInfo(candidate).isSymLink()) add(candidate, &builds);
        }
        if (builds.isEmpty()) result.warnings.append("No eligible " + source.executable + " found in "
            + QDir::toNativeSeparators(source.folder) + ". Check the executable name and scan scope.");
    }
    for (const auto &path : type.explicitBuilds) add(path, nullptr);
    if (!type.fixed.isEmpty()) add(type.fixed, nullptr);
    std::sort(result.builds.begin(), result.builds.end(), [](const Build &a, const Build &b){ return naturalCompare(a.name, b.name) < 0; });
    return result;
}
static QString buildDate(const Build &build) {
    static const QRegularExpression re("(?<![0-9])(20[0-9]{2})[._-]?([01][0-9])[._-]?([0-3][0-9])(?![0-9])");
    auto m = re.match(build.name); if (!m.hasMatch()) return {};
    QDate date(m.captured(1).toInt(), m.captured(2).toInt(), m.captured(3).toInt());
    return date.isValid() ? date.toString("yyyyMMdd") : QString();
}
Resolution resolveDefault(const FileType &type, const ScanResult &scan, const QString &self) {
    if (type.mode == "fixed") {
        if (validExecutable(type.fixed, self)) return {type.fixed, "Fixed executable", true};
        return {{}, "Choose an available executable. Selected path: " + (type.fixed.isEmpty() ? "(none)" : type.fixed), false};
    }
    auto builds = scan.sources.value(type.sourceId);
    builds.erase(std::remove_if(builds.begin(), builds.end(), [&](const Build &b){
        return !validExecutable(b.path, self) || (type.order == "version" && !knownVersion(b.version));
    }), builds.end());
    if (builds.isEmpty()) return {{}, type.order == "version" ? "No available builds with a readable version in the selected source. Choose another ordering mode or build." : "No available builds in the selected source. Check its folder and executable name.", false};
    auto less = [&](const Build &a, const Build &b) {
        int cmp = 0;
        if (type.order == "modified") cmp = a.modified < b.modified ? -1 : a.modified > b.modified ? 1 : 0;
        else if (type.order == "version") cmp = versionCompare(a.version, b.version);
        else {
            const auto x = buildDate(a), y = buildDate(b);
            if (!x.isEmpty() && !y.isEmpty()) cmp = QString::compare(x, y);
            else if (x.isEmpty() != y.isEmpty()) cmp = x.isEmpty() ? -1 : 1;
            if (!cmp) cmp = naturalCompare(a.name, b.name);
        }
        return cmp ? cmp < 0 : pathKey(a.path) < pathKey(b.path);
    };
    const auto winner = *std::max_element(builds.begin(), builds.end(), less);
    return {winner.path, "Latest by " + orderLabel(type.order).toLower() + ": " + winner.name
        + (winner.version.isEmpty() ? "" : " · " + winner.version), true};
}
const FileType *typeForFile(const Config &config, const QString &file) {
    const auto ext = "." + QFileInfo(file).suffix().toLower();
    for (const auto &t : config.types) if (t.extensions.contains(ext)) return &t;
    return nullptr;
}
bool validateConfig(const Config &config, QString &error) {
    QSet<QString> ids, extensions;
    for (const auto &t : config.types) {
        if (t.id.isEmpty() || ids.contains(t.id) || t.name.trimmed().isEmpty() || t.extensions.isEmpty()) { error = "Each file type needs a unique ID, name and extensions."; return false; }
        ids.insert(t.id);
        for (const auto &e : t.extensions) {
            if (e != normalizedExtension(e) || extensions.contains(e)) { error = "Invalid or duplicate extension: " + e; return false; }
            extensions.insert(e);
        }
        QSet<QString> sources;
        for (const auto &s : t.sources) {
            if (s.id.isEmpty() || sources.contains(s.id) || !QFileInfo(s.folder).isAbsolute() || !validExecutableName(s.executable)) {
                error = "Each search folder needs an absolute path and executable filename (for example scadmaxx.exe)."; return false;
            }
            sources.insert(s.id);
        }
        if (!QStringList{"fixed", "latest"}.contains(t.mode) || !QStringList{"name", "version", "modified"}.contains(t.order)
            || (t.mode == "latest" && !sources.contains(t.sourceId))) { error = "Choose a valid source and ordering for Latest."; return false; }
        QStringList paths = t.explicitBuilds + t.excludedBuilds; if (!t.fixed.isEmpty()) paths.append(t.fixed);
        for (const auto &p : paths) if (!QFileInfo(p).isAbsolute()) { error = "Build paths must be absolute."; return false; }
        if (!t.fixed.isEmpty()) for (const auto &p : t.excludedBuilds) if (pathKey(p) == pathKey(t.fixed)) { error = "Change the fixed selection before excluding it."; return false; }
    }
    return true;
}
QJsonObject configJson(const Config &config) {
    QJsonArray types;
    for (const auto &t : config.types) {
        QJsonArray sources;
        for (const auto &s : t.sources) sources.append(QJsonObject{{"id", s.id}, {"folder", s.folder}, {"executable", s.executable}, {"collection", s.collection}});
        types.append(QJsonObject{{"id", t.id}, {"name", t.name}, {"extensions", QJsonArray::fromStringList(t.extensions)},
            {"sources", sources}, {"explicitBuilds", QJsonArray::fromStringList(t.explicitBuilds)}, {"excludedBuilds", QJsonArray::fromStringList(t.excludedBuilds)},
            {"mode", t.mode}, {"fixed", t.fixed}, {"sourceId", t.sourceId}, {"order", t.order}});
    }
    return {{"schema", 2}, {"types", types}, {"ask", config.ask}, {"tray", config.tray}, {"startup", config.startup}, {"scanOnStartup", config.scanOnStartup}};
}
bool readConfig(const QString &file, Config &config, QString &error) {
    if (!QFileInfo::exists(file)) { config = Config(); return true; }
    QFile in(file); if (!in.open(QIODevice::ReadOnly)) { error = in.errorString(); return false; }
    auto doc = QJsonDocument::fromJson(in.readAll()); auto obj = doc.object();
    if (!doc.isObject() || obj["schema"].toInt() != 2 || !obj["types"].isArray()) {
        error = "Settings are damaged or use an older format. The original file has been preserved."; return false;
    }
    Config next; next.types.clear();
    bool valid = true;
    auto strings = [&](const QJsonValue &v) { QStringList list; if (!v.isArray()) valid = false;
        for (const auto &item : v.toArray()) { if (!item.isString()) valid = false; list.append(item.toString()); } return list; };
    for (const auto &value : obj["types"].toArray()) {
        auto o = value.toObject(); FileType t;
        for (const auto &key : {"id", "name", "mode", "fixed", "sourceId", "order"}) if (!o[key].isString()) valid = false;
        t.id = o["id"].toString(); t.name = o["name"].toString(); t.mode = o["mode"].toString(); t.fixed = o["fixed"].toString();
        t.sourceId = o["sourceId"].toString(); t.order = o["order"].toString(); t.extensions = strings(o["extensions"]);
        t.explicitBuilds = strings(o["explicitBuilds"]); t.excludedBuilds = strings(o["excludedBuilds"]);
        if (!o["sources"].isArray()) valid = false;
        for (const auto &sv : o["sources"].toArray()) {
            auto s = sv.toObject();
            for (const auto &key : {"id", "folder", "executable"}) if (!s[key].isString()) valid = false;
            if (!s["collection"].isBool()) valid = false;
            t.sources.append({s["id"].toString(), s["folder"].toString(), s["executable"].toString(), s["collection"].toBool()});
        }
        next.types.append(t);
    }
    for (const auto &key : {"ask", "tray", "startup", "scanOnStartup"}) if (!obj[key].isBool()) valid = false;
    next.ask = obj["ask"].toBool(); next.tray = obj["tray"].toBool(); next.startup = obj["startup"].toBool(); next.scanOnStartup = obj["scanOnStartup"].toBool();
    if (!valid) { error = "Invalid settings fields. Original file preserved."; return false; }
    if (!validateConfig(next, error)) return false;
    config = next; return true;
}
bool writeConfig(const QString &file, const Config &config, QString &error) {
    if (!validateConfig(config, error)) return false;
    if (!QDir().mkpath(QFileInfo(file).absolutePath())) { error = "Cannot create settings directory."; return false; }
    QSaveFile out(file); if (!out.open(QIODevice::WriteOnly)) { error = out.errorString(); return false; }
    auto bytes = QJsonDocument(configJson(config)).toJson();
    if (out.write(bytes) != bytes.size() || !out.commit()) { error = out.errorString(); return false; }
    return true;
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

bool writeHandlerRegistration(QSettings &registry, const Config &config, const QString &executable, QString &error) {
    if (!validateConfig(config, error)) return false;
    if (config.types.isEmpty() || !validExecutable(executable, {})) {
        error = "Configure at least one file type and use an installed launcher executable before Windows setup."; return false;
    }
    const QString exe = QDir::toNativeSeparators(QFileInfo(executable).absoluteFilePath());
    const QString command = '"' + exe + "\" --open \"%1\"";
    const QString icon = '"' + exe + "\",0";
    const QString appName = "SCADMaxx Launcher";
    const QString capabilities = "SCADMaxx/Launcher/Capabilities";
    const QString app = "Classes/Applications/" + QFileInfo(executable).fileName();
    const QString appPath = "Microsoft/Windows/CurrentVersion/App Paths/" + QFileInfo(executable).fileName();
    QMap<QString, QString> expected;
    auto put = [&](const QString &key, const QString &value) { registry.setValue(key, value); expected[key] = value; };
    // Advertise the executable itself as well as the per-extension ProgIDs. Windows uses the
    // Applications identity for its Open With/default-app chooser and the capabilities for the app page.
    put(app + "/FriendlyAppName", appName);
    put(app + "/DefaultIcon/.", icon);
    put(app + "/shell/open/command/.", command);
    put(appPath + "/.", exe);
    registry.remove(app + "/SupportedTypes");
    registry.remove(capabilities + "/FileAssociations");
    put(capabilities + "/ApplicationName", appName);
    put(capabilities + "/ApplicationDescription", "Open SCAD files with your selected editor build");
    put(capabilities + "/ApplicationIcon", icon);
    for (const auto &type : config.types) for (const auto &extension : type.extensions) {
        const QString progId = "SCADMaxx.Launcher" + extension;
        const QString base = "Classes/" + progId;
        put(base + "/.", type.name + " document (" + extension + ")");
        put(base + "/DefaultIcon/.", icon);
        put(base + "/shell/.", "open");
        put(base + "/shell/open/command/.", command);
        put(base + "/Application/ApplicationName", appName);
        put(base + "/Application/ApplicationDescription", "Open with your selected editor build");
        put(base + "/Application/ApplicationIcon", icon);
        put("Classes/" + extension + "/OpenWithProgids/" + progId, QString());
        put(app + "/SupportedTypes/" + extension, QString());
        put(capabilities + "/FileAssociations/" + extension, progId);
    }
    // Publish after the class/application records exist. Never write extension defaults or UserChoice.
    registry.sync();
    if (registry.status() != QSettings::NoError) { error = "Could not register launcher file types for this user."; return false; }
    put("RegisteredApplications/" + appName, "Software\\SCADMaxx\\Launcher\\Capabilities");
    registry.sync();
    if (registry.status() != QSettings::NoError) { error = "Could not publish the launcher to Windows Default Apps."; return false; }
    for (auto it = expected.cbegin(); it != expected.cend(); ++it) {
        if (!registry.contains(it.key()) || registry.value(it.key()).toString() != it.value()) {
            error = "Windows registration could not be verified: " + it.key(); return false;
        }
    }
    return true;
}
bool registerHandlers(const Config &config, const QString &executable, QString &error) {
#ifdef Q_OS_WIN
    QSettings registry("HKEY_CURRENT_USER\\Software", QSettings::NativeFormat);
    if (!writeHandlerRegistration(registry, config, executable, error)) return false;
    SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST | SHCNF_FLUSH, nullptr, nullptr);
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
