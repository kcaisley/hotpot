# Workshop slides

`background.tex` is the editable Beamer source. `background.pdf` is the rendered
16-slide opening sequence. Build with `make -C docs/slides` from the repository
root. The first slide is the requested layout/flow overview; no extra cover is
inserted. The Nord colors, default Beamer headings, white canvas and lower-left
page numbers follow the Frida FSiC 2026 deck. Section navigation uses the
cumulative Nord progress dots from the August 2026 ADC characterization deck:
completed/current slides are filled and future slides are hollow. A Background title-page definition
is included in the source for later use.

Regenerate figures with `make -C docs/slides figures`, then rebuild the deck.
This needs Python 3, netlistsvg, librsvg (`rsvg-convert`), and TeX Live with
CircuitikZ. Normal slide builds use the checked-in figure PDFs and need only
LaTeX/latexmk. All code excerpts live in `examples/` and can be edited directly. Start every
code excerpt with its filename in a native comment: `// filename.v` for Verilog,
`* filename.sp` for SPICE, and `# filename.tcl` or `# filename.py` for Tcl/Python.
SPICE excerpts retain the actual Nangate45 CDL cell, node, device and model
names, PININFO/EQN comments, and W/L values. Device lines wrap using native
SPICE `+` continuation lines. Model cards remain external, as in the original
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

- Deck: `background.tex` + `extension_slides.tex`; 48 slides.
- Regenerate: `make extensions`, then `make` from this directory.
- `build_extension.py`: literal Nangate excerpts, exact LEF pin polygons, illustrative rows/tracks and straight arrows from right-side labels; SVG → vector PDF.
- `formats/build_top.py`: DEF from the existing GDS demonstration's placement/routing geometry.
- `formats/roundtrip.tcl`, `reload.tcl`: write and reload OpenDB; assert two instances, three BTerms and six nets.
- `formats/timing_session.tcl`: load Liberty + saved OpenDB + SDC; produce an actual STA report. No SPEF: wires are ideal for this check. An unrelated TAPCELL_X1 missing-master warning is expected.
- `simulation/inverter_test.sp`: isolated INV_X1, actual dimensions and nominal FreePDK45 cards; ngspice transient data.
- `simulation/plot_results.py`: waveforms, threshold measurements, cycle-energy integration and plots of the actual Liberty lookup table.
- `assets/loaded-inverter.tex`: CircuitikZ RC testbench illustration.
- `research/SOURCES.md`: lecture coverage, photo credits, model provenance and limitations.
- Sources/credits stay in linked footers; extended notes stay out of the slide body.
- LEF/DEF examples with omission comments are excerpts, not standalone complete files. Full `formats/top.def` is executable.
- Simulation illustrates timing/power definitions; it does not reproduce the characterization data.
