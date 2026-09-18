# Workshop slides

The editable Beamer decks share `slide_style.tex`:

| Deck | PDF | Contents |
| --- | --- | --- |
| `intro.tex` | `intro.pdf` | 3 slides: cover, plan and logistics |
| `filetypes.tex` | `filetypes.pdf` | 29 slides, ending with **To recap** |
| `def.tex` | `def.pdf` | 6 slides, former background slides 24–29 |
| `lib.tex` | `lib.pdf` | 9 slides, former background slides 36–44 |

`make -C docs/slides` builds all four PDFs; individual targets also work.
The split refers to the 46-slide version before this edit. The former database
summary slides 30 and 46 are replaced by the recap. The remaining background
extension is in `extension_slides.tex`. No extra cover slides are inserted.
Nord colors, Latin Modern fonts, white canvas, linked source footers and
cumulative section progress dots are shared by all four decks.

Regenerate figures with `make -C docs/slides figures`, then rebuild the deck.
This needs Python 3, netlistsvg, librsvg (`rsvg-convert`), and TeX Live with
CircuitikZ. Normal slide builds use the checked-in figure PDFs and need only
LaTeX/latexmk. All code excerpts live in `examples/` and can be edited directly. Start every
code excerpt with its filename in a native comment: `// filename.v` for Verilog,
`* filename.sp` for SPICE, and `# filename.tcl` or `# filename.py` for Tcl/Python.
SPICE excerpts retain the actual Nangate45 CDL cell, node, device and model
names, PININFO/EQN comments, and W/L values. Device statements use one line each, with compact W/L values. Model cards remain external, as in the original
library; these excerpts are not standalone simulation decks.

## Figure sources

- Finished layout: `../../images/design.png` from this workshop repository.
- OpenROAD flow image: `assets/openroad-flow.png`, copied from the Frida reference
  `docs/images/orfs.png`, depicting the main OpenROAD README flow diagram:
  https://github.com/The-OpenROAD-Project/OpenROAD . This image retains its
  original colors. The workshop starts after synthesis.
- Logic symbols: netlistsvg digital skin, adapted to Nord colors. Its MIT license
  is included as `assets/netlistsvg-LICENSE`.
  https://github.com/nturley/netlistsvg
- `build_digital.py` creates small explicit Yosys-format JSON graphs and renders
  them with netlistsvg. These preserve the teaching structure without synthesis
  optimization. Connectivity agrees with `examples/*.v`.
- `annotate_top.py` extracts the actual generated NAND/inverter paths, arranges
  them on a teaching canvas, and adds wires, boundary and terminal markers.
  It writes the plain detailed view and an identical view with Nord OpenDB
  callout arrows. `dbMaster` points to the type label, `dbInst` to its usage name. Instance names and the block name/label are Nord
green; OpenDB annotations and arrows are Nord blue.
- CMOS figures: original editable CircuitikZ sources `assets/*-cmos.tex`.
  Connectivity follows INV_X1 and NAND2_X1 in the Nangate45 CDL library, with
  the original cell, pin, device and model names and transistor dimensions:
  https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/platforms/nangate45/cdl/NangateOpenCellLibrary.cdl
- OpenDB object meanings:
  https://openroad.readthedocs.io/en/latest/main/src/odb/README.html
  and https://github.com/The-OpenROAD-Project/OpenROAD/blob/master/src/odb/include/odb/db.h

The instructional sequence was inspired by Austin Rovinski's Circuit Taxonomy
lecture (https://www.youtube.com/watch?v=bRUf6BLq1V0). No professor slide images
are embedded or cropped into this deck. Source context and technical distinctions
are included in Beamer speaker notes (`\note{...}`).

## Next sections

The physical-view sequence now follows the connectivity slides: separate
annotated Nangate45 cells, the connected GDS layout, a metal-only view, and the
LEF pin view. See `layout/README.md` for native KLayout rendering and geometry details.
Continue with file formats, saved OpenDB databases and functional/timing/power
representations. The separate
Floorplanning presentation has not been started.

The overview includes a foundry world map (`make -C docs/slides fabs`), with source credits in `assets/fabs/SOURCES.md`. The physical section opens with Cepheiden’s credited CMOS/SOI cross-section illustration.

## File formats, timing and power extension

- Decks: `intro.tex`, `filetypes.tex` + `extension_slides.tex`, `def.tex`, and `lib.tex`.
- Regenerate: `make extensions`, then `make` from this directory.
- `build_extension.py`: literal Nangate excerpts, exact LEF pin polygons, illustrative rows/tracks and straight arrows from right-side labels; SVG → vector PDF.
- `formats/build_design.py`: DEF from the existing GDS demonstration's placement/routing geometry.
- `formats/roundtrip.tcl`, `reload.tcl`: write and reload OpenDB; assert two instances, three BTerms and six nets.
- `formats/timing_session.tcl`: load Liberty + saved OpenDB + SDC; produce an actual STA report. No SPEF: wires are ideal for this check. An unrelated TAPCELL_X1 missing-master warning is expected.
- `simulation/inverter_test.sp`: isolated INV_X1, actual dimensions and nominal FreePDK45 cards; ngspice transient data.
- `simulation/plot_results.py`: waveforms, threshold measurements, cycle-energy integration and plots of the actual Liberty lookup table.
- `assets/loaded-inverter.tex`: CircuitikZ RC testbench illustration.
- `research/SOURCES.md`: lecture coverage, photo credits, model provenance and limitations.
- Sources/credits stay in linked footers; extended notes stay out of the slide body.
- LEF/DEF examples with omission comments are excerpts, not standalone complete files. Full `formats/design.def` is executable.
- Simulation illustrates timing/power definitions; it does not reproduce the characterization data.

## Overview and linked physical examples

- `make overview`: regenerate the horizontal input → implementation → output diagram (`build_overview.py`).
- Former slides 1–3 are now a single overview; later slide numbers are two lower.
- `layout/vector_abstract.py`: exact LEF polygons, M2 routes and VIA1 cuts rendered directly as SVG/PDF; no raster layer in the pin-only figures.
- Highlighted variants select in1, wire1 or VDD; the corresponding file rows receive the same highlight.
- `examples/*-slide.sp`: display-only // comments; native simulation decks retain valid * comments. Pin identifiers are blue and MOS instance identifiers green.
- CMOS cross-section uses the original English material legend.

## Recap and design filenames

- `make recap`: regenerate `assets/recap.svg` and its vector PDF.
- `build_recap.py`: original source → derived library → P&R data-flow diagram.
- One P&R block on the recap; plaintext outputs `design.v` and `design.def`; OpenDB checkpoint `design.odb`.
- `cells.v` denotes cell functional models; `design.v` denotes instantiated connectivity.
- `formats/recap_import.tcl`: executable LEF/Liberty/Verilog import check; two instances, three ports, four signal nets; hierarchical linking enabled. Behavioral cells.v models are for simulation, not this reader.
- `formats/roundtrip.tcl`: physical DEF import, binary checkpoint and DEF/Verilog export.
- `examples/design.v` and `formats/design.{def,odb,sdc}` use the same design name.
- Technology LEF, device models and characterization settings remain additional inputs.
- Recap labels actual OpenDB and OpenSTA objects; detailed source links and qualifications are in speaker notes and `research/SOURCES.md`.

Background sections: Intro; Connectivity (Netlists and Verilog); Physical (GDS, LEF, DEF); Timing and Power (Liberty); Recap. Navigation uses the short section names to keep the progress dots readable.

## Two opening views and regenerated CTS

- Page 1: Day 1 libraries, formats, OpenROAD, floorplanning; Day 2 global/detailed placement and CTS; Day 3 global/detailed routing and finishing.
- Page 2: the same seven stages inside a dotted OpenROAD boundary, official logo, file icons and design.v/design.def outputs; no commands or schedule.
- `make stages`: native OpenROAD screenshots from `results/*.odb` using `render_stages.tcl`; image bounds are taken from the actual die.
- `build_cts_view.py`: readable vector clock fly-lines from exact post-CTS pin coordinates. Five buffers, six clock nets, 43 connections; no invented routing.
- `make overview recap`: regenerate the two opening figures and the final recap; `make`: rebuild the PDFs.
- `assets/stages/`: native snapshots, rendering logs, exact CTS geometry TSV, vector CTS view.
- `examples/cells.v`: functional INV_X1/NAND2_X1 primitives for simulation. OpenROAD's structural reader rejects these Boolean expressions; loading empty stubs instead also shadows the Liberty cells. The recap's cells.v → design.v arrow denotes the referenced cell types.
- `link_design -hier` enables retained module hierarchy in the local development build. The Verilog output can preserve it; DEF exports a physical block with master instances rather than nested RTL hierarchy.
- Detailed-routing and finishing images share the saved final routed checkpoint; filler visibility distinguishes them because no separate pre-filler ODB was saved.

## Schedule spacing and final GDS thumbnail

- The schedule starts with an input block: Cell library / Design files / Flow script.
- Eight blocks share width 180, height 104 and a 40-unit gap; seven arrow gaps are identical.
- No extra text below Day 1 or below the schedule.
- `make finishing`: run the upstream ORFS `flow/util/def2stream.py` with the actual final DEF, the same LEFs as the workshop, and `NangateOpenCellLibrary.gds`.
- Output: `assets/stages/design.gds` (top cell `gcd`). Stream-out uses ORFS's physical layer map in a generated local `.lyt`; it does not alter the installed technology.
- `render_finished_layout.py` opens the merged GDS in native KLayout and loads `~/Documents/asiclab/tech/nangate45/nangate45.lyp` unchanged. Both opening slides use `finishing_klayout.png`.
- Validation: no missing/empty/orphan cells; every DEF component master count matches the merged GDS. Summary in `assets/stages/streamout-validation.json`.
- Rebuild all opening assets: `make stages finishing overview`, then `make`.

## File overview revision

- Library file order: cells.v, cells.lef, tech.lef, cells.lib.
- Lower-left input: flow.tcl / flow.py; one combined design.v / design.def output icon.
- CTS and OpenROAD logo SVGs are inlined as vector geometry, avoiding low-resolution bitmap conversion during PDF export. Native layout PNGs retain their original resolution.

## Physical views and source footers

- GDS introduction and separate-cell layouts share one slide; background now has 30 slides.
- `layout/label_positions.py` defines shared, cell-local pin anchors for GDS and LEF. Black on-shape labels avoid dark via cuts; narrow ZN fingers use rotated labels.
- Rebuild annotations: `python3 layout/annotate_layout.py`, then `python3 build_extension.py`, then `make`.
- `slide_style.tex` right-aligns sources and supplies “Sources:” automatically. Pass only short, dot-separated hyperlinks to `\slidesource{...}`.
- Library citations point to individual upstream files; DMC65 links to the SiLab group site. Full attribution remains in notes and `research/SOURCES.md`.

## Intro and file-types split

- `intro.tex`: logistics and workshop day-by-day flow, with the Arithmeum photograph.
- `filetypes.tex`: remaining 29 slides from the former background deck.
- Monday: cell libraries, formats, floorplanning; Tuesday: placement and timing; Wednesday: global/detailed routing, finishing and fabrication.
- Build individually with `make intro.pdf` or `make filetypes.pdf`, or run `make` for all four decks.

- Intro exception: no section navigation or visible source footer; keep page numbers and source attribution in notes. Order: cover, The plan, logistics.

## Overview image clarity

- `build_stage_vectors.py` draws exact OpenDB row and placed-cell boundaries exported by `render_stages.tcl`; it omits microscopic pin patterns for legibility.
- Floorplan, global placement, detailed placement and CTS are inlined vectors in both overview PDFs. Routing and final KLayout images retain their full raster resolution.
- The final GDS contains 671 FILLCELL instances, matching the DEF. Fillers provide wells/implants and power rails, without transistor gates. The renderer records the per-master counts in `streamout-validation.json`.
- Cover subtitle and emphasized HOTPOT initials match the root `poster.tex`.
