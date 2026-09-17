# build_layout.py -- run with klayout -b -r
import pya, json, re, os
from pathlib import Path
root=Path(os.environ.get('HOTPOT_ROOT',os.getcwd()))
out=root/'docs/slides/layout';out.mkdir(exist_ok=True)
pdk=Path(os.environ.get('NANGATE45_DIR','/home/kcaisley/Documents/libs/OpenROAD-flow-scripts/flow/platforms/nangate45'))
lib=pya.Layout();lib.read(str(pdk/'gds/NangateOpenCellLibrary.gds'))
l=pya.Layout();l.dbu=lib.dbu
top=l.create_cell('top'); cells={}
for name,x in [('NAND2_X1',0),('INV_X1',.57)]:
 c=l.create_cell(name);c.copy_tree(lib.cell(name));cells[name]=c
 top.insert(pya.CellInstArray(c.cell_index(),pya.Trans(int(round(x/l.dbu)),0)))
# Manual demonstration routing; via1_5 geometry from the technology LEF.
def box(layer,x0,y0,x1,y1):
 top.shapes(l.layer(layer,0)).insert(pya.DBox(x0,y0,x1,y1).to_itype(l.dbu))
def via(x,y):
 box(12,x-.035,y-.035,x+.035,y+.035)
 box(11,x-.035,y-.07,x+.035,y+.07)
 box(13,x-.07,y-.035,x+.07,y+.035)
routes={'in1':[(-.22,.91),(.4475,.91),(.4475,.63)],'in2':[(-.22,.595),(.1225,.595)],'wire1':[(.285,.46),(.6825,.46),(.6825,.595)],'out':[(.8475,1.12),(1.18,1.12)]}
for pts in routes.values():
 top.shapes(l.layer(13,0)).insert(pya.DPath([pya.DPoint(*xy) for xy in pts],.07).to_itype(l.dbu))
for xy in [(.4475,.63),(.1225,.595),(.285,.46),(.6825,.595),(.8475,1.12)]:via(*xy)
l.write(str(out/'nand_inv.gds'))
# Export each real master as its own GDS, without extra routes.
for name,c in cells.items():
 opt=pya.SaveLayoutOptions();opt.select_cell(c.cell_index());l.write(str(out/(name+'.gds')),opt)
# LEF abstract: keep only declared PORT polygons, excluding obstructions.
lef=(pdk/'lef/NangateOpenCellLibrary.macro.lef').read_text()
a=pya.Layout();a.dbu=l.dbu;at=a.create_cell('top_pins');pins={}
for name,dx in [('NAND2_X1',0),('INV_X1',.57)]:
 block=lef.split('MACRO '+name+'\n',1)[1].split('END '+name,1)[0]
 c=a.create_cell(name+'_pins');pins[name]={}
 for pin,body in re.findall(r'  PIN (\S+)\n(.*?)  END \1',block,re.S):
  shapes=[]
  for coords in re.findall(r'POLYGON\s+([\d.\s-]+);',body):
   f=list(map(float,coords.split()));xy=list(zip(f[::2],f[1::2]));shapes.append(xy)
   c.shapes(a.layer(11,0)).insert(pya.DPolygon([pya.DPoint(*pt) for pt in xy]).to_itype(a.dbu))
  pins[name][pin]=shapes
 at.insert(pya.CellInstArray(c.cell_index(),pya.Trans(round(dx/a.dbu),0)))
for layer in [11,12,13]:
 # Copy only top-level added routing/pads, not GDS cell internals.
 for sh in top.shapes(l.layer(layer,0)).each():at.shapes(a.layer(layer,0)).insert(sh)
a.write(str(out/'nand_inv_lef_pins.gds'))
# Basic geometric checks: vias land on intended LEF pins; routed nets do not touch.
intended=[('NAND2_X1','A1',0,.4475,.63),('NAND2_X1','A2',0,.1225,.595),('NAND2_X1','ZN',0,.285,.46),('INV_X1','A',.57,.6825,.595),('INV_X1','ZN',.57,.8475,1.12)]
for name,pin,dx,x,y in intended:
 region=pya.Region()
 for poly in pins[name][pin]:region.insert(pya.DPolygon([pya.DPoint(px+dx,py) for px,py in poly]).to_itype(l.dbu))
 cut=pya.Region(pya.DBox(x-.035,y-.035,x+.035,y+.035).to_itype(l.dbu))
 assert (cut-region).is_empty(),(name,pin,'via cut outside pin')
regions={}
for net,pts in routes.items():
 r=pya.Region(pya.DPath([pya.DPoint(*xy) for xy in pts],.07).to_itype(l.dbu).polygon())
 for x,y in pts:
  if x not in [-.22,1.18] and (x,y) in [(v[3],v[4]) for v in intended]:r.insert(pya.DBox(x-.07,y-.035,x+.07,y+.035).to_itype(l.dbu))
 regions[net]=r
for n,r in regions.items():
 for m,s in regions.items():
  if n<m:assert (r&s).is_empty(),(n,m,'short')
(out/'geometry.json').write_text(json.dumps({'dbu_um':l.dbu,'cells':{'inst1':{'master':'NAND2_X1','origin':[0,0],'size':[.57,1.4]},'inst2':{'master':'INV_X1','origin':[.57,0],'size':[.38,1.4]}},'routes_um':routes,'pins':pins},indent=2))
print('Created actual GDS masters, connected pair, and LEF pin abstract. Via landing and no M2 short checks passed.')
