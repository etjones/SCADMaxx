"""Run README language-guide code blocks against an explicit SCADMaxx delivery."""
import argparse
import json
import math
import os
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument("--runtime", type=Path, required=True)
p.add_argument("--output", type=Path, required=True)
p.add_argument("--source", type=Path, required=True)
a = p.parse_args()
a.output.mkdir(parents=True, exist_ok=False)
docs = Path(__file__).resolve().parents[2] / "docs"
env = os.environ.copy()
env.update(QT_QPA_PLATFORM="offscreen", QT_PLUGIN_PATH=str(a.runtime),
           QT_QPA_PLATFORM_PLUGIN_PATH=str(a.runtime / "platforms"))
env["PATH"] = str(a.runtime) + ";C:/Windows/System32;C:/Windows"
rows = []

def run(name, code, backend, echoes=(), bounds=None, diagnostic=False):
    stem = a.output / (name + "-" + backend)
    scad = stem.with_suffix(".scad")
    scad.write_text(code, encoding="utf-8")
    output = stem.with_suffix(".stl" if bounds else ".echo")
    cmd = [str(a.runtime / "scadmaxx.com"), "--enable=object-function",
           "--backend=" + backend, "-o", str(output)]
    if bounds:
        cmd += ["--export-format=asciistl"]
    cmd.append(str(scad))
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
    result = output.read_text(encoding="utf-8", errors="replace") if output.exists() else ""
    log = proc.stdout + proc.stderr + (result if not bounds else "")
    stem.with_suffix(".log").write_text(log, encoding="utf-8")
    errors = bool(re.search(r"ERROR:|WARNING:|DEPRECATED:", log))
    ok = proc.returncode == 0 and output.exists() and not errors
    if diagnostic:
        ok = proc.returncode in (0, 1) and "WARNING:" in log and "ECHO: undef" in log and "ERROR:" not in log
    for expected in echoes:
        ok = ok and expected in log
    actual_bounds = None
    if bounds:
        vertices = [tuple(map(float, v)) for v in re.findall(
            r"\bvertex\s+(\S+)\s+(\S+)\s+(\S+)", result)]
        if vertices:
            actual_bounds = [[f(v[i] for v in vertices) for i in range(3)] for f in (min, max)]
            ok = ok and all(math.isclose(x, y, abs_tol=1e-5)
                            for av, ev in zip(actual_bounds, bounds) for x, y in zip(av, ev))
        else:
            ok = False
    rows.append(dict(name=name, backend=backend, passed=ok, exit=proc.returncode,
                     bounds=actual_bounds, command=cmd))
    print(f"{'PASS' if ok else 'FAIL'} {name} {backend}", flush=True)

expected_echo = {
    ("objects", 1): ['ECHO: "Plate"'], ("objects", 2): ['ECHO: 30, 45'],
    ("objects", 3): ['ECHO: 10'],
    ("geometry-bounds", 1): ['ECHO: [10, 0, 0]', 'ECHO: [50, 30, 20]',
                               'ECHO: [40, 30, 20]', 'ECHO: [30, 15, 10]'],
}
expected_bounds = {
    ("objects", 1): [[0,0,0],[30,20,4]],
    ("customizer-attributes", 1): [[0,0,0],[30,20,4]],
    ("customizer-attributes", 2): [[0,0,0],[30,20,4]],
    ("parts-assemblies", 1): [[0,0,0],[75,20,4]],
    ("anchors-attachments", 1): [[0,0,0],[40,20,16]],
    ("anchors-attachments", 2): [[0,0,0],[1,1,1]],
    ("geometry-bounds", 1): [[55,0,0],[60,5,5]],
    ("geometry-bounds", 2): [[0,0,0],[35,30,5]],
}
for guide in sorted(docs.glob("language-*.md")):
    slug = guide.stem.removeprefix("language-")
    blocks = re.findall(r"```scad\s*\n(.*?)```", guide.read_text(encoding="utf-8"), re.S)
    for n, code in enumerate(blocks, 1):
        if (slug, n) == ("anchors-attachments", 2):
            # The guide explicitly locates this fragment inside a Part body.
            code = '@{type:Part,id:"example"} module example() {\n' + code + '\ncube(1); }\n@{type:Component,id:"example"} example();\n'
        for backend in ("Manifold", "CGAL"):
            run(f"{slug}-{n}-echo", code, backend, expected_echo.get((slug,n), ()))
            bounds = expected_bounds.get((slug,n))
            if bounds:
                run(f"{slug}-{n}-render", code, backend, bounds=bounds)

fixture = a.source / "tests/data/scad/experimental/object/geometry-bounds-tests.scad"
for backend in ("Manifold", "CGAL"):
    run("geometry-regression", fixture.read_text(encoding="utf-8"), backend,
        ['ECHO: "geometry bounds passed"'])
    for name, expr in {
        "empty": "{{ }}", "mixed": "{{ cube(1); square(2); }}",
        "wrong-type": "42", "subtracted-empty": "{{ difference() { cube(1); cube(2); } }}",
    }.items():
        run("geometry-error-"+name, f"echo(geometry_bounds({expr}));", backend, diagnostic=True)

(a.output / "results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
print(f"{sum(r['passed'] for r in rows)}/{len(rows)} checks passed")
raise SystemExit(0 if all(r["passed"] for r in rows) else 1)
