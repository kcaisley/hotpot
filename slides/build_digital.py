from pathlib import Path
import json, subprocess, re
p=Path(__file__).parent/'assets'
skin=p/'nord-digital.svg'
s=skin.read_text().replace('#000','#4C566A').replace('font-weight: bold','font-weight: normal')
skin.write_text(s)
def cell(t,con): return dict(type=t,port_directions={k:'output' if k=='Y' else 'input' for k in con},connections={k:[v] for k,v in con.items()})
def net(ports,cells): return {'modules':{'top':{'ports':{k:{'direction':d,'bits':[b]} for k,d,b in ports},'cells':cells,'netnames':{}}}}
data={
'inverter':net([('A','input',2),('ZN','output',3)],{'INV_X1':cell('$_NOT_',{'A':2,'Y':3})}),
'nand':net([('A1','input',2),('A2','input',3),('ZN','output',4)],{'NAND2_X1':cell('$_NAND_',{'A':2,'B':3,'Y':4})}),
 'top':net([('in1','input',2),('in2','input',3),('out','output',5)],{'inst1':cell('$_NAND_',{'A':2,'B':3,'Y':4}),'inst2':cell('$_NOT_',{'A':4,'Y':5})})}
for name,d in data.items():
 (p/f'{name}.json').write_text(json.dumps(d,indent=2)+'\n')
 subprocess.run(['netlistsvg',str(p/f'{name}.json'),'--skin',str(skin),'-o',str(p/f'{name}.svg')],check=True)
 if name == 'top':
  svg=p/'top.svg'
  text=svg.read_text()
  labels=[]
  for ident in ['inst1','inst2']:
   m=re.search(r'<g[^>]*transform="translate\(([^,]+),([^\)]+)\)"[^>]*id="cell_'+ident+'"',text)
   x,y=map(float,m.groups())
   labels.append(f'<text x="{x}" y="{y-7}" style="fill:#A3BE8C;font-size:9px">{ident}</text>')
  labels.append('<text x="128" y="54" style="fill:#B48EAD;font-size:8px;text-anchor:middle">wire1</text>')
  svg.write_text(text.replace('</svg>',''.join(labels)+'</svg>'))
 subprocess.run(['rsvg-convert','-f','pdf','-o',str(p/f'{name}.pdf'),str(p/f'{name}.svg')],check=True)
