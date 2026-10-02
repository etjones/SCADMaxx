#pragma once
#include <QMap>
#include <QStringList>
#include <QVector>

struct Build { QString path, name, version; };
struct Config {
    QMap<QString, QString> mappings{{".scad", {}}, {".scadmax", {}}};
    QVector<Build> builds;
    QStringList folders;
    QStringList excludedBuilds;
    bool tray = true, startup = false, scanOnStartup = false;
};
QString normalizedExtension(QString value);
QString pathKey(const QString &path);
bool validExecutable(const QString &path, const QString &self);
Build describeBuild(const QString &path);
QVector<Build> discover(const QStringList &folders);
QVector<Build> discoverInstalled(const QString &folder);
bool excludedCollectionFolder(const QString &folder);
bool applyBuildReview(Config &config, const QVector<Build> &candidates, const QStringList &selected,
                      const QStringList &protectedPaths, QString &error);
void mergeBuilds(Config &config, const QVector<Build> &found);
bool readConfig(const QString &file, Config &config, QString &error);
bool writeConfig(const QString &file, const Config &config, QString &error);
bool resolveOpen(const Config &config, const QString &file, const QString &self,
                 QString &program, QStringList &arguments, QString &error);
QString configLocation();
bool registerHandlers(const Config &config, const QString &executable, QString &error);
bool isDefaultHandler(const QString &extension, const QString &executable);
bool setStartup(bool enabled, const QString &executable, QString &error);
