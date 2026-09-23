# HOTPOT: physical design with open-source tools

Slides and examples for the **Hands-On Tutorial for Physical Design with Open-Source Tooling**. Start with the [workshop introduction](slides/intro.pdf), then follow the presentations below from design files through fabrication. The [workshop poster](poster/hotpot-workshop-poster.pdf) is also available.

<p align="center">
  <img src="slides/images/finishing/finishing_klayout.png" alt="Routed chip layout viewed in KLayout" width="560">
</p>

## From design files to a layout

The diagram from the final [design file types slide](slides/filetypes.pdf) shows how cell geometry, circuit models, logic, and timing constraints enter OpenROAD, and how the updated design is exported.

![Cell views and design files flowing through OpenROAD to the exported design](slides/images/recap-readme.png)

[Open the full-size flow diagram](slides/images/recap-readme.png).

## Presentations

For each stage, read the **background lecture** first, then the **workshop tutorial**. The background decks are PDF-only; the workshop decks also have TeX source in `slides/`.

| Stage | Background lecture (PDF) | Workshop tutorial (PDF) |
| --- | --- | --- |
| **Cells and design files** | [Transistor-level layout](slides/leafcell.pdf) | [Design file types](slides/filetypes.pdf) · [Liberty](slides/lib.pdf) · [DEF](slides/def.pdf) |
| **Floorplanning and pins** | [Floorplanning, macro placement and pin placement](slides/floorplanning-paula.pdf) | [Floorplanning in OpenROAD](slides/floorplanning.pdf) |
| **Placement** | [Placement in OpenROAD](slides/placement-martin.pdf) | [Placement tutorial](slides/placement.pdf) |
| **Clock tree and timing** | [Clock-tree synthesis and timing closure](slides/clocktree-synthesis-louis.pdf) | [CTS and timing paths](slides/cts.pdf) |
| **Routing** | [Global routing](slides/openroad_global_routing.pdf) · [Detailed routing](slides/openroad_detailed_routing_beamer.pdf) | [Routing tutorial](slides/routing.pdf) |
| **Finishing and verification** | — | [Finishing, export, DRC and LVS](slides/finishing.pdf) |

After implementation: [Chip fabrication and shared wafers](slides/fab.pdf).
