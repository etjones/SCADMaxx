"""Choose a documented diverse validation sample from a completed baseline, retaining exclusions."""
import argparse
from collections import defaultdict
import json
import re
from pathlib import Path
from corpus import save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--count", type=int, default=24)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    meta = json.loads((args.run / "metadata.json").read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in (args.run / "results.jsonl").read_text(encoding="utf-8").splitlines()]
    groups = defaultdict(dict)
    for row in rows:
        groups[row["id"]][row["stage"]] = row
    eligible = [m for m in meta["models"] if all(groups[m["id"]].get(s, {}).get("status") == "ok" for s in ("csg", "preview", "stl"))]
    eligible = [dict(m) for m in eligible]
    for model in eligible:
        csg = (args.run / groups[model["id"]]["csg"]["output"]).read_text(encoding="utf-8", errors="replace")
        model["expanded_csg_tags"] = [tag for tag in ("hull", "minkowski", "text", "import", "surface", "polyhedron", "linear_extrude", "rotate_extrude", "offset", "projection", "difference", "intersection") if re.search(r"\b" + tag + r"\s*\(", csg)]
    eligible.sort(key=lambda m: groups[m["id"]]["stl"]["seconds"])
    bins = [eligible[i * len(eligible) // 4:(i + 1) * len(eligible) // 4] for i in range(4)]
    selected, repos, tags = [], set(), set()
    while len(selected) < min(args.count, len(eligible)):
        changed = False
        for pool in bins:
            options = [m for m in pool if m["id"] not in {s["id"] for s in selected} and m["repository"] not in repos]
            if not options:
                continue
            options.sort(key=lambda m: (-len(set(m["expanded_csg_tags"]) - tags), m["id"]))
            model = options[0]
            selected.append(model)
            repos.add(model["repository"])
            tags.update(model["expanded_csg_tags"])
            changed = True
            if len(selected) == args.count:
                break
        if not changed:
            break
    result = {"ids": [m["id"] for m in selected], "models": selected, "eligible_models": len(eligible),
              "source_run": str(args.run.resolve()), "manifest_sha256": meta["manifest_sha256"],
              "baseline_stl_seconds": {m["id"]: groups[m["id"]]["stl"]["seconds"] for m in selected},
              "excluded_models": len(meta["models"]) - len(eligible),
              "selection": "At most one model/repository, four baseline STL-time quartiles and expanded-CSG operation diversity among models whose baseline CSG/preview/STL completed cleanly. This validation sample is success-conditioned and not a corpus-wide speedup estimate."}
    save(args.output, result)
    print(",".join(result["ids"]))


if __name__ == "__main__":
    main()
