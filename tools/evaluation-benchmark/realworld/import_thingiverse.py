"""Retain original SCAD text from the pinned Thingiverse OpenSCAD Pile dataset."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import pyarrow.parquet as pq
from corpus import fetch, save, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    root = args.root
    discovery = root / 'discovery' / 'thingiverse-dataset'
    discovery.mkdir(parents=True, exist_ok=True)
    metadata_path = discovery / 'metadata.json'
    if not metadata_path.exists():
        save(metadata_path, json.loads(fetch('https://huggingface.co/api/datasets/redcathode/thingiverse-openscad')))
    metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    revision = metadata['sha']
    base = f'https://huggingface.co/datasets/redcathode/thingiverse-openscad/resolve/{revision}'
    for name in ['README.md', 'data/train-00000-of-00001.parquet']:
        destination = discovery / Path(name).name
        if not destination.exists():
            destination.write_bytes(fetch(f'{base}/{name}'))
    archive_hash = sha((discovery / 'train-00000-of-00001.parquet').read_bytes())
    rows = pq.read_table(discovery / 'train-00000-of-00001.parquet').to_pylist()
    rejected = []
    retained = files_count = 0
    for row in rows:
        thing = str(row['thingiverse_id'])
        snapshot = sha(row['scad'].encode('utf-8'))[:16]
        repository = f"thingiverse-{row['creator_name']}/{thing}-{snapshot}"
        record_path = root / 'sources' / f'thingiverse__{thing}__{snapshot}.json'
        source_root = root / 'repos' / f'thingiverse__{thing}__{snapshot}'
        matches = list(re.finditer(r'^([^\r\n]+\.scad):\r?\n```[^\r\n]*\r?\n(.*?)^```[ \t]*\r?$', row['scad'], re.M | re.S))
        if not matches:
            rejected.append({'thingiverse_id': thing, 'reason': 'No unambiguous filename/code fences'})
            continue
        files = []
        names = set()
        for match in matches:
            name, text = match.groups()
            path = PurePosixPath(name)
            if path.is_absolute() or any(p in ('.', '..') or ':' in p or '\\' in p for p in path.parts) or name.casefold() in names:
                rejected.append({'thingiverse_id': thing, 'reason': 'Unsafe or duplicate filename', 'filename': name})
                files = []
                break
            names.add(name.casefold())
            content = text.encode('utf-8')
            files.append({'path': name, 'sha256': sha(content), 'bytes': len(content), 'license_file': False})
        if not files:
            continue
        source_root.mkdir(parents=True, exist_ok=True)
        for match in matches:
            name, text = match.groups()
            target = source_root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            content = text.encode('utf-8')
            if target.exists() and target.read_bytes() != content:
                raise ValueError(f'Modified retained source: {target}')
            target.write_bytes(content)
        attribution = {k: row[k] for k in ['thingiverse_id', 'name', 'creator_name', 'license', 'description', 'added']}
        save(source_root / 'attribution.json', attribution)
        files.append({'path': 'attribution.json', 'sha256': sha((source_root / 'attribution.json').read_bytes()),
                      'bytes': (source_root / 'attribution.json').stat().st_size, 'license_file': True})
        save(record_path, {'repository': repository, 'revision': revision, 'url': f'https://www.thingiverse.com/thing:{thing}',
                          'archive_url': f'{base}/data/train-00000-of-00001.parquet', 'archive_sha256': archive_hash,
                          'root': source_root.relative_to(root).as_posix(), 'license': row['license'],
                          'description': row['name'], 'topics': [], 'files': files, 'source_site': 'Thingiverse',
                          'acquisition': 'Pinned public dataset mirror; original code fences extracted without source edits',
                          'dependencies': 'Only SCAD text included by dataset; external assets and libraries may be missing'})
        retained += 1
        files_count += len(matches)
    save(discovery / 'import-summary.json', {'revision': revision, 'parquet_sha256': archive_hash,
         'dataset_rows': len(rows), 'retained_designs': retained, 'scad_files': files_count, 'rejected': rejected})
    print(json.dumps({'retained_designs': retained, 'scad_files': files_count, 'rejected': len(rejected)}), flush=True)


if __name__ == '__main__':
    main()
