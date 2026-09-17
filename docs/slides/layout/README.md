# Nangate45 physical-view figures

The source masters are `NAND2_X1` (0.57 × 1.40 µm) and `INV_X1`
(0.38 × 1.40 µm), copied without alteration from the Nangate45 GDS library.
`nand_inv.gds` places inst1 at (0, 0) and inst2 at (0.57, 0), in µm.
The shared M1 VDD and VSS rails abut.

`build_layout.py` adds hand-authored M2 signal routes and VIA1 connections:

- `in1` connects to NAND2_X1/A1.
- `in2` connects to NAND2_X1/A2.
- `wire1` connects NAND2_X1/ZN to INV_X1/A.
- `out` connects to INV_X1/ZN.

The vias use the exact `via1_5` rectangles in the technology LEF: a 70 nm
square cut, 70 × 140 nm M1 enclosure, and 140 × 70 nm M2 enclosure.
M2 strips are 70 nm wide. The script checks via cuts against the intended
LEF PORT polygons and checks that distinct added M2 nets do not intersect.
This manually assembled illustration has not undergone full DRC/LVS signoff.
The external net labels are annotations, not OpenDB BTerm objects.

## Rendering

KLayout renders GDS directly through `render_klayout.py`, using the shared Nord
layer properties in `~/Documents/asiclab/tech/nangate45/nangate45.lyp`.
`NANGATE45_TECH` can override this directory. Fixed export bounds preserve
alignment with vector pin labels, instance labels and placement boundaries.
Nord colors are visualization choices, not material colors.
GDS well/implant shapes naturally extend beyond those placement boundaries.

- `nand_cell_labeled.pdf`, `inv_cell_labeled.pdf`: separate unconnected GDS cells.
- `pair_full_labeled.pdf`: every physical mask layer present in the cells,
  plus the added M2 and VIA1 geometry. Original GDS text/marker layers are hidden.
- `pair_metal_labeled.pdf`: the same GDS, showing only M1, M2 and VIA1.
- `pair_pins_labeled.pdf`: actual LEF PORT polygons plus the same added routes.
  This intentionally excludes obstructions; it is a pin view, not a complete LEF
  abstract. Most of these simple cells' M1 geometry is also declared as pins,
  explaining the similarity to the filtered GDS view.

The small extracted GDS files are supplied for inspection in KLayout, alongside
an exact `geometry.json` record of placement, routing, and source pin polygons.

## Reproduce

From the repository root, with KLayout, Python 3 and librsvg installed:

```sh
make -C docs/slides layouts
make -C docs/slides
klayout -n nangate45 docs/slides/layout/nand_inv.gds
```

The local KLayout technology links to `~/Documents/asiclab/tech/nangate45`.
Select its entry under Tools → 2.5d View for the stack visualization.
Metal elevations follow technology LEF HEIGHT/THICKNESS values; FEOL elevations
are illustrative. See the technology directory's README and `stack.csv`.

`NANGATE45_DIR` can point to another ORFS Nangate45 library directory.
The default is the existing local copy under `~/Documents/libs`.
Source library files are never modified.

Source: https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/tree/master/flow/platforms/nangate45

The source library notice is retained in `Nangate45-LICENSE`.
