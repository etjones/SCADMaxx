#include "launcher-version.h"
#include "core.h"
#include <cstdio>
#include <QtWidgets>
#include <QtConcurrent>
#include <QLocalServer>
#include <QLocalSocket>

class BuildComboBox final : public QComboBox {
protected:
    void paintEvent(QPaintEvent *event) override {
        QComboBox::paintEvent(event);
        QPainter painter(this); painter.setRenderHint(QPainter::Antialiasing);
        painter.setPen(QPen(palette().color(isEnabled() ? QPalette::Active : QPalette::Disabled, QPalette::Text), 1.4));
        const QPointF center(width()-17, height()/2.0);
        painter.drawLine(center+QPointF(-4,-2),center+QPointF(0,2));
        painter.drawLine(center+QPointF(0,2),center+QPointF(4,-2));
    }
};

static QString selfPath() { return QCoreApplication::applicationFilePath(); }
static QString newId() { return QUuid::createUuid().toString(QUuid::WithoutBraces); }
static QLabel *label(const QString &text, const QString &name = {}) {
    auto *w = new QLabel(text); w->setObjectName(name); w->setWordWrap(true); return w;
}
static QPushButton *button(QHBoxLayout *layout, const QString &text, QObject *context, std::function<void()> action) {
    auto *b = new QPushButton(text); layout->addWidget(b); QObject::connect(b, &QPushButton::clicked, context, action); return b;
}
static QComboBox *orderCombo() {
    auto *box = new BuildComboBox;
    for (const auto &mode : {"name", "version", "modified"}) box->addItem(orderLabel(mode), mode);
    return box;
}
static ScanResult scanWithProgress(QWidget *parent, const FileType &type, const QString &cacheFile) {
    QProgressDialog progress("Looking for builds in " + type.name + " search folders…", QString(), 0, 0, parent);
    progress.setWindowTitle("SCADMaxx Launcher"); progress.setWindowModality(Qt::WindowModal);
    progress.setCancelButton(nullptr); progress.setMinimumDuration(150);
    QFutureWatcher<ScanResult> watcher; QEventLoop loop;
    QObject::connect(&watcher, &QFutureWatcher<ScanResult>::finished, &loop, &QEventLoop::quit);
    const auto self = selfPath();
    watcher.setFuture(QtConcurrent::run([type, cacheFile, self] { BuildCache cache(cacheFile); auto r = scanType(type, cache, self); cache.save(); return r; }));
    if (!watcher.isFinished()) loop.exec();
    progress.close(); return watcher.result();
}
static void compactBuildTable(QTableWidget *table) {
    table->ensurePolished();
    table->setWordWrap(false);
    table->setTextElideMode(Qt::ElideMiddle);
    table->verticalHeader()->setSectionResizeMode(QHeaderView::Fixed);
    table->verticalHeader()->setDefaultSectionSize(qMax(26, table->fontMetrics().height() + 10));
}
static QString buildText(const Build &b) { return b.name + (b.version.isEmpty() ? " · version unknown" : " · " + b.version); }
static QString pickExecutable(QWidget *parent, const QString &start = {}) {
    return QFileDialog::getOpenFileName(parent, "Choose an editor executable", start, "Windows executables (*.exe)");
}
static bool editSource(QWidget *parent, BuildSource &source) {
    QDialog dialog(parent); dialog.setObjectName("sourceEditor"); dialog.setWindowTitle(source.id.isEmpty() ? "Add search folder" : "Edit search folder"); dialog.resize(640, 380);
    auto *layout = new QVBoxLayout(&dialog); auto *form = new QFormLayout;
    auto *folder = new QLineEdit(source.folder);
    folder->setObjectName("sourceFolder");
    auto *exe = new QLineEdit(source.executable); exe->setObjectName("executableName"); exe->setPlaceholderText("scadmaxx.exe or openscad.exe");
    auto *scope = new BuildComboBox; scope->addItem("Build collection — folder, children and their bin folders", true);
    scope->addItem("One installed build — folder and bin only", false); scope->setCurrentIndex(source.collection ? 0 : 1);
    auto *pathRow = new QHBoxLayout; pathRow->addWidget(folder);
    button(pathRow, "Browse…", &dialog, [&]{
        auto selected = QFileDialog::getExistingDirectory(&dialog, "Select a search folder", folder->text().isEmpty() ? "D:/openscad" : folder->text());
        if (!selected.isEmpty()) folder->setText(selected);
    });
    form->addRow("Folder", pathRow); form->addRow("Executable name", exe); form->addRow("Look in", scope); layout->addLayout(form);
    layout->addWidget(label("Choose the narrowest useful folder. Collections scan immediate children, including their bin and staging folders. Source worktrees, artifacts and dependencies below it are skipped. Select a specific build directly to include it.", "mappingStatus"));
    auto *warning = label({}); layout->addWidget(warning);
    auto *buttons = new QDialogButtonBox(QDialogButtonBox::Save | QDialogButtonBox::Cancel); layout->addWidget(buttons);
    QObject::connect(buttons, &QDialogButtonBox::rejected, &dialog, &QDialog::reject);
    QObject::connect(buttons, &QDialogButtonBox::accepted, &dialog, [&]{
        if (!QFileInfo(folder->text()).isAbsolute() || !validExecutableName(exe->text())) {
            warning->setText("Enter an absolute folder and executable basename ending in .exe."); return;
        }
        source = {source.id.isEmpty() ? newId() : source.id, QDir::cleanPath(folder->text()), exe->text(), scope->currentData().toBool()};
        dialog.accept();
    });
    return dialog.exec() == QDialog::Accepted;
}

class TypeDialog final : public QDialog {
public:
    FileType value;
    TypeDialog(FileType type, QString cacheFile, QWidget *parent = nullptr) : QDialog(parent), value(std::move(type)), cacheFile(std::move(cacheFile)) {
        setWindowTitle("Configure file type"); resize(900, 900);
        auto *layout = new QVBoxLayout(this); layout->setSpacing(12);
        auto *form = new QFormLayout; name = new QLineEdit(value.name); extensions = new QLineEdit(value.extensions.join(", "));
        name->setObjectName("typeName"); extensions->setObjectName("typeExtensions");
        form->addRow("File type", name); form->addRow("File extensions", extensions); layout->addLayout(form);
        layout->addWidget(label("Search folders", "sectionTitle"));
        sources = new QListWidget; sources->setMaximumHeight(130); layout->addWidget(sources);
        auto *sourceActions = new QHBoxLayout;
        button(sourceActions, "Add folder…", this, [this]{addSource();});
        button(sourceActions, "Edit…", this, [this]{
            int i = sources->currentRow(); if (i < 0) return; auto s = value.sources[i];
            if (editSource(this, s)) { value.sources[i] = s; updateSources(); refresh(); }
        });
        button(sourceActions, "Remove", this, [this]{
            int i = sources->currentRow(); if (i < 0) return;
            if (value.sources[i].id == sourceChoice->currentData().toString() && mode->currentData() == "latest") {
                message->setText("Choose another default before removing its search folder."); return;
            }
            value.sources.removeAt(i); updateSources(); refresh();
        }); sourceActions->addStretch(); layout->addLayout(sourceActions);
        layout->addWidget(label("Default when opening", "sectionTitle"));
        auto *selection = new QFormLayout;
        mode = new BuildComboBox; mode->setObjectName("selectionMode"); mode->addItem("Fixed executable", "fixed"); mode->addItem("Latest from folder", "latest");
        mode->setCurrentIndex(value.mode == "latest" ? 1 : 0); selection->addRow("Selection", mode);
        fixed = new BuildComboBox; fixed->setObjectName("fixedBuild"); fixed->setSizeAdjustPolicy(QComboBox::AdjustToMinimumContentsLengthWithIcon); fixed->setMinimumContentsLength(30);
        auto *fixedRow = new QHBoxLayout; fixedRow->addWidget(fixed, 1);
        button(fixedRow, "Browse executable…", this, [this]{
            auto path = pickExecutable(this); if (path.isEmpty()) return;
            if (!validExecutable(path, selfPath())) { message->setText("Choose an available editor executable, not this launcher."); return; }
            value.explicitBuilds.removeAll(path); value.explicitBuilds.append(path); value.fixed = path;
            value.excludedBuilds.removeAll(pathKey(path)); { QSignalBlocker block(mode); mode->setCurrentIndex(0); } refresh();
        }); selection->addRow("Fixed build", fixedRow);
        sourceChoice = new BuildComboBox; sourceChoice->setObjectName("latestSource");
        auto *latestRow = new QHBoxLayout; latestRow->addWidget(sourceChoice, 1);
        button(latestRow, "Choose folder…", this, [this]{addSource(true);}); selection->addRow("Search folder", latestRow);
        order = orderCombo(); order->setObjectName("latestOrder"); order->setCurrentIndex(order->findData(value.order)); selection->addRow("Order by", order);
        layout->addLayout(selection);
        preview = label({}, "mappingStatus"); preview->setTextInteractionFlags(Qt::TextSelectableByMouse); layout->addWidget(preview);
        auto *buildActions = new QHBoxLayout; buildActions->addWidget(label("Available builds", "sectionTitle")); buildActions->addStretch();
        button(buildActions, "Rescan / preview", this, [this]{refresh();}); layout->addLayout(buildActions);
        builds = new QTableWidget(0, 3); builds->setObjectName("sourceBuilds"); compactBuildTable(builds); builds->setHorizontalHeaderLabels({"Include / build", "Version", "Executable path"});
        builds->setMinimumHeight(160); builds->verticalHeader()->hide(); builds->setEditTriggers(QAbstractItemView::NoEditTriggers); builds->setSelectionBehavior(QAbstractItemView::SelectRows);
        builds->horizontalHeader()->setSectionResizeMode(0, QHeaderView::ResizeToContents); builds->horizontalHeader()->setSectionResizeMode(1, QHeaderView::ResizeToContents);
        builds->horizontalHeader()->setSectionResizeMode(2, QHeaderView::Stretch); layout->addWidget(builds, 1);
        layout->addWidget(label("Checked builds participate in this file type's choices and Latest rules. New matching builds are included automatically. Uncheck to exclude; exclusions survive rescans.", "mappingStatus"));
        message = label({}); layout->addWidget(message);
        auto *buttons = new QDialogButtonBox(QDialogButtonBox::Save | QDialogButtonBox::Close); layout->addWidget(buttons);
        buttons->button(QDialogButtonBox::Close)->setToolTip("Close without saving changes in this dialog.");
        connect(buttons, &QDialogButtonBox::rejected, this, &QDialog::reject);
        connect(buttons, &QDialogButtonBox::accepted, this, [this]{
            readSelection(); value.name = name->text().trimmed(); value.extensions.clear();
            for (const auto &e : extensions->text().split(QRegularExpression("[,;\\s]+"), Qt::SkipEmptyParts)) value.extensions.append(normalizedExtension(e));
            Config check; check.types = {value}; QString error;
            if (!validateConfig(check, error)) { message->setText(error); return; } accept();
        });
        connect(mode, &QComboBox::currentIndexChanged, this, [this]{updatePreview();});
        connect(fixed, &QComboBox::currentIndexChanged, this, [this]{updatePreview();});
        connect(sourceChoice, &QComboBox::currentIndexChanged, this, [this]{updatePreview();});
        connect(order, &QComboBox::currentIndexChanged, this, [this]{updatePreview();});
        connect(builds, &QTableWidget::itemChanged, this, [this](QTableWidgetItem *item){
            if (item->column() != 0) return; const auto path = item->data(Qt::UserRole).toString();
            if (item->checkState() == Qt::Unchecked && pathKey(path) == pathKey(fixed->currentData().toString())) {
                QSignalBlocker blocker(builds); item->setCheckState(Qt::Checked); message->setText("Choose another fixed build before excluding this one."); return;
            }
            value.excludedBuilds.removeAll(pathKey(path)); if (item->checkState() == Qt::Unchecked) value.excludedBuilds.append(pathKey(path));
            updatePreview();
        });
        updateSources(); refresh();
    }
private:
    QString cacheFile; QLineEdit *name, *extensions; QListWidget *sources;
    QComboBox *mode, *fixed, *sourceChoice, *order; QTableWidget *builds; QLabel *preview, *message;
    ScanResult scan;
    void readSelection() { value.mode = mode->currentData().toString(); value.fixed = fixed->currentData().toString(); value.sourceId = sourceChoice->currentData().toString(); value.order = order->currentData().toString(); }
    void updateSources() {
        QSignalBlocker block(sourceChoice); sources->clear(); sourceChoice->clear();
        for (const auto &s : value.sources) { sources->addItem(QDir::toNativeSeparators(s.folder) + "\n" + s.executable); sourceChoice->addItem(QDir::toNativeSeparators(s.folder), s.id); sourceChoice->setItemData(sourceChoice->count()-1, s.folder, Qt::ToolTipRole); }
        sourceChoice->setCurrentIndex(sourceChoice->findData(value.sourceId));
    }
    void addSource(bool latest = false) {
        readSelection(); BuildSource source; source.executable = value.extensions.contains(".scadmaxx") ? "scadmaxx.exe" : "openscad.exe";
        if (!editSource(this, source)) return;
        value.sources.append(source); value.sourceId = source.id; updateSources(); if (latest) mode->setCurrentIndex(1); refresh();
    }
    void updatePreview() {
        readSelection(); fixed->setEnabled(value.mode == "fixed"); sourceChoice->setEnabled(value.mode == "latest"); order->setEnabled(value.mode == "latest");
        auto filtered = scan; for (auto it = filtered.sources.begin(); it != filtered.sources.end(); ++it)
            it.value().removeIf([this](const Build &b){return value.excludedBuilds.contains(pathKey(b.path));});
        auto r = resolveDefault(value, filtered, selfPath()); preview->setText(r.reason + (r.valid ? "\n" + r.path : ""));
    }
    void refresh() {
        // Scan without exclusions so previously excluded candidates remain restorable in the review list.
        FileType all = value; all.excludedBuilds.clear(); scan = scanWithProgress(this, all, cacheFile);
        QSignalBlocker fixedBlock(fixed), tableBlock(builds);
        const auto selection = value.fixed; fixed->clear(); fixed->addItem("Choose a build", QString());
        builds->setRowCount(scan.builds.size()); int row = 0;
        for (const auto &b : scan.builds) {
            bool excluded = value.excludedBuilds.contains(pathKey(b.path));
            if (!excluded) { fixed->addItem(buildText(b), b.path); fixed->setItemData(fixed->count()-1, b.path, Qt::ToolTipRole); }
            auto *item = new QTableWidgetItem(b.name); item->setToolTip(b.name); item->setData(Qt::UserRole, b.path); item->setCheckState(excluded ? Qt::Unchecked : Qt::Checked);
            builds->setItem(row, 0, item); builds->setItem(row, 1, new QTableWidgetItem(b.version.isEmpty() ? "Unknown" : b.version));
            auto *path = new QTableWidgetItem(b.path); path->setToolTip(b.path); builds->setItem(row++, 2, path);
        }
        if (!selection.isEmpty() && fixed->findData(selection) < 0) fixed->addItem("Unavailable: " + selection, selection);
        fixed->setCurrentIndex(qMax(0, fixed->findData(selection)));
        message->setText(scan.warnings.join('\n')); updatePreview();
    }
};

static QString chooseBuild(QWidget *parent, const FileType &type, const ScanResult &scan, const Resolution &preferred, const QStringList &documents, const QString &lastUsed = {}) {
    QDialog dialog(parent); dialog.setObjectName("buildChooser"); dialog.setWindowTitle("Choose build — " + type.name); dialog.resize(1200, 520);
    auto *layout = new QVBoxLayout(&dialog);
    layout->addWidget(label(documents.size() == 1 ? "Open " + QFileInfo(documents.first()).fileName() : QString("Open %1 files").arg(documents.size()), "pageTitle"));
    QString selectedPath = preferred.path;
    bool remembered = false;
    for (const auto &build : scan.builds) if (!lastUsed.isEmpty() && pathKey(build.path) == pathKey(lastUsed)) {
        selectedPath = build.path; remembered = true; break;
    }
    layout->addWidget(label(remembered ? "Your last-used build is selected. Successful opens are remembered for this file type."
        : preferred.valid ? "Your configured default is selected. Successful opens are remembered for this file type." : preferred.reason, "mappingStatus"));
    auto *list = new QTableWidget(scan.builds.size(), 3); list->setObjectName("chooserBuilds"); compactBuildTable(list); list->setHorizontalHeaderLabels({"Build", "Version", "Path"});
    list->verticalHeader()->hide(); list->setEditTriggers(QAbstractItemView::NoEditTriggers); list->setSelectionBehavior(QAbstractItemView::SelectRows); list->setSelectionMode(QAbstractItemView::SingleSelection);
    list->horizontalHeader()->setSectionResizeMode(0, QHeaderView::ResizeToContents); list->horizontalHeader()->setSectionResizeMode(1, QHeaderView::ResizeToContents); list->horizontalHeader()->setSectionResizeMode(2, QHeaderView::Stretch);
    int selected = -1, row = 0;
    for (const auto &b : scan.builds) {
        auto *nameItem = new QTableWidgetItem(b.name); nameItem->setToolTip(b.name); list->setItem(row, 0, nameItem); list->setItem(row, 1, new QTableWidgetItem(b.version.isEmpty() ? "Unknown" : b.version));
        auto *p = new QTableWidgetItem(b.path); p->setToolTip(b.path); list->setItem(row, 2, p);
        if (pathKey(b.path) == pathKey(selectedPath)) selected = row; ++row;
    }
    if (selected >= 0) list->selectRow(selected); layout->addWidget(list, 1);
    list->setFocus(Qt::OtherFocusReason);
    int nameWidth = 100, versionWidth = 90, pathWidth = 400;
    for (const auto &build : scan.builds) {
        nameWidth = qMax(nameWidth, list->fontMetrics().horizontalAdvance(build.name) + 28);
        versionWidth = qMax(versionWidth, list->fontMetrics().horizontalAdvance(build.version) + 28);
        pathWidth = qMax(pathWidth, list->fontMetrics().horizontalAdvance(build.path) + 28);
    }
    const auto available = dialog.screen()->availableGeometry();
    dialog.resize(qMin(qMax(1200, nameWidth + versionWidth + pathWidth + 50), available.width() - 40),
        qMin(520, available.height() - 40));
    if (scan.builds.isEmpty()) layout->addWidget(label("No available builds. Add a search folder or executable in the manager."));
    auto *buttons = new QDialogButtonBox(QDialogButtonBox::Open | QDialogButtonBox::Cancel); layout->addWidget(buttons);
    buttons->button(QDialogButtonBox::Open)->setEnabled(selected >= 0); buttons->button(QDialogButtonBox::Open)->setDefault(true);
    QObject::connect(list, &QTableWidget::itemSelectionChanged, &dialog, [=]{buttons->button(QDialogButtonBox::Open)->setEnabled(list->currentRow() >= 0);});
    QObject::connect(list, &QTableWidget::cellDoubleClicked, &dialog, [&]{dialog.accept();});
    QObject::connect(buttons, &QDialogButtonBox::accepted, &dialog, &QDialog::accept); QObject::connect(buttons, &QDialogButtonBox::rejected, &dialog, &QDialog::reject);
    if (dialog.exec() != QDialog::Accepted || list->currentRow() < 0) return {};
    return scan.builds[list->currentRow()].path;
}

static void applyAppearance(bool testing = false) {
        bool dark = qApp->palette().color(QPalette::Window).lightness() < 128;
#if QT_VERSION >= QT_VERSION_CHECK(6, 5, 0)
        dark = qApp->styleHints()->colorScheme() == Qt::ColorScheme::Dark;
#endif
        if (testing && qEnvironmentVariable("SCADMAXX_LAUNCHER_THEME") == "dark") dark = true;
        const QString bg = dark ? "#202126" : "#fafafa", panel = dark ? "#292a31" : "#ffffff";
        const QString text = dark ? "#ececf2" : "#202127", muted = dark ? "#b8bbc9" : "#626572";
        const QString border = dark ? "#444650" : "#dedee5", accent = dark ? "#b4a9ff" : "#5143ba";
        const QString onAccent = dark ? "#202126" : "#ffffff";
        QPalette theme = qApp->palette();
        theme.setColor(QPalette::Window, QColor(bg)); theme.setColor(QPalette::Base, QColor(panel));
        theme.setColor(QPalette::Text, QColor(text)); theme.setColor(QPalette::WindowText, QColor(text));
        theme.setColor(QPalette::Button, QColor(panel)); theme.setColor(QPalette::ButtonText, QColor(text));
        theme.setColor(QPalette::Highlight, QColor(accent)); theme.setColor(QPalette::HighlightedText, QColor(onAccent));
        qApp->setPalette(theme);
        qApp->setStyleSheet(QString(R"(
            QWidget { font-family: 'Segoe UI'; font-size: 14px; color: %1; }
            QMainWindow, QWidget#mappingContent, QScrollArea#mappingArea { background: %2; }
            QLabel { background: transparent; }
            QFrame#appHeader, QFrame#appFooter { background: %3; }
            QFrame#appHeader { border-bottom: 1px solid %4; }
            QFrame#appFooter { border-top: 1px solid %4; }
            QLabel#brandMark { background: %5; color: %6; border-radius: 6px; font-size: 18px; font-weight: 600; }
            QLabel#brandName { font-weight: 600; }
            QLabel#pageTitle { font-size: 22px; font-weight: 600; }
            QLabel#extensionName { font-size: 17px; font-weight: 600; }
            QLabel#sectionTitle { font-weight: 600; }
            QLabel#buildPath { font-family: Consolas; font-size: 12px; color: %7; }
            QLabel#mappingStatus { font-size: 12px; color: %7; }
            QFrame#mappingRow { border-bottom: 1px solid %4; }
            QFrame#separator { background: %4; }
            QPushButton, QComboBox, QLineEdit { background: %3; border: 1px solid %4; border-radius: 6px; padding: 8px 11px; }
            QPushButton:hover, QComboBox:hover { border-color: %5; }
            QPushButton:focus, QComboBox:focus, QLineEdit:focus { border: 2px solid %5; padding: 7px 10px; }
            QPushButton:disabled { color: %7; background: %2; }
            QPushButton#primaryButton, QLabel#brandMark { background: %5; color: %6; }
            QPushButton#primaryButton:disabled { background: %4; color: %7; }
            QPushButton#removeExtension { border: none; background: transparent; color: %7; padding: 0; }
            QPushButton#removeExtension:hover { color: %1; background: %3; }
            QComboBox { padding-right: 30px; min-height: 20px; }
            QComboBox::drop-down { border: none; width: 26px; }
            QComboBox::down-arrow { image: none; }
            QComboBox:disabled { color: %7; background: %2; }
            QTableWidget { background: %3; color: %1; gridline-color: %4; border: 1px solid %4; selection-background-color: %5; selection-color: %6; }
            QTableWidget::item:selected, QTableWidget::item:selected:!active { background-color: %5; color: %6; }
            QHeaderView::section { background: %2; color: %1; padding: 5px; border: none; border-bottom: 1px solid %4; }

            QComboBox QAbstractItemView, QListWidget { background: %3; color: %1; border: 1px solid %4; selection-background-color: %5; selection-color: %6; }
            QListWidget { border-radius: 6px; padding: 4px; }
            QCheckBox { spacing: 8px; padding: 4px 0; }
            QCheckBox::indicator { width: 15px; height: 15px; }
            QMenu { background: %3; color: %1; border: 1px solid %4; padding: 5px; }
            QMenu::item { padding: 8px 22px; }
            QMenu::item:selected { background: %5; color: %6; }
            QMenu::item:disabled { color: %7; }
        )").arg(text, bg, panel, border, accent, onAccent, muted));
    }



class Manager final : public QMainWindow {
public:
    Manager(Config config, QString file, bool smoke = false) : saved(std::move(config)), draft(saved), settingsFile(std::move(file)), testing(smoke) {
        setWindowTitle("SCADMaxx Launcher"); setObjectName("launcher"); resize(900, 700); setMinimumSize(740, 580);
        setWindowIcon(QIcon(":/launcher.ico"));
        auto *central = new QWidget; setCentralWidget(central); auto *outer = new QVBoxLayout(central); outer->setContentsMargins(0,0,0,0);
        auto *header = new QFrame; header->setObjectName("appHeader"); auto *head = new QHBoxLayout(header); head->setContentsMargins(24,14,24,14);
        auto *logo = label("S", "brandMark"); logo->setAlignment(Qt::AlignCenter); logo->setFixedSize(34,32); head->addWidget(logo);
        head->addWidget(label("SCADMaxx Launcher", "brandName")); head->addStretch(); head->addWidget(label(QCoreApplication::applicationVersion(), "mappingStatus")); outer->addWidget(header);
        auto *body = new QWidget; auto *layout = new QVBoxLayout(body); layout->setContentsMargins(24,22,24,20); layout->setSpacing(16); outer->addWidget(body,1);
        layout->addWidget(label("File associations", "pageTitle"));
        auto *scroll = new QScrollArea; scroll->setObjectName("mappingArea"); scroll->setWidgetResizable(true); scroll->setFrameShape(QFrame::NoFrame);
        auto *content = new QWidget; content->setObjectName("mappingContent"); rows = new QVBoxLayout(content); rows->setContentsMargins(0,0,0,0); rows->setSpacing(0);
        scroll->setWidget(content); layout->addWidget(scroll,1);
        auto *actions = new QHBoxLayout;
        button(actions, "+ File type", this, [this]{editType(-1);}); button(actions, "Rescan builds", this, [this]{rescan();}); actions->addStretch(); layout->addLayout(actions);
        ask = new QCheckBox("Choose build when opening"); ask->setObjectName("askEveryTime"); ask->setToolTip("Show a chooser for every handled file type, with its default preselected.");
        ask->setChecked(saved.ask); layout->addWidget(ask);
        connect(ask, &QCheckBox::toggled, this, [this](bool on){setAsk(on);});
        auto *setup = new QHBoxLayout; association = label("Windows setup needed", "mappingStatus"); setup->addWidget(association,1);
        button(setup, "Set up Windows associations…", this, [this]{setupWindows();}); layout->addLayout(setup);
        auto *prefs = new QHBoxLayout; keepTray = new QCheckBox("Keep in system tray"); startup = new QCheckBox("Start at sign-in"); scanAtStart = new QCheckBox("Refresh builds at startup");
        keepTray->setChecked(saved.tray); startup->setChecked(saved.startup); scanAtStart->setChecked(saved.scanOnStartup);
        prefs->addWidget(keepTray); prefs->addWidget(startup); prefs->addWidget(scanAtStart); prefs->addStretch(); layout->addLayout(prefs);
        connect(keepTray, &QCheckBox::toggled, this, [this](bool on){ Config next = saved; next.tray = on; if (persist(next)) {draft.tray = on; updateTray();} else {QSignalBlocker b(keepTray); keepTray->setChecked(saved.tray);} });
        connect(scanAtStart, &QCheckBox::toggled, this, [this](bool on){ Config next = saved; next.scanOnStartup = on; if (persist(next)) draft.scanOnStartup = on; else {QSignalBlocker b(scanAtStart); scanAtStart->setChecked(saved.scanOnStartup);} });
        connect(startup, &QCheckBox::toggled, this, [this](bool on){
            QString error; if (testing || setStartup(on, selfPath(), error)) {
                Config next = saved; next.startup = on;
                if (persist(next)) { draft.startup = on; return; }
                if (!testing) setStartup(saved.startup, selfPath(), error);
            } else fail(error);
            QSignalBlocker b(startup); startup->setChecked(saved.startup);
        });
        auto *footer = new QFrame; footer->setObjectName("appFooter"); auto *bottom = new QHBoxLayout(footer); bottom->setContentsMargins(24,16,24,16);
        status = label("Ready", "mappingStatus"); bottom->addWidget(status,1);
        revert = button(bottom, "Revert", this, [this]{draft = saved; render(); status->setText("Pending file-type changes discarded.");});
        apply = button(bottom, "Apply", this, [this]{applyChanges();}); apply->setObjectName("primaryButton");
        button(bottom, "Close", this, [this]{close();}); outer->addWidget(footer);
        tray = new QSystemTrayIcon(windowIcon(), this); tray->setToolTip("SCADMaxx Launcher"); menu = new QMenu(this); tray->setContextMenu(menu);
        connect(menu, &QMenu::aboutToShow, this, [this]{refreshMenu();});
        connect(tray, &QSystemTrayIcon::activated, this, [this](QSystemTrayIcon::ActivationReason reason){if (reason == QSystemTrayIcon::Trigger || reason == QSystemTrayIcon::DoubleClick) openWindow();});
        connect(qApp, &QApplication::applicationStateChanged, this, [this](Qt::ApplicationState s){if (s == Qt::ApplicationActive) refreshAssociations();});
        refreshAppearance(); render(); updateTray();
#if QT_VERSION >= QT_VERSION_CHECK(6,5,0)
        connect(qApp->styleHints(), &QStyleHints::colorSchemeChanged, this, [this]{refreshAppearance();});
#endif
        if (saved.scanOnStartup && !testing) QTimer::singleShot(0, this, [this]{rescan();});
    }
    void openWindow() {showNormal(); raise(); activateWindow();}
    bool hasTray() const {return tray->isVisible();}
    bool smokeTest();
protected:
    void closeEvent(QCloseEvent *event) override {
        if (!confirmDiscard()) {event->ignore(); return;}
        if (hasTray()) {hide(); event->ignore();} else {event->accept(); qApp->quit();}
    }
private:
    Config saved, draft; QString settingsFile; bool testing;
    QVBoxLayout *rows; QLabel *status, *association; QPushButton *apply, *revert;
    QCheckBox *ask, *keepTray, *startup, *scanAtStart; QSystemTrayIcon *tray; QMenu *menu;
    QMap<QString, ScanResult> scans, savedScans;
    QString cacheFile() const {return QFileInfo(settingsFile).dir().filePath("build-cache.json");}
    bool dirty() const {return configJson(saved) != configJson(draft);}
    void fail(const QString &error) {QMessageBox::warning(this, "SCADMaxx Launcher", error);}
    bool persist(const Config &next) {QString error; if (!writeConfig(settingsFile,next,error)) {fail(error); return false;} saved = next; return true;}
    void setAsk(bool on) {
        Config next = saved; next.ask = on; if (persist(next)) {draft.ask = on; status->setText(on ? "Build chooser enabled for all file types." : "Files open directly with their configured defaults.");}
        QSignalBlocker b(ask); ask->setChecked(saved.ask);
    }
    void updateTray() {if (!testing && saved.tray && QSystemTrayIcon::isSystemTrayAvailable()) tray->show(); else tray->hide();}
    bool confirmDiscard() {
        if (!dirty()) return true;
        if (QMessageBox::question(this,"Pending changes","Discard pending file-type changes?",QMessageBox::Discard|QMessageBox::Cancel,QMessageBox::Cancel) != QMessageBox::Discard) return false;
        draft = saved; render(); return true;
    }
    void applyChanges() {if (persist(draft)) {savedScans.clear(); render(); status->setText("File-type settings saved.");}}
    void refreshAssociations() {
        QStringList states;
        for (const auto &type : saved.types) for (const auto &ext : type.extensions)
            states.append(ext + (isDefaultHandler(ext,selfPath()) ? " — ready" : " — Windows setup needed"));
        association->setText(states.isEmpty() ? "Add a file type first" : states.join("\n"));
    }
    void setupWindows() {
        if (dirty()) {fail("Apply or revert changes before Windows setup."); return;}
        QString error; if (!registerHandlers(saved,selfPath(),error)) {fail(error); return;}
        QUrl url("ms-settings:defaultapps"); QUrlQuery query;
        query.addQueryItem("registeredAppUser", "SCADMaxx Launcher"); url.setQuery(query);
        if (!QDesktopServices::openUrl(url)) {
            fail("Registration succeeded, but Windows Settings could not be opened. Open Settings > Apps > Default apps and search for SCADMaxx Launcher."); return;
        }
        status->setText("Registered with Windows. On the SCADMaxx Launcher page, select each extension and choose SCADMaxx Launcher. If the general page opens, search for SCADMaxx Launcher. Return here to check the result.");
    }
    void editType(int index) {
        FileType type; if (index >= 0) type = draft.types[index]; else {type.id = newId(); type.name = "New file type";}
        TypeDialog dialog(type, cacheFile(), this);
        if (dialog.exec() != QDialog::Accepted) return;
        Config next = draft; if (index >= 0) next.types[index] = dialog.value; else next.types.append(dialog.value);
        QString error; if (!validateConfig(next,error)) {fail(error); return;}
        draft = next; scans[dialog.value.id] = scanWithProgress(this,dialog.value,cacheFile()); render();
        status->setText("File-type changes pending. Apply to save.");
    }
    void rescan() {
        for (const auto &type : saved.types) savedScans[type.id] = scanWithProgress(this,type,cacheFile());
        if (!dirty()) scans = savedScans;
        else for (const auto &type : draft.types) scans[type.id] = scanWithProgress(this,type,cacheFile());
        render(); status->setText("Build lists refreshed. Fixed defaults unchanged.");
    }
    void render() {
        while (auto *item = rows->takeAt(0)) {if (item->widget()) {item->widget()->hide(); item->widget()->deleteLater();} delete item;}
        for (int i = 0; i < draft.types.size(); ++i) {
            const auto type = draft.types[i]; auto *row = new QFrame; row->setObjectName("mappingRow"); auto *h = new QHBoxLayout(row); h->setContentsMargins(0,18,0,18); h->setSpacing(18);
            auto *identity = new QWidget; auto *id = new QVBoxLayout(identity); id->setContentsMargins(0,0,0,0); identity->setFixedWidth(150);
            id->addWidget(label(type.extensions.join("\n"), "extensionName")); id->addWidget(label(type.name,"mappingStatus")); id->addStretch(); h->addWidget(identity);
            auto *cell = new QWidget; auto *v = new QVBoxLayout(cell); v->setContentsMargins(0,0,0,0); v->setSpacing(7); h->addWidget(cell,1);
            QString selection = "Fixed executable";
            if (type.mode == "latest") {selection = "Latest from folder"; for (const auto &s : type.sources) if (s.id == type.sourceId) selection += " · " + QDir::toNativeSeparators(s.folder);}
            v->addWidget(label(selection,"sectionTitle"));
            Resolution resolved;
            if (type.mode == "latest" && !scans.contains(type.id)) resolved.reason = "By " + orderLabel(type.order).toLower() + " · resolves when opening a file";
            else resolved = resolveDefault(type,scans.value(type.id),selfPath());
            auto *path = label(resolved.valid ? resolved.path : resolved.reason,"buildPath"); path->setTextInteractionFlags(Qt::TextSelectableByMouse); v->addWidget(path);
            if (resolved.valid) v->addWidget(label(resolved.reason,"mappingStatus"));
            v->addWidget(label(QString("%1 search folder(s) · %2 explicit build(s)").arg(type.sources.size()).arg(type.explicitBuilds.size()),"mappingStatus"));
            auto *controls = new QVBoxLayout;
            auto *edit = new QPushButton("Configure…"); controls->addWidget(edit); connect(edit,&QPushButton::clicked,this,[this,i]{editType(i);});
            auto *remove = new QPushButton("Remove"); controls->addWidget(remove); connect(remove,&QPushButton::clicked,this,[this,i]{draft.types.removeAt(i); render();}); controls->addStretch(); h->addLayout(controls);
            rows->addWidget(row);
        }
        rows->addStretch(); apply->setEnabled(dirty()); revert->setEnabled(dirty()); refreshMenu(); refreshAssociations();
    }
    void selectFromTray(const QString &id, const QString &mode, const QString &target, const QString &order = "name") {
        Config next = saved; int index = -1; for (int i = 0; i < next.types.size(); ++i) if (next.types[i].id == id) index = i;
        if (index < 0) return; auto &type = next.types[index];
        if (mode == "fixed" && !validExecutable(target,selfPath())) {openWindow(); fail("Build unavailable: " + target); return;}
        type.mode = mode; if (mode == "fixed") type.fixed = target; else {type.sourceId = target; type.order = order;}
        if (!persist(next)) return;
        bool found = false; for (auto &t : draft.types) if (t.id == id) {t = type; found = true;}
        if (!found) draft.types.append(type);
        render(); status->setText(type.name + " default saved. Pending edits to this file type replaced.");
    }
    void refreshMenu() {
        menu->clear();
        auto *askAction = menu->addAction("Choose build when opening"); askAction->setObjectName("trayAsk"); askAction->setCheckable(true); askAction->setChecked(saved.ask);
        connect(askAction,&QAction::triggered,this,[this](bool on){setAsk(on);}); menu->addSeparator();
        for (const auto &t : saved.types) {
            auto *sub = menu->addMenu(t.extensions.join(", ") + " — " + t.name);
            auto builds = savedScans.value(t.id).builds;
            // Only use saved type sources here; draft source edits must not become saved shortcuts.
            QSet<QString> allowed;
            for (const auto &s : t.sources) for (const auto &b : savedScans.value(t.id).sources.value(s.id)) allowed.insert(pathKey(b.path));
            for (const auto &p : t.explicitBuilds) allowed.insert(pathKey(p)); allowed.insert(pathKey(t.fixed));
            BuildCache cache(cacheFile());
            for (const auto &p : t.explicitBuilds + QStringList{t.fixed}) if (validExecutable(p,selfPath())) {
                bool exists = false; for (const auto &b : builds) exists |= pathKey(p) == pathKey(b.path); if (!exists) builds.append(cache.describe(p));
            }
            for (const auto &b : builds) if (allowed.contains(pathKey(b.path)) && !t.excludedBuilds.contains(pathKey(b.path))) {
                auto *a = sub->addAction(buildText(b)); a->setCheckable(true); a->setChecked(t.mode == "fixed" && pathKey(t.fixed) == pathKey(b.path));
                a->setEnabled(validExecutable(b.path,selfPath())); a->setToolTip(b.path);
                connect(a,&QAction::triggered,this,[this,id=t.id,path=b.path]{selectFromTray(id,"fixed",path);});
            }
            for (const auto &s : t.sources) {
                auto *latest = sub->addMenu("Latest · " + QDir::toNativeSeparators(s.folder));
                for (const auto &order : {"name", "version", "modified"}) {
                    auto *a = latest->addAction(orderLabel(order)); a->setCheckable(true); a->setChecked(t.mode == "latest" && t.sourceId == s.id && t.order == order);
                    connect(a,&QAction::triggered,this,[this,id=t.id,source=s.id,order=QString(order)]{selectFromTray(id,"latest",source,order);});
                }
            }
            sub->addSeparator(); sub->addAction("Configure…", this, [this,id=t.id]{openWindow(); for (int i=0;i<draft.types.size();++i) if(draft.types[i].id==id) {editType(i); return;}});
        }
        menu->addSeparator(); menu->addAction("Rescan builds",this,[this]{rescan();}); menu->addAction("Open manager",this,[this]{openWindow();});
        menu->addAction("Quit",this,[this]{if(confirmDiscard()) qApp->quit();});
    }
    void refreshAppearance() { applyAppearance(testing); }

};

static int openDocuments(const Config &, const QStringList &, const QString &);

bool Manager::smokeTest() {
    if (draft.types.size() != 2 || draft.types[1].extensions != QStringList{".scadmaxx"} || apply->isEnabled()) return false;
    QTemporaryDir temp;
    const auto first = temp.filePath("first.exe"), second = temp.filePath("second.exe");
    for (const auto &p : {first,second}) {QFile f(p); if(!f.open(QIODevice::WriteOnly)) return false; f.write("fixture");}
    draft.types[0].fixed = first; draft.types[0].explicitBuilds = {first,second}; render();
    if (!apply->isEnabled()) return false; apply->click();
    Config loaded; QString error; if(!readConfig(settingsFile,loaded,error) || loaded.types[0].fixed != first) return false;
    draft.types[1].name = "Pending other type";
    selectFromTray("scad","fixed",second);
    if (saved.types[0].fixed != second || draft.types[1].name != "Pending other type") return false;
    ask->setChecked(true); if (!saved.ask || !readConfig(settingsFile,loaded,error) || !loaded.ask) return false;
    refreshMenu(); auto *toggle = menu->findChild<QAction *>("trayAsk"); if(!toggle || !toggle->isChecked()) return false;
    toggle->trigger(); if (saved.ask || ask->isChecked()) return false;
    BuildCache cache; auto scan = scanType(saved.types[0],cache,selfPath()); auto preferred = resolveDefault(saved.types[0],scan,selfPath());
    bool sawDefault = false;
    QTimer::singleShot(0,this,[&]{
        auto *d = qobject_cast<QDialog *>(QApplication::activeModalWidget()); if(!d) return;
        auto *table = d->findChild<QTableWidget *>("chooserBuilds");
        sawDefault = table && !table->wordWrap() && table->rowHeight(0) == table->verticalHeader()->defaultSectionSize() && table->currentRow() >= 0 && table->item(table->currentRow(),2)->text() == second;
        if(table) table->selectRow(0);
        const auto capture=qEnvironmentVariable("SCADMAXX_LAUNCHER_CAPTURE"); if(!capture.isEmpty()) d->grab().save(capture+".chooser.png");
        d->accept();
    });
    const auto chosen = chooseBuild(this,saved.types[0],scan,preferred,{"example.scad"});
    if(!sawDefault || chosen != first || saved.types[0].fixed != second) return false;
    for (const auto &previous : {first, temp.filePath("removed.exe")}) {
        const auto expected = previous == first ? first : second;
        QTimer::singleShot(0,this,[&]{if(auto *d=qobject_cast<QDialog *>(QApplication::activeModalWidget())) d->accept();});
        if(chooseBuild(this,saved.types[0],scan,preferred,{"example.scad"},previous)!=expected) return false;
    }
    QTimer::singleShot(0,this,[]{if(auto *d=qobject_cast<QDialog *>(QApplication::activeModalWidget())) d->reject();});
    if(!chooseBuild(this,saved.types[0],scan,preferred,{"example.scad"}).isEmpty()) return false;
    TypeDialog editor(saved.types[0],cacheFile(),this);
    editor.findChild<QLineEdit *>("typeExtensions")->setText(".scad, .csg");
    QTimer::singleShot(0,&editor,[&]{
        const auto capture=qEnvironmentVariable("SCADMAXX_LAUNCHER_CAPTURE"); if(!capture.isEmpty()) editor.grab().save(capture+".editor.png");
        editor.findChild<QDialogButtonBox *>()->button(QDialogButtonBox::Save)->click();
    });
    if(editor.exec()!=QDialog::Accepted || !editor.value.extensions.contains(".csg")) return false;
    revert->click(); if(draft.types[1].name != saved.types[1].name || apply->isEnabled()) return false;
    BuildSource added;
    QTimer::singleShot(0,this,[&]{
        auto *d=qobject_cast<QDialog *>(QApplication::activeModalWidget()); if(!d) return;
        d->findChild<QLineEdit *>("sourceFolder")->setText(temp.path());
        d->findChild<QLineEdit *>("executableName")->setText("second.exe");
        d->findChild<QDialogButtonBox *>()->button(QDialogButtonBox::Save)->click();
    });
    if(!editSource(this,added) || added.executable!="second.exe" || added.folder!=QDir::cleanPath(temp.path())) return false;
    auto latest=saved.types[0]; latest.sources={added}; latest.mode="latest"; latest.sourceId=added.id;
    TypeDialog latestEditor(latest,cacheFile(),this);
    latestEditor.findChild<QComboBox *>("latestOrder")->setCurrentIndex(2);
    QTimer::singleShot(0,&latestEditor,[&]{latestEditor.findChild<QDialogButtonBox *>()->button(QDialogButtonBox::Save)->click();});
    if(latestEditor.exec()!=QDialog::Accepted || latestEditor.value.mode!="latest" || latestEditor.value.order!="modified") return false;
    saved.types[0]=latestEditor.value; draft=saved;
    selectFromTray("scad","latest",added.id,"name");
    if(saved.types[0].mode!="latest" || saved.types[0].order!="name") return false;

    // Exercise the real batch dispatcher against the test executable, never an editor or user settings.
    const auto receiver=QCoreApplication::applicationDirPath()+"/launcher-tests.exe";
    if(QFileInfo::exists(receiver)) {
        const auto document=temp.filePath(QString::fromUtf8("spaced é 中文.scad"));
        const auto secondDocument=temp.filePath("second.scad");
        for(const auto &p : {document,secondDocument}) {QFile f(p); if(!f.open(QIODevice::WriteOnly)) return false; f.write("// test");}
        Config dispatch; dispatch.types[0].fixed=receiver;
        const auto record=temp.filePath("dispatch.json"); qputenv("SCADMAXX_TEST_ARGUMENTS",record.toUtf8());
        const auto result=openDocuments(dispatch,{document,secondDocument},cacheFile()); qunsetenv("SCADMAXX_TEST_ARGUMENTS");
        if(result!=0) return false;
        QSettings history(QFileInfo(cacheFile()).dir().filePath("last-used.ini"),QSettings::IniFormat);
        if(history.value(dispatch.types[0].id).toString()!=receiver || history.contains(dispatch.types[1].id)) return false;
        QElapsedTimer wait; wait.start(); QJsonArray received;
        while(wait.elapsed()<5000) {
            QFile f(record); if(f.open(QIODevice::ReadOnly)) received=QJsonDocument::fromJson(f.readAll()).array();
            if(received.size()==2) break; QThread::msleep(20);
        }
        if(received.size()!=2 || received[0].toString()!=document || received[1].toString()!=secondDocument) return false;
    }
    // Representative screenshot data uses only temporary local paths and never writes normal settings.
    draft.types[0].sources = {{"official",temp.path(),"openscad.exe",true}};
    draft.types[0].mode = "latest"; draft.types[0].sourceId = "official";
    draft.types[1].sources = {{"releases",temp.path(),"scadmaxx.exe",true}};
    draft.types[1].mode = "latest"; draft.types[1].sourceId = "releases"; draft.types[1].order = "version";
    render(); return !windowIcon().isNull();
}

static int openDocuments(const Config &config, const QStringList &documents, const QString &cacheFile) {
    QMap<QString,QStringList> groups;
    for (const auto &document : documents) {
        if(!QFileInfo(document).isFile()) {QMessageBox::warning(nullptr,"Cannot open file","File not found: " + document); return 1;}
        auto *type = typeForFile(config,document);
        if(!type) {QMessageBox::warning(nullptr,"Cannot open file","No configured file type handles: " + document); return 1;}
        groups[type->id].append(QFileInfo(document).absoluteFilePath());
    }
    QVector<QPair<QString,QStringList>> launches;
    QStringList launchedTypes;
    QSettings recent(QFileInfo(cacheFile).dir().filePath("last-used.ini"), QSettings::IniFormat);
    for (const auto &type : config.types) if (groups.contains(type.id)) {
        ScanResult scan;
        if(config.ask || type.mode == "latest") scan = scanWithProgress(nullptr,type,cacheFile);
        auto resolved = resolveDefault(type,scan,selfPath()); QString program = resolved.path;
        if(config.ask) {
            program = chooseBuild(nullptr,type,scan,resolved,groups[type.id],recent.value(type.id).toString());
            if(program.isEmpty()) return 0; // No editors launched until all groups have been confirmed.
        } else if (!resolved.valid) {
            QMessageBox box(QMessageBox::Warning,"Cannot open file",resolved.reason,QMessageBox::Close);
            auto *manage = box.addButton("Open manager",QMessageBox::ActionRole); box.exec();
            if(box.clickedButton()==manage) QProcess::startDetached(selfPath(),QStringList{});
            return 1;
        }
        launches.append({program,groups[type.id]}); launchedTypes.append(type.id);
    }
    int launchIndex = 0;
    for (const auto &launch : launches) {
        if(!validExecutable(launch.first,selfPath()) || !QProcess::startDetached(launch.first,launch.second,QFileInfo(launch.second.first()).absolutePath())) {
            QMessageBox::warning(nullptr,"Cannot start editor","The selected build is unavailable or failed to start:\n" + launch.first); return 1;
        }
        recent.setValue(launchedTypes[launchIndex++], launch.first); recent.sync();
        if (recent.status() != QSettings::NoError)
            QMessageBox::warning(nullptr,"Build history","The editor started, but its selection could not be saved.");
    }
    return 0;
}
int main(int argc,char **argv) {
    QApplication app(argc,argv);
    QCoreApplication::setOrganizationName("SCADMaxx"); QCoreApplication::setApplicationName("Launcher");
    QApplication::setApplicationDisplayName("SCADMaxx Launcher"); QCoreApplication::setApplicationVersion(QStringLiteral(SCADMAXX_LAUNCHER_VERSION));
    QApplication::setWindowIcon(QIcon(":/launcher.ico")); QApplication::setQuitOnLastWindowClosed(false);
    applyAppearance();
    const auto args = app.arguments();
    if(args.contains("--version")) {fprintf(stdout,"SCADMaxx Launcher %s\n",SCADMAXX_LAUNCHER_VERSION); return 0;}
    if(args.contains("--smoke-test")) {
        if(qEnvironmentVariable("QT_QPA_PLATFORM")=="offscreen") {
            int id=QFontDatabase::addApplicationFont(qEnvironmentVariable("WINDIR")+"/Fonts/segoeui.ttf");
            QFontDatabase::addApplicationFont(qEnvironmentVariable("WINDIR")+"/Fonts/seguisb.ttf");
            if(id>=0) app.setFont(QFont(QFontDatabase::applicationFontFamilies(id).value(0),9));
        }
        QTemporaryDir temp; Manager manager(Config(),temp.filePath("settings.json"),true); manager.show(); app.processEvents();
        bool success=manager.smokeTest(); QCoreApplication::sendPostedEvents(nullptr,QEvent::DeferredDelete); app.processEvents();
        const auto capture=qEnvironmentVariable("SCADMAXX_LAUNCHER_CAPTURE"); if(!capture.isEmpty()) manager.grab().save(capture);
        return success ? 0 : 1;
    }
    const QString file=configLocation(); Config config; QString error;
    // Dispatch is read-only with respect to settings and does not need the manager lock.
    if(args.size()>1 && args[1]=="--open") {
        if(!readConfig(file,config,error)) {QMessageBox::critical(nullptr,"Settings error",error+"\nOpen the manager to review settings.\n"+file); return 1;}
        if(args.size()<3) {QMessageBox::warning(nullptr,"SCADMaxx Launcher","No file specified."); return 2;}
        return openDocuments(config,args.mid(2),QFileInfo(file).dir().filePath("build-cache.json"));
    }
    if(args.size()>1 && args[1]!="--tray") {QMessageBox::warning(nullptr,"SCADMaxx Launcher","Use --open <file...>, --tray or --version."); return 2;}
    QDir().mkpath(QFileInfo(file).absolutePath());
    const QString serverName="SCADMaxxLauncher-"+QString::fromLatin1(QCryptographicHash::hash(file.toUtf8(),QCryptographicHash::Sha256).toHex().left(24));
    QLockFile lock(file+".manager.lock");
    if(!lock.tryLock(0)) {
        QLocalSocket socket;
        for(int attempt=0;attempt<10;++attempt) {
            socket.connectToServer(serverName);
            if(socket.waitForConnected(300)) {socket.write(args.contains("--tray")?"ping":"show"); socket.waitForBytesWritten(1000); return 0;}
            socket.abort(); QThread::msleep(100);
        }
        QMessageBox::warning(nullptr,"SCADMaxx Launcher","Another manager is starting or unavailable. Try again shortly."); return 1;
    }
    if(!readConfig(file,config,error)) {
        QMessageBox box(QMessageBox::Warning,"Settings need attention",error+"\n"+file,QMessageBox::Cancel);
        auto *reset=box.addButton("Back up and start fresh",QMessageBox::ActionRole); box.exec();
        if(box.clickedButton()!=reset) return 1;
        const auto backup=file+".backup-"+QUuid::createUuid().toString(QUuid::WithoutBraces);
        if(!QFile::copy(file,backup) || !writeConfig(file,Config(),error)) {QMessageBox::critical(nullptr,"Settings error","Could not back up/reset settings. "+error); return 1;}
        config=Config();
    }
    QLocalServer::removeServer(serverName); QLocalServer server; server.setSocketOptions(QLocalServer::UserAccessOption);
    if(!server.listen(serverName)) {QMessageBox::critical(nullptr,"SCADMaxx Launcher",server.errorString()); return 1;}
    Manager manager(config,file);
    QObject::connect(&server,&QLocalServer::newConnection,&manager,[&]{
        while(auto *client=server.nextPendingConnection()) {
            auto receive=[client,&manager]{if(client->readAll().contains("show")) manager.openWindow(); client->disconnectFromServer();};
            QObject::connect(client,&QLocalSocket::readyRead,&manager,receive);
            QObject::connect(client,&QLocalSocket::disconnected,client,&QObject::deleteLater); if(client->bytesAvailable()) receive();
        }
    });
    if(!args.contains("--tray") || !manager.hasTray()) manager.show();
    return app.exec();
}
