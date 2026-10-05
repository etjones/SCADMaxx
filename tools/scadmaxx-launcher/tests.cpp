#include "core.h"
#include <QtTest>
#include <QtCore>

class CoreTests : public QObject {
    Q_OBJECT
    static void touch(const QString &path, const QByteArray &bytes = "fixture") {
        QDir().mkpath(QFileInfo(path).absolutePath()); QFile f(path); QVERIFY(f.open(QIODevice::WriteOnly)); f.write(bytes);
    }
    static void version(const QString &directory, const QString &patch, const QString &identifier = {}) {
        touch(QDir(directory).filePath("version.xml"), QString("<version><current><major_version>1</major_version><minor_version>2</minor_version><patchlevel>%1</patchlevel><identifier>%2</identifier></current></version>").arg(patch,identifier).toUtf8());
    }
    static FileType collection(const QString &folder, const QString &exe = "openscad.exe") {
        FileType t; t.id="test"; t.name="Test"; t.extensions={".scad"}; t.sources={{"source",folder,exe,true}};
        t.mode="latest"; t.sourceId="source"; return t;
    }
private slots:
    void windowsRegistrationIsCompleteAndPreservesDefaults() {
#ifdef Q_OS_WIN
        const auto branch = "HKEY_CURRENT_USER\\Software\\SCADMaxxLauncherRegistrationTests\\" + QUuid::createUuid().toString(QUuid::WithoutBraces);
        QSettings registry(branch, QSettings::NativeFormat);
        struct Cleanup { QSettings &settings; ~Cleanup() {settings.clear(); settings.sync();} } cleanup{registry};
        registry.setValue("Classes/.scad/.", "Existing.OpenSCAD");
        registry.setValue("Microsoft/Windows/CurrentVersion/Explorer/FileExts/.scad/UserChoice/ProgId", "Existing.OpenSCAD");
        registry.setValue("Microsoft/Windows/CurrentVersion/Explorer/FileExts/.scad/UserChoice/Hash", "untouched");
        QTemporaryDir temp; const auto exe = temp.filePath(QString::fromUtf8("spaced é/scadmaxx-launcher.exe")); touch(exe);
        Config config; QString error;
        QVERIFY2(writeHandlerRegistration(registry, config, exe, error), qPrintable(error));
        QSettings readback(branch, QSettings::NativeFormat);
        const auto command = '"' + QDir::toNativeSeparators(exe) + "\" --open \"%1\"";
        QCOMPARE(readback.value("Classes/Applications/scadmaxx-launcher.exe/FriendlyAppName").toString(), "SCADMaxx Launcher");
        QCOMPARE(readback.value("Classes/Applications/scadmaxx-launcher.exe/shell/open/command/.").toString(), command);
        QCOMPARE(readback.value("Microsoft/Windows/CurrentVersion/App Paths/scadmaxx-launcher.exe/.").toString(), QDir::toNativeSeparators(exe));
        for (const auto &ext : {".scad", ".scadmaxx"}) {
            const QString prog = "SCADMaxx.Launcher" + QString(ext);
            QVERIFY(readback.contains("Classes/Applications/scadmaxx-launcher.exe/SupportedTypes/" + QString(ext)));
            QVERIFY(readback.contains("Classes/" + QString(ext) + "/OpenWithProgids/" + prog));
            QCOMPARE(readback.value("SCADMaxx/Launcher/Capabilities/FileAssociations/" + QString(ext)).toString(), prog);
            QCOMPARE(readback.value("Classes/" + prog + "/shell/open/command/.").toString(), command);
            QCOMPARE(readback.value("Classes/" + prog + "/Application/ApplicationName").toString(), "SCADMaxx Launcher");
        }
        QCOMPARE(readback.value("RegisteredApplications/SCADMaxx Launcher").toString(), "Software\\SCADMaxx\\Launcher\\Capabilities");
        QCOMPARE(readback.value("Classes/.scad/.").toString(), "Existing.OpenSCAD");
        QVERIFY(!readback.contains("Classes/.scadmaxx/."));
        QCOMPARE(readback.value("Microsoft/Windows/CurrentVersion/Explorer/FileExts/.scad/UserChoice/Hash").toString(), "untouched");
        QCOMPARE(readback.value("Microsoft/Windows/CurrentVersion/Explorer/FileExts/.scad/UserChoice/ProgId").toString(), "Existing.OpenSCAD");
        QVERIFY(writeHandlerRegistration(registry, config, exe, error)); // Repeated button press repairs idempotently.
        Config empty; empty.types.clear(); QVERIFY(!writeHandlerRegistration(registry, empty, exe, error));
#else
        QSKIP("Windows registry contract");
#endif
    }
    void extensionsAndValidation() {
        Config c; QCOMPARE(c.types[1].extensions,QStringList{".scadmaxx"});
        QCOMPARE(normalizedExtension(" SCADMAXX "),".scadmaxx");
        for(const auto &s:{"", ".", "a/b", "a b", "a.b"}) QVERIFY(normalizedExtension(s).isEmpty());
        QVERIFY(validExecutableName("scadmaxx.exe")); QVERIFY(!validExecutableName("../openscad.exe")); QVERIFY(!validExecutableName("*.exe"));
        QString error; QVERIFY(validateConfig(c,error)); c.types[1].extensions.append(".scad"); QVERIFY(!validateConfig(c,error));
    }
    void persistenceAndCorruption() {
        QTemporaryDir d; Config c; c.types[0]=collection(d.path()); c.ask=true; c.types[0].explicitBuilds={d.filePath("manual.exe")};
        c.types[0].excludedBuilds={d.filePath("excluded.exe")}; c.types[0].order="version";
        QString error; const auto path=d.filePath("settings.json"); QVERIFY(writeConfig(path,c,error));
        Config loaded; QVERIFY(readConfig(path,loaded,error)); QCOMPARE(configJson(loaded),configJson(c));
        touch(path,"{\"schema\":1}"); QVERIFY(!readConfig(path,loaded,error)); QCOMPARE(configJson(loaded),configJson(c));
        QFile f(path); QVERIFY(f.open(QIODevice::ReadOnly)); QCOMPARE(f.readAll(),QByteArray("{\"schema\":1}")); f.close();
        auto json=configJson(c); json["ask"]="yes"; touch(path,QJsonDocument(json).toJson()); QVERIFY(!readConfig(path,loaded,error));
        touch(d.filePath("blocked")); QVERIFY(!writeConfig(d.filePath("blocked/settings.json"),c,error));
    }
    void boundedScopeAndFilenameFilters() {
        QTemporaryDir d;
        for(const auto &p:{"openscad.exe","bin/openscad.exe","release/openscad.exe","release/bin/openscad.exe","release/scadmaxx.exe",
            "too/deep/openscad.exe","artifacts/openscad.exe","wt-feature/openscad.exe","vcpkg/openscad.exe","checkout/openscad.exe"}) touch(d.filePath(p));
        touch(d.filePath("checkout/.git")); BuildCache cache; auto t=collection(d.path());
        auto result=scanType(t,cache); QCOMPARE(result.builds.size(),4);
        t.sources[0].executable="scadmaxx.exe"; QCOMPARE(scanType(t,cache).builds.size(),1);
        t.sources[0].folder=d.filePath("artifacts"); t.sources[0].executable="openscad.exe"; t.sources[0].collection=false;
        QCOMPARE(scanType(t,cache).builds.size(),1); // Explicit roots are allowed even under artifacts.
    }
    void mixedEditorSearchFolders() {
        QTemporaryDir d; const auto oldRelease=d.filePath("old-release");
        touch(QDir(oldRelease).filePath("attempt-5/staging/openscad.exe"));
        touch(d.filePath("nightlies/OpenSCAD/openscad.exe"));
        auto t=collection(d.filePath("nightlies"));
        t.sources.append({"scadmaxx",oldRelease,"scadmaxx.exe",true});
        BuildCache cache; auto scan=scanType(t,cache);
        QCOMPARE(scan.builds.size(),1); QCOMPARE(scan.warnings.size(),1);
        QVERIFY(scan.warnings.first().contains("scadmaxx.exe"));
        QVERIFY(scan.warnings.first().contains(QDir::toNativeSeparators(oldRelease)));
        t.sources[1].executable="openscad.exe"; scan=scanType(t,cache);
        QCOMPARE(scan.builds.size(),2); QVERIFY(scan.warnings.isEmpty());
        touch(QDir(oldRelease).filePath("attempt-6/staging/scadmaxx.exe"));
        t.sources[1].executable="scadmaxx.exe"; scan=scanType(t,cache);
        QCOMPARE(scan.builds.size(),2); QVERIFY(scan.warnings.isEmpty());
    }
    void stagingAttemptDiscovery() {
        QTemporaryDir d; const auto root=d.filePath("SCADMaxx-20261003");
        for (const auto &p : {"attempt-2/staging/scadmaxx.exe", "attempt-10/staging/bin/scadmaxx.exe",
                "attempt-11/extracted-check/scadmaxx.exe", "attempt-12/deeper/staging/scadmaxx.exe"})
            touch(QDir(root).filePath(p));
        auto t=collection(root,"scadmaxx.exe"); BuildCache cache;
        const auto scan=scanType(t,cache); QCOMPARE(scan.builds.size(),2);
        auto winner=resolveDefault(t,scan,{}); QVERIFY(winner.valid); QVERIFY(winner.path.contains("attempt-10"));
        QVERIFY(cache.describe(winner.path).name.contains("SCADMaxx-20261003 / attempt-10"));
        t.sources[0].collection=false; QCOMPARE(scanType(t,cache).builds.size(),0);
        t.sources[0].folder=QDir(root).filePath("attempt-2"); QCOMPARE(scanType(t,cache).builds.size(),1);
    }
    void nameAndDateOrdering() {
        QTemporaryDir d; auto t=collection(d.path()); BuildCache cache;
        touch(d.filePath("build-9/openscad.exe")); touch(d.filePath("build-10/openscad.exe"));
        auto r=resolveDefault(t,scanType(t,cache),{}); QVERIFY(r.valid); QVERIFY(r.path.contains("build-10"));
        touch(d.filePath("OpenSCAD-2026.10.03/openscad.exe")); touch(d.filePath("OpenSCAD-20261004/openscad.exe"));
        r=resolveDefault(t,scanType(t,cache),{}); QVERIFY(r.path.contains("20261004"));
        QVERIFY(naturalCompare("build-0009","build-10")<0);
    }
    void versionsPrereleasesAndNoFallback() {
        QVERIFY(versionCompare("1.10.0","1.9.99")>0); QVERIFY(versionCompare("1.2.0","1.2.0-rc99")>0);
        QVERIFY(versionCompare("1.2.0-rc10","1.2.0-rc2")>0); QVERIFY(versionCompare("1.2.0-beta2","1.2.0-alpha9")>0);
        QCOMPARE(versionCompare("1.2.0.0","1.2.0"),0); QVERIFY(!knownVersion("not a version"));
        QTemporaryDir d; auto t=collection(d.path()); t.order="version"; BuildCache cache;
        touch(d.filePath("older/openscad.exe")); touch(d.filePath("newer/openscad.exe"));
        auto r=resolveDefault(t,scanType(t,cache),{}); QVERIFY(!r.valid); QVERIFY(r.reason.contains("readable version"));
        version(d.filePath("older"),"9"); version(d.filePath("newer"),"10","rc1");
        r=resolveDefault(t,scanType(t,cache),{}); QVERIFY(r.path.contains("newer"));
        t.sourceId="missing"; QVERIFY(!resolveDefault(t,scanType(t,cache),{}).valid);
    }
    void modifiedTimeAndStableTies() {
        QTemporaryDir d; auto t=collection(d.path()); t.order="modified"; BuildCache cache;
        const auto a=d.filePath("a/openscad.exe"), b=d.filePath("b/openscad.exe"); touch(a); touch(b);
        QFile f(a); QVERIFY(f.open(QIODevice::ReadWrite)); QVERIFY(f.setFileTime(QDateTime::fromSecsSinceEpoch(1000),QFileDevice::FileModificationTime)); f.close();
        QFile g(b); QVERIFY(g.open(QIODevice::ReadWrite)); QVERIFY(g.setFileTime(QDateTime::fromSecsSinceEpoch(2000),QFileDevice::FileModificationTime)); g.close();
        auto scan=scanType(t,cache); QCOMPARE(resolveDefault(t,scan,{}).path,b);
        scan.sources["source"][0].modified=5; scan.sources["source"][1].modified=5;
        QCOMPARE(resolveDefault(t,scan,{}).path,b); std::reverse(scan.sources["source"].begin(),scan.sources["source"].end()); QCOMPARE(resolveDefault(t,scan,{}).path,b);
    }
    void persistentCacheAndFreshEnumeration() {
        QTemporaryDir d; const auto path=d.filePath("a/openscad.exe"), file=d.filePath("cache.json"); touch(path); version(d.filePath("a"),"1");
        auto t=collection(d.path()); BuildCache first(file); auto found=scanType(t,first); QCOMPARE(first.metadataReads,1); QCOMPARE(found.builds[0].version,"1.2.1"); first.save();
        BuildCache next(file); scanType(t,next); QCOMPARE(next.metadataReads,0);
        touch(path,"changed-size"); scanType(t,next); QCOMPARE(next.metadataReads,1);
        version(d.filePath("a"),"100"); found=scanType(t,next); QCOMPARE(found.builds[0].version,"1.2.100"); QCOMPARE(next.metadataReads,2);
        touch(d.filePath("b/openscad.exe")); QCOMPARE(scanType(t,next).builds.size(),2);
        QVERIFY(QFile::remove(path)); QCOMPARE(scanType(t,next).builds.size(),1);
        touch(file,"broken"); BuildCache corrupt(file); QCOMPARE(scanType(t,corrupt).builds.size(),1);
    }
    void isolationExclusionsAndFixedRebuild() {
        QTemporaryDir d; touch(d.filePath("build-1/openscad.exe")); touch(d.filePath("build-2/openscad.exe")); touch(d.filePath("build-2/scadmaxx.exe"));
        auto scad=collection(d.path()), maxx=collection(d.path(),"scadmaxx.exe"); BuildCache cache;
        QCOMPARE(scanType(scad,cache).builds.size(),2); QCOMPARE(scanType(maxx,cache).builds.size(),1);
        scad.excludedBuilds={pathKey(d.filePath("build-2/openscad.exe"))};
        auto r=resolveDefault(scad,scanType(scad,cache),{}); QVERIFY(r.path.contains("build-1"));
        scad.mode="fixed"; scad.fixed=r.path; touch(scad.fixed,"rebuilt"); QCOMPARE(resolveDefault(scad,{},{}).path,scad.fixed);
        QVERIFY(!resolveDefault(scad,{},scad.fixed).valid); QVERIFY(QFile::remove(scad.fixed)); QVERIFY(!resolveDefault(scad,{},{}).valid);
        Config c; c.types[1].fixed=d.filePath("build-2/openscad.exe"); QVERIFY(typeForFile(c,"cross-editor.scadmaxx"));
        QCOMPARE(typeForFile(c,"cross-editor.scadmaxx")->fixed,c.types[1].fixed); QVERIFY(!typeForFile(c,"unknown.txt"));
    }
    void unicodeArgumentRoundTrip() {
        QTemporaryDir d; const auto document=d.filePath(QString::fromUtf8("spaced é 中文.scad")); touch(document);
        FileType t; t.mode="fixed"; t.fixed=QCoreApplication::applicationFilePath();
        auto r=resolveDefault(t,{},d.filePath("launcher.exe")); QVERIFY(r.valid);
        QProcess child; auto env=QProcessEnvironment::systemEnvironment(); const auto record=d.filePath("arguments.json"); env.insert("SCADMAXX_TEST_ARGUMENTS",record);
        child.setProcessEnvironment(env); child.start(r.path,QStringList{document}); QVERIFY(child.waitForFinished(10000)); QCOMPARE(child.exitCode(),0);
        QFile f(record); QVERIFY(f.open(QIODevice::ReadOnly)); QCOMPARE(QJsonDocument::fromJson(f.readAll()).array()[0].toString(),document);
    }
};
int main(int argc,char **argv) {
    QCoreApplication app(argc,argv); const auto record=qEnvironmentVariable("SCADMAXX_TEST_ARGUMENTS");
    if(!record.isEmpty()) {QFile f(record); if(!f.open(QIODevice::WriteOnly)) return 2; f.write(QJsonDocument(QJsonArray::fromStringList(app.arguments().mid(1))).toJson()); return 0;}
    CoreTests tests; return QTest::qExec(&tests,argc,argv);
}
#include "tests.moc"
