# KLayout batch export of two unmodified Nangate45 filler masters.
from pathlib import Path
import os
import pya

root = Path(__file__).resolve().parents[2]
out = root / 'slides' / 'images' / 'placement'
out.mkdir(parents=True, exist_ok=True)
pdk = Path(os.environ.get(
    'NANGATE45_DIR',
    '/home/kcaisley/Documents/libs/OpenROAD-flow-scripts/flow/platforms/nangate45'))
tech = Path(os.environ.get(
    'NANGATE45_TECH',
    '/home/kcaisley/Documents/asiclab/tech/nangate45'))
lib = pya.Layout()
lib.read(str(pdk / 'gds' / 'NangateOpenCellLibrary.gds'))

for name in ('FILLCELL_X1', 'FILLCELL_X4'):
    master = lib.cell(name)
    if master is None:
        raise RuntimeError(f'Missing GDS master: {name}')
    layout = pya.Layout()
    layout.dbu = lib.dbu
    cell = layout.create_cell(name)
    cell.copy_tree(master)
    gds = out / f'{name}.gds'
    options = pya.SaveLayoutOptions()
    options.select_cell(cell.cell_index())
    layout.write(str(gds), options)

    view = pya.LayoutView()
    for key, value in {
        'background-color': '#ffffff',
        'grid-visible': 'false',
        'text-visible': 'false',
        'cell-frame-visible': 'false',
    }.items():
        view.set_config(key, value)
    view.load_layout(str(gds), False)
    view.load_layer_props(str(tech / 'nangate45.lyp'))
    view.max_hier()
    for layer in view.each_layer():
        layer.visible = layer.source_layer in {1, 2, 3, 4, 5, 9, 10, 11, 12, 13} and layer.source_datatype == 0
    box = cell.bbox()
    margin = round(0.12 / layout.dbu)
    area = pya.DBox(
        (box.left - margin) * layout.dbu,
        (box.bottom - margin) * layout.dbu,
        (box.right + margin) * layout.dbu,
        (box.top + margin) * layout.dbu,
    )
    width = max(900, round(area.width() * 1400))
    height = max(900, round(area.height() * 1400))
    png = out / f'{name}.png'
    view.save_image_with_options(str(png), width, height, 1, 2, 1, area, False)
    view.destroy()
    print(name, box, png)
