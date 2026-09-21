"""Stream the final workshop DEF into GDS with the upstream ORFS utility.

Use ORFS's physical layer map, the LEFs used by the workshop, and the real
Nangate45 cell GDS. Render the result with the user's existing Nord .lyp.
"""
from pathlib import Path
import os
import subprocess
import xml.etree.ElementTree as ET

P = Path(__file__).resolve().parent
ROOT = P.parent.parent
ORFS = Path(os.environ.get('OPENROAD_FLOW_SCRIPTS', str(Path.home()/'Documents/libs/OpenROAD-flow-scripts')))
OPENROAD = Path(os.environ.get('OPENROAD_SOURCE', str(Path.home()/'Documents/libs/OpenROAD')))
PLATFORM = ORFS/'flow/platforms/nangate45'
OUT = P/'assets/stages'
OUT.mkdir(exist_ok=True)

# This local stream-out configuration does not change the installed technology.
tree = ET.parse(PLATFORM/'FreePDK45.lyt')
tree.find('base-path').text = str(PLATFORM)
cfg = tree.find('reader-options/lefdef')
for node in cfg.findall('lef-files'):
    cfg.remove(node)
for name in ['Nangate45_tech.lef', 'Nangate45_stdcell.lef']:
    ET.SubElement(cfg, 'lef-files').text = str(OPENROAD/'test/Nangate45'/name)
tech = OUT/'streamout.lyt'
tree.write(tech, encoding='utf-8', xml_declaration=True)

args = ['klayout', '-b']
for key, value in {
    'design_name': 'gcd',
    'in_def': ROOT/'results/gcd/gcd_final.def',
    'in_files': PLATFORM/'gds/NangateOpenCellLibrary.gds',
    'seal_file': '',
    'out_file': OUT/'design.gds',
    'tech_file': tech,
    'layer_map': '',
}.items():
    args += ['-rd', f'{key}={value}']
args += ['-r', str(ORFS/'flow/util/def2stream.py')]
env = os.environ.copy()
env['QT_QPA_PLATFORM'] = 'offscreen'
result = subprocess.run(args, env=env, capture_output=True, text=True)
(OUT/'streamout.log').write_text(result.stdout+result.stderr)
print(result.stdout, result.stderr)
result.check_returncode()
subprocess.run(['klayout', '-b', '-r', str(P/'render_finished_layout.py')], env=env, check=True)
