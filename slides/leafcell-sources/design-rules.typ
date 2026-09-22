#import "@preview/cetz:0.5.2": canvas, draw

#let metal = rgb(0, 126, 23).lighten(40%);

#let draw-metal(min, max, name: none) = {
  draw.rect(min, max, fill: metal.lighten(40%), stroke: (paint: metal, thickness: 1mm), name: name);
};

#let draw-distance(min, max) = {
  draw.line(min, max, stroke: (thickness: 1mm), mark: (start: ">", end: ">"));
};

#let draw_trio_via(variable_filter, uncover) = {
  let via_size = 2cm
  let draw_via_at(x, y, index) = {
    let radius = via_size / 2
    let name = "via" + str(index)
    draw-metal((x - radius, y - radius), (x + radius, y + radius), name: name)
    uncover(variable_filter, draw.content(name, $x_#index$))
  }
  draw_via_at(0cm, 0cm, 1)
  draw_via_at(1.5 * via_size, 1.5 * via_size, 2)
  draw_via_at(3 * via_size, 0cm, 3)
};

#let min-width = {
  draw-metal((0, 0), (rel: (5cm, 2cm)), name: "wire");
  draw-distance("wire.north", "wire.south");
}

#let min-space = {
  draw-metal((0, 0), (rel: (2cm, 2cm)), name: "left");
  draw-metal((4cm, 0), (rel: (2cm, 2cm)), name: "right");
  draw-distance("left", "right");
}

#let min-area = {
  draw-metal((0, 0), (5cm, 2cm), name: "wire");
  draw-distance("wire.north-east", "wire.south-west");
  draw-distance("wire.north-west", "wire.south-east");
}
