"""Draw actual post-CTS geometry and clock connectivity, with readable strokes."""
from pathlib import Path
from collections import defaultdict
import subprocess
P=Path(__file__).resolve().parent/'assets/stages'
rows=[line.split('\t') for line in (P/'cts_geometry.tsv').read_text().splitlines()]
die=list(map(float,rows[0][1:]))
scale=850/max(die[2]-die[0],die[3]-die[1])
def xy(x,y):return 25+(float(x)-die[0])*scale,875-(float(y)-die[1])*scale
def rect(x0,y0,x1,y1,fill,stroke,width=1):
    x,y=xy(x0,y1);X,Y=xy(x1,y0)
    return f'<rect x="{x}" y="{y}" width="{X-x}" height="{Y-y}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
nets=defaultdict(list);cells=[]
for row in rows[1:]:
    if row[0]=='CELL':cells.append(row)
    else:nets[row[1]].append(row)
buffers={r[2] for pins in nets.values() for r in pins if r[0]=='PIN' and r[3]=='OUTPUT'}
s=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="900" viewBox="0 0 900 900"><rect width="900" height="900" fill="white"/>',rect(*die,'none','#D8DEE9',2)]
for _,name,master,*box in cells:
    s.append(rect(*box,'#F4F6F8','#D8DEE9',.7))
for _,name,master,*box in cells:
    if name in buffers:s.append(rect(*box,'#A3BE8C','#4C566A',1.3))
    elif master.startswith('DFF'):s.append(rect(*box,'#EAE3F0','#B48EAD',1.1))
edges=0
for name,pins in nets.items():
    drivers=[p for p in pins if (p[0]=='PIN' and p[3]=='OUTPUT') or (p[0]=='PORT' and p[3]=='INPUT')]
    assert len(drivers)==1,(name,drivers)
    driver=drivers[0];x,y=xy(*driver[4:6])
    for pin in pins:
        if pin is driver:continue
        X,Y=xy(*pin[4:6]);width=4 if pin[2] in buffers else 2.7
        s.append(f'<path d="M{x},{y} L{X},{Y}" stroke="#5E81AC" stroke-width="{width}" fill="none"/>')
        s.append(f'<circle cx="{X}" cy="{Y}" r="3.5" fill="#5E81AC"/>');edges+=1
    s.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="#4C566A"/>')
s.append('</svg>');out=P/'cts.svg';out.write_text('\n'.join(s))
subprocess.run(['rsvg-convert','-f','pdf','-o',str(P/'cts.pdf'),str(out)],check=True)
print(f'CTS: {len(cells)} placed cells, {len(nets)} clock nets, {len(buffers)} drivers, {edges} connections')
