"""Audit frozen corpus diversity and source identity without changing the manifest."""
import argparse
from collections import Counter
import json
from pathlib import Path
from corpus import save, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((args.root / "manifest.json").read_text(encoding="utf-8"))
    models = manifest["models"]
    repositories = Counter(m["repository"] for m in models)
    owners = Counter(m["repository"].split("/")[0].lower() for m in models)
    directories = Counter(m["repository"] + "/" + str(Path(m["path"]).parent) for m in models)
    problems = []
    for model in models:
        if sha((args.root / model["file"]).read_bytes()) != model["sha256"]:
            problems.append("hash mismatch: " + model["id"])
    for label, values in (("repository", repositories), ("directory", directories), ("owner", owners)):
        if max(values.values()) > manifest["caps"][label]:
            problems.append(label + " cap exceeded")
    if len({m["normalized_sha256"] for m in models}) != len(models):
        problems.append("duplicate normalized source")
    report = {"passed": not problems, "problems": problems, "models": len(models),
              "repositories": len(repositories), "owners": len(owners), "directories": len(directories),
              "max_per_repository": max(repositories.values()), "max_per_directory": max(directories.values()),
              "max_per_owner": max(owners.values()), "tags": dict(Counter(t for m in models for t in m["tags"])),
              "licenses": dict(Counter(m["license"] for m in models)),
              "selected_source_bytes": sum(m["bytes"] for m in models),
              "manifest_sha256": sha((args.root / "manifest.json").read_bytes()),
              "repository_counts": dict(repositories),
              "limits": "Static candidate audit; not standalone execution or valid-solid certification. Preserve original warnings and failures."}
    save(args.output, report)
    print(json.dumps({k: v for k,v in report.items() if k != "repository_counts"}), flush=True)
    raise SystemExit(0 if not problems else 1)


if __name__ == "__main__":
    main()
