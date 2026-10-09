"""Reconcile selected feature test sources with integrated runners, without building or executing tests."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

CONTROL = Path(__file__).resolve().parents[2]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def selection(text):
    section = re.search(r"^## Enabled stack[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not section:
        raise ValueError("Enabled stack section is missing")
    entries = []
    for line in section[1].splitlines():
        if re.match(r"\|\s*\d+\s*\|", line):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 8:
                raise ValueError("Expected eight selection columns")
            order, name, kind, source, revision, _, _, reason = cells
            entries.append(dict(order=int(order), id=name, kind=kind, source=source, revision=revision, reason=reason))
    if not entries or len({e["id"] for e in entries}) != len(entries):
        raise ValueError("Empty or duplicate feature selection")
    return entries


def test_path(path):
    return (path.startswith("src/guitests/") or path.endswith("_test.cc") or
            path.startswith("tests/") and (path.endswith((".py", ".cc", ".h", ".scad")) or Path(path).name == "CMakeLists.txt"))


def cases(text):
    return re.findall(r'TEST_CASE(?:_METHOD)?\s*\(\s*(?:\w+\s*,\s*)?"([^"\n]+)"', text)


def export_index(report, destination, report_path):
    features = []
    for feature in report["features"]:
        gaps = [test for test in feature["tests"] if test["status"] in
                ("NOT_IN_INTEGRATION", "REVIEW_SOURCE_WIRING", "REVIEW_MISSING_GUI_SLOTS", "RECONFIGURE_REQUIRED")]
        features.append({"id": feature["id"], "revision": feature["audited_revision"],
                         "in_integration_ancestry": feature["revision_in_integration_ancestry"],
                         "source_ready": feature["source_ready"], "test_path_count": len(feature["tests"]),
                         "suites": sorted({test["suite"] for test in feature["tests"] if test["suite"]}),
                         "coverage_gaps": gaps})
    index = {"schema": 1, "integration_head": report["integration_head"],
             "selection_sha256": report["selection_sha256"], "dependencies_sha256": report["dependencies_sha256"],
             "detailed_report": str(report_path.resolve()), "features": features, "companion": report["companion"],
             "limits": report["limits"]}
    Path(destination).write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")


def classify(path, text, target, target_text, root_cmake, gui_runner, ctest_paths, ctest_names, tests_cmake, fixture_references=""):
    row = {"path": path, "present_in_integration": target.exists(), "cases": cases(text)}
    if not target.exists():
        return dict(row, suite=None, status="NOT_IN_INTEGRATION")
    if path.startswith("tests/annotations/"):
        row.update(suite="gui/http-live" if path.endswith("LiveHttpWorkflow.py") else "annotations", status="SEPARATE_INPUT_REQUIRED")
    elif path.startswith("tests/customizer-group-visibility/"):
        row.update(suite="customizer", status="SEPARATE_INPUT_REQUIRED")
    elif path.endswith("_test.cc"):
        row["missing_case_names"] = sorted(set(row["cases"]) - set(cases(target_text)))
        wired = (path in root_cmake or any(path.startswith(prefix) for prefix in
                 ("src/core/", "src/utils/", "src/io/", "src/glview/", "src/gui/")))
        row.update(suite="vim" if path.endswith("VimEngine_test.cc") else "unit",
                   status="SOURCE_WIRED" if wired and not row["missing_case_names"] else "REVIEW_SOURCE_WIRING")
        hidden = re.findall(r'TEST_CASE\s*\(\s*"([^"\n]+)"\s*,\s*"([^"\n]*\[\.\][^"\n]*)"', text)
        row["hidden_cases"] = [{"name": name, "tags": tags,
                                "suite": "nested-unit-child" if "restart" in tags else "unit-visual"} for name, tags in hidden]
        if "[providers-external]" in text or "[insertion-providers]" in text:
            row["additional_suite"] = "provider-external"
    elif path.startswith("src/guitests/"):
        name = Path(path).stem
        row.update(suite="gui", status="SOURCE_WIRED" if name in gui_runner or name in ("guitests", "UXTest") else "GUI_REGISTRATION_REVIEW")
        if path.endswith(".h"):
            declared = set(re.findall(r"void\s+(\w+)\s*\([^;{}]*\)\s*;", text))
            integrated = set(re.findall(r"void\s+(\w+)\s*\([^;{}]*\)\s*;", target_text))
            row["missing_slot_names"] = sorted(declared - integrated)
            if row["missing_slot_names"]:
                row["status"] = "REVIEW_MISSING_GUI_SLOTS"
    elif path.endswith(".py"):
        registered = path in ctest_paths
        declared = Path(path).name in tests_cmake
        helper = Path(path).name in ("image_compare.py", "validatestl.py", "test_pretty_print.py") or "/data/python/" in path
        row.update(suite="cli-deep" if registered or declared else "helper" if helper else None,
                   status="BUILD_REGISTERED" if registered else "RECONFIGURE_REQUIRED" if declared else "HELPER" if helper else "SCRIPT_REGISTRATION_REVIEW")
    elif path.endswith(".scad"):
        row.update(suite="cli-deep/test-fixture" if path in ctest_paths else "source-test-fixture",
                   status="BUILD_REFERENCED" if path in ctest_paths else "SOURCE_REFERENCED" if Path(path).name in fixture_references else "SUPPORT_FIXTURE")
    else:
        row.update(suite="test-definition/helper", status="SOURCE_DEFINITION")
    return row


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repository", type=Path)
    p.add_argument("--integration", type=Path)
    p.add_argument("--ctest-plan", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--catalog-index", type=Path)
    p.add_argument("--from-report", type=Path, help="Export the catalog index from an already retained audit")
    a = p.parse_args()
    if a.from_report:
        if not a.catalog_index:
            p.error("--from-report requires --catalog-index")
        export_index(read(a.from_report), a.catalog_index, a.from_report)
        return
    if not all((a.repository, a.integration, a.ctest_plan, a.output)):
        p.error("Audit requires --repository, --integration, --ctest-plan and --output")
    a.repository = a.repository.resolve()
    a.integration = a.integration.resolve()

    def git(*arguments, directory=a.repository):
        command = ["git", "-c", "safe.directory=" + str(directory), "-C", str(directory), *arguments]
        return subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=True).stdout

    nodes = read(CONTROL / "experimental/DEPENDENCIES.json")["nodes"]
    sources = read(CONTROL / "experimental/SOURCES.json")
    entries = selection((CONTROL / "experimental/PR_STACK.md").read_text(encoding="utf-8"))
    plan = read(a.ctest_plan)
    inventory = next(command["inventory"] for command in plan["commands"] if "inventory" in command)
    ctest_names = {test["name"] for tests in inventory.values() for test in tests}
    ctest_paths = {str(Path(argument).relative_to(a.integration)).replace("\\", "/")
                   for tests in inventory.values() for test in tests for argument in test.get("command", [])
                   if Path(argument).is_absolute() and Path(argument).is_relative_to(a.integration)}
    root_cmake = (a.integration / "CMakeLists.txt").read_text(encoding="utf-8")
    tests_cmake = (a.integration / "tests/CMakeLists.txt").read_text(encoding="utf-8")
    gui_runner = (a.integration / "src/guitests/guitests.cc").read_text(encoding="utf-8")
    fixture_references = tests_cmake + "\n" + "\n".join(file.read_text(encoding="utf-8", errors="replace")
        for file in (a.integration / "src").rglob("*") if file.is_file() and
        (file.name.endswith("_test.cc") or "guitests" in file.parts) and file.suffix in (".cc", ".h"))
    worktrees = {}
    for block in git("worktree", "list", "--porcelain").strip().split("\n\n"):
        values = dict(line.split(" ", 1) for line in block.splitlines() if " " in line)
        if "branch" in values:
            worktrees[values["branch"]] = Path(values["worktree"])
    cache = {}

    def blob(revision, path):
        key = git("rev-parse", revision + ":" + path).strip()
        if key not in cache:
            cache[key] = git("show", revision + ":" + path)
        return cache[key]

    target_head = git("rev-parse", "HEAD", directory=a.integration).strip()
    rows = []
    for entry in entries:
        node = nodes[entry["id"]]
        revision = entry["revision"] if entry["revision"] != "latest" else node["acceptedHead"]
        revision = git("rev-parse", revision + "^{commit}").strip()
        base = git("merge-base", "upstream/master", revision).strip()
        paths = [path for path in git("diff", "--name-only", base, revision).splitlines() if test_path(path)]
        live = worktrees.get(node.get("ref", ""))
        dirty = []
        if live:
            tracked = git("diff", "HEAD", "--name-only", directory=live).splitlines()
            untracked = git("ls-files", "--others", "--exclude-standard", directory=live).splitlines()
            dirty = [path for path in sorted(set(tracked + untracked)) if test_path(path)]
        tests = []
        for path in paths:
            text = blob(revision, path)
            target = a.integration / path
            target_text = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
            tests.append(classify(path, text, target, target_text, root_cmake, gui_runner, ctest_paths, ctest_names, tests_cmake, fixture_references))
        for path in dirty:
            file = live / path
            if not file.is_file():
                continue
            text = file.read_text(encoding="utf-8", errors="replace")
            target = a.integration / path
            target_text = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
            row = classify(path, text, target, target_text, root_cmake, gui_runner, ctest_paths, ctest_names, tests_cmake, fixture_references)
            row.update(origin="owner-working-tree", sha256=hashlib.sha256(file.read_bytes()).hexdigest())
            tests.append(row)
        state = subprocess.run(["git", "-c", "safe.directory=" + str(a.repository), "-C", str(a.repository),
                                "merge-base", "--is-ancestor", revision, target_head]).returncode
        rows.append({**entry, "audited_revision": revision, "comparison_base": base, "owner_worktree": str(live) if live else None,
                     "revision_in_integration_ancestry": state == 0, "source_ready": sources.get(entry["source"], {}).get("ready"),
                     "tests": tests})
        print(f"Audited {entry['id']}: {len(tests)} test/fixture paths", flush=True)
    report = {"schema": 1, "integration": str(a.integration), "integration_head": target_head,
              "selection_sha256": hashlib.sha256((CONTROL / "experimental/PR_STACK.md").read_bytes()).hexdigest(),
              "dependencies_sha256": hashlib.sha256((CONTROL / "experimental/DEPENDENCIES.json").read_bytes()).hexdigest(),
              "features": rows, "registered_ctest_names": sorted(ctest_names),
              "companion": {"id": "agent-skill-workflows", "source": sources["agent-skill-workflows-local"],
                            "runners": ["experimental/scripts/Test-SkillCompanion.ps1", "experimental/scripts/Test-ScadmaxxSkill.py"],
                            "status": "PACKAGE_INPUTS_REQUIRED"},
              "limits": "Feature deltas include inherited dependency tests. Source wiring is not execution evidence. Working-tree changes are separately hashed."}
    a.output.mkdir(parents=True, exist_ok=False)
    (a.output / "feature-tests.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Selected feature test coverage", "", f"Integration source: `{target_head}`.", "",
             "Read-only reconciliation; no application tests or builds executed. Dependency tests may appear under multiple owners.", "",
             "| Selected feature | Test/fixture paths | Selected revision in integration |", "| --- | ---: | --- |"]
    for row in rows:
        lines.append(f"| {row['id']} | {len(row['tests'])} | {'yes' if row['revision_in_integration_ancestry'] else 'no'} |")
    lines += ["", "Detailed path, case-name, hidden-test, working-tree and registration evidence is in feature-tests.json.", "",
              "An older compiled registration can require reconfiguration even when source tests are present."]
    lines += ["", "## Outstanding source/build coverage", ""]
    for row in rows:
        if not row["revision_in_integration_ancestry"]:
            lines.append(f"- {row['id']}: selected revision `{row['audited_revision']}` is not in this integration's ancestry.")
    seen = set()
    for feature in rows:
        for test in feature["tests"]:
            if test["status"] not in ("NOT_IN_INTEGRATION", "REVIEW_SOURCE_WIRING", "REVIEW_MISSING_GUI_SLOTS", "RECONFIGURE_REQUIRED"):
                continue
            key = (test["path"], test["status"], tuple(test.get("missing_case_names", [])), tuple(test.get("missing_slot_names", [])))
            if key in seen:
                continue
            seen.add(key)
            names = test.get("missing_case_names", []) + test.get("missing_slot_names", [])
            lines.append(f"- `{test['path']}`: {test['status']}" + ("; " + ", ".join(names) if names else "") + ".")
    lines += ["", "The selected skill companion has two separately cataloged package runners; staged skill/runtime inputs are required."]
    (a.output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if a.catalog_index:
        export_index(report, a.catalog_index, a.output / "feature-tests.json")


if __name__ == "__main__":
    main()
