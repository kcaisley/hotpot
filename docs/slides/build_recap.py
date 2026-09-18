"""Editable recap with grouped cell views, library imports and an OpenDB checkpoint.

cells.v carries functional models; design.v references their cell types.
Functional simulation models and hierarchy/DEF qualifications are in the notes.
"""
from pathlib import Path
import html
import subprocess
P = Path(__file__).resolve().parent
B,D,G,U = '#5E81AC','#4C566A','#A3BE8C','#B48EAD'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="850" viewBox="0 0 1920 850">',
   '<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7" fill="'+B+'"/></marker></defs>',
   '<rect width="1920" height="850" fill="white"/>']
def text(x,y,value,size=25,color=D,anchor='start',mono=False):
    family='DejaVu Sans Mono' if mono else 'Latin Modern Sans,sans-serif'
    s.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{html.escape(value)}</text>')
def path(d,arrow=False,color=B):
    marker=' marker-end="url(#arrow)"' if arrow else ''
    s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2"{marker}/>')
def bracket(x,X,y): path(f'M{x},{y+15} V{y} H{X} V{y+15}')
def rule(y): path(f'M1090,{y} H1545',color='#D8DEE9')

# Horizontal group brackets replace the loose headings.
text(130,31,'Authoritative',27,B,'middle')
text(130,61,'cell sources',27,B,'middle')
text(130,92,'Authored by hand or tool',20,D,'middle')
text(130,119,'Assumed to exist',20,D,'middle')
bracket(15,245,139)
text(712,80,'Derived cell views',29,B,'middle')
bracket(590,840,139)
text(1317,77,'flow.tcl (or flow.py)',29,U,'middle',True)
path('M1317,91 V134',True)

# GDS -> physical abstract.
text(25,225,'cells.gds',30,B,mono=True)
text(25,260,'GDSII · geometry',23)
text(415,194,'Abstract generator',25,B,'middle')
path('M218,217 H582',True)
text(415,253,'+ layer / pin definitions',22,D,'middle')
text(605,225,'cells.lef',30,B,mono=True)
text(605,260,'pins · outline · obstructions',22)
text(605,292,'+ technology LEF',23,U)
path('M811,217 H1056',True)
text(934,197,'read_lef',23,B,'middle',True)

# SPICE -> timing/power and logic views.
text(25,365,'cells.sp',30,B,mono=True)
text(25,400,'SPICE · devices',23)
text(415,334,'Cell characterizer',25,B,'middle')
path('M218,357 H582',True)
text(415,392,'+ models / PVT / loads',22,D,'middle')
text(605,365,'cells.lib',30,B,mono=True)
text(605,400,'timing · power',23)
path('M811,357 H1056',True)
text(934,337,'read_liberty',23,B,'middle',True)
path('M240,357 V497 H582',True)
text(415,474,'Logic extraction',25,B,'middle')
text(415,534,'transistor logic abstraction',21,D,'middle')
text(605,505,'cells.v',30,B,mono=True)
text(605,540,'logic primitives',23)
text(605,620,'design.v',30,B,mono=True)
text(605,655,'instances + nets',23)
# Cell-model/type relationship; only the structural design is read by OpenROAD.
# Behavioral cells.v models cannot be passed directly to its Verilog reader.
path('M720,553 V588',True)
text(739,578,'cell types',20,U)
path('M811,612 H1056',True)
text(934,591,'read_verilog',22,B,'middle',True)
text(934,644,'link_design -hier',20,B,'middle',True)
text(605,715,'design.sdc',27,B,mono=True)
path('M811,707 H1056',True)
text(934,687,'read_sdc',23,B,'middle',True)

# One P&R block; loading commands stay outside on their arrows.
s.append(f'<rect x="1065" y="140" width="505" height="600" fill="#F4F6F8" stroke="{B}" stroke-width="2"/>')
text(1317,179,'P&R engine (i.e. OpenROAD)',28,B,'middle')
text(1090,232,'OpenDB: dbTech + dbLib',25)
text(1090,268,'dbMaster · dbMTerm',24,G)
rule(306)
text(1090,359,'OpenSTA: LibertyLibrary',25)
text(1090,398,'LibertyCell · LibertyPort',23,G)
text(1090,429,'TimingArcSet · timing graph',23,G)
rule(461)
text(1090,540,'OpenDB: dbBlock',25)
text(1090,578,'dbInst · dbNet · dbITerm · dbBTerm',21,G)
text(1090,615,'dbModule · dbModInst',23,G)
text(1090,710,'OpenSTA: timing constraints',24)

# Exports: retained Verilog hierarchy; DEF describes one physical block.
text(1780,179,'Updated design',28,B,'middle')
path('M1571,306 H1732',True)
text(1652,282,'write_verilog',20,B,'middle',True)
text(1745,315,'design.v',27,B,mono=True)
text(1745,354,'hierarchical',24)
text(1745,384,'connectivity',24)
path('M1571,486 H1732',True)
text(1652,462,'write_def',20,B,'middle',True)
text(1745,495,'design.def',27,B,mono=True)
text(1745,534,'hierarchical',24)
text(1745,564,'instance names',23)
text(1745,595,'placement + routing',20)

# Explicit write and reload arrows at the bottom of the engine.
path('M1190,741 V793',True)
text(1175,777,'write_db',22,B,'end',True)
path('M1445,797 V745',True)
text(1460,777,'read_db',22,B,'start',True)
s.append(f'<rect x="1155" y="800" width="330" height="45" fill="#ECEFF4" stroke="{B}" stroke-width="1.5"/>')
text(1320,831,'design.odb',28,B,'middle',True)
s.append('</svg>')
out=P/'assets/recap.svg';out.write_text('\n'.join(s))
subprocess.run(['rsvg-convert','-f','pdf','-o',str(out.with_suffix('.pdf')),str(out)],check=True)
