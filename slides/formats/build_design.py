# build_design.py -- same two-cell placement/routing as layout/build_layout.py.
from pathlib import Path
import json
P=Path(__file__).resolve().parent;G=json.loads((P.parent/'layout/geometry.json').read_text())
lines=['# design.def','VERSION 5.8 ;','DIVIDERCHAR "/" ;','BUSBITCHARS "[]" ;','DESIGN design ;','UNITS DISTANCE MICRONS 2000 ;','DIEAREA ( -600 -400 ) ( 2600 3400 ) ;','ROW ROW_0 FreePDK45_38x28_10R_NP_162NW_34O 0 0 N DO 5 BY 1 STEP 380 0 ;','TRACKS Y 140 DO 10 STEP 280 LAYER metal1 ;','TRACKS X 190 DO 5 STEP 380 LAYER metal2 ;','COMPONENTS 2 ;','- inst1 NAND2_X1 + PLACED ( 0 0 ) N ;','- inst2 INV_X1 + PLACED ( 1140 0 ) N ;','END COMPONENTS','PINS 3 ;']
for pin,d,x,y in [('in1','INPUT',-440,1820),('in2','INPUT',-440,1190),('out','OUTPUT',2360,2240)]:
 lines += [f'- {pin} + NET {pin} + DIRECTION {d} + USE SIGNAL',f'  + LAYER metal2 ( -70 -70 ) ( 70 70 )',f'  + PLACED ( {x} {y} ) N ;']
lines += ['END PINS','SPECIALNETS 2 ;','- VDD ( inst1 VDD ) ( inst2 VDD ) + USE POWER','  + ROUTED metal1 340 ( 0 2800 ) ( 1900 2800 ) ;','- VSS ( inst1 VSS ) ( inst2 VSS ) + USE GROUND','  + ROUTED metal1 340 ( 0 0 ) ( 1900 0 ) ;','END SPECIALNETS','NETS 4 ;']
con={'in1':'( PIN in1 ) ( inst1 A1 )','in2':'( PIN in2 ) ( inst1 A2 )','wire1':'( inst1 ZN ) ( inst2 A )','out':'( inst2 ZN ) ( PIN out )'}
vias={'in1':[(.4475,.63)],'in2':[(.1225,.595)],'wire1':[(.285,.46),(.6825,.595)],'out':[(.8475,1.12)]}
for name,pts in G['routes_um'].items():
 xy=lambda pt:f'( {round(pt[0]*2000)} {round(pt[1]*2000)} )'
 lines += [f'- {name} {con[name]}','  + ROUTED metal2 '+' '.join(xy(pt) for pt in pts)]
 for v in vias[name]:lines += ['    NEW metal2 '+xy(v)+' via1_5']
 lines[-1]+=' ;'
lines+=['END NETS','END DESIGN'];(P/'design.def').write_text('\n'.join(lines)+'\n')
