#import "@preview/cetz:0.4.2": canvas, draw

#let mark-cell(cell_name, color) = {
  draw.rect(cell_name + ".south-west", cell_name + ".north-east", stroke: color + 3pt, fill: none)
};

#let cross-cell(cell_name) = {
  mark-cell(cell_name, red);
  draw.line(cell_name + ".south-west", cell_name + ".north-east", stroke: red + 3pt);
  draw.line(cell_name + ".north-west", cell_name + ".south-east", stroke: red + 3pt);
};
  
#let draw-branchbound-tree() = {
  import draw: *

  let cell-width = 1
  let cell-height = 1
  let fet-height = 0.3
  let power-height = 0.1

  // Color definitions
  let nofet = none
  let nfet1 = rgb("#FF7F00")
  let pfet1 = rgb("#B22222")
  let nfet2 = rgb("#00FF7F").darken(20%)
  let pfet2 = rgb("#808000")
  let bonncell-m1 = rgb(16, 171, 255)

  // Function to draw a FET
  let draw-fet(x, y, color) = {
    draw.rect(
      (x - cell-width/6, y - fet-height/2),
      (x + cell-width/6, y + fet-height/2),
      fill: color,
      stroke: none
    )
  };

  // Function to draw a power rail
  let draw-power-rail(x, y) = {
    draw.rect(
      (x - cell-width/2, y - power-height/2),
      (x + cell-width/2, y + power-height/2),
      fill: bonncell-m1,
      stroke: none
    )
  };

  let draw-cell(x, y, nfet-left, nfet-right, pfet-left, pfet-right, name: none) = {
    // Draw cell border
    draw.rect(
      (x - cell-width/2, y - cell-height/2),
      (x + cell-width/2, y + cell-height/2),
      stroke: black + 0.2pt,
      name: name
    )
    
    // Draw power rails
    draw-power-rail(x, y - cell-height/2 + power-height/2)
    draw-power-rail(x, y + cell-height/2 - power-height/2)
    
    // Draw bottom FETs (NFETs)
    draw-fet(x - cell-width/6, y - cell-height/2 + power-height + fet-height/2, nfet-left)
    draw-fet(x + cell-width/6, y - cell-height/2 + power-height + fet-height/2, nfet-right)
    
    // Draw top FETs (PFETs)
    draw-fet(x - cell-width/6, y + cell-height/2 - power-height - fet-height/2, pfet-left)
    draw-fet(x + cell-width/6, y + cell-height/2 - power-height - fet-height/2, pfet-right)
  }

  // Root node
  draw-cell(0, 0, nofet, nofet, nofet, nofet, name: "root")
  
  // Level 1 nodes
  draw-cell(-1.7, -1.7, nfet1, nofet, nofet, nofet, name: "cell11")
  draw-cell(0, -1.7, nofet, nfet1, nofet, nofet, name: "cell12")
  draw-cell(1.7, -1.7, nfet2, nofet, nofet, nofet, name: "cell13")
  
  // Dots below cell13
  content((1.7, -3.7), text(size: 20pt)[$dots.v$], name: "dots13")
  
  // Level 2 nodes
  draw-cell(-2.9, -3.7, nfet1, nofet, pfet2, nofet, name: "cell21")
  draw-cell(-1.7, -3.7, nfet1, nofet, nofet, pfet2, name: "cell22")
  draw-cell(-0.5, -3.7, nfet1, nofet, pfet1, nofet, name: "cell23")
  
  // Dots below cell21 and cell23
  content((-2.9, -4.8), text(size: 20pt)[$dots.v$])
  content((-0.5, -4.8), text(size: 20pt)[$dots.v$])
  
  // Level 3 nodes
  draw-cell(-2.9, -5.8, nfet1, nfet2, pfet2, pfet1, name: "cell41")
  draw-cell(-0.5, -5.8, nfet1, nfet2, pfet1, pfet2, name: "cell43")
  draw-cell(1.7, -5.8, nfet2, nfet1, pfet2, pfet1, name: "cell44")
  
  // Draw connections
  line("root", "cell11", mark: (end: ">"))
  line("root", "cell12", mark: (end: ">"))
  line("root", "cell13", mark: (end: ">"))
  
  line("cell11", "cell21", mark: (end: ">"))
  line("cell11", "cell22", mark: (end: ">"))
  line("cell11", "cell23", mark: (end: ">"))
  
  line("cell13", "dots13.south", mark: (end: ">"))
  line("dots13.north", "cell44", mark: (end: ">"))
};
