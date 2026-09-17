# build_fabs.py -- original map composition from attributed source assets.
from pathlib import Path
import base64, mimetypes, subprocess
P=Path(__file__).resolve().parent/'assets/fabs'
def img(file,x,y,w,h):
 data=(P/file).read_bytes();mime=mimetypes.guess_type(file)[0] or 'image/svg+xml'
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{base64.b64encode(data).decode()}"/>'
# Original map is Robinson, centered 10 E. City-scale markers, not parcel boundaries.
world=(P/'world.svg').read_text().replace('#c0c0c0','#D8DEE9')
(P/'world-nord.svg').write_text(world)
s=['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1400" height="650" viewBox="0 0 1400 650">','<rect width="1400" height="650" fill="white"/>',img('world-nord.svg',300,-12,800,406)]
# Locations calibrated to the source map projection, rounded at this world-map scale.
for (mx,my),end,ctrl in [((665,310),230,270),((1406,251),700,700),((2094,685),1170,1130)]:
 x=300+mx*800/2754;y=-12+my*406/1398
 s += [f'<path d="M {x} {y} C {ctrl} {y+40}, {end} 285, {end} 342" fill="none" stroke="#5E81AC" stroke-width="3"/>',f'<circle cx="{x}" cy="{y}" r="7" fill="#5E81AC" stroke="white" stroke-width="3"/>']
for x,logo,photo,pdk,place in [(20,'skywater-logo.svg','skywater-site.jpg','SKY130 · 130 nm CMOS','Bloomington, Minnesota, USA'),(490,'ihp-logo.svg','ihp-site.jpg','IHP SG13G2 · 130 nm BiCMOS','Frankfurt (Oder), Germany'),(960,'gf-logo.svg','gf-site.webp','GF180MCU · 180 nm CMOS','Singapore')]:
 s += [img(logo,x+75,346,270,51),img(photo,x,410,420,186),f'<text x="{x+210}" y="620" text-anchor="middle" font-family="Latin Modern Sans, sans-serif" font-size="24" fill="#5E81AC">{pdk}</text>',f'<text x="{x+210}" y="647" text-anchor="middle" font-family="Latin Modern Sans, sans-serif" font-size="22" fill="#4C566A">{place}</text>']
s.append('</svg>');(P/'fabs-map.svg').write_text('\n'.join(s))
subprocess.run(['rsvg-convert','-f','pdf','-o',str(P/'fabs-map.pdf'),str(P/'fabs-map.svg')],check=True)
