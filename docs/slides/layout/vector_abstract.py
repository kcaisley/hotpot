# vector_abstract.py -- exact LEF polygons and teaching routes, with shared net highlights.
from pathlib import Path
import json,html,subprocess
from label_positions import PIN_LABELS, NET_LABELS, on_shape
P=Path(__file__).resolve().parent;g=json.loads((P/'geometry.json').read_text())
B='#5E81AC';D='#4C566A';G='#A3BE8C';U='#B48EAD';R='#BF616A';FADE='#D8DEE9'
def build(focus=None):
 s=['<svg xmlns="http://www.w3.org/2000/svg" width="1150" height="1240" viewBox="0 0 1150 1240"><rect width="1150" height="1240" fill="white"/>']
 def pt(x,y):return 280+x*600,1050-y*600
 def tx(x,y,label,color=D,size=34,anchor='middle'):
  s.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-size="{size}" fill="{color}" text-anchor="{anchor}">{html.escape(label)}</text>')
 def poly(points,fill,stroke=B):s.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in map(lambda p:pt(*p),points))+'" fill="'+fill+'" stroke="'+stroke+'" stroke-width="2"/>')
 connections={('inst1','A1'):'in1',('inst1','A2'):'in2',('inst1','ZN'):'wire1',('inst2','A'):'wire1',('inst2','ZN'):'out'}
 for inst,c in g['cells'].items():
  dx,dy=c['origin'];master=c['master'];w,h=c['size']
  for pin,polys in g['pins'][master].items():
   net=pin if pin in ['VDD','VSS'] else connections.get((inst,pin))
   active=focus is not None and net==focus
   for p in polys:poly([(x+dx,y+dy) for x,y in p],U if active else '#E5E9F0',U if active else B)
  x,y=pt(dx,h);s.append(f'<rect x="{x}" y="{y}" width="{w*600}" height="{h*600}" stroke="{D}" stroke-width="2.5" stroke-dasharray="9 7" fill="none"/>')
  tx(x+w*300,65,inst,G,42);tx(x+w*300,110,master,D,32)
 for net,route in g['routes_um'].items():
  col=U if not focus or net==focus else FADE
  points=[pt(*p) for p in route];s.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" stroke="{col}" stroke-width="42" stroke-linejoin="miter" stroke-linecap="square" fill="none"/>')
  # Source-library VIA1 cut is 70 nm; on each selected cell access point.
  ends=[route[-1]] if net in ['in1','in2'] else [route[0]] if net=='out' else [route[0],route[-1]]
  for x,y in ends:
   X,Y=pt(x,y);s.append(f'<rect x="{X-21}" y="{Y-21}" width="42" height="42" fill="{D if not focus or net==focus else FADE}"/>')
 for net,x,y in NET_LABELS:
  if not focus or net==focus:
   X,Y=pt(x,y);s.append(on_shape(X,Y,net))
 for inst,c in g['cells'].items():
  for pin,x,y,rotation in PIN_LABELS[c['master']]:
   if not focus or connections[(inst,pin)]==focus:
    X,Y=pt(x+c['origin'][0],y);s.append(on_shape(X,Y,pin,30,rotation))
 for pin,y in [('VDD',1.4),('VSS',0)]:
  if not focus or focus==pin:
   X,Y=pt(.475,y);s.append(on_shape(X,Y,pin,34))
 if focus:tx(575,1195,'Highlighted net: '+focus,'#000000',31)
 else:
  for x,name,col in [(400,'M1',B),(565,'M2',U),(730,'VIA1',D)]:
   s.append(f'<rect x="{x}" y="1172" width="26" height="26" fill="{col}"/>');tx(x+40,1198,name,'#000000',32,'start')
 s+=['</svg>'];name='pair_pins_labeled' if not focus else 'pair_pins_'+focus
 (P/(name+'.svg')).write_text(''.join(s));subprocess.run(['rsvg-convert','-f','pdf','-o',str(P/(name+'.pdf')),str(P/(name+'.svg'))],check=True)
for focus in [None,'in1','wire1','VDD','VSS']:build(focus)
