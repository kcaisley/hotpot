"""Regenerate the seven overview snapshots in OpenROAD's native GUI renderer."""
from pathlib import Path
import os
import subprocess

P = Path(__file__).resolve().parent
stages = ['floorplan', 'global_placement', 'detailed_placement', 'cts',
          'global_routing', 'detailed_routing', 'finishing']
(P / 'assets/stages').mkdir(exist_ok=True)
for stage in stages:
    env = os.environ.copy()
    env.update(QT_QPA_PLATFORM='offscreen', HOTPOT_SLIDE_STAGE=stage)
    result = subprocess.run(['openroad', '-gui', '-no_init', '-exit', str(P/'render_stages.tcl')],
                            env=env, capture_output=True, text=True)
    (P/f'assets/stages/{stage}.log').write_text(result.stdout + result.stderr)
    result.check_returncode()
    out = P/f'assets/stages/{stage}.png'
    assert out.exists() and '[ERROR' not in result.stdout, result.stdout
    print(stage, out.stat().st_size)
subprocess.run(['python3', str(P/'build_cts_view.py')], check=True)
subprocess.run(['python3', str(P/'build_stage_vectors.py')], check=True)
