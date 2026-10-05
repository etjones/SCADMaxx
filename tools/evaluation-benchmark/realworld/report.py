"""Generate comparison JSON/CSV, static PNG charts and a searchable local HTML report."""
import argparse
from collections import Counter, defaultdict
import csv
import html
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys
import importlib.metadata
import platform

from corpus import save

PASS = {"exact_surface", "within_tolerance_sampled", "identical_text", "identical_image"}


def verify_output(path, expected):
    from benchmark import file_hash
    return path.exists() and file_hash(path) == expected


def compare_pair(a, b, stage, folder, tolerance, relative, samples):
    from corpus import sha
    if a.get("dependencies") != b.get("dependencies"):
        return {"status": "dependency_mismatch", "reason": "Resolved input dependencies differ"}
    identity = sha(json.dumps([a["output_sha256"], b["output_sha256"], stage, tolerance, relative, samples]).encode())
    target = folder / "checks" / f"{identity}.json"
    if target.exists():
        return json.loads(target.read_text(encoding="utf-8"))
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", str(a["resolved_output"]), str(b["resolved_output"]), stage,
               "--absolute", str(tolerance), "--relative", str(relative), "--samples", str(samples)]
    try:
        process = subprocess.run(command, capture_output=True, text=True, timeout=60)
        result = json.loads(process.stdout) if process.returncode == 0 else {"status": "comparison_error", "error": process.stderr[-3000:]}
    except subprocess.TimeoutExpired:
        result = {"status": "comparison_timeout", "limit_seconds": 60}
    save(target, result)
    return result


def build_report(args):
    output = args.output.resolve()
    if output.exists():
        raise ValueError("Use a new report directory to preserve evidence")
    output.mkdir(parents=True)
    records, metadata, models = [], [], {}
    for run in args.runs:
        meta = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
        if metadata:
            for key in ("schema", "manifest_sha256", "sources", "library_hashes", "backend", "image_size", "machine", "cache_policy", "timeout", "scopes"):
                if meta[key] != metadata[0][key]:
                    raise ValueError(f"Incompatible run field: {key}")
        metadata.append(meta)
        models.update({m["id"]: m for m in meta["models"]})
        for line in (run / "results.jsonl").read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            row["resolved_output"] = str((run / row["output"]).resolve())
            row["run"] = str(run.resolve())
            if row["status"] == "ok" and not verify_output(Path(row["resolved_output"]), row["output_sha256"]):
                row["status"] = "output_changed_or_missing"
            records.append(row)
    identities = {}
    for meta in metadata:
        for label, identity in meta["builds"].items():
            if label in identities and identities[label] != identity:
                raise ValueError(f"Same build label has different binary identity: {label}")
            identities[label] = identity
    if args.baseline not in identities:
        raise ValueError("Baseline label not present")
    groups = defaultdict(list)
    for record in records:
        groups[(record["id"], record["stage"], record["build"])].append(record)
    baseline = args.baseline
    candidates = [c for c in identities if c != baseline]
    table, checks = [], []
    for number, ((identifier, stage, label), rows) in enumerate(sorted(groups.items())):
        if label != baseline:
            continue
        model = models[identifier]
        good = [r for r in rows if r["status"] == "ok"]
        median = statistics.median(r["seconds"] for r in good) if len(good) == len(rows) else None
        for candidate in candidates or [None]:
            other = groups.get((identifier, stage, candidate), [])
            good_other = [r for r in other if r["status"] == "ok"]
            candidate_median = statistics.median(r["seconds"] for r in good_other) if other and len(good_other) == len(other) else None
            outcome = "baseline_only" if candidate is None else "execution_failed_or_missing"
            if candidate is not None and other:
                if median is None and candidate_median is not None:
                    outcome = "baseline_failed_candidate_succeeded"
                elif median is not None and candidate_median is None:
                    outcome = "candidate_execution_regression"
                elif median is None and candidate_median is None:
                    outcome = "both_executions_failed"
            shape = []
            if median is not None and candidate_median is not None:
                # Check every repetition, including baseline stability, against the retained first baseline.
                for row in good[1:] + good_other:
                    result = compare_pair(good[0], row, stage, output, args.absolute, args.relative, args.samples)
                    checks.append({"id": identifier, "stage": stage, "baseline_output": good[0]["resolved_output"], "other_output": row["resolved_output"], "build": row["build"], **result})
                    shape.append(result)
                failures = [r["status"] for r in shape if r["status"] not in PASS]
                outcome = failures[0] if failures else ("within_tolerance_sampled" if any(r["status"] == "within_tolerance_sampled" for r in shape) else "equivalent")
                if any(r["status"] in {"different", "image_changed_review", "text_changed_review"} for r in shape[:len(good)-1]):
                    outcome = "baseline_not_repeatable"
            ratio = median / candidate_median if outcome in ("equivalent", "within_tolerance_sampled") else None
            row = {"id": identifier, "repository": model["repository"], "path": model["path"], "tags": ", ".join(model["tags"]),
                   "source_url": model["source_url"], "stage": stage, "candidate": candidate or "",
                   "baseline_seconds": median, "candidate_seconds": candidate_median,
                   "baseline_min_seconds": min((r["seconds"] for r in good), default=None),
                   "baseline_max_seconds": max((r["seconds"] for r in good), default=None),
                   "candidate_min_seconds": min((r["seconds"] for r in good_other), default=None),
                   "candidate_max_seconds": max((r["seconds"] for r in good_other), default=None),
                   "speedup": ratio, "outcome": outcome, "baseline_samples": len(rows), "candidate_samples": len(other),
                   "baseline_status": ", ".join(f"{k}:{v}" for k, v in Counter(r["status"] for r in rows).items()),
                   "candidate_status": ", ".join(f"{k}:{v}" for k, v in Counter(r["status"] for r in other).items()),
                   "baseline_output": good[0]["resolved_output"] if good else "",
                   "candidate_output": good_other[0]["resolved_output"] if good_other else "",
                   "surface_max_delta": max((r["surface_max_delta"] for r in shape if "surface_max_delta" in r), default=None),
                   "volume_relative_delta": max((r["volume_relative_delta"] for r in shape if "volume_relative_delta" in r), default=None)}
            table.append(row)
        if number % 25 == 0:
            print(f"Report groups {number}/{len(groups)}", flush=True)
    expected = sum(len(m["models"]) * len(m["stages"]) * len(m["builds"]) * m["repetitions"] for m in metadata)
    coverage = {}
    for label in identities:
        label_rows = [r for r in records if r["build"] == label]
        by_model = defaultdict(list)
        for row in label_rows:
            by_model[row["id"]].append(row)
        expected_per_model = defaultdict(int)
        for meta in metadata:
            if label in meta["builds"]:
                for model in meta["models"]:
                    expected_per_model[model["id"]] += len(meta["stages"]) * meta["repetitions"]
        coverage[label] = {"models_with_samples": len(by_model),
                           "models_clean_in_all_requested_stages": sum(len(rows) == expected_per_model[identifier] and all(r["status"] == "ok" for r in rows) for identifier, rows in by_model.items()),
                           "stage_status_counts": dict(Counter(r["stage"] + ":" + r["status"] for r in label_rows))}
    summary = {"models": len(models), "repositories": len({m["repository"] for m in models.values()}), "samples": len(records),
               "expected_samples": expected, "missing_samples": expected - len(records),
               "coverage": coverage,
               "comparison_implementation": {"python": platform.python_version(),
                   "packages": {name: importlib.metadata.version(name) for name in ("numpy", "trimesh", "scipy", "rtree", "pillow", "matplotlib")},
                   "files": {name: hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest() for name in ("geometry.py", "report.py", "uv.lock")}},
               "outcomes": dict(Counter(r["status"] for r in records)), "comparisons": dict(Counter(r["outcome"] for r in table)),
               "baseline": baseline, "candidates": candidates, "absolute_tolerance": args.absolute, "relative_tolerance": args.relative,
               "runs": [str(r.resolve()) for r in args.runs], "builds": identities,
               "limits": "Fresh processes with potentially warm OS caches. Timers overlap; do not subtract them to infer pure phase costs. Geometry surface sampling is not proof. No GUI editor-open or first-present measurement. Timing results are exploratory on a shared host."}
    save(output / "summary.json", summary)
    save(output / "comparisons.json", checks)
    save(output / "table.json", table)
    with (output / "table.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(table[0]) if table else ["id"])
        writer.writeheader()
        writer.writerows(table)
    graphs(output, table, records)
    render_html(output, summary, table)
    print(json.dumps({"report": str(output / "index.html"), "outcomes": summary["outcomes"], "comparisons": summary["comparisons"]}), flush=True)


def graphs(output, table, records):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "figure.facecolor": "#f7f9fc", "axes.spines.top": False, "axes.spines.right": False})
    figure, axes = plt.subplots(1, 2, figsize=(13, 4), layout="constrained")
    categories = sorted({r["stage"] for r in records})
    statuses = sorted({r["status"] for r in records})
    bottom = [0] * len(categories)
    colors = {"ok": "#1d8c78", "timeout": "#df9d29", "error": "#c64d56", "diagnostic": "#8f6caf",
              "empty": "#a5afbd", "empty_geometry": "#7f8d9f", "unfrozen_dependency": "#4c7faf"}
    for status in statuses:
        values = [sum(r["stage"] == stage and r["status"] == status for r in records) for stage in categories]
        axes[0].bar(categories, values, bottom=bottom, label=status, color=colors.get(status, "#555555"))
        bottom = [a+b for a,b in zip(bottom, values)]
    axes[0].set(title="Execution coverage — failures retained", ylabel="Samples")
    axes[0].legend(fontsize=8)
    data = [[r["seconds"] for r in records if r["stage"] == stage and r["status"] == "ok"] for stage in categories]
    if any(data):
        axes[1].boxplot([d or [float("nan")] for d in data], tick_labels=categories, showfliers=False)
        axes[1].set(yscale="log", title="Successful process wall time", ylabel="Seconds (log scale)")
    else:
        axes[1].text(.5, .5, "No successful timing samples", ha="center", va="center", transform=axes[1].transAxes)
        axes[1].set_axis_off()
    figure.savefig(output / "coverage.png", dpi=160)
    plt.close(figure)
    eligible = [r for r in table if r["speedup"] is not None]
    if eligible:
        figure, axes = plt.subplots(1, 2, figsize=(13, 4), layout="constrained")
        for stage in sorted({r["stage"] for r in eligible}):
            rows = [r for r in eligible if r["stage"] == stage]
            axes[0].scatter([r["baseline_seconds"] for r in rows], [r["candidate_seconds"] for r in rows], s=14, alpha=.7, label=stage)
        low = min(min(r["baseline_seconds"], r["candidate_seconds"]) for r in eligible)
        high = max(max(r["baseline_seconds"], r["candidate_seconds"]) for r in eligible)
        axes[0].plot([low, high], [low, high], "--", color="#555")
        axes[0].set(xscale="log", yscale="log", xlabel="Baseline seconds", ylabel="Candidate seconds", title="Compared outputs within tolerance")
        axes[0].legend()
        speeds = sorted(r["speedup"] for r in eligible)
        axes[1].plot(speeds, [(i+1)/len(speeds) for i in range(len(speeds))])
        axes[1].axvline(1, linestyle="--", color="#555")
        axes[1].set(xscale="log", xlabel="Baseline / candidate (greater than 1 is faster)", ylabel="Fraction of eligible comparisons", title="Speed ratio distribution — no failed cases")
        figure.savefig(output / "comparison.png", dpi=160)
        plt.close(figure)


def render_html(output, summary, rows):
    esc = html.escape
    heads = ["Model", "Stage", "Build", "Baseline median s", "Candidate median s", "Speed ratio", "Comparison", "Max surface Δ", "Run status", "Outputs"]
    body = []
    def number(value):
        return "—" if value is None else f"{value:.6g}"
    for row in rows:
        model = f"{row['repository']} / {row['path']}"
        links = []
        for label in ("baseline", "candidate"):
            if row[label + "_output"]:
                links.append(f'<a href="{esc(Path(row[label + "_output"]).as_uri(), quote=True)}">{label}</a>')
        cells = [f'<a href="{esc(row["source_url"], quote=True)}">{esc(model)}</a>', esc(row["stage"]), esc(row["candidate"]),
                 number(row["baseline_seconds"]), number(row["candidate_seconds"]), number(row["speedup"]), esc(row["outcome"]),
                 number(row["surface_max_delta"]), esc(row["baseline_status"] + " | " + row["candidate_status"]), " / ".join(links)]
        body.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")
    comparison = '<img src="comparison.png" alt="Paired timing and speed ratio charts">' if (output / "comparison.png").exists() else ""
    clean = "; ".join(f"{label}: {values['models_clean_in_all_requested_stages']} models clean in every requested stage" for label, values in summary["coverage"].items())
    document = f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>SCADMaxx real-world benchmarks</title>
<style>body{{font:15px system-ui;margin:36px;color:#17263b;background:#f7f9fc}}h1{{font-size:30px}}p{{max-width:1100px;line-height:1.5}}.stats{{display:flex;gap:25px;font-size:22px;margin:25px 0}}img{{max-width:100%;display:block}}input{{padding:12px;width:450px;max-width:90%;margin:16px 0}}table{{border-collapse:collapse;width:100%;font-size:12px;background:white}}th,td{{padding:9px;text-align:left;border-bottom:1px solid #dde2ec}}th{{position:sticky;top:0;background:#e6edf5;cursor:pointer}}a{{color:#126396}}td:first-child{{max-width:500px;overflow-wrap:anywhere}}</style>
<h1>Real-world OpenSCAD performance</h1><p>Frozen source models · original geometry settings · explicit failed outcomes</p>
<div class="stats"><span>{summary['models']} models</span><span>{summary['repositories']} repositories</span><span>{summary['samples']} / {summary['expected_samples']} samples</span></div>
<p><strong>{esc(clean)}</strong>. Corpus entries are source-file candidates; helper files and failed models remain in the coverage accounting.</p>
<p>{esc(summary['limits'])}</p><p>Geometry tolerance = {summary['absolute_tolerance']:g} + {summary['relative_tolerance']:g} × bounding-box diagonal, in model units. No alignment or scaling. Topology and volume changes are checked separately. “Within tolerance sampled” is evidence, not proof.</p>
<p>Speed ratios appear only for successful comparable outputs. Image and text equality do not establish full 3D equivalence. Counts include failed models; timings never treat timeouts as measured completion times.</p>
<p><a href="table.csv">CSV table</a> · <a href="comparisons.json">Detailed geometric differences</a> · <a href="summary.json">Run identities and coverage</a></p>
<img src="coverage.png" alt="Coverage and timing distributions">{comparison}
<input id="filter" placeholder="Filter by model, stage, result or repository" aria-label="Filter results"><p id="count"></p>
<table><thead><tr>{''.join('<th>'+esc(h)+'</th>' for h in heads)}</tr></thead><tbody>{''.join(body)}</tbody></table>
<script>const allRows=[...document.querySelectorAll('tbody tr')];const counter=document.querySelector('#count');function filter(){{const q=document.querySelector('#filter').value.toLowerCase();let n=0;for(const row of allRows){{row.hidden=!row.textContent.toLowerCase().includes(q);if(!row.hidden)n++;}}counter.textContent=n+' of '+allRows.length+' comparisons';}}document.querySelector('#filter').addEventListener('input',filter);filter();document.querySelectorAll('th').forEach((h,i)=>h.onclick=()=>{{let direction=h.dataset.direction==='1'?-1:1;h.dataset.direction=direction;allRows.sort((a,b)=>{{let x=a.cells[i].textContent,y=b.cells[i].textContent;return direction*(x!==''&&y!==''&&Number.isFinite(Number(x))&&Number.isFinite(Number(y))?Number(x)-Number(y):x.localeCompare(y));}}).forEach(r=>document.querySelector('tbody').append(r));}});</script></html>'''
    (output / "index.html").write_text(document, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="*", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--baseline", default="baseline")
    parser.add_argument("--absolute", type=float, default=1e-5)
    parser.add_argument("--relative", type=float, default=1e-6)
    parser.add_argument("--samples", type=int, default=4096)
    parser.add_argument("--worker", nargs=3)
    args = parser.parse_args()
    if args.worker:
        from geometry import compare_outputs
        a, b, stage = args.worker
        print(json.dumps(compare_outputs(a, b, stage, absolute=args.absolute, relative=args.relative, samples=args.samples)))
    elif args.runs and args.output:
        build_report(args)
    else:
        parser.error("Supply run directories and --output")


if __name__ == "__main__":
    main()
