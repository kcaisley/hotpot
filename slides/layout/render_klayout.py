# render_klayout.py -- native KLayout image export; all coordinates in micrometers.
from pathlib import Path
import os
import pya
ROOT = Path(__file__).resolve().parent
TECH = Path(os.environ.get('NANGATE45_TECH', str(Path.home()/'Documents/asiclab/tech/nangate45')))
full = {1,2,3,4,5,9,10,11,12,13}
for name, file, bounds, layers in [
    ('nand_cell','NAND2_X1.gds',(-.15,-.15,.87,1.7),full),
    ('inv_cell','INV_X1.gds',(-.15,-.15,.68,1.7),full),
    ('pair_full','nand_inv.gds',(-.3,-.15,1.55,1.7),full),
    ('pair_metal','nand_inv.gds',(-.3,-.15,1.55,1.7),{11,12,13}),
    ('pair_pins','nand_inv_lef_pins.gds',(-.3,-.15,1.55,1.7),{11,12,13}),
]:
    view = pya.LayoutView()
    for key,value in {'background-color':'#ffffff','grid-visible':'false','text-visible':'false','cell-frame-visible':'false'}.items():view.set_config(key,value)
    view.load_layout(str(ROOT/file),False)
    view.load_layer_props(str(TECH/'nangate45.lyp'))
    view.max_hier()
    for lp in view.each_layer():lp.visible = lp.source_layer in layers and lp.source_datatype == 0
    x,y,w,h=bounds
    view.save_image_with_options(str(ROOT/(name+'.png')),round(w*1400),round(h*1400),1,2,1,pya.DBox(x,y,x+w,y+h),False)
    view.destroy()
    print('Rendered',name)
