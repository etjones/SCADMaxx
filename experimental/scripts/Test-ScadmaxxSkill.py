# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "trimesh", "rtree", "networkx"]
# ///
"""Exercise an extracted skill's examples; run with uv run and explicit executables."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

import numpy as np
import trimesh


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill', type=Path, required=True)
    parser.add_argument('--openscad', type=Path, required=True)
    parser.add_argument('--extended', type=Path, required=True)
    parser.add_argument('--bosl-parent', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, OPENSCADPATH=str(args.bosl_parent))
    report = {'commands': [], 'meshes': {}, 'capabilities': {}}

    def run(executable, name, arguments, expect_success=True):
        command = [str(executable), *map(str, arguments)]
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=120)
        log = result.stdout + result.stderr
        (args.output / (name + '.log')).write_text(log, encoding='utf-8')
        good = result.returncode == 0 and not re.search(r'ERROR:|WARNING:|Parser error', log)
        report['commands'].append({'name': name, 'command': command, 'exit': result.returncode,
                                   'clean_success': good})
        if expect_success is not None:
            assert good == expect_success, f'{name}: unexpected result; see log'
        return good

    try:
        for doc in args.skill.rglob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)', doc.read_text(encoding='utf-8-sig')):
                if '://' in link or link.startswith('#'):
                    continue
                assert (doc.parent / link.split('#')[0]).exists(), f'Broken link: {doc}: {link}'
        provenance = json.loads((args.skill / 'references/bundle-source.json').read_text(encoding='utf-8-sig'))
        canonical = args.skill / 'references/customizer-attributes.md'
        assert hashlib.sha256(canonical.read_bytes()).hexdigest() == provenance['document_sha256']
        for label, exe in [('upstream', args.openscad), ('extended', args.extended)]:
            run(exe, label + '-version', ['--version'])
            run(exe, label + '-help', ['--help'])

        model = args.skill / 'assets/parametric-plate.scad'
        cases = [
            ('base', ['finish=false'], [60,40,8], 10, 5),
            ('zero', ['edge_size=0'], [60,40,8], 10, 5),
            ('round', [], [60,40,8], 10, 5),
            ('chamfer', ['treatment="chamfer"'], [60,40,8], 10, 5),
            ('near-limit', ['edge_size=7.49'], [60,40,8], 10, 5),
            ('small', ['length=20','width=18','thickness=3','hole_inset=4',
                       'hole_diameter=2','edge_size=2'], [20,18,3], 4, 2),
        ]
        for name, defines, dimensions, inset, diameter in cases:
            output = args.output / (name + '.stl')
            arguments = ['-o', output]
            for define in defines:
                arguments += ['-D', define]
            run(args.openscad, name, arguments + [model])
            mesh = trimesh.load_mesh(output)
            length, width, height = dimensions
            expected = [[-length/2,-width/2,0],[length/2,width/2,height]]
            assert np.allclose(mesh.bounds, expected, atol=1e-5), (name, mesh.bounds)
            assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0, name
            assert len(mesh.split()) == 1, name
            # A vertical ray through each bore must miss; one just outside must hit material.
            centers = [(x,y) for x in (-length/2+inset,length/2-inset)
                       for y in (-width/2+inset,width/2-inset)]
            origins = [[x,y,-1] for x,y in centers]
            origins += [[x+diameter/2+0.2,y,-1] for x,y in centers]
            hits = mesh.ray.intersects_any(np.array(origins), np.tile([0,0,1], (8,1)))
            assert not hits[:4].any() and hits[4:].all(), (name, hits)
            report['meshes'][name] = {'bounds': mesh.bounds.tolist(), 'volume': float(mesh.volume),
                                      'watertight': True, 'bore_rays': 'pass'}
        volumes = {key: value['volume'] for key,value in report['meshes'].items()}
        assert abs(volumes['base']-volumes['zero']) < 1e-6
        assert volumes['near-limit'] < volumes['round'] < volumes['base']
        assert volumes['chamfer'] < volumes['base']
        run(args.openscad, 'invalid-limit', ['-o', args.output/'invalid.stl', '-D','edge_size=7.5',model], False)
        for label, exe in [('upstream', args.openscad), ('extended', args.extended)]:
            for example in ['objects', 'reactive-customizer']:
                arguments = ['-o', args.output/f'{label}-{example}.csg']
                if label == 'extended' and example == 'objects':
                    arguments += ['--enable=object-function']
                arguments += [args.skill / f'assets/{example}.scad']
                good = run(exe, f'{label}-{example}', arguments, True if label == 'extended' else None)
                report['capabilities'][f'{label}-{example}'] = good
        run(args.openscad, 'base-image', ['-o', args.output/'base.png','--render','--viewall',
            '--autocenter','--imgsize=800,600','-D','finish=false',model])
        run(args.openscad, 'round-image', ['-o', args.output/'round.png','--render','--viewall',
            '--autocenter','--imgsize=800,600',model])
        report['result'] = 'pass'
    finally:
        (args.output/'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'result': report['result'], 'meshes': len(report['meshes']),
                      'capabilities': report['capabilities']}, indent=2))


if __name__ == '__main__':
    main()
