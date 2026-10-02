#include "core.h"
#include <QtWidgets>
#include <QtConcurrent>
#include <QLocalServer>
#include <QLocalSocket>
#include <QLockFile>
#include <QCryptographicHash>
#include <QTemporaryDir>

class BuildComboBox final : public QComboBox {
protected:
    void paintEvent(QPaintEvent *event) override {
        QComboBox::paintEvent(event);
        QPainter painter(this); painter.setRenderHint(QPainter::Antialiasing);
        painter.setPen(QPen(palette().color(QPalette::Text), 1.4));
        const QPointF center(width() - 17, height() / 2.0);
        painter.drawLine(center + QPointF(-4, -2), center + QPointF(0, 2));
        painter.drawLine(center + QPointF(0, 2), center + QPointF(4, -2));
    }
};

class Manager final : public QMainWindow {
public:
    Manager(Config config, QString file, bool smoke = false)
        : saved(std::move(config)), draft(saved.mappings), settingsFile(std::move(file)), testing(smoke) {
        setWindowTitle("SCADMaxx Launcher"); setObjectName("launcher"); resize(760, 580); setMinimumSize(660, 560);
        QPixmap pixmap(32, 32); pixmap.fill(QColor("#5143ba"));
        QPainter painter(&pixmap); painter.setPen(Qt::white); QFont font = painter.font();
        font.setPixelSize(23); font.setBold(true); painter.setFont(font); painter.drawText(pixmap.rect(), Qt::AlignCenter, "S"); painter.end();
        setWindowIcon(QIcon(pixmap));
        auto *central = new QWidget; setCentralWidget(central); auto *outer = new QVBoxLayout(central);
        outer->setContentsMargins(0, 0, 0, 0); outer->setSpacing(0);
        auto *header = new QFrame; header->setObjectName("appHeader"); auto *headerLayout = new QHBoxLayout(header);
        headerLayout->setContentsMargins(24, 14, 24, 14); headerLayout->setSpacing(10);
        auto *logo = new QLabel("S"); logo->setObjectName("brandMark"); logo->setAlignment(Qt::AlignCenter); logo->setFixedSize(34, 32);
        auto *brand = new QLabel("SCADMaxx Launcher"); brand->setObjectName("brandName");
        headerLayout->addWidget(logo); headerLayout->addWidget(brand); headerLayout->addStretch(); outer->addWidget(header);
        auto *body = new QWidget; auto *layout = new QVBoxLayout(body);
        layout->setContentsMargins(24, 22, 24, 20); layout->setSpacing(16); outer->addWidget(body, 1);
        auto *heading = new QLabel("File associations"); heading->setObjectName("pageTitle"); layout->addWidget(heading);
        mappingArea = new QScrollArea; mappingArea->setObjectName("mappingArea"); mappingArea->setFrameShape(QFrame::NoFrame);
        mappingArea->setWidgetResizable(true); mappingArea->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        auto *mappingContent = new QWidget; mappingContent->setObjectName("mappingContent");
        mappingLayout = new QVBoxLayout(mappingContent); mappingLayout->setContentsMargins(0, 0, 0, 0); mappingLayout->setSpacing(0);
        mappingArea->setWidget(mappingContent); layout->addWidget(mappingArea);
        auto *actions = new QHBoxLayout;
        actions->setSpacing(8);
        button(actions, "+ Extension", [this]{addExtension();});
        scan = button(actions, "Rescan builds", [this]{rescan();});
        auto *folderToggle = button(actions, "Manage builds…", [this]{
            discoveryPanel->setVisible(!discoveryPanel->isVisible());
            if (discoveryPanel->isVisible()) resize(width(), qMax(height(), 860));
        });
        folderToggle->setCheckable(true);
        reviewPending = button(actions, "Review new builds", [this]{
            if (reviewBuilds(pendingCandidates, "Review discovered builds")) {pendingCandidates.clear(); reviewPending->hide();}
        });
        reviewPending->hide();
        actions->addStretch(); layout->addLayout(actions);
        discoveryPanel = new QWidget; discoveryPanel->setObjectName("discoveryPanel");
        auto *discoveryLayout = new QVBoxLayout(discoveryPanel); discoveryLayout->setContentsMargins(0, 0, 0, 0);
        auto *addActions = new QHBoxLayout;
        button(addActions, "Add installed build…", [this]{addInstalledBuild();});
        button(addActions, "Add builds collection…", [this]{addFolder();});
        button(addActions, "Add executable…", [this]{addBuild();}); addActions->addStretch(); discoveryLayout->addLayout(addActions);
        auto *folderTitle = new QLabel("Build collections"); folderTitle->setObjectName("sectionTitle"); discoveryLayout->addWidget(folderTitle);
        auto *guidance = new QLabel("Collections scan one level down. Artifacts, runs, source worktrees and dependencies are skipped.\nChoose an installed build directly to include one from those locations.");
        guidance->setWordWrap(true); guidance->setObjectName("mappingStatus"); discoveryLayout->addWidget(guidance);
        folders = new QListWidget; folders->setFixedHeight(72); folders->addItems(saved.folders); discoveryLayout->addWidget(folders);
        auto *folderActions = new QHBoxLayout;
        button(folderActions, "Remove collection", [this]{removeFolder();});
        button(folderActions, "Included builds…", [this]{reviewBuilds(saved.builds, "Manage included builds");});
        button(folderActions, "Excluded builds…", [this]{
            QVector<Build> candidates; for (const auto &path : saved.excludedBuilds) candidates.append(describeBuild(path));
            reviewBuilds(candidates, "Restore excluded builds");
        });
        folderActions->addStretch();
        scanAtStart = new QCheckBox("Scan at startup"); scanAtStart->setChecked(saved.scanOnStartup);
        folderActions->addWidget(scanAtStart); discoveryLayout->addLayout(folderActions); layout->addWidget(discoveryPanel); discoveryPanel->hide();
        connect(scanAtStart, &QCheckBox::toggled, this, [this](bool enabled){
            Config next = saved; next.scanOnStartup = enabled;
            if (!persist(next)) { QSignalBlocker block(scanAtStart); scanAtStart->setChecked(saved.scanOnStartup); }
        });
        auto *setupActions = new QHBoxLayout;
        associationSummary = new QLabel("Windows setup needed"); setupActions->addWidget(associationSummary, 1);
        button(setupActions, "Open Windows Default Apps", [this]{setupWindows();});
        layout->addLayout(setupActions);
        auto *separator = new QFrame; separator->setObjectName("separator"); separator->setFixedHeight(1); layout->addWidget(separator);
        auto *preferences = new QHBoxLayout;
        keepTray = new QCheckBox("Keep in system tray"); keepTray->setChecked(saved.tray);
        startup = new QCheckBox("Start at sign-in"); startup->setChecked(saved.startup);
        preferences->addWidget(keepTray); preferences->addWidget(startup); preferences->addStretch(); layout->addLayout(preferences);
        layout->addStretch();
        connect(keepTray, &QCheckBox::toggled, this, [this](bool enabled){
            Config next = saved; next.tray = enabled;
            if (persist(next)) updateTray(); else { QSignalBlocker block(keepTray); keepTray->setChecked(saved.tray); }
        });
        connect(startup, &QCheckBox::toggled, this, [this](bool enabled){
            QString error;
            if (!setStartup(enabled, QCoreApplication::applicationFilePath(), error)) { fail(error); QSignalBlocker block(startup); startup->setChecked(saved.startup); return; }
            Config next = saved; next.startup = enabled;
            if (!persist(next)) { setStartup(saved.startup, QCoreApplication::applicationFilePath(), error); QSignalBlocker block(startup); startup->setChecked(saved.startup); }
        });
        auto *footer = new QFrame; footer->setObjectName("appFooter"); auto *bottom = new QHBoxLayout(footer);
        bottom->setContentsMargins(24, 16, 24, 16); bottom->setSpacing(8);
        status = new QLabel("Ready"); status->setWordWrap(true); bottom->addWidget(status, 1);
        revert = button(bottom, "Revert", [this]{draft = saved.mappings; render(); status->setText("Pending mapping changes discarded.");});
        apply = button(bottom, "Apply", [this]{applyMappings();}); apply->setObjectName("primaryButton"); apply->setDefault(true); outer->addWidget(footer);
        tray = new QSystemTrayIcon(windowIcon(), this); tray->setToolTip("SCADMaxx Launcher");
        menu = new QMenu(this); tray->setContextMenu(menu);
        connect(menu, &QMenu::aboutToShow, this, [this]{refreshMenu();});
        connect(tray, &QSystemTrayIcon::activated, this, [this](QSystemTrayIcon::ActivationReason reason){
            if (reason == QSystemTrayIcon::Trigger || reason == QSystemTrayIcon::DoubleClick) openWindow();
        });
        connect(&watcher, &QFutureWatcher<QVector<Build>>::finished, this, [this]{
            scan->setEnabled(true);
            QVector<Build> candidates;
            for (const auto &build : watcher.result())
                if (!saved.excludedBuilds.contains(pathKey(build.path))) candidates.append(build);
            if (backgroundScan) {
                pendingCandidates.clear();
                for (const auto &candidate : candidates) {
                    bool known = false; for (const auto &build : saved.builds) known |= pathKey(build.path) == pathKey(candidate.path);
                    if (!known) pendingCandidates.append(candidate);
                }
                reviewPending->setVisible(!pendingCandidates.isEmpty());
                status->setText(pendingCandidates.isEmpty() ? "Scan complete. No new builds." : "New builds found. Review them before importing.");
            } else reviewBuilds(candidates, "Review discovered builds");
        });
        connect(qApp, &QApplication::applicationStateChanged, this, [this](Qt::ApplicationState state){
            if (state == Qt::ApplicationActive) refreshAssociationStatus();
        });
        refreshAppearance(); render(); updateTray();
        resize(760, qMax(640, minimumSizeHint().height()));
#if QT_VERSION >= QT_VERSION_CHECK(6, 5, 0)
        connect(qApp->styleHints(), &QStyleHints::colorSchemeChanged, this, [this]{refreshAppearance();});
#endif
        if (saved.scanOnStartup && !testing) QTimer::singleShot(0, this, [this]{rescan(true);});
    }

    ~Manager() override { watcher.waitForFinished(); }
    void openWindow() { showNormal(); raise(); activateWindow(); }
    bool hasTray() const { return tray->isVisible(); }

    bool smokeTest() {
        if (mappingRows.size() != 2 || apply->isEnabled()) return false;
        QTemporaryDir fixture;
        const auto first = fixture.filePath("master-A.exe"), second = fixture.filePath("master-B.exe");
        for (const auto &path : {first, second}) { QFile f(path); if (!f.open(QIODevice::WriteOnly)) return false; f.write("fixture"); }
        Config seeded = saved;
        seeded.builds = {{first, "Master A", {}}, {second, "Master B", {}}};
        seeded.mappings[".scad"] = first; seeded.mappings[".scadmax"] = first;
        if (!persist(seeded)) return false;
        draft = saved.mappings; render();
        auto *combo = mappingRows.value(".scad")->findChild<QComboBox *>();
        combo->setCurrentIndex(combo->findData(second));
        if (draft[".scad"] != second || !apply->isEnabled()) return false;
        apply->click();
        Config loaded; QString error;
        if (!readConfig(settingsFile, loaded, error) || loaded.mappings[".scad"] != second) return false;
        draft[".scadmax"] = second;
        refreshMenu();
        auto *sub = menu->actions().first()->menu();
        if (!sub || !sub->actions().at(1)->isChecked()) return false;
        sub->actions().first()->trigger();
        if (saved.mappings[".scad"] != first || draft[".scad"] != first || draft[".scadmax"] != second) return false;
        if (!readConfig(settingsFile, loaded, error) || loaded.mappings[".scad"] != first) return false;
        // Exercise the review dialog without changing Windows settings.
        const Build third{fixture.filePath("third.exe"), "Another build", "1.0"};
        bool reviewSeen = false;
        QTimer::singleShot(0, this, [&]{
            auto *dialog = qobject_cast<QDialog *>(QApplication::activeModalWidget());
            if (!dialog) return;
            auto *review = dialog->findChild<QTableWidget *>("buildReview");
            reviewSeen = review && review->item(0, 0)->checkState() == Qt::Unchecked;
            if (reviewSeen) review->item(0, 0)->setCheckState(Qt::Checked);
            dialog->accept();
        });
        if (!reviewBuilds({third}, "Review test") || !reviewSeen || saved.builds.size() != 3) return false;
        QTimer::singleShot(0, this, []{
            if (auto *dialog = qobject_cast<QDialog *>(QApplication::activeModalWidget())) dialog->reject();
        });
        if (reviewBuilds({third}, "Cancel test") || saved.builds.size() != 3) return false;
        saved = Config(); draft = saved.mappings; render();
        draft[".scad"] = "missing.exe"; render();
        if (!apply->isEnabled()) return false;
        revert->click();
        refreshMenu();
        const bool passed = draft == saved.mappings && !apply->isEnabled() && menu->actions().size() == 6;
        if (qEnvironmentVariableIsSet("SCADMAXX_LAUNCHER_MANAGE_CAPTURE")) {
            discoveryPanel->show(); resize(850, 860);
        }
        return passed;
    }

protected:
    void closeEvent(QCloseEvent *event) override {
        if (!confirmDiscard()) { event->ignore(); return; }
        if (hasTray()) { hide(); event->ignore(); }
        else { event->accept(); qApp->quit(); }
    }

private:
    Config saved; QMap<QString, QString> draft; QString settingsFile; bool testing;
    QScrollArea *mappingArea; QVBoxLayout *mappingLayout; QMap<QString, QWidget *> mappingRows;
    QWidget *discoveryPanel; QListWidget *folders; QLabel *status, *associationSummary;
    QPushButton *apply, *revert, *scan, *reviewPending; QCheckBox *keepTray, *startup, *scanAtStart;
    QVector<Build> pendingCandidates; bool backgroundScan = false;
    QSystemTrayIcon *tray; QMenu *menu; QFutureWatcher<QVector<Build>> watcher;

    void refreshAppearance() {
        bool dark = palette().color(QPalette::Window).lightness() < 128;
#if QT_VERSION >= QT_VERSION_CHECK(6, 5, 0)
        dark = qApp->styleHints()->colorScheme() == Qt::ColorScheme::Dark;
#endif
        if (testing && qEnvironmentVariable("SCADMAXX_LAUNCHER_THEME") == "dark") dark = true;
        const QString bg = dark ? "#202126" : "#fafafa", panel = dark ? "#292a31" : "#ffffff";
        const QString text = dark ? "#ececf2" : "#202127", muted = dark ? "#b8bbc9" : "#626572";
        const QString border = dark ? "#444650" : "#dedee5", accent = dark ? "#b4a9ff" : "#5143ba";
        const QString onAccent = dark ? "#202126" : "#ffffff";
        QPalette theme = palette();
        theme.setColor(QPalette::Window, QColor(bg)); theme.setColor(QPalette::Base, QColor(panel));
        theme.setColor(QPalette::Text, QColor(text)); theme.setColor(QPalette::WindowText, QColor(text));
        theme.setColor(QPalette::Button, QColor(panel)); theme.setColor(QPalette::ButtonText, QColor(text));
        theme.setColor(QPalette::Highlight, QColor(accent)); theme.setColor(QPalette::HighlightedText, QColor(onAccent));
        setPalette(theme);
        setStyleSheet(QString(R"(
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

    template<class F> QPushButton *button(QHBoxLayout *layout, const QString &text, F callback) {
        auto *result = new QPushButton(text); layout->addWidget(result);
        connect(result, &QPushButton::clicked, this, callback); return result;
    }
    void fail(const QString &error) { QMessageBox::warning(this, "SCADMaxx Launcher", error); }
    bool persist(const Config &next) {
        QString error;
        if (!writeConfig(settingsFile, next, error)) { fail(error); return false; }
        saved = next; return true;
    }
    bool confirmDiscard() {
        if (draft == saved.mappings) return true;
        if (QMessageBox::question(this, "Pending changes", "Discard pending mapping changes?",
            QMessageBox::Discard | QMessageBox::Cancel, QMessageBox::Cancel) != QMessageBox::Discard) return false;
        draft = saved.mappings; render(); return true;
    }
    void updateTray() {
        if (!testing && saved.tray && QSystemTrayIcon::isSystemTrayAvailable()) tray->show();
        else tray->hide();
    }
    void refreshAssociationStatus() {
        bool allAssociated = !mappingRows.isEmpty();
        for (auto it = mappingRows.begin(); it != mappingRows.end(); ++it) {
            const auto ext = it.key();
            const bool associated = isDefaultHandler(ext, QCoreApplication::applicationFilePath());
            allAssociated &= associated;
            const auto selected = draft.value(ext);
            QString label = draft.value(ext) != saved.mappings.value(ext) ? "Pending change"
                : associated ? "Windows → Launcher → selected build" : "Windows setup needed";
            if (!selected.isEmpty() && !validExecutable(selected, QCoreApplication::applicationFilePath()))
                label = "Executable missing · choose a replacement";
            it.value()->findChild<QLabel *>("mappingStatus")->setText(label);
        }
        associationSummary->setText(allAssociated ? "Windows uses SCADMaxx Launcher" : "Windows setup needed");
    }
    void render() {
        mappingRows.clear();
        while (auto *item = mappingLayout->takeAt(0)) {
            if (item->widget()) { item->widget()->hide(); item->widget()->deleteLater(); }
            delete item;
        }
        for (auto it = draft.begin(); it != draft.end(); ++it) {
            const QString ext = it.key();
            auto *row = new QFrame; row->setObjectName("mappingRow"); row->setMinimumHeight(120);
            row->setAttribute(Qt::WA_StyledBackground, true);
            auto *rowLayout = new QHBoxLayout(row); rowLayout->setContentsMargins(0, 16, 0, 16); rowLayout->setSpacing(14);
            auto *extension = new QLabel(ext); extension->setObjectName("extensionName");
            extension->setFixedWidth(96); rowLayout->addWidget(extension, 0, Qt::AlignTop);
            auto *cell = new QWidget; auto *layout = new QVBoxLayout(cell); layout->setContentsMargins(0, 0, 0, 0); layout->setSpacing(6);
            rowLayout->addWidget(cell, 1);
            auto *combo = new BuildComboBox; combo->setAccessibleName("Build for " + ext);
            combo->setSizeAdjustPolicy(QComboBox::AdjustToMinimumContentsLengthWithIcon); combo->setMinimumContentsLength(12);
            combo->addItem("Choose a build", QString());
            for (const auto &build : saved.builds) {
                const bool exists = validExecutable(build.path, QCoreApplication::applicationFilePath());
                combo->addItem(build.name + (build.version.isEmpty() ? "" : " · " + build.version) + (exists ? "" : " — missing"), build.path);
                combo->setItemData(combo->count() - 1, QDir::toNativeSeparators(build.path), Qt::ToolTipRole);
            }
            int selection = combo->findData(it.value());
            if (selection < 0) { combo->addItem("Unavailable: " + it.value(), it.value()); selection = combo->count() - 1; }
            combo->setCurrentIndex(selection); layout->addWidget(combo);
            auto *path = new QLabel(it.value().isEmpty() ? "No executable selected" : QDir::toNativeSeparators(it.value()));
            path->setObjectName("buildPath"); path->setMinimumWidth(0); path->setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Preferred);
            path->setWordWrap(true); path->setTextInteractionFlags(Qt::TextSelectableByMouse); layout->addWidget(path);
            auto *rowStatus = new QLabel; rowStatus->setObjectName("mappingStatus"); rowStatus->setWordWrap(true); layout->addWidget(rowStatus);
            auto *remove = new QPushButton("×"); remove->setObjectName("removeExtension"); remove->setFixedSize(22, 32);
            remove->setAccessibleName("Remove " + ext); remove->setToolTip("Remove " + ext);
            rowLayout->addWidget(remove, 0, Qt::AlignTop); connect(remove, &QPushButton::clicked, this, [this, ext]{removeExtension(ext);});
            mappingLayout->addWidget(row); mappingRows.insert(ext, row);
            auto *line = new QFrame; line->setObjectName("separator"); line->setFixedHeight(1); mappingLayout->addWidget(line);
            connect(combo, &QComboBox::currentIndexChanged, this, [this, combo, ext, path]{
                draft[ext] = combo->currentData().toString(); path->setText(draft[ext].isEmpty() ? "No executable selected" : QDir::toNativeSeparators(draft[ext]));
                updateDirty(); refreshAssociationStatus();
            });
        }
        mappingLayout->addStretch();
        mappingArea->setFixedHeight(qMin(440, qMax(120, static_cast<int>(draft.size()) * 121 + 2)));
        refreshAssociationStatus(); updateDirty();
    }
    void updateDirty() {
        const bool dirty = draft != saved.mappings; apply->setEnabled(dirty); revert->setEnabled(dirty);
        status->setText(dirty ? "Pending mapping changes" : "No pending mapping changes");
    }
    void applyMappings() {
        for (auto it = draft.begin(); it != draft.end(); ++it) {
            // Allow unconfigured extensions; dispatch will provide a recoverable error.
            if (!it.value().isEmpty() && !validExecutable(it.value(), QCoreApplication::applicationFilePath())) {
                fail("Choose an available executable for " + it.key() + ".\n" + it.value()); return;
            }
        }
        Config next = saved; next.mappings = draft;
        if (persist(next)) { render(); status->setText("Mappings saved. Future opens use these builds."); }
    }
    void addExtension() {
        bool ok = false; const auto text = QInputDialog::getText(this, "Add extension", "File extension (for example .scadmax)", QLineEdit::Normal, {}, &ok);
        if (!ok) return; const auto ext = normalizedExtension(text);
        if (ext.isEmpty() || draft.contains(ext)) { fail("Enter a valid, unique extension."); return; }
        draft.insert(ext, {}); render();
    }
    void removeExtension(const QString &ext) {
        if (QMessageBox::question(this, "Remove extension", "Remove " + ext + " from the launcher? If Windows uses this launcher, choose another default app in Windows Settings.") != QMessageBox::Yes) return;
        draft.remove(ext); render();
    }
    void addBuild() {
        const auto path = QFileDialog::getOpenFileName(this, "Choose editor executable", buildPickerStart(), "Executables (*.exe)");
        if (path.isEmpty()) return;
        if (!validExecutable(path, QCoreApplication::applicationFilePath())) { fail("Choose an editor executable, not this launcher."); return; }
        reviewBuilds({describeBuild(path)}, "Add executable");
    }
    QString buildPickerStart() const {
        if (!saved.folders.isEmpty()) return saved.folders.last();
        return QDir("D:/openscad").exists() ? "D:/openscad" : QDir::homePath();
    }
    void addInstalledBuild() {
        const auto folder = QFileDialog::getExistingDirectory(this, "Select one extracted build folder", buildPickerStart());
        if (!folder.isEmpty()) reviewBuilds(discoverInstalled(folder), "Add installed build");
    }
    bool reviewBuilds(const QVector<Build> &candidates, const QString &title) {
        if (candidates.isEmpty()) {
            status->setText("No candidates found. Choose an extracted build folder or add its executable directly.");
            return false;
        }
        // Copy: accepting the dialog can change saved.builds, which may be the input vector.
        const auto choices = candidates;
        QDialog dialog(this); dialog.setWindowTitle(title); dialog.resize(850, 450);
        auto *layout = new QVBoxLayout(&dialog); layout->setContentsMargins(20, 20, 20, 20); layout->setSpacing(14);
        auto *hint = new QLabel("Check the builds to include in selectors and tray menus. Unchecked builds stay excluded on rescans.");
        hint->setWordWrap(true); layout->addWidget(hint);
        auto *list = new QTableWidget(choices.size(), 3); list->setObjectName("buildReview");
        list->setHorizontalHeaderLabels({"Build", "Version", "Full path"}); list->verticalHeader()->hide();
        list->setEditTriggers(QAbstractItemView::NoEditTriggers); list->setSelectionBehavior(QAbstractItemView::SelectRows);
        list->horizontalHeader()->setSectionResizeMode(0, QHeaderView::ResizeToContents);
        list->horizontalHeader()->setSectionResizeMode(1, QHeaderView::ResizeToContents);
        list->horizontalHeader()->setSectionResizeMode(2, QHeaderView::Stretch); list->setWordWrap(true);
        int row = 0;
        for (const auto &build : choices) {
            const auto key = pathKey(build.path); bool known = false, inUse = false;
            for (const auto &current : saved.builds) known |= pathKey(current.path) == key;
            for (const auto &path : saved.mappings) inUse |= !path.isEmpty() && pathKey(path) == key;
            for (const auto &path : draft) inUse |= !path.isEmpty() && pathKey(path) == key;
            auto *item = new QTableWidgetItem(build.name + (inUse ? " (in use)" : ""));
            item->setFlags(Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsUserCheckable);
            item->setCheckState(known || inUse ? Qt::Checked : Qt::Unchecked);
            if (inUse) { item->setFlags(item->flags() & ~Qt::ItemIsUserCheckable); item->setToolTip("Change its extension mapping before excluding this build."); }
            list->setItem(row, 0, item); list->setItem(row, 1, new QTableWidgetItem(build.version.isEmpty() ? "Unknown" : build.version));
            auto *pathItem = new QTableWidgetItem(QDir::toNativeSeparators(build.path)); pathItem->setToolTip(build.path);
            list->setItem(row++, 2, pathItem);
        }
        list->resizeRowsToContents(); layout->addWidget(list, 1);
        auto *buttons = new QDialogButtonBox(QDialogButtonBox::Save | QDialogButtonBox::Cancel);
        buttons->button(QDialogButtonBox::Save)->setText("Save selection");
        buttons->button(QDialogButtonBox::Save)->setObjectName("primaryButton"); layout->addWidget(buttons);
        connect(buttons, &QDialogButtonBox::accepted, &dialog, &QDialog::accept);
        connect(buttons, &QDialogButtonBox::rejected, &dialog, &QDialog::reject);
        if (dialog.exec() != QDialog::Accepted) return false;
        QStringList selected; for (int i = 0; i < choices.size(); ++i)
            if (list->item(i, 0)->checkState() == Qt::Checked) selected.append(choices[i].path);
        Config next = saved; QString error;
        if (!applyBuildReview(next, choices, selected, draft.values(), error)) {fail(error); return false;}
        if (!persist(next)) return false;
        render(); status->setText("Build list updated. Extension mappings unchanged."); return true;
    }
    void addFolder() {
        const auto folder = QFileDialog::getExistingDirectory(this, "Select a collection of installed builds", buildPickerStart());
        if (folder.isEmpty()) return;
        if (excludedCollectionFolder(folder)) {
            fail("This is an artifacts, source or dependency folder. Use Add installed build to select one specific build inside it."); return;
        }
        for (const auto &existing : saved.folders) if (pathKey(existing) == pathKey(folder)) return;
        Config next = saved; next.folders.append(folder);
        if (persist(next)) { folders->clear(); folders->addItems(saved.folders); rescan(); }
    }
    void removeFolder() {
        const int row = folders->currentRow(); if (row < 0) return;
        Config next = saved; next.folders.removeAt(row);
        if (persist(next)) { folders->clear(); folders->addItems(saved.folders); }
    }
    void rescan(bool background = false) {
        if (watcher.isRunning()) return;
        if (saved.folders.isEmpty()) {
            if (!background) {openWindow(); discoveryPanel->show(); resize(width(), qMax(height(), 860));}
            status->setText("Add an installed build or a builds collection first."); return;
        }
        backgroundScan = background;
        scan->setEnabled(false); status->setText("Scanning configured folders…");
        const auto roots = saved.folders;
        watcher.setFuture(QtConcurrent::run([roots]{ return discover(roots); }));
    }
    void setupWindows() {
        if (draft != saved.mappings) { fail("Apply or revert mapping changes before Windows setup."); return; }
        QString error;
        if (!registerHandlers(saved, QCoreApplication::applicationFilePath(), error)) { fail(error); return; }
        if (!QDesktopServices::openUrl(QUrl("ms-settings:defaultapps?registeredAppUser=SCADMaxx%20Launcher")))
            fail("Open Windows Settings > Apps > Default apps, then select SCADMaxx Launcher.");
        else status->setText("Choose SCADMaxx Launcher for each extension in Windows Settings.");
    }
    void selectFromTray(const QString &ext, const QString &path) {
        if (!validExecutable(path, QCoreApplication::applicationFilePath())) { openWindow(); fail("Build is unavailable:\n" + path); return; }
        const bool replaced = draft.value(ext) != saved.mappings.value(ext) || !draft.contains(ext);
        Config next = saved; next.mappings[ext] = path;
        if (!persist(next)) return;
        draft[ext] = path; render();
        status->setText(ext + " mapping saved." + (replaced ? " Pending edit to this extension replaced." : ""));
        if (!testing) tray->showMessage("SCADMaxx Launcher", ext + " → " + QFileInfo(path).dir().dirName(), QSystemTrayIcon::Information, 2000);
    }
    void refreshMenu() {
        menu->clear();
        for (auto it = saved.mappings.begin(); it != saved.mappings.end(); ++it) {
            const QString ext = it.key(); auto *sub = menu->addMenu(ext);
            for (const auto &build : saved.builds) {
                auto *action = sub->addAction(build.name); action->setCheckable(true);
                action->setChecked(pathKey(build.path) == pathKey(it.value())); action->setToolTip(build.path);
                action->setEnabled(validExecutable(build.path, QCoreApplication::applicationFilePath()));
                connect(action, &QAction::triggered, this, [this, ext, path = build.path]{selectFromTray(ext, path);});
            }
            if (saved.builds.isEmpty()) sub->addAction("Add builds in the manager")->setEnabled(false);
        }
        menu->addSeparator(); menu->addAction("Open manager", this, [this]{openWindow();});
        auto *rescanAction = menu->addAction("Rescan builds", this, [this]{rescan();}); rescanAction->setEnabled(!watcher.isRunning());
        menu->addAction("Quit", this, [this]{if (confirmDiscard()) qApp->quit();});
    }
};

int main(int argc, char **argv) {
    QApplication app(argc, argv);
    QCoreApplication::setOrganizationName("SCADMaxx"); QCoreApplication::setApplicationName("Launcher");
    QApplication::setApplicationDisplayName("SCADMaxx Launcher");
    QApplication::setQuitOnLastWindowClosed(false);
    const auto args = app.arguments();
    if (args.contains("--smoke-test")) {
        // Offscreen QPA has no Windows font database; load a local font only for capture tests.
        if (qEnvironmentVariable("QT_QPA_PLATFORM") == "offscreen") {
            const auto fontFile = qEnvironmentVariable("WINDIR") + "/Fonts/segoeui.ttf";
            const int fontId = QFontDatabase::addApplicationFont(fontFile);
            QFontDatabase::addApplicationFont(qEnvironmentVariable("WINDIR") + "/Fonts/seguisb.ttf");
            if (fontId >= 0) app.setFont(QFont(QFontDatabase::applicationFontFamilies(fontId).value(0), 9));
        }
        QTemporaryDir temp; Manager manager(Config(), temp.filePath("settings.json"), true);
        manager.show(); app.processEvents();
        const bool success = manager.smokeTest();
        QCoreApplication::sendPostedEvents(nullptr, QEvent::DeferredDelete); app.processEvents();
        const auto capture = qEnvironmentVariable("SCADMAXX_LAUNCHER_CAPTURE");
        if (!capture.isEmpty()) manager.grab().save(capture);
        return success ? 0 : 1;
    }
    Config config; QString error; const QString file = configLocation();
    if (!readConfig(file, config, error)) { QMessageBox::critical(nullptr, "Settings error", error + "\n" + file); return 1; }
    if (args.size() > 1 && args.at(1) == "--open") {
        if (args.size() < 3) { QMessageBox::warning(nullptr, "SCADMaxx Launcher", "No file specified."); return 2; }
        for (const auto &document : args.mid(2)) {
            QString program; QStringList arguments;
            if (!resolveOpen(config, document, app.applicationFilePath(), program, arguments, error)
                || !QProcess::startDetached(program, arguments, QFileInfo(document).absolutePath())) {
                if (error.isEmpty()) error = "Could not start editor: " + program;
                QMessageBox box(QMessageBox::Warning, "Cannot open file", error, QMessageBox::Close);
                auto *manage = box.addButton("Open manager", QMessageBox::ActionRole); box.exec();
                if (box.clickedButton() == manage) QProcess::startDetached(app.applicationFilePath(), QStringList{});
                return 1;
            }
        }
        return 0;
    }
    if (args.size() > 1 && args.at(1) != "--tray") {
        QMessageBox::warning(nullptr, "SCADMaxx Launcher", "Use --open <file> to open a document, or --tray to start quietly."); return 2;
    }
    QDir().mkpath(QFileInfo(file).absolutePath());
    const QString serverName = "SCADMaxxLauncher-" + QString::fromLatin1(QCryptographicHash::hash(file.toUtf8(), QCryptographicHash::Sha256).toHex().left(24));
    QLockFile lock(file + ".manager.lock");
    if (!lock.tryLock(0)) {
        QLocalSocket socket;
        for (int attempt = 0; attempt < 10; ++attempt) {
            socket.connectToServer(serverName);
            if (socket.waitForConnected(300)) {
                socket.write(args.contains("--tray") ? "ping" : "show"); socket.waitForBytesWritten(1000); return 0;
            }
            socket.abort(); QThread::msleep(100);
        }
        QMessageBox::warning(nullptr, "SCADMaxx Launcher", "Another manager is starting or unavailable. Try again shortly."); return 1;
    }
    QLocalServer::removeServer(serverName); QLocalServer server;
    server.setSocketOptions(QLocalServer::UserAccessOption);
    if (!server.listen(serverName)) { QMessageBox::critical(nullptr, "SCADMaxx Launcher", server.errorString()); return 1; }
    // Read again after taking the manager lock; another process may just have saved changes.
    if (!readConfig(file, config, error)) { QMessageBox::critical(nullptr, "Settings error", error); return 1; }
    Manager manager(config, file);
    QObject::connect(&server, &QLocalServer::newConnection, &manager, [&]{
        while (auto *client = server.nextPendingConnection()) {
            auto receive = [client, &manager]{ if (client->readAll().contains("show")) manager.openWindow(); client->disconnectFromServer(); };
            QObject::connect(client, &QLocalSocket::readyRead, &manager, receive);
            QObject::connect(client, &QLocalSocket::disconnected, client, &QObject::deleteLater);
            if (client->bytesAvailable()) receive();
        }
    });
    if (!args.contains("--tray") || !manager.hasTray()) manager.show();
    return app.exec();
}
