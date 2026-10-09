"""Sequentially retain a small pinned CodeCAD sample with per-design attribution."""
import argparse
import json
from pathlib import Path
import time
import urllib.parse
from corpus import fetch, save, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--limit', type=int, default=25)
    args = parser.parse_args()
    root = args.root
    api = 'https://gitlab.lrz.de/api/v4/projects/247043/repository'
    discovery = root / 'discovery' / 'codecad'
    discovery.mkdir(parents=True, exist_ok=True)
    commit_path = discovery / 'commit.json'
    if not commit_path.exists():
        save(commit_path, json.loads(fetch(api + '/commits/master')))
    revision = json.loads(commit_path.read_text(encoding='utf-8'))['id']
    catalog_path = discovery / 'catalog.json'
    if not catalog_path.exists():
        save(catalog_path, json.loads(fetch(api + '/tree?' + urllib.parse.urlencode(
            {'per_page': 100, 'ref': revision, 'path': 'dataset'}))))
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    retained = 0
    for design in catalog[:args.limit]:
        identifier = design['name']
        record_path = root / 'sources' / f'codecad__{identifier}.json'
        if record_path.exists():
            retained += 1
            continue
        listing = json.loads(fetch(api + '/tree?' + urllib.parse.urlencode(
            {'per_page': 100, 'ref': revision, 'path': design['path']})))
        source_root = root / 'repos' / f'codecad__{identifier}'
        source_root.mkdir(parents=True, exist_ok=True)
        files, attribution = [], {}
        for entry in listing:
            if entry['type'] != 'blob' or not entry['name'].lower().endswith(('.scad', '.json', '.txt', '.svg', '.dxf', '.dat')):
                continue
            url = f"https://gitlab.lrz.de/ai-ad/codecad/-/raw/{revision}/{urllib.parse.quote(entry['path'])}"
            content = fetch(url)
            destination = source_root / entry['name']
            destination.write_bytes(content)
            files.append({'path': entry['name'], 'sha256': sha(content), 'bytes': len(content),
                          'license_file': entry['name'] == 'info.json', 'download_url': url})
            if entry['name'] == 'info.json':
                attribution = json.loads(content)
            time.sleep(2)
        save(record_path, {'repository': f"codecad-{attribution.get('creator_name', 'unknown')}/{identifier}",
             'revision': revision, 'url': f"https://gitlab.lrz.de/ai-ad/codecad/-/tree/{revision}/{design['path']}",
             'root': source_root.relative_to(root).as_posix(), 'license': attribution.get('license', 'UNKNOWN'),
             'description': attribution.get('title'), 'topics': [], 'files': files, 'source_site': 'CodeCAD',
             'acquisition': 'Pinned university GitLab dataset; original author/license in info.json'})
        retained += 1
        print(f'Retained CodeCAD {identifier}', flush=True)
        time.sleep(2)
    print(f'CodeCAD designs retained: {retained}', flush=True)


if __name__ == '__main__':
    main()
