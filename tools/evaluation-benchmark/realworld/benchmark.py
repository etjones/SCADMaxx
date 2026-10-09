"""Sequential, resumable real-world OpenSCAD timing; immutable inputs and explicit failed outcomes."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import re
import shutil
import subprocess
import time

from corpus import sha, save

STAGES = {"ast": ".ast", "csg": ".csg", "preview": ".png", "stl": ".stl", "off": ".off"}
SCOPES = {
    "ast": "Fresh process: startup, source loading/parsing, model instantiation and AST serialization. Not pure parse or native editor-open latency.",
    "csg": "Fresh process: startup, parsing, language evaluation and CSG serialization.",
    "preview": "Fresh process: startup, parsing/evaluation, CSG preparation, offscreen drawing and PNG encoding. Not GUI first-present time.",
    "stl": "Fresh process: startup, parsing/evaluation, full geometry and binary STL export.",
    "off": "Fresh process: startup, parsing/evaluation, full geometry and indexed OFF export."}


def host_load():
    if os.name != "nt":
        return {"load_average": os.getloadavg()}
    # Evidence only. Never stop another user's build or model render.
    result = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True)
    return {"competing_processes": [line for line in result.stdout.splitlines()
                                    if re.match(r'"(?:cl|ninja|MSBuild|openscad|scadmaxx)\.', line, re.I)]}


def file_hash(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def execute(command, cwd, env, timeout, stem):
    stem.parent.mkdir(parents=True, exist_ok=True)
    with stem.with_suffix(".stdout.txt").open("wb") as stdout, stem.with_suffix(".stderr.txt").open("wb") as stderr:
        started = time.perf_counter()
        process = subprocess.Popen(command, cwd=cwd, env=env, stdout=stdout, stderr=stderr,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                                   start_new_session=os.name != "nt")
        timed_out = False
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)
            else:
                import signal
                os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=15)
        seconds = time.perf_counter() - started
    logs = stem.with_suffix(".stdout.txt").read_text(errors="replace") + stem.with_suffix(".stderr.txt").read_text(errors="replace")
    warnings = re.findall(r"(?im)^.*(?:WARNING:|ERROR:|Parser error:|Fontconfig error:|Current top level object is empty).*$", logs)
    return {"seconds": seconds, "exit_code": process.returncode, "timed_out": timed_out, "diagnostics": warnings,
            "command": [str(p) for p in command]}


def runtime_identity(executable):
    files = [executable]
    companion = executable.with_suffix(".exe")
    if companion.exists() and companion != executable:
        files.append(companion)
    files.extend(sorted(executable.parent.glob("*.dll")))
    for directory in ("libraries", "fonts", "platforms", "imageformats"):
        files.extend(p for p in sorted((executable.parent / directory).rglob("*")) if p.is_file())
    identity = {"executable": str(executable), "files": {p.relative_to(executable.parent).as_posix(): file_hash(p) for p in files}}
    info = executable.parent / "build-info.json"
    if info.exists():
        identity["build_info"] = json.loads(info.read_text(encoding="utf-8-sig"))
        identity["build_info_sha256"] = file_hash(info)
    return identity


def dependency_identity(path, corpus, runtime):
    records, external = [], []
    if not path.exists():
        return records, external
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[1:]
    for line in lines:
        value = line.strip().removesuffix("\\").strip().replace("\\ ", " ").replace("\\#", "#")
        if not value:
            continue
        dependency = Path(value).resolve()
        if not dependency.is_file():
            external.append(value)
            continue
        if dependency.is_relative_to(corpus):
            key = "corpus/" + dependency.relative_to(corpus).as_posix()
        elif dependency.is_relative_to(runtime / "libraries"):
            key = "runtime/" + dependency.relative_to(runtime).as_posix()
        else:
            key = str(dependency)
            external.append(key)
        records.append({"path": key, "sha256": file_hash(dependency)})
    return sorted(records, key=lambda r: r["path"]), external


def prepare_libraries(corpus):
    aliases = {"BelfrySCAD/BOSL2": "BOSL2", "revarbat/BOSL": "BOSL", "JustinSDK/dotSCAD": "dotSCAD",
               "OskarLinde/scad-utils": "scad-utils", "Irev-Dev/Round-Anything": "Round-Anything",
               "adrianschlatter/threadlib": "threadlib"}
    libraries = corpus / "libraries"
    libraries.mkdir(exist_ok=True)
    for repo, alias in aliases.items():
        record = corpus / "sources" / (repo.replace("/", "__") + ".json")
        if record.exists() and not (libraries / alias).exists():
            source = json.loads(record.read_text(encoding="utf-8"))
            shutil.copytree(corpus / source["root"], libraries / alias)
    return libraries


def verify_corpus(corpus, manifest):
    # Includes/assets affect results too. Verify every retained source file before timing begins.
    repositories = {m["repository"] for m in manifest["models"]}
    records = []
    for path in sorted((corpus / "sources").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record["repository"] not in repositories and record["repository"] not in {"BelfrySCAD/BOSL2", "revarbat/BOSL", "JustinSDK/dotSCAD", "OskarLinde/scad-utils", "Irev-Dev/Round-Anything", "adrianschlatter/threadlib"}:
            continue
        for file in record["files"]:
            actual = file_hash(corpus / record["root"] / file["path"])
            if actual != file["sha256"]:
                raise ValueError(f"Source changed: {record['repository']}/{file['path']}")
        records.append({"repository": record["repository"], "revision": record["revision"], "record_sha256": file_hash(path)})
        if len(records) % 40 == 0:
            print(f"Verified {len(records)} source snapshots", flush=True)
    return records


def run(args):
    corpus, output = args.corpus.resolve(), args.output.resolve()
    manifest = json.loads((corpus / "manifest.json").read_text(encoding="utf-8"))
    models = manifest["models"][:args.limit] if args.limit else manifest["models"]
    if args.ids:
        wanted = set(args.ids.split(","))
        models = [m for m in models if m["id"] in wanted]
    if not models:
        raise ValueError("No models selected")
    builds = {}
    for build in args.build:
        label, file = build.split("=", 1)
        if not re.fullmatch(r"[A-Za-z0-9_-]+", label) or label in builds:
            raise ValueError("Build labels must be unique plain identifiers")
        builds[label] = Path(file).resolve(strict=True)
    build_arguments = {label: [] for label in builds}
    for item in args.build_argument:
        label, argument = item.split("=", 1)
        if label not in builds or not argument:
            raise ValueError("Build arguments require a known label and nonempty argument")
        build_arguments[label].append(argument)
    print("Preparing pinned libraries and verifying corpus inputs before timing", flush=True)
    libraries = prepare_libraries(corpus)
    records = verify_corpus(corpus, manifest)
    env = os.environ.copy()
    env["OPENSCADPATH"] = str(libraries)
    library_hashes = {p.relative_to(libraries).as_posix(): file_hash(p) for p in sorted(libraries.rglob("*")) if p.is_file()}
    config = {"schema": 1, "corpus": str(corpus), "manifest_sha256": file_hash(corpus / "manifest.json"),
              "models": models, "builds": {label: dict(runtime_identity(p), effective_arguments=build_arguments[label])
                                           for label, p in builds.items()},
              "sources": records, "library_hashes": library_hashes, "stages": args.stages,
              "repetitions": args.repetitions, "timeout": args.timeout, "seed": args.seed,
              "backend": args.backend, "image_size": "512,512", "scopes": SCOPES,
              "build_arguments": build_arguments,
              "cache_policy": "Fresh process; OS disk caches uncontrolled; default application caches. No quality overrides.",
              "machine": {"platform": platform.platform(), "processor": platform.processor(), "logical_cpus": os.cpu_count(), "host": platform.node()},
              "runner_sha256": file_hash(__file__)}
    if output.exists():
        if not args.resume:
            raise ValueError("Output directory exists; select a new directory or explicitly --resume")
        old = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
        if old != config:
            raise ValueError("Resume inputs differ from frozen metadata")
    else:
        output.mkdir(parents=True)
        save(output / "metadata.json", config)
        save(output / "host-load-start.json", host_load())
        for label, executable in builds.items():
            execute([str(executable), "--version"], output, env, 20, output / f"{label}-version")
            execute([str(executable), "--info"], output, env, 20, output / f"{label}-info")
    result_file = output / "results.jsonl"
    complete = set()
    if result_file.exists():
        for line in result_file.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            complete.add((row["id"], row["stage"], row["build"], row["repetition"]))
    labels = list(builds)
    plan = [(model, stage, repetition) for repetition in range(args.repetitions) for model in models for stage in args.stages]
    random.Random(args.seed).shuffle(plan)
    counts = Counter()
    with result_file.open("a", encoding="utf-8", buffering=1) as stream:
        for index, (model, stage, repetition) in enumerate(plan):
            # Alternate build order within adjacent matched input pairs to reduce drift bias.
            order = labels if index % 2 == 0 else labels[::-1]
            for label in order:
                key = (model["id"], stage, label, repetition)
                if key in complete:
                    continue
                folder = output / "samples" / model["id"] / stage / str(repetition) / label
                folder.mkdir(parents=True, exist_ok=True)
                result_path = folder / ("model" + STAGES[stage])
                source = corpus / model["file"]
                command = [str(builds[label]), *build_arguments[label], "--backend=" + args.backend, "-o", str(result_path),
                           "-d", str(folder / "dependencies.txt")]
                if stage == "preview":
                    command += ["--preview", "--imgsize=512,512", "--autocenter", "--viewall"]
                if stage == "stl":
                    command += ["--export-format=binstl"]
                if stage in ("off", "stl"):
                    command += ["--summary=all", "--summary-file", str(folder / "summary.json")]
                command += [str(source)]
                row = execute(command, source.parent, env, args.timeout, folder / "process")
                dependencies, external = dependency_identity(folder / "dependencies.txt", corpus, builds[label].parent)
                exists = result_path.exists() and result_path.stat().st_size > 0
                if row["timed_out"]:
                    status = "timeout"
                elif row["exit_code"] != 0:
                    status = "error"
                elif not exists:
                    status = "empty"
                elif row["diagnostics"]:
                    status = "diagnostic"
                elif external:
                    status = "unfrozen_dependency"
                elif stage == "csg" and not re.search(r"\b(cube|sphere|cylinder|polyhedron|polygon|square|circle|text|import|surface)\s*\(", result_path.read_text(errors="replace")):
                    status = "empty_geometry"
                else:
                    status = "ok"
                row.update(id=model["id"], repository=model["repository"], path=model["path"], stage=stage,
                           build=label, repetition=repetition, status=status,
                           dependencies=dependencies, unfrozen_dependencies=external,
                           output=str(result_path.relative_to(output)),
                           output_sha256=file_hash(result_path) if exists else None,
                           output_bytes=result_path.stat().st_size if exists else 0)
                summary = folder / "summary.json"
                if summary.exists():
                    try:
                        row["native_summary"] = json.loads(summary.read_text(encoding="utf-8"))
                    except ValueError:
                        row["native_summary_error"] = "Invalid JSON retained on disk"
                stream.write(json.dumps(row) + "\n")
                counts[status] += 1
                if sum(counts.values()) % 20 == 0:
                    print(f"Completed {len(complete) + sum(counts.values())}/{len(plan)*len(labels)}: {dict(counts)}", flush=True)
    print(json.dumps({"output": str(output), "outcomes": counts}), flush=True)
    save(output / "host-load-end.json", host_load())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--build", action="append", required=True, help="label=absolute executable path; repeat for paired builds")
    parser.add_argument("--build-argument", action="append", default=[], help="label=argument; repeat for explicitly enabled experimental features")
    parser.add_argument("--stages", nargs="+", choices=STAGES, default=["ast", "csg", "preview", "stl"])
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--backend", choices=["Manifold", "CGAL"], default="Manifold")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--ids")
    parser.add_argument("--seed", type=int, default=20261004)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.repetitions < 1 or args.timeout <= 0:
        parser.error("repetitions and timeout must be positive")
    run(args)


if __name__ == "__main__":
    main()
