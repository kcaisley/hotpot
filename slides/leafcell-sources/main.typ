#import "@preview/touying:0.7.4": *
#import themes.university: *
#import "@preview/cetz:0.5.2"
#import cetz: *

#import "branchbound-tree.typ" as bbtree
#import "fet.typ" as fet
#import "sharing.typ" as sharing
#import "design-rules.typ" as rules

#set text(
  font: "New Computer Modern Sans",
)

// cetz and fletcher bindings for touying
#let cetz-canvas = touying-reducer.with(reduce: cetz.canvas, cover: cetz.draw.hide.with(bounds: true))

#show: university-theme.with(
  aspect-ratio: "16-9",
  config-info(
    // TODO rename
    title: [Transistor-level layout],
    author: [Malte Schürks],
    date: "September 21, 2026",
    institution: [University of Bonn],
    logo: box(image("images/uni-logo.pdf", width: 4cm)),
  ),
  header-right: [],
)

#set heading(numbering: none)
#let mygreen = green.darken(40%);

#title-slide()

// TODO is there no better way to split a slide?
#let fet-slide(final) = slide(repeat: 2, self => [
  == What is a FET?

  - FET = #strong("F")ield #strong("E")ffect #strong("T")ransistor
  - Voltage at *Gate* controls connection between *Source* and *Drain*
  #if final [
  - Two types
    - *N*(-channel) FET: Conducts if gate at logic 1 #pause (Pictured)
    - *P*(-channel) FET: Conducts if gate at logic 0
  ]

  #jump(1)
  #v(1fr)
  #align(center, cetz-canvas(fet.draw-fet(final or self.subslide > 1)))
])

#fet-slide(false)

== FinFET and Gate-All-Around FETs

#box(width: 1fr, align(center)[
  *Planar*\
  #image("images/samsung-planar.jpg", height: 12cm)
])
#pause
#box(width: 1fr, align(center)[
  *FinFET*\
  #image("images/samsung-finfet.jpg", height: 12cm)
])
#pause
#box(width: 1fr, align(center)[
  *Gate-All-Around*\
  #image("images/samsung-mbc.jpg", height: 12cm)
])

#fet-slide(true)

== Building logic from FETs

#box(width: 1fr, baseline: horizon, align(center, image(height: 13cm, "images/NAND.svg")))
$~~>$
#box(width: 1fr, baseline: horizon, align(center, image(height: 13cm, "images/intro/nand_schematic.pdf")))

== Lithography and design rules

#box(width: 1fr, baseline: top)[
  Important manufacturing step:\
  *Photolithography*

  #pause
  Problem: Interference\
  #pause
  Fix: Forbid problematic patterns\
  $~~>$ *Design rules*

  #pause
  Common rules:\
  Min spacing, width, area, ...

  Overall: $~1300$ pages for 2nm

  #pause
  Higher density $=>$ more rules
]
#jump(1)
#box(width: 1fr, baseline: top)[
  #alternatives-match((
    "1": align(center, image(width: 6cm, "images/optics.png")),
    "2": align(center, image(width: 6cm, "images/litho.svg")),
    "3-4": align(center)[
      #cetz.canvas(rules.min-space)

      #v(1fr)
      #cetz.canvas(rules.min-width)

      #v(1fr)
      #cetz.canvas(rules.min-area)
      #v(1fr)
    ],
    "5": align(center, image(width: 10cm, "images/layers.png")),
  ))
]

== Motivation for standard cells

#slide[
  #box(width: 1fr, baseline: top, [
    - Modern chips: $>40 dot 10^9$ FETs
    - Low-layer rules too complex
    #pause
    #list(marker: $=>$)["Hide" FETs inside *cells*:\ Logic, latches, ...]
    #pause
    Advantages:
    - Smaller instance sizes
    - Independent building blocks
    - Easier timing analysis
    - Reusable across chips
  ])
  #meanwhile
  #box(width: 1fr, baseline: top, [
    #alternatives-match((
      "-2": image(width: 100%, "images/intro/zMetis.png"),
      "3-": image(width: 100%, "images/intro/cdme.png"),
    ))
  ])
]

== What defines a cell?

#box(width: 1fr, baseline: horizon)[
  #image("images/abstract.png")
]
#pause
#box(width: 1fr, baseline: horizon)[
  #rotate(-90deg, image(width: 25mm, "images/NAND.svg"), reflow: true)
]
#pause
#box(width: 1fr, baseline: horizon)[
  #image("images/timing.png")
]

#jump(1)
#box(width: 1fr)[
*Geometric properties*
- Size
- Possible positions
- Pin shapes
- Blockages
]
#pause
#box(width: 1fr)[
*Logical function*
- Potentially including state
]
#pause
#box(width: 1fr)[
*Timing and power*
- Delays
- Static power
- Dynamic power
]

== Building a cell

#slide(align: horizon)[
  #box(width: 1fr, baseline: horizon, image(width: 100%, "images/intro/nand1.pdf"))
  #pause
  $~>$
  #box(width: 1fr, baseline: horizon, image(width: 100%, "images/intro/nandfeol.pdf"))
  #pause
  $~>$
  #box(width: 1fr, baseline: horizon, image(width: 100%, "images/intro/nandfull.pdf"))
]


//== Placing small cells
//
//#box(baseline: top, width: 1fr)[
//  Assume:
//  - Have routability oracle
//  - Fixed cell width
//  #pause
//  Goal: "Best" routable placement
//  - Bounding-box netlength
//  - Alignment
//  - ...
//  #pause
//  Mathematically hard problem\
//  $=>$ Exponential worst-case runtime
//]
//#meanwhile
//#box(baseline: top, width: 1fr)[
//  #alternatives-match((
//    // /lfs/user/schuerks/cell-tests/2026-08-07_09-44-57_CW_OAI22_X2P5M_A200S_plot
//    "1-2": image(width: 100%, "images/small-cell.pdf"),
//    "3": [
//      #align(center, image(width: 90%, "images/time-complexity.svg"))
//
//      #v(-1cm)
//      #text(size: 0.5em, gray)[Source: https://commons.wikimedia.org/wiki/File:Comparison_computational_complexity.svg]
//    ],
//  ));
//]

== Exact placement by Branch&Bound

#slide(repeat: 5, self => [
  #let (uncover, only, alternatives, alternatives-match) = utils.methods(self)
  #box(baseline: horizon, width: 1fr)[
    *Assume given*: Routability oracle

    #pause
    *Algorithmic structure*:
    - Place FETs one at a time
    #pause
    - Prune useless branches early
    #pause
    - Check routability of full placements
    #pause
    - Find best remaining
  ]
  #meanwhile
  #box(baseline: horizon, width: 1fr)[
    #cetz-canvas({
      import cetz.draw: *
      let uncover = uncover.with(cover-fn: hide.with(bounds: true))

      scale(2)
      uncover("2-", bbtree.draw-branchbound-tree())
      uncover("3-", {
        bbtree.cross-cell("cell12")
        bbtree.cross-cell("cell22")
      })
      uncover("4-", bbtree.cross-cell("cell41"))
      uncover("5-", bbtree.mark-cell("cell44", mygreen))
    })
  ]
])

== Pruning techniques

#box(width: 1fr, baseline: top)[
  Width bounds:
  - Is there space for all FETs?
  - Remove many useless branches
  - Never prunes full nodes
  #pause
  Routing checks:
  - Basic checks on partial nodes
  - Prunes unroutable full nodes
  - Only consider FEOL shapes
    - I.e. shapes "close to FETs"
]
#jump(1)
#box(width: 1fr, baseline: top)[
  #align(center)[
    #scale(80%, cetz-canvas({
      sharing.draw-fets(false)
    }))

    #v(-15mm)
    #cetz-canvas({
      sharing.draw-graph(1)
    })
  ]
]

== ILP-based routing

#slide(repeat: 5, self => [
  #let (uncover, only, alternatives, alternatives-match) = utils.methods(self)
  #box(baseline: top, width: 1fr)[
    "Direct" routing algorithms:
    - Usually heuristic
    - Tricky to extend
    #pause
    Instead:
    - Describe mathematically as ILP
    - Use black-box solver CPLEX
    #jump(5)
    Connectivity:
    - Steiner tree per net
    - Multicommodity flow relaxation
  ]
  #meanwhile
  #box(baseline: top, width: 1fr)[
    #align(center, [
      Design rule: 3 incompatible vias

      #cetz-canvas({
        import cetz.draw: *
        let uncover = uncover.with(cover-fn: hide.with(bounds: true))
        rules.draw_trio_via("3-", uncover)
      })
      #pause
      #pause
      $ x_i in {0, 1} $
      #pause
      ILP constraint: $x_1 + x_2 + x_3 <= 2$
    ])
    // TODO MCF relaxation?
  ]
])

== Further concepts in BonnCell

#slide(repeat: 2, self => [
  #let (uncover, only, alternatives, alternatives-match) = utils.methods(self)
  #box(width: 1fr)[
    *Placing larger cells*
    - Partition FETs
    - Solve "subcells" optimally
    - Use pins to ensure routability
  ]
  #pause
  #box(width: 1fr)[
    *Faster routing checks*
    - Bottleneck during placement
    - Transform ILP to SAT
    - Extension: Decision-guided SAT
  ]

  #jump(1)
  #box(width: 1fr, baseline: top)[
    #align(center, image(height: 7cm, "images/lcble-blocks.svg"))
  ]
  #box(width: 1fr, baseline: top)[
    #align(center)[
      #if self.subslide == 2 [
        #cetz-canvas({
          import cetz.draw: *
          let uncover = uncover.with(cover-fn: hide.with(bounds: true))
          rules.draw_trio_via("1-", uncover)
        })

        $x_1 + x_2 + x_3 <= 2$\
        $~> not x_1 or not x_2 or not x_3$
      ]
    ]
  ]
])
