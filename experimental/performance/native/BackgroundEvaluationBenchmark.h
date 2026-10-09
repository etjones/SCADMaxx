#pragma once
// Validation-only adapter for the background-evaluation branch. Keep this out
// of release source. The ordinary baseline adapter remains separate.
#include "GuiPreviewBenchmark.h"
#include "gui/evaluation/EvaluationController.h"
#include <QTimer>
#include <algorithm>

inline int runBackgroundEvaluationBenchmark(MainWindow *window)
{
  const auto output = qEnvironmentVariable("OPENSCAD_BENCHMARK_OUTPUT");
  if (output.isEmpty() || !window->backgroundEvaluation) return 1;
  QJsonArray attempts, frames, heartbeat;
  QElapsedTimer clock;
  clock.start();
  qint64 previous = 0;
  bool previouslyBusy = false;
  QObject lifetime;
  QObject::connect(window->backgroundEvaluation, &BackgroundEvaluation::Controller::attemptFinished,
    &lifetime, [&](QJsonObject metrics) { attempts.append(metrics); });
  QObject::connect(window->backgroundEvaluation, &BackgroundEvaluation::Controller::framePresented,
    &lifetime, [&](QJsonObject metrics) { frames.append(metrics); });
  QTimer timer;
  QObject::connect(&timer, &QTimer::timeout, &lifetime, [&] {
    const auto now = clock.nsecsElapsed();
    const bool busy = window->backgroundEvaluation->busy();
    // Include the interval which finishes a job. Publication removes pending
    // state before returning to this timer; checking only current busy state
    // would silently exclude exactly the GUI stalls we need to measure.
    if (busy || previouslyBusy) heartbeat.append(double(now - previous) / 1e6);
    previouslyBusy = busy;
    previous = now;
  });
  timer.start(50);
  const int ordinary = runGuiPreviewBenchmark(window);
  // Let the final normal on-screen frame complete (framebuffer capture alone
  // is not evidence of first on-screen presentation).
  QTest::qWait(100);

  QJsonObject cancellation{{"requested", false}};
  const auto cancelModel = qEnvironmentVariable("OPENSCAD_BENCHMARK_CANCEL_MODEL");
  const auto cancelStage = qEnvironmentVariable("OPENSCAD_BENCHMARK_CANCEL_STAGE");
  if (!cancelModel.isEmpty() && !cancelStage.isEmpty()) {
    window->tabManager->open(cancelModel);
    window->on_designActionPreview_triggered();
    QElapsedTimer limit; limit.start();
    bool requested = false;
    double requestAt = -1;
    while (limit.elapsed() < 90000) {
      QCoreApplication::processEvents(QEventLoop::AllEvents, 10);
      for (const auto& entry : window->backgroundEvaluation->status()) {
        const auto job = entry.toObject();
        if (!requested && job.value("stage").toString() == cancelStage) {
          cancellation["attempt_id"] = job.value("attempt_id");
          requestAt = double(limit.nsecsElapsed()) / 1e6;
          window->backgroundEvaluation->cancel(window->activeEditor);
          cancellation["acknowledgement_ms"] = double(limit.nsecsElapsed()) / 1e6 - requestAt;
          requested = true;
        }
      }
      if (!window->backgroundEvaluation->busy(window->activeEditor)) break;
      QTest::qWait(1);
    }
    cancellation["requested"] = requested;
    cancellation["stage"] = cancelStage;
    cancellation["stopped"] = requested && !window->backgroundEvaluation->busy(window->activeEditor);
    if (requested) cancellation["request_to_idle_ms"] = double(limit.nsecsElapsed()) / 1e6 - requestAt;
    // A missed stage/timeout is an unsuccessful cancellation sample, never a pass.
  }
  timer.stop();
  std::vector<double> gaps;
  for (const auto& gap : heartbeat) gaps.push_back(gap.toDouble());
  std::sort(gaps.begin(), gaps.end());
  QJsonObject summary{{"count", int(gaps.size())}};
  if (!gaps.empty()) {
    summary["max_gap_ms"] = gaps.back();
    summary["p95_gap_ms"] = gaps[std::min(gaps.size() - 1, size_t(0.95 * gaps.size()))];
    summary["target_met"] = gaps.back() <= 250 && summary["p95_gap_ms"].toDouble() < 100;
  }
  QJsonObject report{{"schema", 2}, {"ordinary_exit_code", ordinary}, {"attempts", attempts},
    {"frames", frames}, {"heartbeat_gaps_ms", heartbeat}, {"heartbeat", summary}, {"cancellation", cancellation},
    {"scope", "Native GUI observations. Stage times are elapsed offsets. Library-call stop latency is cooperative; no forced termination. Peak memory must be captured by the process runner."}};
  QFile file(output + "/background-evaluation.json");
  if (!file.open(QIODevice::WriteOnly)) return 3;
  const auto bytes = QJsonDocument(report).toJson();
  if (file.write(bytes) != bytes.size()) return 3;
  if (ordinary) return ordinary;
  if (!cancelModel.isEmpty() && !cancellation.value("stopped").toBool()) return 4;
  return 0;
}
