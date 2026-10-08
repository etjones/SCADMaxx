#pragma once
// Shared validation-only helper: normal document/Preview paths, no capture bypasses.
#include "gui/MainWindow.h"
#include "gui/TabManager.h"
#include "gui/QGLView.h"
#include "gui/Console.h"
#include <QApplication>
#include <QElapsedTimer>
#include <QFile>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QCryptographicHash>
#include <QDir>
#include <QTest>
#include <QEventLoop>
#include <QTimer>

inline int runGuiPreviewBenchmark(MainWindow *window)
{
  const auto model = qEnvironmentVariable("OPENSCAD_BENCHMARK_MODEL");
  const auto output = qEnvironmentVariable("OPENSCAD_BENCHMARK_OUTPUT");
  if (model.isEmpty() || output.isEmpty() || !QFile::exists(model)) return 1;
  QDir().mkpath(output);
  window->designActionAutoReload->setChecked(false);
  window->resize(1280, 820);
  window->show();
  if (!QTest::qWaitForWindowExposed(window, 10000)) return 2;
  QTest::qWait(100);
  QJsonArray samples;
  bool failed = false;
  QByteArray expected;
  for (int iteration = 0; iteration < 3; ++iteration) {
    bool done = false;
    // Let the GUI thread sleep while a background evaluator works. Polling
    // processEvents in a tight loop competes for CPU and biases native timings.
    QEventLoop completionLoop;
    QTimer timeout;
    timeout.setSingleShot(true);
    QObject::connect(&timeout, &QTimer::timeout, &completionLoop, &QEventLoop::quit);
    double signalSeconds = -1;
    QElapsedTimer timer;
    const auto connection = QObject::connect(window, &MainWindow::compilationDone, window,
      [&](SourceFile *) { done = true; signalSeconds = timer.nsecsElapsed() / 1e9; completionLoop.quit(); });
    window->console->clear();
    timer.start();
    if (iteration == 0) window->tabManager->open(model);
    window->actionRenderPreview();
    if (!done) {
      timeout.start(90000);
      completionLoop.exec();
      timeout.stop();
    }
    const double returnedSeconds = timer.nsecsElapsed() / 1e9;
    QObject::disconnect(connection);
    const bool valid = done && window->compileErrors == 0 && window->rootNode && window->previewRenderer;
    QByteArray csg;
    if (valid) csg = QByteArray::fromStdString(window->tree.getString(*window->rootNode, "  "));
    const auto hash = QCryptographicHash::hash(csg, QCryptographicHash::Sha256).toHex();
    if (iteration == 0) expected = hash;
    QElapsedTimer capture;
    capture.start();
    const auto frame = window->qglview->grabFramebuffer();
    const double captureSeconds = capture.nsecsElapsed() / 1e9;
    const bool saved = !frame.isNull() && frame.save(output + "/viewport-" + QString::number(iteration) + ".png");
    QFile source(output + "/result-" + QString::number(iteration) + ".csg");
    const bool sourceSaved = source.open(QIODevice::WriteOnly) && source.write(csg) == csg.size();
    source.close();
    QCoreApplication::processEvents();
    const auto log = window->console->toPlainText();
    QFile console(output + "/console-" + QString::number(iteration) + ".txt");
    if (console.open(QIODevice::WriteOnly)) console.write(log.toUtf8());
    const bool diagnostic = log.contains("ERROR:") || log.contains("WARNING:");
    const bool ok = valid && !csg.isEmpty() && hash == expected && saved && sourceSaved && !diagnostic;
    samples.append(QJsonObject{{"iteration", iteration}, {"initial", iteration == 0},
      {"compilation_signal_seconds", signalSeconds}, {"preview_return_seconds", returnedSeconds},
      {"frame_capture_seconds", captureSeconds}, {"csg_sha256", QString::fromLatin1(hash)},
      {"status", ok ? "ok" : "failed"}});
    if (!ok) { failed = true; break; }
    QTest::qWait(100);
  }
  const QJsonObject report{{"schema", 1}, {"model", model}, {"samples", samples},
    {"status", failed ? "failed" : "ok"},
    {"scope", "Existing window: initial file open plus Preview, then unchanged Preview requests. Completion signal and return measured separately. Framebuffer capture is not first on-screen presentation."}};
  QFile result(output + "/gui.json");
  if (!result.open(QIODevice::WriteOnly)) return 3;
  result.write(QJsonDocument(report).toJson());
  return failed ? 4 : 0;
}
