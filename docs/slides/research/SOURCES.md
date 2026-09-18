# Sources and reproduction notes

- **Lecture reference:** Austin Rovinski, [Lecture 3: Liberty/LEF/DEF Formats](https://www.youtube.com/watch?v=2oh1QffM7tg), 37:47. Reviewed the complete sequence of YouTube storyboard contact sheets for visual topic coverage; the transcript endpoint was unavailable. Audio was not transcribed. No lecture screenshots are reused in the deck.
- **Coverage:** Liberty units, conditions, cell properties, pins, timing arcs, lookup tables and power; LEF macro, pins, power rails, units, sites, layers and vias; DEF placement, rows, tracks, ports, signal routes and special nets. Our two-cell example replaces the lecture's example.
- **Die photo:** [NXP PCF8577C LCD driver with I²C (Colour Corrected)](https://commons.wikimedia.org/wiki/File:NXP_PCF8577C_LCD_driver_with_I%C2%B2C_(Colour_Corrected).jpg), cole8888 / Cole L, 15 May 2020; [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/). [Original Flickr](https://www.flickr.com/photos/187597251@N05/49899342293/). Resized to 1800 pixels and JPEG recompressed; image otherwise unchanged. The chip is not our GCD or a Nangate45 fabricated example. Image adaptations retain the source license.
- **LEF/DEF cover:** Cadence, *LEF/DEF Language Reference*, version 5.7, November 2009; [reference PDF](https://www.ispd.cc/contests/18/lefdefref.pdf). First page rendered with `pdftoppm -f 1 -singlefile -scale-to 1000 -png`; cover reproduced for identification and instruction, not an assertion of an open image license. The toy DEF declares 5.8; Nangate source LEFs declare 5.6. [Si2 specifications](https://si2.org/lef-def-downloads/).
- **SPICE screenshot:** [Berkeley SPICE page](https://bwrcs.eecs.berkeley.edu/Classes/IcBook/SPICE/), captured in a browser. Historical origin: Nagel and Pederson, Berkeley, 1973. The user-supplied URL repeated the address; the corrected page was used.
- **GDS history:** [Calma GDS II Users Operating Manual, November 1978](https://bitsavers.computerhistory.org/pdf/calma/GDS_II_Users_Operating_Manual_Nov78.pdf). The illustration is our actual Nangate GDS render, not a manual image.
- **Nangate45 data:** [OpenROAD-flow-scripts platform](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/tree/master/flow/platforms/nangate45). Installed local source: `~/Documents/libs/OpenROAD-flow-scripts/flow/platforms/nangate45`. Retained library license: `../layout/Nangate45-LICENSE`. Excerpts retain original values, with explicit omission comments and line wrapping. Full extracted INV and NOR groups are under `../examples/extension/`.
- **Rows and tracks:** [OpenROAD IFP](https://openroad.readthedocs.io/en/latest/main/src/ifp/README.html). Original vector diagrams show the toy DEF's actual pitches, offsets and placement sites; lines are guides, not metal geometry. Manual toy routes are not constrained to all preferred tracks and are not signoff verified.
- **Physical database:** [OpenDB](https://openroad.readthedocs.io/en/latest/main/src/odb/README.html). `roundtrip.tcl` imports LEF/DEF and writes `.odb`; `reload.tcl` verifies the saved database in a fresh process. Two instances, three BTerms, six nets.
- **Timing data:** [OpenSTA](https://openroad.readthedocs.io/en/latest/main/src/sta/README.html). Reads Liberty directly. The proprietary Synopsys `.db` path is conceptual; no proprietary compiler or compiled library was generated. `.odb` is not a full timing-session checkpoint.
- **Model families:** [Synopsys characterization](https://www.synopsys.com/blogs/chip-design/library-characterization-for-advanced-process-designs.html), [LVF introduction](https://news.synopsys.com/2014-09-30-Synopsys-Announces-New-Additions-to-Liberty-to-Significantly-Speed-up-Timing-Closure), [Cadence ECSM](https://www.cadence.com/en_US/home/alliances/standards-and-languages/ecsm-library-format.html). NLDM, current-source models and variation extensions are not three mutually exclusive file format versions. No dedicated live Liberty-format Wikipedia article was found; the deck links the related standard-cell page.
- **Simulation models:** [ngspice-cmos FreePDK45](https://github.com/Teddy-van-Jerry/ngspice-cmos/tree/9f470c6d2558dc3d63fc21681dbdc131a7fea095/FreePDK45), NCSU FreePDK45 v1.4 cards adapted for ngspice by Wuqiong Zhao; Apache 2.0 license and upstream README retained under `../simulation/models/`. [NCSU platform background](https://eda.ncsu.edu/freepdk/freepdk45/). Nominal NMOS_VTL/PMOS_VTL, actual Nangate INV device dimensions. Model release and omitted extracted parasitics prevent interpreting this experiment as reproduction of Nangate library characterization.
- **Simulation:** ngspice 45.2, 1.1 V, 25°C; input 2 kΩ + 5 fF, output 1 kΩ + 10 fF; 10 ps source edges. A→ZN delay: 10.773 ps falling, 11.443 ps rising. Input 30–70% rise slew: 11.645 ps. Integrated total supply energy per 700 ps cycle: 15.136 fJ. Total supply energy is not the Liberty internal-power table entry.
- **Earlier figures:** `../assets/fabs/SOURCES.md`, `../layout/README.md` and speaker notes retain CMOS cross-section, DMC65 and fab-image attribution.

- **STA check:** `formats/timing_session.tcl` successfully combines Liberty, saved OpenDB and SDC. The two-cell path reports through inst1/A2 → inst1/ZN → inst2/A → inst2/ZN. No extracted parasitics are loaded; this check uses ideal wires. It is separate from the isolated inverter transient experiment. The library includes TAPCELL_X1 without a matching LEF master; OpenROAD marks that unused cell don't-use.

## LEF/DEF introduction revision

- Combined the separate format introductions; framed the existing Cadence cover with a thin black border.
- Timeline labels are **reference-manual editions**, not initial release dates: 5.6 September 2004 ([Cadence manual mirror](https://citeseerx.ist.psu.edu/document?doi=3d7699d9c6b3a498e48f74fc9ae0c029aaf777aa&repid=rep1&type=pdf)); 5.7 November 2009 ([manual](https://www.ispd.cc/contests/18/lefdefref.pdf)); 5.8 May 2017 ([manual](https://coriolis.lip6.fr/doc/lefdef/lefdefref/lefdefref.pdf)).
- [Si2](https://si2.org/lef-def-downloads/) identifies Cadence as developer and Si2 as distributor, and now also lists version 6.0. The timeline selects the historical editions relevant to these examples.
- Historical donation detail: Cadence released the LEF text specification to Si2 on 9 November 1999, reported contemporaneously by [Richard Goering](https://www.edn.com/cadence-donates-lef-but-specs-future-still-uncertain/); this did not yet include DEF. Both formats subsequently became publicly available through Si2. No single joint donation date is asserted on the slide.
- The two-input Liberty example now uses **NAND2_X1**, matching the existing netlistsvg symbol, pin capacitances, Boolean function and two negative-unate timing arcs. The earlier NOR excerpt remains a research artifact and is not used in the deck.

## Supply-power comparison

- Identical-scale edge plots retain negative supply power (brief energy return to the ideal source). Full half-cycle integrals: output fall 0.3699 fJ; output rise 14.7663 fJ; total 15.1362 fJ.
- This measures VDD supply power, not total instantaneous dissipation. Load charging draws energy from VDD; discharge releases stored capacitor energy. See [Berkeley EECS16B circuit notes, CMOS inverter chain](https://www-inst.eecs.berkeley.edu/~ee16b/fa21/student-resources/circuits_reader.pdf). The 10 fF external load alone draws approximately C VDD² = 12.1 fJ during charging; the simulation also includes cell capacitances and other currents.
- Testbench resistor element names now match the diagram: RS (source) and RL (load). Electrical values and connectivity are unchanged.

## Combined overview and physical-view highlights

- The opening three slides are replaced by one editable horizontal implementation flow, based on the [OpenROAD overview](https://github.com/The-OpenROAD-Project/OpenROAD). The GCD image remains the repository's own `images/design.png`.
- Standard-cell representations are grouped for teaching; SPICE is used for simulation, GDS masters for final assembly, and DEF is a design-level interchange. The workshop begins with a synthesized netlist.
- LEF pin abstractions now use exact polygons from `layout/geometry.json` directly in SVG. M2 route centers, widths and VIA1 cuts match the existing teaching layout. Geometry is not reinterpreted from lecture screenshots.
- Shared highlights connect PIN A/VDD and DEF in1/wire1/VDD to their corresponding source rows.
- SPICE display files use // comments at the user's request. Executable files retain * comments, compact W/L values and unchanged dimensions; ngspice delay/energy results remain unchanged.
- The original English CMOS material legend is restored.


## 2026-09-18: split decks and the final recap

- DEF deck preserves original slides 24–29; Liberty deck preserves original slides 36–44 of the 46-slide background deck. Original slides 30/46 are replaced by one recap.
- Abstract generation: https://community.cadence.com/cadence_blogs_8/b/cic/posts/layout-to-abstract-how-virtuoso-abstract-generator-enhances-design-productivity-2133230963 — Cadence's description of abstracts derived from detailed GDSII/layout data; outlines, terminal positions and obstructions.
- Characterization: https://community.cadence.com/cadence_blogs_8/b/di/posts/basics-of-standard-cell-characterization-and-more — SPICE devices/models, PVT settings, input-slew/output-load sweeps, Liberty output.
- Logic extraction / transistor logic abstraction: https://community.cadence.com/cadence_technology_forums/f/logic-design/2465/tip-of-the-month-verifying-final-netlist — transistor groups abstracted into Verilog primitives for digital logic. This supports the process name, not a claim that every characterizer exports Verilog or arbitrary analog circuits can be converted automatically. Functional models can also be authored and verified.
- OpenROAD imports and checkpoints: https://openroad.readthedocs.io/en/latest/main/src/README.html — read_lef/read_def, read_verilog followed by link_design, read_db/write_db.
- Object mapping checked against local OpenROAD src/dbSta/include/db_sta/dbNetwork.hh: LibertyLibrary, LibertyCell, LibertyPort and mappings to OpenDB dbMaster/dbInst. OpenSTA timing models and graph are separate from the OpenDB checkpoint.
- Technology LEF is provided by the PDK; a macro abstract generator does not infer a technology's routing rules solely from GDS. Cell abstracts also need layer/pin identification and abstraction settings.
- “Authoritative cell sources” is the teaching workflow assumption, not a claim that all custom design tools internally store GDS or SPICE as their authoring database. LVS checks source-view consistency; parasitic extraction may augment the SPICE netlist used in characterization.
- Final outputs shown: design.v (updated netlist), design.def (placement and routing). GDS stream-out is outside this recap's P&R engine boundary, per the requested scope.
- Validation: formats/recap_import.tcl links the actual two-cell design using LEF + Liberty + design.v, without cells.v. formats/roundtrip.tcl emits the physical checkpoint and both DEF and Verilog exports; reload.tcl checks saved instances, ports and nets.


## 2026-09-18: annotation review, schedule and stage images

- Background now has 31 pages: the old first slide became a three-day timetable and a separate seven-stage file/engine diagram; recap is page 31. The DEF and Liberty short decks retain six and nine pages.
- `render_stages.tcl` reads this repository's saved GCD checkpoints with native OpenROAD, bounds each image to the real die, and uses no modified design data.
- Global route segments come from `results/6_global_route.guide`, rendered with `read_guides` and `draw_route_segments`. Commands: https://openroad.readthedocs.io/en/latest/main/src/grt/README.html .
- CTS geometry: 427 instances, six clock nets, five buffer drivers, 43 driver-to-load edges exported from `results/5_cts.odb`. `getAvgXY` gives actual terminal coordinates. `build_cts_view.py` draws grey placed cells, purple flip-flops, green clock buffers and blue fly-lines. These are logical clock connections over actual placement, not physical clock routes. The native snapshot is also retained.
- Detailed-routing and finishing snapshots both use `gcd_final.odb`; filler instances are hidden only in the detailed-routing view. They share the same final route geometry; no separate pre-filler snapshot is claimed.
- Official logo: inline SVG from https://openroad.org/ retrieved 2026-09-18. Stopwatch/circuit/24h mark; monochrome currentColor resolved to Nord blue. Retained in assets/openroad-logo.svg, source linked in the slide footer. This is the chip-design OpenROAD project, not the similarly named automotive company.
- Local import check: Boolean assign expressions in the functional cell models fail the OpenROAD structural reader. Empty named module stubs shadow the Liberty cell definitions and create zero physical leaf instances. The final illustration therefore connects cells.v to design.v as a cell-type relationship; only structural design.v carries read_verilog/link_design. examples/cells.v contains the real functional primitives for simulation and is not read by recap_import.tcl.
- Hierarchy check: a two-level pair/design example was linked with link_design -hier and exported with write_verilog; the exported module hierarchy was retained. DEF exports the physical block's flattened leaf instances. No claim of nested Verilog hierarchy in ordinary DEF. Local implementation: src/dbSta/src/dbReadVerilog.tcl and dbReadVerilog.cc. Public API reference: https://openroad.readthedocs.io/en/latest/main/src/README.html . The local -hier mode emits a development-status warning; this is a teaching example.
- flow.py denotes the Python scripting alternative; Python API coverage differs and Verilog import/export may need a Tcl bridge. The recap command labels use Tcl spelling.

Checkpoint SHA-256 used for stage images:
- `1_floorplan.odb`: `4877e04cfb3558aae47a6a63184d37772e66f3d2b9bcd50e01573594154ec704`
- `2_power_grid.odb`: `3afca461577050f56e34e22dbd1b8df5ca679b342982b3e23ff542140f1d738f`
- `3_global_placement.odb`: `628e59e9cc0867ee3b168fde0a61622bcae75cf3dd2a5703d1f1656e457330b7`
- `4_repaired.odb`: `c864073cc33b83aeda1e2b72c2d6c299c9739500b71c51f89471569e0e75ec45`
- `5_cts.odb`: `3e05f69e37935695c069cdad54eec3128d4e824080c6c2261d93f8184fd8a8fd`
- `6_global_route.odb`: `afacb60e3474a309c01f9c8c3a45f8531b3fefc61b68ac7af1df0ed549be4cad`
- `gcd_final.odb`: `6f6791be25c9a0717c49b41941a561e2e5beb2bb0f9b6f29b00756e1fbf7d46f`


## 2026-09-18: finished GDS and schedule revision

- The first schedule view now includes an input bundle before floorplanning, with uniform block and arrow spacing. Day 1 explanatory text and the lower GCD tagline were removed.
- Final stream-out uses the existing local OpenROAD-flow-scripts `flow/util/def2stream.py` without modifying that script: https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/util/def2stream.py .
- Inputs: repository `results/gcd_final.def`, OpenROAD test Nangate45 tech and standard-cell LEFs (the original flow's LEFs), and ORFS `flow/platforms/nangate45/gds/NangateOpenCellLibrary.gds`.
- The generated local `assets/stages/streamout.lyt` preserves ORFS's physical GDS layer mapping and supplies absolute LEF paths. Existing user technology/configuration is not changed.
- The output `assets/stages/design.gds` has top `gcd`, and is rendered with KLayout LayoutView using the user's existing asiclab `tech/nangate45/nangate45.lyp`. All physical mask layers 1–29, datatype 0, are visible; text and boundary annotations are hidden.
- DEF units are 0.0005 µm; the ORFS stream-out DBU is the finer 0.0001 µm. KLayout reports that difference; the integral 5:1 conversion preserves the DEF coordinate grid.
- Stream-out checks: all library cells resolved, no empty/orphan cells; actual GDS component-master counts agree with DEF. This is stream-out integrity checking, not an additional DRC/LVS claim.

## 2026-09-18: physical slides and source footers

- LEF/DEF 6.0 verified against Si2's current download list: https://si2.org/lef-def-downloads/ . The list includes 5.8 and 6.0, with no 5.9 reference found. No unverified year is assigned to 6.0. Earlier years identify the reference editions already cited above, not necessarily first releases.
- DEF wording uses “hierarchical instance names” to distinguish physical placement from nested Verilog module hierarchy.
- DMC65 caption identifies the group's example chip, 2022. Group link requested by the author: https://silab-bonn.github.io/ . Image provenance remains the original local DMC65 rendering described above; the group homepage is not claimed to host the image.
- All source notes use a bottom-right “Sources:” prefix, compact dot-separated link labels, and direct upstream file links for Nangate45 GDS, CDL, macro LEF, technology LEF and Liberty.
- GDS history is merged into the separate-cell view. Physical net/pin labels use common anchors in `layout/label_positions.py`; black labels lie within metal geometry and avoid via cuts. Layer legends use color swatches.
- SVG file annotation paint order is geometry, highlight backgrounds, source text, callouts. Arrows therefore remain visible over the highlights.

## 2026-09-18: standalone introduction

- Arithmeum photograph downloaded unchanged from https://www.or.uni-bonn.de/pic/Arithmeum.jpg , the building image linked by the Research Institute for Discrete Mathematics homepage https://www.or.uni-bonn.de/index.eng.html . That page also confirms Lennéstraße 2, Bonn. Photographer/license not stated on the page; retain the institute source link.
- Workshop dates, opening hours, lunch, front-desk instructions, optional self-funded dinner and preparation contacts are supplied by the organizer in this task. Dates are 21–23 September 2026 (Monday–Wednesday).
- Intro contains the separated schedule and logistics. Remaining background material is renamed to filetypes.tex/filetypes.pdf.

- Intro photo replaced with the user-selected https://www.arithmeum.uni-bonn.de/fileadmin/user_upload/Arithmeum-Hausfoto.jpg (saved unchanged as `assets/arithmeum-house.jpg`). Intro source links are retained in notes rather than displayed, per request.
