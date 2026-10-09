"""Retain explicitly discovered public SCAD downloads with hashes and attribution."""
import argparse
import json
from pathlib import Path
import time
import urllib.parse
from corpus import fetch, save, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('catalog', type=Path)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding='utf-8'))
    for item in catalog:
        identifier = sha(item['url'].encode())[:16]
        record_path = args.root / 'sources' / f'web__{identifier}.json'
        if record_path.exists():
            continue
        content = fetch(item['url'])
        if content.lstrip().lower().startswith((b'<!doctype html', b'<html')):
            raise ValueError(f"HTML returned instead of source: {item['url']}")
        name = Path(urllib.parse.unquote(urllib.parse.urlparse(item['url']).path)).name
        if not name.lower().endswith('.scad'):
            raise ValueError('Catalog entry is not a SCAD source')
        destination = args.root / 'repos' / f'web__{identifier}'
        destination.mkdir(parents=True, exist_ok=True)
        (destination / name).write_bytes(content)
        save(destination / 'attribution.json', item)
        attribution = (destination / 'attribution.json').read_bytes()
        save(record_path, {'repository': f"web-{item['author']}/{identifier}", 'revision': sha(content),
             'url': item['page_url'], 'root': destination.relative_to(args.root).as_posix(),
             'license': item['license'], 'source_site': item['source_site'], 'topics': [],
             'description': name, 'files': [{'path': name, 'sha256': sha(content), 'bytes': len(content),
             'license_file': False, 'download_url': item['url']}, {'path': 'attribution.json',
             'sha256': sha(attribution), 'bytes': len(attribution), 'license_file': True}],
             'acquisition': 'Public direct source URL; content pinned by hash, copyright retained'})
        print(f"Retained {item['source_site']} {name}", flush=True)
        time.sleep(2)


if __name__ == '__main__':
    main()
