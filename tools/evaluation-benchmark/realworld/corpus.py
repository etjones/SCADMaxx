"""Discover, freeze and diversity-sample public OpenSCAD projects. Never executes repository scripts."""
import argparse
from collections import Counter, defaultdict
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import random
import re
import time
import urllib.parse
import urllib.request
import urllib.error
from email.utils import parsedate_to_datetime
import zipfile

USER_AGENT = "SCADMaxx-realworld-benchmark/0.1"
ASSETS = {".scad", ".stl", ".off", ".obj", ".3mf", ".svg", ".dxf", ".dat", ".csv", ".txt", ".json", ".png", ".jpg", ".jpeg", ".ttf", ".otf", ".md"}
EXCLUDE = {".git", "node_modules", "test", "tests", "regression", "attic", "deprecated", "backup"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def fetch(url, limit=40_000_000):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                data = response.read(limit + 1)
                if len(data) > limit:
                    raise ValueError(f"Download exceeds {limit} bytes")
                return data
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            limited = error.code == 429 or (error.code == 403 and
                       (error.headers.get("X-RateLimit-Remaining") == "0" or "rate limit" in body.lower()))
            if not limited and error.code not in (500, 502, 503, 504):
                raise
            if attempt == 5:
                raise RuntimeError(f"Request retries exhausted: HTTP {error.code} for {url}") from error
            delay = (60 if limited else 5) * 2 ** attempt
            retry = error.headers.get("Retry-After")
            if retry:
                try:
                    delay = max(delay, float(retry))
                except ValueError:
                    delay = max(delay, parsedate_to_datetime(retry).timestamp() - time.time())
            reset = error.headers.get("X-RateLimit-Reset")
            if limited and reset:
                delay = max(delay, float(reset) - time.time() + 2)
            print(f"HTTP {error.code}; honoring rate limit/backoff for {delay:.0f}s", flush=True)
            time.sleep(delay)


def discover(root, queries=None, pages=2):
    if queries is None:
        queries = ["language:OpenSCAD fork:false stars:>=2", "openscad models fork:false", "openscad collection fork:false", "language:OpenSCAD fork:false stars:0..10"]
    repos = {}
    for index, query in enumerate(queries):
        for page in range(1, pages + 1):
            cache = root / "discovery" / f"search-{sha(query.encode())[:16]}-{page}.json"
            if cache.exists():
                result = json.loads(cache.read_text(encoding="utf-8"))
            else:
                url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({"q": query, "sort": "stars", "per_page": 100, "page": page})
                result = json.loads(fetch(url))
                save(cache, result)
                print(f"Search {query}, page {page}: {len(result.get('items', []))} repositories", flush=True)
                time.sleep(10)
            for repo in result.get("items", []):
                description = (repo["full_name"] + " " + (repo.get("description") or "")).lower()
                if any(word in description for word in ("fosscad", "firearm", "gun", "weapon")):
                    continue
                if not repo["fork"] and repo["size"] < 180_000:
                    repos[repo["full_name"]] = repo
            if len(result.get("items", [])) < 100:
                break
    save(root / "discovery" / "repositories.json", list(repos.values()))
    print(f"Discovered {len(repos)} repositories", flush=True)
    return list(repos.values())


def acquire(root, repo, locked=None):
    name = repo["full_name"]
    slug = name.replace("/", "__")
    record_path = root / "sources" / f"{slug}.json"
    if record_path.exists() and locked is None:
        return json.loads(record_path.read_text(encoding="utf-8"))
    url = locked["archive_url"] if locked else f"https://codeload.github.com/{name}/zip/refs/heads/{urllib.parse.quote(repo['default_branch'], safe='')}"
    data = fetch(url)
    if locked and sha(data) != locked["archive_sha256"]:
        raise ValueError("Pinned archive hash differs; retain original evidence and investigate")
    archive = zipfile.ZipFile(io.BytesIO(data))
    revision = archive.comment.decode("ascii").strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("GitHub archive lacks a full commit identity")
    if sum(f.file_size for f in archive.infolist()) > 350_000_000:
        raise ValueError("Expanded repository exceeds 350 MB")
    destination = root / "repos" / slug
    files = []
    for member in archive.infolist():
        parts = PurePosixPath(member.filename).parts[1:]
        if not parts or member.is_dir():
            continue
        if any(p in ("..", ".") or ":" in p or "\\" in p for p in parts):
            raise ValueError("Unsafe archive path")
        if (member.external_attr >> 16) & 0o170000 == 0o120000:
            continue
        relative = PurePosixPath(*parts)
        license_file = any(word in relative.name.lower() for word in ("license", "licence", "copying", "copyright"))
        if relative.suffix.lower() not in ASSETS and not license_file:
            continue
        if member.file_size > 35_000_000:
            continue
        target = destination.joinpath(*parts)
        if not target.resolve().is_relative_to(destination.resolve()):
            raise ValueError("Archive path escaped repository")
        content = archive.read(member)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        files.append({"path": relative.as_posix(), "sha256": sha(content), "bytes": len(content), "license_file": license_file})
    record = {"repository": name, "revision": revision, "url": repo["html_url"], "archive_url": f"https://codeload.github.com/{name}/zip/{revision}", "archive_sha256": sha(data), "root": destination.relative_to(root).as_posix(), "license": (repo.get("license") or {}).get("spdx_id", "UNKNOWN"), "description": repo.get("description"), "topics": repo.get("topics", []), "files": files}
    if locked:
        if revision != locked["revision"] or record["files"] != locked["files"]:
            raise ValueError("Restored repository differs from frozen source record")
        return locked
    save(record_path, record)
    return record


def select(root, records, target, repo_cap, directory_cap, excluded=None, site_cap=None, all_files=False):
    pools, seen = {}, set(excluded or [])
    rejected = Counter()
    processed = 0
    for record in sorted(records, key=lambda x: x["repository"]):
        groups = defaultdict(list)
        for file in record["files"]:
            path = PurePosixPath(file["path"])
            if path.suffix.lower() != ".scad" or (not all_files and any(p.lower() in EXCLUDE for p in path.parts)):
                continue
            content = (root / record["root"] / file["path"]).read_text(encoding="utf-8", errors="replace")
            normalized = re.sub(r"/\*.*?\*/|//[^\n]*", "", content, flags=re.S)
            normalized = re.sub(r"\s+", "", normalized)
            digest = sha(normalized.encode())
            if not normalized or digest in seen:
                rejected["duplicate_or_empty"] += 1
                continue
            # Exclude obvious helpers with no geometry vocabulary; dynamic evaluation is screened separately.
            if not all_files and not re.search(r"\b(cube|sphere|cylinder|polyhedron|polygon|square|circle|linear_extrude|rotate_extrude|import|text|surface)\s*\(", content):
                rejected["no_geometry_vocabulary"] += 1
                continue
            seen.add(digest)
            tags = [op for op in ("hull", "minkowski", "text", "import", "surface", "polyhedron", "linear_extrude", "rotate_extrude", "offset", "projection", "difference", "intersection", "for") if re.search(r"\b" + op + r"\s*\(", content)]
            identifier = sha((record["repository"] + "/" + file["path"]).encode())[:16]
            source_site = record.get('source_site', 'GitHub')
            source_url = record['url'] if source_site != 'GitHub' else f"{record['url']}/blob/{record['revision']}/{urllib.parse.quote(file['path'])}"
            groups[str(path.parent)].append({"id": identifier, "repository": record["repository"], "revision": record["revision"], "path": file["path"], "file": f"{record['root']}/{file['path']}", "sha256": file["sha256"], "normalized_sha256": digest, "bytes": file["bytes"], "license": record["license"], "tags": tags, "source_url": source_url, 'source_site': source_site})
        queue = []
        for group in groups.values():
            random.Random(20261004).shuffle(group)
        for index in range(max((len(g) for g in groups.values()), default=0) if all_files else directory_cap):
            for directory in sorted(groups):
                if index < len(groups[directory]):
                    queue.append(groups[directory][index])
        pools[record["repository"]] = queue if all_files else queue[:repo_cap]
        processed += 1
        if processed % 500 == 0:
            print(f'Indexed {processed}/{len(records)} source records', flush=True)
    selected, owners, sites = [], Counter(), Counter()
    for index in range(max((len(q) for q in pools.values()), default=0) if all_files else repo_cap):
        for name in sorted(pools):
            owner = name.split("/")[0].lower()
            if index < len(pools[name]) and (all_files or owners[owner] < 40):
                model = pools[name][index]
                site = model['source_site']
                if site_cap is not None and sites[site] >= site_cap:
                    continue
                selected.append(model)
                owners[owner] += 1
                sites[site] += 1
                if not all_files and len(selected) == target:
                    break
        if not all_files and len(selected) == target:
            break
    manifest = {"schema": 1, "seed": 20261004, "requested": target, "caps": {"repository": repo_cap, "directory": directory_cap, "owner": 40, 'source_site': site_cap}, "selection": "Round-robin repositories and directories; normalized source deduplication; no generated parameter variants. Static candidates, run outcomes retained separately.", "repositories": len(set(m["repository"] for m in selected)), "owners": len(owners), 'source_sites': dict(sites), "rejected": dict(rejected), "models": selected}
    if all_files:
        manifest['requested'] = 'all'
        manifest['caps'] = None
        manifest['selection'] = 'All nonempty normalized-source-unique SCAD files; original corpus excluded. No count, owner, repository, directory or geometry-vocabulary culling. All raw downloads retained separately.'
    save(root / "manifest.json", manifest)
    print(json.dumps({k: v for k, v in manifest.items() if k != "models"}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--target", type=int, default=1000)
    parser.add_argument("--repo-cap", type=int, default=25)
    parser.add_argument("--directory-cap", type=int, default=10)
    parser.add_argument('--site-cap', type=int, help='Maximum selected candidates from one source site')
    parser.add_argument('--all', action='store_true', help='Retain all unique nonempty SCAD candidates without diversity or count caps')
    parser.add_argument("--select-only", action="store_true")
    parser.add_argument("--max-repositories", type=int, default=300)
    parser.add_argument("--query", action="append", help="Repeatable GitHub repository search query")
    parser.add_argument("--pages", type=int, default=2)
    parser.add_argument("--exclude-manifest", type=Path, help="Exclude normalized source hashes from a frozen corpus")
    parser.add_argument("--restore", action="store_true", help="Rehydrate missing files from retained sources/*.json using pinned commits, not live branches")
    args = parser.parse_args()
    args.root.mkdir(parents=True, exist_ok=True)
    if args.restore:
        for path in sorted((args.root / "sources").glob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            missing = [f for f in record["files"] if not (args.root / record["root"] / f["path"]).exists()]
            if not missing:
                continue
            for file in record["files"]:
                target = args.root / record["root"] / file["path"]
                if target.exists() and sha(target.read_bytes()) != file["sha256"]:
                    raise ValueError(f"Modified retained file: {target}")
            repo = {"full_name": record["repository"], "html_url": record["url"], "license": {"spdx_id": record["license"]}, "description": record["description"], "topics": record["topics"]}
            acquire(args.root, repo, locked=record)
            print(f"Restored {record['repository']} at {record['revision']}", flush=True)
        return
    if args.select_only:
        records = [json.loads(p.read_text(encoding="utf-8")) for p in (args.root / "sources").glob("*.json")]
    else:
        repos = discover(args.root, args.query, args.pages)[:args.max_repositories]
        records, errors = [], []
        for repo in repos:
            try:
                record = acquire(args.root, repo)
                records.append(record)
                print(f"Retained {record['repository']}: {sum(f['path'].lower().endswith('.scad') for f in record['files'])} SCAD", flush=True)
            except Exception as error:
                errors.append({"repository": repo["full_name"], "error": str(error)})
                save(args.root / "acquisition-errors.json", errors)
                print(f"Skipped {repo['full_name']}: {error}", flush=True)
                if "retries exhausted" in str(error):
                    raise
            time.sleep(2)
        save(args.root / "acquisition-errors.json", errors)
    excluded = set()
    if args.exclude_manifest:
        previous = json.loads(args.exclude_manifest.read_text(encoding="utf-8"))
        excluded = {model["normalized_sha256"] for model in previous["models"]}
    select(args.root, records, args.target, args.repo_cap, args.directory_cap, excluded, None if args.all else args.site_cap, args.all)


if __name__ == "__main__":
    main()
