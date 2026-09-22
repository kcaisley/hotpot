"""Regenerate the seven overview snapshots in OpenROAD's native GUI renderer."""
from pathlib import Path
import os
import subprocess

P = Path(__file__).resolve().parent
stages = ['floorplan', 'global_placement', 'detailed_placement', 'cts',
          'global_routing', 'detailed_routing', 'finishing']
stage_dirs = {
    'floorplan': 'placement', 'global_placement': 'placement',
    'detailed_placement': 'placement', 'cts': 'routing',
    'global_routing': 'routing', 'detailed_routing': 'routing',
    'finishing': 'finishing',
}
for directory in set(stage_dirs.values()):
    (P / 'images' / directory).mkdir(exist_ok=True)
for stage in stages:
    env = os.environ.copy()
    env.update(QT_QPA_PLATFORM='offscreen', HOTPOT_SLIDE_STAGE=stage)
    result = subprocess.run(['openroad', '-gui', '-no_init', '-exit', str(P/'render_stages.tcl')],
                            env=env, capture_output=True, text=True)
    directory = stage_dirs[stage]
    (P/f'images/{directory}/{stage}.log').write_text(result.stdout + result.stderr)
    result.check_returncode()
    out = P/f'images/{directory}/{stage}.png'
    assert out.exists() and '[ERROR' not in result.stdout, result.stdout
    print(stage, out.stat().st_size)
subprocess.run(['python3', str(P/'build_cts_view.py')], check=True)
subprocess.run(['python3', str(P/'build_stage_vectors.py')], check=True)
