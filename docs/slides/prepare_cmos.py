# prepare_cmos.py -- remove the material legend from the source illustration.
from pathlib import Path
import xml.etree.ElementTree as ET
import subprocess
P=Path(__file__).resolve().parent/'assets'
ET.register_namespace('', 'http://www.w3.org/2000/svg')
t=ET.parse(P/'cmos-cross-section.svg');ns={'s':'http://www.w3.org/2000/svg'}
g=t.find('.//s:g[@id="layer1"]',ns)
legend_groups={'g3933','g3949','g3957','g3973','g3981','g3989','g4018','g4026','g4042','g3941','g3965','g4001','g4009','g4034','g4050'}
for node in list(g):
 if node.get('id') in legend_groups:
  g.remove(node)
 elif node.tag.endswith('}switch'):
  ids=[n.get('id','') for n in node]
  if any(i=='text3974' or i.startswith('text3978') for i in ids):g.remove(node)
out=P/'cmos-cross-section-clean.svg';t.write(out,encoding='utf-8',xml_declaration=True)
subprocess.run(['rsvg-convert','--accept-language=en','-f','pdf',str(out),'-o',str(P/'cmos-cross-section.pdf')],check=True)
