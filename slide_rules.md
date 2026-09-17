- **Format:** LaTeX Beamer; 16:9; white background; match Frida docs templates.
- **Fonts:** Latin Modern; Beamer sans for titles/body; monospace for code; code 10 pt / 13 pt leading.
- **Colors:** body `#4C566A`; blue `#5E81AC`; red `#BF616A`; purple `#B48EAD`; green `#A3BE8C`; panel `#ECEFF4`.
- **Titles:** blue, top-left; short, sentence case; cover uses the existing title/author/institute/date definition.
- **Navigation:** cumulative section dots; past/current filled, future hollow; slide count bottom-left.
- **Content:** one idea per slide; large diagrams; minimal text; no prose walls.
- **Slide types:** overview images; checklist; expanded checklist; diagram/code pair; detailed diagram; annotated repeat; physical-layer comparison.
- **Pairs:** diagram left, code right; align vertically; preserve readable code size.
- **Repeats:** keep geometry, scale and framing fixed; add only the next teaching layer.
- **Labels:** instances and block names green; pins red; nets purple; OpenDB callouts blue.
- **Arrows:** smooth cubic Bézier curves, blue arrowheads; avoid elbow bends and label crossings.
- **Code:** editable files in `docs/slides/examples/`; first line is a native filename comment: `// inverter.v`, `* inverter.sp`, `# flow.tcl`, `# build.py`.
- **Names:** retain Nangate45 cell/pin/device/model names and W/L; distinguish masters from instances.
- **SPICE:** preserve terminal order and bulk connections; wrap with `+`; external models stay external.
- **Logic:** `build_digital.py` creates explicit Yosys JSON and renders with the Nord netlistsvg skin; preserve the NAND→INV teaching structure.
- **SVG:** edit generators, not generated paths; `annotate_top.py` adds boundaries, terminals, labels and curved OpenDB arrows.
- **Transistors:** edit `assets/*-cmos.tex`; use CircuitikZ; verify wiring against source CDL; compile to vector PDF.
- **Layouts:** preserve source GDS masters; `layout/build_layout.py` adds placements, M2 routes and VIA1; label real LEF pin polygons.
- **Rendering:** use native KLayout via `layout/render_klayout.py`; fixed bounds; Nord `.lyp`; no ArtistIC dependency.
- **Views:** separate annotated cells → connected full layers → M1/M2/VIA1 → LEF pins.
- **Technology:** `~/Documents/asiclab/tech/nangate45`; registered at `~/.klayout/tech/nangate45`; 2.5D script under `d25/`.
- **Stack:** metal elevations from technology LEF; FEOL elevations illustrative; 2.5D is a visualization, not a process cross section.
- **Build deck:** `make -C docs/slides` from repository root.
- **Build circuit figures:** `make -C docs/slides figures`.
- **Build layout figures:** `make -C docs/slides layouts`.
- **Dependencies:** latexmk/TeX Live, CircuitikZ, Python 3, Node/netlistsvg, librsvg, KLayout.
- **Inspect:** `klayout -n nangate45 docs/slides/layout/nand_inv.gds`; choose the Nangate45 entry under Tools → 2.5d View.
- **Check:** rebuild; render PDF pages; inspect clipping, labels, colors, arrows and progress dots; verify connectivity after edits.
- **Provenance:** keep source links/technical caveats in speaker notes; retain licenses; create original diagrams instead of cropping lecture slides.
- **Limits:** manual route checks are not full DRC/LVS; external text labels are not OpenDB BTerms.

- **Source credits:** footer only; use short hyperlinks such as “CMOS stackup image (Source: Wikimedia Commons)”; never consume slide content space with credit blocks.
- **Attribution details:** retain author, license, modifications and technical caveats in speaker notes and the source manifest. Use `\slidesource{\href{URL}{short label}}` for the footer.

- **Format figures:** edit `docs/slides/build_extension.py`; real source snippets; omissions marked; curved SVG callouts.
- **Rebuild format/simulation assets:** `make -C docs/slides extensions`; then `make -C docs/slides`.
- **Simulation:** real CDL dimensions + FreePDK45 model cards; preserve units; measure cell delay at A/ZN; distinguish total supply energy from internal power.
- **Databases:** `.odb` = OpenDB physical design; Synopsys `.db` = compiled timing library; OpenSTA reads `.lib` directly.
- **History slides:** image or manual cover + expanded name + origin + purpose; short linked footer; no bullet list.

- **Code callouts:** labels to the right of the code; straight horizontal arrows point left toward the line; no arrows crossing the illustration.
- **Liberty continuity:** keep the inverter image at the same position and size; use the original netlistsvg SVG with a valid viewBox; NAND example uses NAND2_X1 data and the existing NAND artwork.
- **Reference cover:** thin black paper border; one shared LEF/DEF introduction.

- **Balance:** reserve the left half for the illustration; start code near the middle; vertically center excerpts by their rendered line count.
- **Arrow length:** keep right-side callouts close to their target line; use short horizontal left-pointing arrows.
- **Circuit testbench:** source label left of source; positive terminal up; explicit VDD/VSS connections; source/load resistors RS/RL.
- **Power plots:** compare edges on identical axes; preserve negative supply power; distinguish supply energy from device dissipation.

- **Vertical centering:** center visible diagram bounds in the left half; center code independently by line count in the right half.
- **Design filenames:** `top.def`, `top.odb`, `top.sdc`; use `top` consistently in displayed examples.
- **Liberty overview:** three underlined headings, no boxes; short bullets permitted on this comparison slide. LVF adds statistical variation to nominal models.

- **Format introductions:** plain origin/purpose text; no directional arrows in these introductions.
- **Inverter testbench:** INV_X1 label above-left of the gate; connected VDD stem and T-shaped bar in black.

- **Code spacing:** preserve SVG whitespace; measure the actual monospace font for arrow endpoints. Arrowheads finish immediately beside the target text.
- **Column spacing:** code begins at x=700 on the 1400-wide format figure canvas, leaving a clear gap after the left illustration.

- **LEF pin abstracts:** Nord blue outlines, pale blue-grey fill (#E5E9F0); A/ZN/VDD/VSS labels in Nord red. Short arrows identify signal-pin shapes; avoid crossing other pins.

- **Gate scale:** later NAND/inverter symbols match their original symbol-and-Verilog slides (45% of text width); preserve aspect ratio and allow the NAND's full height.
