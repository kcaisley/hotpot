# build_extension.py -- reproducible Nangate45 file excerpts and teaching diagrams.
from pathlib import Path
import re, json, html, base64, mimetypes, subprocess, textwrap
from layout.label_positions import PIN_LABELS, on_shape
P=Path(__file__).resolve().parent;A=P/'assets/extension';E=P/'examples/extension'
A.mkdir(exist_ok=True);E.mkdir(exist_ok=True)
PDK=Path.home()/'Documents/libs/OpenROAD-flow-scripts/flow/platforms/nangate45'
lef=(PDK/'lef/NangateOpenCellLibrary.macro.lef').read_text();tech=(PDK/'lef/NangateOpenCellLibrary.tech.lef').read_text();lib=(PDK/'lib/NangateOpenCellLibrary_typical.lib').read_text()
def block(text,pattern):
 m=re.search(pattern,text);assert m,pattern
 start=m.start();b=text.index('{',m.start());level=1;i=b+1
 while level:
  level+=(text[i]=='{')-(text[i]=='}');i+=1
 return text[start:i]
inv=block(lib,r'\bcell\s*\(INV_X1\)\s*\{');nor=block(lib,r'\bcell\s*\(NAND2_X1\)\s*\{')
(E/'INV_X1.full.lib').write_text('/* INV_X1.full.lib — extracted cell group */\n'+inv+'\n')
(E/'NAND2_X1.full.lib').write_text('/* NAND2_X1.full.lib — extracted cell group */\n'+nor+'\n')
macro=lef.split('MACRO INV_X1\n')[1].split('END INV_X1')[0]
(E/'INV_X1.full.lef').write_text('# INV_X1.full.lef\nMACRO INV_X1\n'+macro+'END INV_X1\n')
def put(name,s):
 s=textwrap.dedent(s).strip()+'\n';(E/name).write_text(s);return s
sn={}
sn['lef_macro']=put('macro.lef','# NangateOpenCellLibrary.macro.lef\nMACRO INV_X1\n  CLASS core ;\n  FOREIGN INV_X1 0.0 0.0 ;\n  ORIGIN 0 0 ;\n  SYMMETRY X Y ;\n  SITE FreePDK45_38x28_10R_NP_162NW_34O ;\n  SIZE 0.38 BY 1.4 ;\n  # PIN groups omitted\nEND INV_X1')
sn['lef_signal']=put('signal_pin.lef','# NangateOpenCellLibrary.macro.lef\n# Within MACRO INV_X1\nPIN A\n  DIRECTION INPUT ;\n  ANTENNAGATEAREA 0.05225 ;\n  # Other antenna attributes omitted\n  PORT\n    LAYER metal1 ;\n    POLYGON 0.06 0.525 0.165 0.525\n            0.165 0.7 0.06 0.7 ;\n  END\nEND A')
sn['lef_power']=put('power_pin.lef','# NangateOpenCellLibrary.macro.lef\n# Within MACRO INV_X1\nPIN VDD\n  DIRECTION INOUT ;\n  USE power ;\n  SHAPE ABUTMENT ;\n  PORT\n    LAYER metal1 ;\n    POLYGON 0 1.315 0.04 1.315\n      0.04 0.975 0.11 0.975\n      0.11 1.315 0.38 1.315\n      0.38 1.485 0 1.485 ;\n  END\nEND VDD')
sn['lef_site']=put('site.lef','# NangateOpenCellLibrary.tech.lef\nUNITS\n  DATABASE MICRONS 2000 ;\nEND UNITS\nMANUFACTURINGGRID 0.0050 ;\n\nSITE FreePDK45_38x28_10R_NP_162NW_34O\n  SYMMETRY Y ;\n  CLASS core ;\n  SIZE 0.19 BY 1.4 ;\nEND FreePDK45_38x28_10R_NP_162NW_34O')
# Preserve exact tech SITE rather than assuming symmetry.
site=re.search(r'SITE FreePDK45_38x28_10R_NP_162NW_34O\n.*?END FreePDK45_38x28_10R_NP_162NW_34O',tech,re.S).group();sn['lef_site']=put('site.lef','# NangateOpenCellLibrary.tech.lef\nUNITS\n  DATABASE MICRONS 2000 ;\nEND UNITS\nMANUFACTURINGGRID 0.0050 ;\n\n'+site)
sn['lef_layer']=put('layer.lef','# NangateOpenCellLibrary.tech.lef\n'+re.search(r'LAYER metal1\n.*?END metal1',tech,re.S).group())
sn['lef_via']=put('via.lef','# NangateOpenCellLibrary.tech.lef\n'+re.search(r'VIA via1_5\b.*?END via1_5',tech,re.S).group())
deftext=(P/'formats/design.def').read_text()
sn['def_placement']=put('placement.def','# design.def\nDESIGN design ;\nUNITS DISTANCE MICRONS 2000 ;\nDIEAREA ( -600 -400 ) ( 2600 3400 ) ;\n\nCOMPONENTS 2 ;\n- inst1 NAND2_X1 + PLACED ( 0 0 ) N ;\n- inst2 INV_X1 + PLACED ( 1140 0 ) N ;\nEND COMPONENTS')
sn['def_rows']=put('rows.def','# design.def\nROW ROW_0\n  FreePDK45_38x28_10R_NP_162NW_34O\n  0 0 N\n  DO 5 BY 1\n  STEP 380 0 ;')
sn['def_tracks']=put('tracks.def','# design.def\nTRACKS Y 140\n  DO 10 STEP 280\n  LAYER metal1 ;\n\nTRACKS X 190\n  DO 5 STEP 380\n  LAYER metal2 ;')
sn['def_pins']=put('pins.def','# design.def\nPINS 3 ;\n- in1 + NET in1\n  + DIRECTION INPUT + USE SIGNAL\n  + LAYER metal2 ( -70 -70 ) ( 70 70 )\n  + PLACED ( -440 1820 ) N ;\n# in2 and out omitted\nEND PINS')
sn['def_nets']=put('nets.def','# design.def\nNETS 4 ;\n# Other nets omitted\n- wire1 ( inst1 ZN ) ( inst2 A )\n  + ROUTED metal2\n    ( 570 920 ) ( 1365 920 )\n    ( 1365 1190 )\n    NEW metal2 ( 570 920 ) via1_5\n    NEW metal2 ( 1365 1190 ) via1_5 ;\nEND NETS')
sn['def_power']=put('power.def','# design.def\nSPECIALNETS 2 ;\n- VDD ( inst1 VDD ) ( inst2 VDD )\n  + USE POWER\n  + ROUTED metal1 340\n    ( 0 2800 ) ( 1900 2800 ) ;\n- VSS ( inst1 VSS ) ( inst2 VSS )\n  + USE GROUND\n  + ROUTED metal1 340\n    ( 0 0 ) ( 1900 0 ) ;\nEND SPECIALNETS')
sn['lib_units']=put('units.lib','''/* NangateOpenCellLibrary_typical.lib */
library (NangateOpenCellLibrary) {
  delay_model : table_lookup;
  time_unit : "1ns";
  leakage_power_unit : "1nW";
  voltage_unit : "1V";
  current_unit : "1mA";
  capacitive_load_unit (1,ff);
  nom_process : 1.00;
  nom_temperature : 25.00;
  nom_voltage : 1.10;
  /* Other groups omitted */
}''')
sn['lib_pins']=put('inverter_pins.lib','''/* NangateOpenCellLibrary_typical.lib */
cell (INV_X1) {
  area : 0.532000;
  pin (A) {
    direction : input;
    capacitance : 1.700230;
  }
  pin (ZN) {
    direction : output;
    function : "!A";
    max_capacitance : 60.730000;
    /* Timing/power groups omitted */
  }
  /* Other attributes omitted */
}''')
sn['lib_supply']=put('inverter_supply.lib','/* NangateOpenCellLibrary_typical.lib */\n/* Within cell (INV_X1) */\n'+block(inv,r'pg_pin\s*\(VDD\)\s*\{')+'\n'+block(inv,r'pg_pin\s*\(VSS\)\s*\{')+'\n/* Within signal pins A and ZN */\nrelated_power_pin : "VDD";\nrelated_ground_pin : "VSS";')
sn['lib_threshold']=put('thresholds.lib','''/* NangateOpenCellLibrary_typical.lib */
input_threshold_pct_rise : 50.00;
input_threshold_pct_fall : 50.00;
output_threshold_pct_rise : 50.00;
output_threshold_pct_fall : 50.00;

slew_lower_threshold_pct_rise : 30.00;
slew_upper_threshold_pct_rise : 70.00;
slew_lower_threshold_pct_fall : 30.00;
slew_upper_threshold_pct_fall : 70.00;''')
sn['lib_arc']=put('inverter_arc.lib','''/* NangateOpenCellLibrary_typical.lib */
/* Within INV_X1 / pin (ZN) */
timing () {
  related_pin : "A";
  timing_sense : negative_unate;
  cell_fall (Timing_7_7) {
    /* 7 x 7 delay table */
  }
  cell_rise (Timing_7_7) {
    /* 7 x 7 delay table */
  }
  fall_transition (Timing_7_7) {
    /* 7 x 7 output slew table */
  }
  rise_transition (Timing_7_7) {
    /* 7 x 7 output slew table */
  }
}''')
sn['lib_template']=put('table_template.lib','/* NangateOpenCellLibrary_typical.lib */\n'+block(lib,r'lu_table_template\s*\(Timing_7_7\)\s*\{'))
sn['lib_power']=put('inverter_power.lib','''/* NangateOpenCellLibrary_typical.lib */
/* Within INV_X1 */
cell_leakage_power : 14.353185;
leakage_power () {
  when : "!A";
  value : 10.102224;
}
leakage_power () {
  when : "A";
  value : 18.604146;
}
/* Within pin (ZN) */
internal_power () {
  related_pin : "A";
  fall_power (Power_7_7) { /* omitted */ }
  rise_power (Power_7_7) { /* omitted */ }
}''')
# NOR source attributes and both related-pin arcs.
np=block(nor,r'pin\s*\(ZN\)\s*\{');print('NAND function:',re.search(r'function\s*:\s*"([^"]+)"',np)[1])
sn['lib_nand']=put('nand_arcs.lib','''/* NangateOpenCellLibrary_typical.lib */
/* Within cell (NAND2_X1) */
pin (A1) {
  capacitance : 1.599032;
  /* Other attributes omitted */
}
pin (A2) {
  capacitance : 1.664199;
  /* Other attributes omitted */
}
pin (ZN) {
  function : "!(A1 & A2)";
  timing () {
    related_pin : "A1";
    timing_sense : negative_unate;
    /* Tables omitted */
  }
  timing () {
    related_pin : "A2";
    timing_sense : negative_unate;
    /* Tables omitted */
  }
}''')
# Assert the displayed numeric attributes came from the actual source files.
assert '!(A1 & A2)' in nor
for v in ['1.599032','1.664199']:assert v in nor
B='#5E81AC';R='#BF616A';G='#A3BE8C';U='#B48EAD';D='#4C566A'
def text(x,y,t,size=24,c=D,anchor='start',mono=False):return f'<text x="{x}" y="{y}" font-family="{("DejaVu Sans Mono" if mono else "Latin Modern Sans, sans-serif")}" font-size="{size}" fill="{c}" text-anchor="{anchor}" xml:space="preserve">{html.escape(str(t))}</text>'
def rect(x,y,w,h,c,fill='none',dash=''):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{c}" stroke-width="2" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'
def line(x,y,xx,yy,c=B,w=2,dash=''):return f'<path d="M{x},{y} L{xx},{yy}" stroke="{c}" stroke-width="{w}" fill="none" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'
def arrow(x,y,xx,yy):return f'<path d="M{x},{y} C{x+55},{y} {xx-80},{yy} {xx},{yy}" stroke="{B}" stroke-width="2" fill="none" marker-end="url(#a)"/>'
def image(path,x,y,w,h):
 path=Path(path);mime=mimetypes.guess_type(str(path))[0] or 'image/svg+xml'
 data=path.read_bytes()
 if path.suffix=='.svg':
  import xml.etree.ElementTree as ET
  root=ET.fromstring(data)
  if 'viewBox' not in root.attrib:
   w0=root.get('width');h0=root.get('height');root.set('viewBox',f'0 0 {w0} {h0}')
   data=ET.tostring(root)
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{base64.b64encode(data).decode()}"/>'
def save(name,parts):
 s='<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="650" viewBox="0 0 1400 650"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="'+B+'"/></marker></defs><rect width="1400" height="650" fill="white"/>'+''.join(parts)+'</svg>'
 (A/(name+'.svg')).write_text(s);subprocess.run(['rsvg-convert','-f','pdf','-o',str(A/(name+'.pdf')),str(A/(name+'.svg'))],check=True)
def code(s,x=560,y=42,size=21,dy=25):
 return [text(x,y+i*dy,t,size,U if t.strip().startswith(('#','/*','*')) else D,mono=True) for i,t in enumerate(s.splitlines())]
def centered_left(parts):
 # Measure rendered ink, not the SVG's padded canvas, then center in the left half.
 from PIL import Image, ImageChops
 import io
 src='<svg xmlns="http://www.w3.org/2000/svg" width="650" height="650"><rect width="650" height="650" fill="white"/>'+''.join(parts)+'</svg>'
 png=subprocess.run(['rsvg-convert','-f','png'],input=src.encode(),stdout=subprocess.PIPE,check=True).stdout
 im=Image.open(io.BytesIO(png)).convert('RGB');bbox=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
 l,t,r,b=bbox;scale=min(1,510/(r-l),550/(b-t));dx=305-scale*(l+r)/2;dy=325-scale*(t+b)/2
 return ['<g transform="translate('+str(dx)+','+str(dy)+') scale('+str(scale)+')">'+''.join(parts)+'</g>']
def gate_view(filename,master):
 # Match the earlier 0.45-textwidth symbol slides. The format figure is height-limited
 # to 0.81 textheight; compensate for that small scale reduction (TeX dimensions).
 import xml.etree.ElementTree as ET
 root=ET.parse(P/'assets'/filename).getroot()
 w=0.45*398.3386/(0.81*227.62207/650)
 h=w*float(root.get('height'))/float(root.get('width'))
 y=(650-h-55)/2
 return [image(P/'assets'/filename,0,y,w,h),text(w/2,y+h+42,master,30,G,'middle')]
def cell(kind='plain'):
 # Real LEF polygons, uniform scale; no invented pin rectangles.
 scale=250;ox=190;oy=420
 o=[rect(ox,oy-1.4*scale,.38*scale,1.4*scale,D,dash='8 5'),text(237,40,'INV_X1',28,G,'middle')]
 for pin in ['A','ZN']+(['VDD','VSS'] if kind=='power' else []):
  group=re.search(r'\bPIN '+pin+r'\s.*?END '+pin+r'\b',macro,re.S).group()
  vals=list(map(float,re.search(r'POLYGON\s+([^;]+)',group)[1].split()))
  pts=[(ox+vals[i]*scale,oy-vals[i+1]*scale) for i in range(0,len(vals),2)]
  o.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="'+('#D8C8E5' if (kind=='signal' and pin=='A') or (kind=='power' and pin=='VDD') else '#E5E9F0')+'" stroke="'+B+'" stroke-width="2"/>')
 # Draw labels last and inside the same pin shapes as the GDS view.
 for pin,x,y,rotation in PIN_LABELS['INV_X1']:
  o.append(on_shape(ox+x*scale,oy-y*scale,pin,19,rotation))
 if kind=='power':
  for pin,y in [('VDD',1.4),('VSS',0)]:
   o.append(on_shape(ox+.19*scale,oy-y*scale,pin,22))
 o += [text(237,460,'0.38 µm',25,B,'middle'),text(80,180,'1.4 µm',23,B)]

 return o
def pair(mode='placement'):
 # Map the same 0.95 x 1.4 um core into a left-hand canvas.
 sx=330;sy=260;ox=100;oy=460
 xy=lambda x,y:(ox+sx*x,oy-sy*y)
 o=[rect(ox,oy-1.4*sy,.95*sx,1.4*sy,D,dash='7 4')]
 if mode=='placement':o += [rect(ox-.3*sx,oy-1.7*sy,1.6*sx,1.9*sy,B,dash='8 5'),text(10,550,'DIEAREA',22,B)]
 for x,w,name in [(0,.57,'inst1'),(.57,.38,'inst2')]:
  xx,yy=xy(x,1.4);o += [rect(xx,yy,w*sx,1.4*sy,G),text(xx+w*sx/2,yy-18,name,25,G,'middle')]
 if mode in ['rows','tracks']:
  for x in [i*.19 for i in range(6)]:
   xx,yy=xy(x,1.4);o.append(line(xx,yy,xx,oy,G,1,'4 5'))
  if mode=='tracks':
   for i in range(10):
    x,y=xy(0,.07+i*.14);o.append(line(x,y,x+.95*sx,y,B,1.5,'5 5'))
   for i in range(5):
    x,y=xy(.095+i*.19,0);o.append(line(x,y,x,y-1.4*sy,U,1.5,'5 5'))
  o += [text(255,510,'5 sites × 0.19 µm',24,G,'middle')]
 else:
  o += [text(ox,510,'(0, 0)',22,B),text(ox+.57*sx,545,'(0.57, 0) µm',22,B,'middle')]
 return o
for name,s in sn.items():
 if name.startswith('lef_'):
  d=cell('signal' if name=='lef_signal' else 'power' if name=='lef_power' else 'plain')
  if name=='lef_site':d=pair('rows')
  if name=='lef_layer':d=pair('tracks')
  if name=='lef_via':
   d=[rect(125,120,140,280,B,'#D8DEE9'),rect(55,190,280,140,U,'#E5DCEB'),rect(125,190,140,140,D,D),text(200,85,'via1_5',28,G,'middle'),text(200,440,'70 nm cut',26,D,'middle'),text(200,485,'M1 / VIA1 / M2',25,B,'middle')]
 elif name.startswith('def_'):
  if name in ['def_nets','def_power','def_pins']:
   focus={'def_pins':'in1','def_nets':'wire1','def_power':'VDD'}[name]
   d=[image(P/('layout/pair_pins_'+focus+'.svg'),10,0,470,550)]
  else:d=pair(name[4:])
 elif name=='lib_nand':
  d=gate_view('nand.svg','NAND2_X1')
 else:
  d=gate_view('inverter.svg','INV_X1')
 # Minimal curved callouts; point at the actual file attributes.
 calls={
 'lef_macro':[('master boundary',355,540,7),('placement symmetry',355,590,5)],
 'lef_signal':[('electrical role',290,540,3),('pin geometry',290,590,8)],
 'lef_power':[('power rail',290,545,4),('rail meets next cell',290,595,5)],
 'lef_site':[('database resolution',305,555,2),('placement site',305,605,9)],
 'lef_layer':[('preferred direction',315,555,6),('routing pitch',315,600,5)],
 'lef_via':[('three mask layers',300,575,2)],
 'def_placement':[],
 'def_rows':[('origin / orientation',310,555,3),('count / step',310,605,4)],
 'def_tracks':[('horizontal M1',305,555,1),('vertical M2',305,605,5)],
 'def_pins':[('block terminal',305,565,2),('shape / position',305,610,4)],
 'def_nets':[('two instance terminals',320,570,3),('route + via',320,610,7)],
 'def_power':[('power connectivity',305,565,2),('explicit wire width',305,610,4)],
 'lib_supply':[('supply identity',320,550,4),('signal-pin association',340,600,11)],
 'lib_arc':[('input-to-output arc',320,570,3)],
 'lib_pins':[('Boolean function',320,570,9)],
 'lib_threshold':[('delay: 50% → 50%',315,555,1),('slew: 30% → 70%',315,605,6)],
 'lib_nand':[('one timing group per input',350,620,13)]}
 # Fixed left image; code in the middle; labels to its right, horizontal arrows leftward.
 size=19;dy=25;xcode=700
 lines=s.expandtabs(2).splitlines()
 # Wrap long comma-separated table strings without changing their values.
 wrapped=[];line_map={}
 for i,t in enumerate(lines):
  line_map[i]=len(wrapped)
  if len(t)>56 and ',' in t and '"' in t:
   while len(t)>56:
    cut=t.rfind(',',0,54)
    if cut<0:break
    wrapped.append(t[:cut+1]+'\\');t='    '+t[cut+1:]
  wrapped.append(t)
 d=d if name.startswith('lib_') else centered_left(d)
 ycode=335-(len(wrapped)-1)*dy/2
 callouts=[]
 for label,x,y,idx in calls.get(name,[]):
  idx=min(idx,len(lines)-1);row=line_map[idx];target=wrapped[row]
  from PIL import ImageFont
  font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',size)
  end=xcode+font.getlength(target.rstrip())+3
  yy=ycode+row*dy-6
  assert end<1260,(name,target,end)
  labelx=end+65
  callouts += [text(labelx,yy+6,label,17.5,B),f'<path d="M{labelx-12},{yy} L{end},{yy}" stroke="{B}" stroke-width="2" fill="none" marker-end="url(#a)"/>']
 # Highlight the same object in the physical view and in the file excerpt.
 focus_rows={'lef_signal':[2,8,9],'lef_power':[2,4,8,9,10,11],
             'def_pins':[2,3,4,5],'def_nets':[3,4,5,6,7,8],
             'def_power':[2,3,4,5],'def_placement':[6,7]}.get(name,[])
 for idx in focus_rows:
  if idx>=len(lines):continue
  row=line_map[idx]
  from PIL import ImageFont
  f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',size)
  width=f.getlength(wrapped[row])+8
  d.append(rect(xcode-4,ycode+row*dy-19,width,24,'none','#EAE3F0'))
 save(name,d+code('\n'.join(wrapped),x=xcode,y=ycode,size=size,dy=dy)+callouts)
# Actual 7x7 table as both plot and selected source rows. No fabricated table data.
b=block(inv,r'cell_fall\s*\(Timing_7_7\)\s*\{');indexes=[list(map(float,re.search(r'index_'+str(i)+r'\s*\("([^"]+)"',b)[1].split(','))) for i in [1,2]]
values=[list(map(float,v.split(','))) for v in re.findall(r'"([\d.,eE+-]+)"',b)[2:]]
(A/'timing_table.json').write_text(json.dumps({'input_slew_ns':indexes[0],'load_ff':indexes[1],'cell_fall_ns':values},indent=2))
# These are literal first-row values, wrapped with a legal string continuation.
put('cell_fall.lib','/* NangateOpenCellLibrary_typical.lib */\ncell_fall (Timing_7_7) {\n  index_1 ("0.00117378,0.00472397,0.0171859,\\\n            0.0409838,0.0780596,0.130081,0.198535");\n  index_2 ("0.365616,1.897810,3.795620,7.591250,\\\n            15.182500,30.365000,60.730000");\n  /* First row; other six rows omitted */\n  values ("0.00334769,0.00529785,0.00763425,\\\n           0.0122592,0.0214710,0.0398747,0.0766650");\n}')
# Database relationship, with names that avoid confusing Synopsys .db and OpenDB .odb.
def boxlabel(x,y,w,h,label,sub=''):
 return [rect(x,y,w,h,B,'#ECEFF4'),text(x+w/2,y+h/2,label,34,B,'middle'),text(x+w/2,y+h/2+40,sub,22,D,'middle')]
s=boxlabel(30,130,330,170,'LEF + DEF','plaintext interchange')+boxlabel(530,130,340,170,'OpenDB','objects in memory')+boxlabel(1040,130,330,170,'design.odb','binary serialization')
s += [arrow(365,210,525,210),arrow(875,190,1035,190),line(1040,260,875,260,B),text(444,180,'read',22,B,'middle'),text(956,155,'write_db',22,B,'middle'),text(956,288,'read_db',22,B,'middle')]
s += code('# roundtrip.tcl\nread_lef NangateOpenCellLibrary.tech.lef\nread_lef NangateOpenCellLibrary.macro.lef\nread_def design.def\nwrite_db design.odb',x=260,y=410,size=25,dy=34)
s += [text(700,620,'dbMaster · dbInst · dbITerm · dbBTerm · dbNet',27,G,'middle')];save('odb',s)
s=boxlabel(100,120,400,180,'Liberty .lib','portable text')+boxlabel(900,120,400,180,'OpenSTA','timing graph in memory')
s += [f'<path d="M500,210 L900,210" stroke="{B}" stroke-width="2" fill="none" marker-end="url(#a)"/>',text(700,175,'read_liberty',25,B,'middle')]
s += code('# timing_session.tcl\nread_liberty NangateOpenCellLibrary_typical.lib\nread_db design.odb\nread_sdc design.sdc\n# read_spef design.spef  (when extracted)',x=260,y=400,size=24,dy=31)
s += [text(700,600,'OpenSTA reads .lib directly; .odb does not replace it.',25,B,'middle')];save('timing_database',s)
# Timing model families are not three incompatible file-format versions.
s=[]
for x,title,sub in [(20,'NLDM','delay / slew tables'),(480,'CCS / ECSM','current-waveform models'),(940,'LVF','variation statistics')]:s+=boxlabel(x,100,420,150,title,sub)
s += [text(220,315,'Nangate45 example',28,G,'middle'),text(690,315,'richer waveform behavior',25,D,'middle'),text(1150,315,'added to timing models',25,D,'middle')]
s += [text(230,420,'delay_model : table_lookup;',21,D,'middle',True),text(230,468,'cell_rise / cell_fall',21,D,'middle',True),text(690,420,'output_current_rise',21,D,'middle',True),text(690,468,'output_current_fall',21,D,'middle',True),text(1150,420,'ocv_sigma_cell_rise',21,D,'middle',True),text(1150,468,'ocv_sigma_cell_fall',21,D,'middle',True),text(700,580,'Model families and extensions can coexist in one library',28,B,'middle')];save('liberty_models',s)
print('Wrote',len(sn),'annotated source excerpts')

parts=gate_view('inverter.svg','INV_X1')
parts+=code((E/'cell_fall.lib').read_text(),x=620,y=42,size=19,dy=25)
# Chart occupies its own area below the excerpt; generated by plot_results.py.
chart=A/'liberty_table.svg'
if chart.exists():parts+=[image(chart,640,340,700,300)]
save('lib_table',parts)
