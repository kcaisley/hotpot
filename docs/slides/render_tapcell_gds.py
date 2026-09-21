"""Render the Nangate45 TAPCELL_X1 master from its GDS in KLayout."""
from pathlib import Path
import os
import pya

here = Path(__file__).resolve().parent
platform = Path(os.environ.get('NANGATE45_PLATFORM', '/home/kcaisley/Documents/libs/OpenROAD-flow-scripts/flow/platforms/nangate45'))
style = Path(os.environ.get('NANGATE45_TECH', '/home/kcaisley/Documents/asiclab/tech/nangate45')) / 'nangate45.lyp'
output = here / 'assets/floorplanning/tapcell_gds.png'
temporary = here / 'build/floorplanning/tapcell_only.gds'
temporary.parent.mkdir(parents=True, exist_ok=True)

layout = pya.Layout()
layout.read(str(platform / 'gds/NangateOpenCellLibrary.gds'))
cell = layout.cell('TAPCELL_X1')
assert cell is not None, 'Nangate45 GDS has no TAPCELL_X1 master'
options = pya.SaveLayoutOptions()
options.select_cell(cell.cell_index())
layout.write(str(temporary), options)

view = pya.LayoutView()
for key, value in {'background-color': '#ffffff', 'grid-visible': 'false',
                   'text-visible': 'false', 'cell-frame-visible': 'false'}.items():
    view.set_config(key, value)
view.load_layout(str(temporary), False)
view.load_layer_props(str(style))
view.max_hier()
for layer in view.each_layer():
    layer.visible = 1 <= layer.source_layer <= 29 and layer.source_datatype == 0
view.save_image_with_options(str(output), 700, 1600, 1, 2, 1,
                             pya.DBox(-0.1, -0.12, 0.29, 1.52), False)
view.destroy()
print(output)
