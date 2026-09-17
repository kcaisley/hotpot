"""Arrange the generated gate paths and add OpenDB teaching annotations."""
from pathlib import Path
import xml.etree.ElementTree as ET
p=Path(__file__).parent/'assets'
ns={'s':'http://www.w3.org/2000/svg'}
r=ET.parse(p/'top.svg').getroot()
parts=[]
for ident,x,y in [('inst1',235,155),('inst2',680,167.5)]:
 g=r.find(f"s:g[@id='cell_{ident}']",ns)
 shapes=''.join(ET.tostring(e,encoding='unicode') for e in g if e.tag.endswith(('path','circle')))
 parts.append(f'<g id="{ident}" transform="translate({x},{y}) scale(5)" stroke="#4C566A" stroke-width="0.65" fill="#ECEFF4">{shapes}</g>')
def text(x,y,t,col='#4C566A',size=22,anchor='start'):
 return f'<text x="{x}" y="{y}" fill="{col}" font-size="{size}" text-anchor="{anchor}">{t}</text>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="480" viewBox="0 0 1100 480">', '<style>text{font-family:monospace} .wire{stroke:#4C566A;stroke-width:3;fill:none}</style>', '<rect x="110" y="105" width="890" height="240" fill="none" stroke="#4C566A" stroke-width="3"/>',text(110,78,'top',col='#A3BE8C',size=30),text(185,78,'block',col='#A3BE8C')]
s+=['<path class="wire" d="M110 180 H235 M110 255 H235 M415 217.5 H680 M805 217.5 H1000"/>']+parts
for x,y in [(110,180),(110,255),(1000,217.5)]:
 s.append(f'<path d="M{x-8} {y-10} L{x+10} {y} L{x-8} {y+10} Z" fill="#EBCB8B" stroke="#B48EAD" stroke-width="2"/>')
for x,y in [(235,180),(235,255),(415,217.5),(680,217.5),(805,217.5)]:
 s.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#BF616A"/>')
for x,y,t in [(235,140,'inst1'),(680,140,'inst2')]: s.append(text(x,y,t,'#A3BE8C',25))
for x,y,t in [(248,187,'A1'),(248,262,'A2'),(423,244,'ZN'),(690,245,'A'),(810,245,'ZN')]: s.append(text(x,y,t,'#BF616A',19))
for x,y,t in [(160,167,'in1'),(160,242,'in2'),(523,205,'wire1'),(885,205,'out')]: s.append(text(x,y,t,'#B48EAD',22,'middle'))
for x,y,t in [(88,187,'in1'),(88,262,'in2')]: s.append(text(x,y,t,'#4C566A',22,'end'))
s.append(text(1020,224,'out'))
s+= [text(310,310,'NAND2_X1',size=24,anchor='middle'),text(742,310,'INV_X1',size=24,anchor='middle')]
s+= [text(110,405,'Boundary ports: BTerms',col='#4C566A',size=21),text(600,405,'Cell pins: ITerms',col='#BF616A',size=21),text(110,445,'Instances: inst1, inst2',col='#5E81AC',size=21),text(600,445,'Connections: nets',col='#B48EAD',size=21),'</svg>']
(p/'top-annotated.svg').write_text('\n'.join(s))

from pathlib import Path
p=Path(__file__).parent/'assets'
s=(p/'top-annotated.svg').read_text()
s=s[:s.index('<text x="110" y="405"')]
# Generic names first; OpenDB annotations belong on the following slide.
s=s.replace('width="1100" height="480" viewBox="0 0 1100 480"','width="1100" height="390" viewBox="0 0 1100 390"')
(p/'top-detail.svg').write_text(s.replace('height="390" viewBox="0 0 1100 390"', 'height="540" viewBox="0 -65 1100 540"')+'</svg>')
s=s.replace('height="390" viewBox="0 0 1100 390"','height="540" viewBox="0 -65 1100 540"')
s+='''<defs><marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0 0 L9 3.5 L0 7 Z" fill="#5E81AC"/></marker></defs>
<g fill="none" stroke="#5E81AC" stroke-width="2.5" marker-end="url(#arrow)">
<path d="M150 -10 C55 5 25 95 105 105"/>
<path d="M335 -10 C355 40 335 90 278 118"/>
<path d="M575 -10 C600 55 580 120 547 182"/>
<path d="M135 402 C60 380 65 315 108 269"/>
<path d="M390 402 C360 390 343 355 332 325"/>
<path d="M720 402 C600 350 590 270 672 224"/>
</g>
<g fill="#5E81AC" font-size="24">
<text x="75" y="-25">dbBlock</text>
<text x="285" y="-25">dbInst</text>
<text x="530" y="-25">dbNet</text>
<text x="75" y="435">dbBTerm</text>
<text x="330" y="435">dbMaster</text>
<text x="685" y="435">dbITerm</text>
</g>
<g fill="#4C566A" font-size="17">
<text x="75" y="462">port on top</text>
<text x="330" y="462">cell definition</text>
<text x="685" y="462">pin on inst2</text>
</g></svg>'''
(p/'top-opendb.svg').write_text(s)
