"""Extract and render one genuine SG13G2 I/O pad for the finishing slides.

Run with: klayout -b -r slides/render_ihp_pad_detail.py
The standalone GDS is also written to Downloads for manual KLayout viewing.
"""

from pathlib import Path
import pya

slides = Path(__file__).resolve().parent
root = slides.parent
pdk = root.parent / "libs/OpenROAD-flow-scripts/flow/platforms/ihp-sg13g2"
source = pdk / "gds/sg13g2_io.gds"
layer_props = Path.home() / ".klayout/tech/sg13g2/sg13g2.lyp"
cell_name = "sg13g2_IOPadInOut4mA"
output_gds = root / "slides/layout/IHP130-IOPadInOut4mA.gds"
download_gds = Path.home() / "Downloads/IHP130-IOPadInOut4mA.gds"
output_png = root / "slides/images/finishing/IHP130-IOPadInOut4mA.png"
detail_png = root / "slides/images/finishing/IHP130-IOPadInOut4mA-detail.png"

library = pya.Layout()
library.read(str(source))
master = library.cell(cell_name)
if master is None:
    raise RuntimeError(f"{cell_name} is missing from {source}")

layout = pya.Layout()
layout.dbu = library.dbu
top = layout.create_cell(cell_name)
top.copy_tree(master)
options = pya.SaveLayoutOptions()
options.select_cell(top.cell_index())
layout.write(str(output_gds), options)
layout.write(str(download_gds), options)

view = pya.LayoutView()
for key, value in {
    "background-color": "#000000",
    "grid-visible": "false",
    "text-visible": "false",
    "cell-frame-visible": "false",
}.items():
    view.set_config(key, value)
view.load_layout(str(output_gds), False)
view.load_layer_props(str(layer_props))
view.max_hier()
for layer in view.each_layer():
    # Keep only physical mask geometry in the image.
    layer.visible = layer.source_datatype == 0
box = top.dbbox()
margin = max(box.width(), box.height()) * 0.035
area = box.enlarged(margin)
view.save_image_with_options(str(output_png), 1800, 1800, 1, 2, 1, area, False)
view.save_image_with_options(
    str(detail_png), 1600, 1600, 1, 2, 1, pya.DBox(-2, 65, 82, 149), False
)
view.destroy()
print(cell_name, "bbox", box, "GDS", output_gds, "PNG", output_png)
