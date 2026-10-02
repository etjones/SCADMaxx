#include "core.h"
#include <QtTest>
#include <QTemporaryDir>
#include <QFile>
#include <QJsonDocument>
#include <QJsonArray>
#include <QProcess>

class CoreTests : public QObject {
    Q_OBJECT
private slots:
    void extensionRules() {
        QCOMPARE(normalizedExtension(" SCAD "), ".scad");
        QCOMPARE(normalizedExtension(".SCADMAX"), ".scadmax");
        for (const auto &invalid : {"", ".", "a/b", "a b", "a.b", "../exe"}) QVERIFY(normalizedExtension(invalid).isEmpty());
    }
    void persistAndCorruption() {
        QTemporaryDir dir; const auto file = dir.filePath("settings.json"); QString error; Config config;
        config.mappings[".scad"] = QCoreApplication::applicationFilePath();
        config.folders = QStringList{dir.path()}; config.scanOnStartup = true;
        config.builds.append(describeBuild(QCoreApplication::applicationFilePath()));
        QVERIFY2(writeConfig(file, config, error), qPrintable(error));
        Config loaded; QVERIFY2(readConfig(file, loaded, error), qPrintable(error));
        QCOMPARE(loaded.mappings, config.mappings); QCOMPARE(loaded.folders, config.folders);
        QVERIFY(loaded.scanOnStartup); QCOMPARE(loaded.builds.size(), 1);
        QFile corrupt(file); QVERIFY(corrupt.open(QIODevice::WriteOnly)); corrupt.write("not JSON"); corrupt.close();
        QVERIFY(!readConfig(file, loaded, error)); QCOMPARE(loaded.mappings, config.mappings);
        QVERIFY(corrupt.open(QIODevice::ReadOnly)); QCOMPARE(corrupt.readAll(), QByteArray("not JSON"));
    }
    void discoveryPinsMappings() {
        QTemporaryDir dir; QDir().mkpath(dir.filePath("nested"));
        for (const auto &name : {"openscad.exe", "nested/scadmaxx.exe", "openscad.com", "other.exe"}) {
            QFile f(dir.filePath(name)); QVERIFY(f.open(QIODevice::WriteOnly)); f.write("fixture");
        }
        auto found = discover({dir.path(), dir.filePath("nested")}); QCOMPARE(found.size(), 2);
        Config config; config.mappings[".scad"] = dir.filePath("gone.exe"); const auto mappings = config.mappings;
        mergeBuilds(config, found); mergeBuilds(config, found); QCOMPARE(config.builds.size(), 2);
        QCOMPARE(config.mappings, mappings);
    }
    void shallowCollectionsAndExplicitInstall() {
        QTemporaryDir dir;
        const QStringList paths{"release/openscad.exe", "artifacts/openscad.exe", "runs/scadmaxx.exe",
            "wt-feature/openscad.exe", "vcpkg/openscad.exe", "source-checkout/openscad.exe",
            "nested/deep/openscad.exe", "openscad.exe"};
        for (const auto &path : paths) {
            QDir().mkpath(QFileInfo(dir.filePath(path)).absolutePath());
            QFile f(dir.filePath(path)); QVERIFY(f.open(QIODevice::WriteOnly)); f.write("fixture");
        }
        QFile gitMarker(dir.filePath("source-checkout/.git")); QVERIFY(gitMarker.open(QIODevice::WriteOnly)); gitMarker.close();
        const auto found = discover({dir.path()}); QCOMPARE(found.size(), 2);
        for (const auto &b : found) QVERIFY(b.path == dir.filePath("openscad.exe") || b.path == dir.filePath("release/openscad.exe"));
        QCOMPARE(discoverInstalled(dir.filePath("artifacts")).size(), 1);
        QVERIFY(discover({dir.filePath("artifacts")}).isEmpty());
    }
    void curatedSelectionPersistsAndProtectsMappings() {
        QTemporaryDir dir; Config config; QString error;
        const Build first{dir.filePath("first.exe"), "First", "1"}, second{dir.filePath("second.exe"), "Second", "2"};
        const auto mappings = config.mappings;
        QVERIFY(applyBuildReview(config, {first, second}, {first.path}, {}, error));
        QCOMPARE(config.builds.size(), 1); QCOMPARE(config.mappings, mappings);
        QVERIFY(config.excludedBuilds.contains(pathKey(second.path)));
        QVERIFY(writeConfig(dir.filePath("settings.json"), config, error));
        Config loaded; QVERIFY(readConfig(dir.filePath("settings.json"), loaded, error));
        QCOMPARE(loaded.excludedBuilds, config.excludedBuilds);
        QVERIFY(applyBuildReview(loaded, {second}, {second.path}, {}, error));
        QVERIFY(loaded.excludedBuilds.isEmpty()); QCOMPARE(loaded.builds.size(), 2);
        loaded.mappings[".scad"] = first.path;
        QVERIFY(!applyBuildReview(loaded, {first}, {}, {}, error));
        QCOMPARE(loaded.builds.size(), 2);
        QVERIFY(!applyBuildReview(loaded, {second}, {}, {second.path}, error));
        QCOMPARE(loaded.builds.size(), 2);
    }
    void missingAndSelfTargets() {
        QTemporaryDir dir; QFile file(dir.filePath("example.scad")); QVERIFY(file.open(QIODevice::WriteOnly)); file.close();
        Config config; QString exe, error; QStringList args;
        QVERIFY(!resolveOpen(config, file.fileName(), QCoreApplication::applicationFilePath(), exe, args, error));
        config.mappings[".scad"] = QCoreApplication::applicationFilePath();
        QVERIFY(!resolveOpen(config, file.fileName(), QCoreApplication::applicationFilePath(), exe, args, error));
        QVERIFY(!resolveOpen(config, dir.filePath("missing.scad"), "launcher.exe", exe, args, error));
    }
    void unicodeArgumentRoundTrip() {
        QTemporaryDir dir; const auto document = dir.filePath(QString::fromUtf8("spaced é 中文.scad"));
        QFile file(document); QVERIFY(file.open(QIODevice::WriteOnly)); file.close();
        Config config; config.mappings[".scad"] = QCoreApplication::applicationFilePath();
        QString exe, error; QStringList arguments;
        QVERIFY2(resolveOpen(config, document, dir.filePath("launcher.exe"), exe, arguments, error), qPrintable(error));
        QCOMPARE(arguments, QStringList{document});
        QProcess child; auto env = QProcessEnvironment::systemEnvironment();
        const auto record = dir.filePath("arguments.json"); env.insert("SCADMAXX_TEST_ARGUMENTS", record);
        child.setProcessEnvironment(env); child.start(exe, arguments);
        QVERIFY(child.waitForFinished(10000)); QCOMPARE(child.exitCode(), 0);
        QFile received(record); QVERIFY(received.open(QIODevice::ReadOnly));
        QCOMPARE(QJsonDocument::fromJson(received.readAll()).array().at(0).toString(), document);
    }
    void failedSavePreservesPrevious() {
        QTemporaryDir dir; QString error; Config config;
        QFile blocker(dir.filePath("blocked")); QVERIFY(blocker.open(QIODevice::WriteOnly)); blocker.write("preserve"); blocker.close();
        QVERIFY(!writeConfig(dir.filePath("blocked/settings.json"), config, error));
        QVERIFY(blocker.open(QIODevice::ReadOnly)); QCOMPARE(blocker.readAll(), QByteArray("preserve"));
    }
};

int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    const auto record = qEnvironmentVariable("SCADMAXX_TEST_ARGUMENTS");
    if (!record.isEmpty()) {
        QFile output(record); if (!output.open(QIODevice::WriteOnly)) return 2;
        QJsonArray args; for (const auto &arg : app.arguments().mid(1)) args.append(arg);
        output.write(QJsonDocument(args).toJson()); return 0;
    }
    CoreTests tests; return QTest::qExec(&tests, argc, argv);
}
#include "tests.moc"
