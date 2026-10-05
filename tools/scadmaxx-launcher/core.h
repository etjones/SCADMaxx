#pragma once
#include <QMap>
#include <QJsonObject>
#include <QStringList>
#include <QVector>

struct Build { QString path, name, version; qint64 modified = 0; };
struct BuildSource {
    QString id, folder, executable = "openscad.exe";
    bool collection = true;
};
struct FileType {
    QString id, name;
    QStringList extensions;
    QVector<BuildSource> sources;
    QStringList explicitBuilds, excludedBuilds;
    QString mode = "fixed", fixed, sourceId, order = "name";
};
struct Config {
    QVector<FileType> types;
    bool ask = false, tray = true, startup = false, scanOnStartup = false;
    Config();
};
struct ScanResult {
    QVector<Build> builds;
    QMap<QString, QVector<Build>> sources;
    QStringList warnings;
};
struct Resolution { QString path, reason; bool valid = false; };
QString normalizedExtension(QString value);
QString pathKey(const QString &path);
bool validExecutable(const QString &path, const QString &self);
bool validExecutableName(const QString &name);
bool excludedCollectionFolder(const QString &folder);
QString orderLabel(const QString &order);
int naturalCompare(QString a, QString b);
int versionCompare(const QString &a, const QString &b);
bool knownVersion(const QString &version);
class BuildCache {
public:
    explicit BuildCache(QString file = {});
    Build describe(const QString &path);
    void save();
    int metadataReads = 0;
private:
    QString file;
    QJsonObject entries;
};
ScanResult scanType(const FileType &type, BuildCache &cache, const QString &self = {});
Resolution resolveDefault(const FileType &type, const ScanResult &scan, const QString &self);
const FileType *typeForFile(const Config &config, const QString &file);
bool validateConfig(const Config &config, QString &error);
bool readConfig(const QString &file, Config &config, QString &error);
bool writeConfig(const QString &file, const Config &config, QString &error);
QJsonObject configJson(const Config &config);
QString configLocation();
class QSettings;
bool writeHandlerRegistration(QSettings &registry, const Config &config, const QString &executable, QString &error);
bool registerHandlers(const Config &config, const QString &executable, QString &error);
bool isDefaultHandler(const QString &extension, const QString &executable);
bool setStartup(bool enabled, const QString &executable, QString &error);
