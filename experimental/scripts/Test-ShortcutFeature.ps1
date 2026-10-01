#requires -Version 7.2
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Source,
    [Parameter(Mandatory)][string]$DependencyPrefix,
    [Parameter(Mandatory)][string]$BuildProfile
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
. "$PSScriptRoot/Common.ps1"
$Source = [IO.Path]::GetFullPath($Source)
$DependencyPrefix = [IO.Path]::GetFullPath($DependencyPrefix)
$directory = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "../../runs/tool-tests/shortcuts-$([guid]::NewGuid().ToString('N'))"))
New-Item -ItemType Directory $directory | Out-Null
$script:LogPath = Join-Path $directory 'test.log'
$script:CommandRecords = [Collections.Generic.List[object]]::new()
$p = Get-Content -LiteralPath $BuildProfile -Raw | ConvertFrom-Json -AsHashtable
$head = Read-Git $Source @('rev-parse','HEAD')
if (Read-Git $Source @('status','--porcelain')) { throw 'Feature probe requires committed clean source.' }
Import-Module (Join-Path $p.visualStudio 'Common7/Tools/Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $p.visualStudio -Arch amd64 -HostArch amd64 -SkipAutomaticLocation `
    -DevCmdArguments "-vcvars_ver=$($p.toolset) -winsdk=$($p.sdk)" | Out-Null
$compiler = Join-Path $env:VCToolsInstallDir 'bin/Hostx64/x64/cl.exe'
$qtTools = Join-Path $DependencyPrefix 'tools/Qt6/bin'
@'
#include "gui/ShortcutConfigurator.h"
#include <QApplication>
#include <QDir>
#include <QFile>
#include <QTemporaryDir>
#include <QTimer>
#include <QDebug>
#include <QFontDatabase>
#include <QtTest/QTest>
#include <cstdlib>
#include <cstdio>
static std::string configPath;
namespace PlatformUtils { std::string userConfigPath() { return configPath; } }
static void require(bool ok, const char *message) {
  if (!ok) { qCritical() << message; std::exit(2); }
  qInfo() << "PASS:" << message;
}
int main(int argc, char **argv) {
  qInstallMessageHandler([](QtMsgType, const QMessageLogContext&, const QString& text) {
    std::fprintf(stderr, "%s\n", text.toUtf8().constData());
  });
  QApplication app(argc, argv);
  const int fontId = QFontDatabase::addApplicationFont("probe-font.ttf");
  require(fontId >= 0, "bundled font loaded for offscreen rendering");
  QApplication::setFont(QFont(QFontDatabase::applicationFontFamilies(fontId).first(), 10));
  QTemporaryDir config;
  require(config.isValid(), "isolated configuration directory");
  configPath = config.path().toStdString();
  QTimer::singleShot(15000, [] { qCritical() << "Probe timed out"; std::exit(91); });
  QWidget firstWindow, secondWindow;
  QAction first(&firstWindow), second(&secondWindow), occupied(&firstWindow);
  first.setObjectName("actionProbe"); second.setObjectName("actionProbe");
  occupied.setObjectName("actionOccupied");
  first.setShortcut(QKeySequence("Ctrl+J")); second.setShortcut(QKeySequence("Ctrl+J"));
  occupied.setShortcut(QKeySequence("Ctrl+K"));
  firstWindow.addAction(&first); secondWindow.addAction(&second);
  int activations = 0;
  QObject::connect(&first, &QAction::triggered, [&] { ++activations; });
  ShortcutConfigurator widget;
  const QList<QAction *> actions{&first, &second, &occupied};
  widget.collectDefaults(actions); widget.initGUI(actions);
  const auto cell = widget.shortcutsTable->model()->index(0, 1);
  auto edit = [&](Qt::Key key, Qt::KeyboardModifiers modifiers, bool collision) {
    int errors = 0;
    bool sent = false;
    QTimer driver;
    QObject::connect(&driver, &QTimer::timeout, [&] {
      for (auto *top : QApplication::topLevelWidgets()) {
        auto *box = qobject_cast<QMessageBox *>(top);
        if (!box || !box->isVisible()) continue;
        if (box->windowTitle() == "Error") { ++errors; box->accept(); }
        else if (!sent && box->standardButtons().testFlag(QMessageBox::Apply)) {
          sent = true;
          QTest::keyClick(box, key, modifiers);
          box->button(QMessageBox::Apply)->click();
        }
      }
    });
    driver.start(10);
    require(QMetaObject::invokeMethod(&widget, "onTableCellClicked", Qt::DirectConnection,
                                    Q_ARG(QModelIndex, cell)), "shortcut editor invoked");
    driver.stop();
    require(sent && (errors > 0) == collision, collision ? "collision rejected" : "shortcut accepted");
  };
  edit(Qt::Key_F12, Qt::AltModifier | Qt::ShiftModifier, false);
  const QKeySequence assigned("Alt+Shift+F12");
  require(first.shortcut() == assigned && second.shortcut() == assigned, "existing windows updated consistently");
  firstWindow.show(); firstWindow.activateWindow(); firstWindow.setFocus();
  QTest::qWait(30);
  QTest::keyClick(&firstWindow, Qt::Key_F12, Qt::AltModifier | Qt::ShiftModifier);
  QTest::qWait(30);
  require(activations == 1, "assigned key invokes intended action");
  for (bool dark : {false, true, false}) {
    QPalette palette;
    const QColor background = dark ? QColor("#252525") : QColor("#ffffff");
    const QColor foreground = dark ? QColor("#eeeeee") : QColor("#202020");
    for (auto role : {QPalette::Window, QPalette::Base, QPalette::Button}) palette.setColor(role, background);
    for (auto role : {QPalette::WindowText, QPalette::Text, QPalette::ButtonText}) palette.setColor(role, foreground);
    palette.setColor(QPalette::PlaceholderText, dark ? QColor("#aaaaaa") : QColor("#666666"));
    QApplication::setPalette(palette);
    widget.resize(800, 450); widget.show(); QTest::qWait(30);
    require(widget.shortcutsTable->palette().color(QPalette::Text) == foreground,
            "shortcut table follows application palette");
    require(widget.grab().save(dark ? "shortcuts-dark.png" : "shortcuts-light.png"), "palette screenshot saved");
    firstWindow.activateWindow(); firstWindow.setFocus(); QTest::qWait(30);
    QTest::keyClick(&firstWindow, Qt::Key_F12, Qt::AltModifier | Qt::ShiftModifier);
    QTest::qWait(30);
  }
  require(activations == 4, "shortcut remains active through light-dark-light palette changes");
  require(QFile::exists(config.path() + "/shortcuts.json"), "shortcut file written");
  QAction restarted;
  restarted.setObjectName("actionProbe"); restarted.setShortcut(QKeySequence("Ctrl+J"));
  ShortcutConfigurator recreated;
  recreated.collectDefaults({&restarted}); recreated.applyConfigFile({&restarted});
  require(restarted.shortcut() == assigned, "new configurator restores persisted shortcut");
  edit(Qt::Key_K, Qt::ControlModifier, true);
  require(first.shortcut() == assigned, "collision leaves prior shortcut intact");
  QTimer::singleShot(10, [] {
    for (auto *top : QApplication::topLevelWidgets()) {
      auto *box = qobject_cast<QMessageBox *>(top);
      if (box && box->isVisible() && box->standardButtons().testFlag(QMessageBox::Yes))
        box->button(QMessageBox::Yes)->click();
    }
  });
  require(QMetaObject::invokeMethod(&widget, "on_reset_clicked", Qt::DirectConnection), "restore defaults invoked");
  require(first.shortcut() == QKeySequence("Ctrl+J") && second.shortcut() == QKeySequence("Ctrl+J"), "defaults restored across windows");
  QFile settings(config.path() + "/shortcuts.json"); settings.open(QIODevice::ReadOnly);
  require(QJsonDocument::fromJson(settings.readAll()).object().isEmpty(), "persisted overrides cleared");
  return 0;
}
'@ | Set-Content (Join-Path $directory 'probe.cc') -Encoding utf8NoBOM
$previousPath = $env:PATH
$previousPlugins = $env:QT_PLUGIN_PATH
$previousPlatform = $env:QT_QPA_PLATFORM
Push-Location $directory
try {
    Copy-Item (Join-Path $Source 'fonts/Liberation-2.00.1/ttf/LiberationSans-Regular.ttf') 'probe-font.ttf'
    Invoke-Logged (Join-Path $qtTools 'uic.exe') @("$Source/src/gui/ShortcutConfigurator.ui",'-o','ui_ShortcutConfigurator.h')
    Invoke-Logged (Join-Path $qtTools 'moc.exe') @("$Source/src/gui/ShortcutConfigurator.h",'-o','moc_ShortcutConfigurator.cc')
    $includes = @("/I$directory","/I$Source/src","/I$Source/src/gui","/I$DependencyPrefix/include",
        "/I$DependencyPrefix/include/Qt6","/I$DependencyPrefix/include/Qt6/QtCore",
        "/I$DependencyPrefix/include/Qt6/QtGui","/I$DependencyPrefix/include/Qt6/QtWidgets",
        "/I$DependencyPrefix/include/Qt6/QtTest")
    Invoke-Logged $compiler (@('/nologo','/MD','/EHsc','/std:c++17','/Zc:__cplusplus','/permissive-',
        '/DSTACKSIZE=8388608','/DNOMINMAX','/DQT_WIDGETS_LIB','/DQT_GUI_LIB','/DQT_CORE_LIB') + $includes + @('probe.cc',"$Source/src/gui/ShortcutConfigurator.cc",
        'moc_ShortcutConfigurator.cc','/Fe:probe.exe','/link',"/LIBPATH:$DependencyPrefix/lib",
        'Qt6Widgets.lib','Qt6Gui.lib','Qt6Core.lib','Qt6Test.lib','intl.lib'))
    $env:PATH = "$DependencyPrefix/bin;$previousPath"
    $env:QT_PLUGIN_PATH = "$DependencyPrefix/Qt6/plugins"
    $env:QT_QPA_PLATFORM = 'offscreen'
    Invoke-Logged (Join-Path $directory 'probe.exe') @()
    Save-Json (Join-Path $directory 'result.json') @{status='passed'; source=$Source; sourceSha=$head;
        isolation='temporary config path; offscreen Qt platform';
        limitations='Widget-level harness, not Windows desktop interaction or full process restart.'}
    "Passed shortcut widget checks. Evidence: $directory"
} finally {
    $env:PATH = $previousPath; $env:QT_PLUGIN_PATH = $previousPlugins; $env:QT_QPA_PLATFORM = $previousPlatform
    Pop-Location
    Save-Json (Join-Path $directory 'commands.json') @($script:CommandRecords.ToArray())
}
