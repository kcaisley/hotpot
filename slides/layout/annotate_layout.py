# annotate_layout.py -- labels reference actual GDS/LEF pin coordinates (um)
from pathlib import Path
import base64, subprocess
from label_positions import PIN_LABELS, NET_LABELS, on_shape
P=Path(__file__).resolve().parent
BODY='#4C566A';GREEN='#A3BE8C';BLUE='#5E81AC';PURPLE='#B48EAD';RED='#BF616A'
def start(w,h):return [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">','<style>text{font-family:DejaVu Sans,sans-serif}</style>']
def txt(s,x,y,t,color=BODY,size=36,anchor='start'):s.append(f'<text class="label" x="{x}" y="{y}" fill="{color}" font-size="{size}" text-anchor="{anchor}">{t}</text>')
def img(s,name,x,y,w,h):
 b=base64.b64encode((P/(name+'.png')).read_bytes()).decode()
 s.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="data:image/png;base64,{b}"/>')
def line(s,x,y,X,Y,color=BODY):s.append(f'<path d="M{x} {y} L{X} {Y}" fill="none" stroke="{color}" stroke-width="2.5"/>')
def save(s,name):
 (P/(name+'.svg')).write_text('\n'.join(s+['</svg>']))
 subprocess.run(['rsvg-convert','-f','pdf','-o',str(P/(name+'.pdf')),str(P/(name+'.svg'))],check=True)
for name,master,inst,w in [('nand_cell','NAND2_X1','inst1',.57),('inv_cell','INV_X1','inst2',.38)]:
 s=start(800,1080);scale=500;x0=205;y0=135
 def pt(x,y):return x0+(x+.15)*scale,y0+(1.55-y)*scale
 img(s,name,x0,y0,(w+.3)*scale,850)
 left,top=pt(0,1.4)
 s.append(f'<rect x="{left}" y="{top}" width="{w*scale}" height="700" fill="none" stroke="{BODY}" stroke-width="2" stroke-dasharray="9 7"/>')
 txt(s,400,55,inst,GREEN,42,'middle');txt(s,400,105,master,BODY,38,'middle')
 pins=[('A1',.4475,.6125,725,660),('A2',.1225,.6125,50,640),('ZN',.285,1.1,725,355)] if name=='nand_cell' else [('A',.1125,.6125,75,640),('ZN',.2775,1.1,690,355)]
 for label,x,y,lx,ly in pins:
  X,Y=pt(x,y);line(s,lx+(42 if lx<300 else -42),ly-12,X,Y,BLUE)
  s.append(f'<circle cx="{X}" cy="{Y}" r="5" fill="{BLUE}"/>');txt(s,lx,ly,label,'#000000',42,'middle')
 txt(s,left+w*250,1015,f'{w:.2f} × 1.40 µm',BODY,34,'middle')
 save(s,name+'_labeled')
for name in ['pair_full','pair_metal','pair_pins']:
 s=start(1150,1240);scale=600;x0=100;y0=120
 def pt(x,y):return x0+(x+.3)*scale,y0+(1.55-y)*scale
 img(s,name,x0,y0,930,1020)
 for x,w,inst,master in [(0,.57,'inst1','NAND2_X1'),(.57,.38,'inst2','INV_X1')]:
  X,Y=pt(x,1.4)
  s.append(f'<rect x="{X}" y="{Y}" width="{w*scale}" height="840" fill="none" stroke="{BODY}" stroke-width="2.5" stroke-dasharray="9 7"/>')
  txt(s,X+w*300,60,inst,GREEN,42,'middle');txt(s,X+w*300,108,master,BODY,32,'middle')
 for label,x,y in NET_LABELS:
  X,Y=pt(x,y);s.append(on_shape(X,Y,label))
 for master,dx in [('NAND2_X1',0),('INV_X1',.57)]:
  for label,x,y,rotation in PIN_LABELS[master]:
   X,Y=pt(x+dx,y);s.append(on_shape(X,Y,label,30,rotation))
 for label,y in [('VDD',1.4),('VSS',0)]:
  X,Y=pt(.475,y);s.append(on_shape(X,Y,label,34))
 for x,label,color in [(400,'M1',BLUE),(565,'M2',PURPLE),(730,'VIA1','#2E3440')]:
  s.append(f'<rect x="{x}" y="1172" width="26" height="26" fill="{color}"/>')
  txt(s,x+40,1198,label,'#000000',32)
 save(s,name+'_labeled')

# Keep the LEF pin-only view entirely vector, including labels and layer legend.
subprocess.run(['python3',str(P/'vector_abstract.py')],check=True)
