"""Create a visual SG13G2 pad-ring example from IHP's public I/O GDS.

Run with KLayout, for example:
  klayout -b -r scripts/make_ihp_pad_ring.py \
    -rd io_gds=/path/to/sg13g2_io.gds \
    -rd output_gds=/path/to/IHP130-pad-ring-demo.gds

This is a placement demonstration, not a connected, DRC-checked tapeout.
"""

import pya


layout = pya.Layout()
layout.read(io_gds)
assert abs(layout.dbu - 0.001) < 1e-9, "Expected IHP SG13G2 1 nm DBU"

pad_names = [
    "sg13g2_IOPadVdd",
    "sg13g2_IOPadVss",
    "sg13g2_IOPadInOut4mA",
    "sg13g2_IOPadIn",
    "sg13g2_IOPadOut4mA",
    "sg13g2_IOPadAnalog",
    "sg13g2_IOPadIOVdd",
    "sg13g2_IOPadIOVss",
]
corner = layout.cell("sg13g2_Corner")
assert corner is not None
pads = [layout.cell(name) for name in pad_names]
assert all(pad is not None for pad in pads)

ring = layout.create_cell("IHP130_PAD_RING_DEMO")
pitch = 80000              # 80 um pad slots
corner_size = 180620       # IHP corner bounding box, in 1 nm DBU
edge = 2 * corner_size + len(pads) * pitch

for rotation, x, y in (
    (0, 0, 0),
    (1, edge, 0),
    (2, edge, edge),
    (3, 0, edge),
):
    ring.insert(pya.CellInstArray(corner.cell_index(), pya.Trans(rotation, False, x, y)))

for index, pad in enumerate(pads):
    offset = corner_size + index * pitch
    placements = (
        (0, offset, 0),
        (1, edge, offset),
        (2, edge - offset, edge),
        (3, 0, edge - offset),
    )
    for rotation, x, y in placements:
        ring.insert(pya.CellInstArray(pad.cell_index(), pya.Trans(rotation, False, x, y)))

options = pya.SaveLayoutOptions()
options.select_cell(ring.cell_index())
layout.write(output_gds, options)
print("Wrote", output_gds, "with 32 pads and four corners; bbox", ring.bbox())
