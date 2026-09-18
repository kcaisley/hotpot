#import "@preview/cetz:0.5.2": canvas, draw

#let gate-color = red;
#let net-colors = (blue, green, orange, purple, yellow);
#let net-names = ("B", "G", "O", "P", "Y");
#let cpp = 25mm;
#let fet-height = 2cm;
#let pc-extend = fet-height / 5;
#let pc-width = cpp / 3;
#let single-ca-width = (cpp - pc-width) / 2;
#let node-radius = 5mm;
#let fet-configs = (
  (1, 3, 4),
  (1, 2, 4),
  (1, 0, 4),
  (2, 4, 1),
);

#let draw-fet(config, swap: false) = {
  let (fingers, source, drain) = config;
  if swap {
    let tmp = source;
    source = drain;
    drain = tmp;
  }
  let pc-min(i) = (i - 0.5) * cpp - pc-width / 2;
  let ca-data(i) = {
    let net = if calc.rem(i, 2) == 0 { source } else { drain };
    let pc = pc-min(i);
    if i == 0 {
      return (net, pc - single-ca-width, pc);
    } else if i == fingers {
      return (net, pc - 2 * single-ca-width, pc - single-ca-width);
    } else {
      return (net, pc - 2 * single-ca-width, pc);
    }
  };
  for i in range(fingers) {
    draw.rect((pc-min(i), -pc-extend), (rel: (pc-width, fet-height + 2 * pc-extend)), fill: gate-color);
  }
  for i in range(fingers + 1) {
    let (net, min, max) = ca-data(i);
    let name = "ca" + str(i);
    draw.rect((min, 0), (max, fet-height), fill: net-colors.at(net), name: name);
    draw.content(name, net-names.at(net));
  }
}

#let draw-placement(fets) = {
  let track = 0;
  for fet in fets {
    let (config, offset, swap) = fet;
    draw.group({
      draw.translate((offset * cpp, 0));
      draw-fet(config, swap: swap);
    });
  }
}

#let net-node(net) = "net-" + str(net);

#let draw-node(position, net) = {
  draw.circle(position, radius: node-radius, fill: net-colors.at(net), name: net-node(net));
  draw.content(net-node(net), net-names.at(net));
}

#let draw-edge(net-a, net-b, dashed: false) = {
  let stroke = (thickness: 1mm);
  if dashed {
    stroke.dash = "dashed";
  }
  if net-a != net-b {
    draw.line(net-node(net-a), net-node(net-b), stroke: stroke);
  } else {
    let node = net-node(net-a);
    let offset = node-radius / calc.sqrt(2);
    draw.arc(
      (rel: (offset, offset), to: node + ".center"),
      radius: node-radius,
      start: -45deg,
      delta: 270deg,
      stroke: stroke
    );
  }
};

#let draw-fets(swap) = {
  draw.group({
    draw.translate((0, 0));
    draw-fet(fet-configs.at(0));
  });
  draw.group({
    draw.translate((1.5 * cpp, 0));
    draw-fet(fet-configs.at(1));
  });
  draw.group({
    draw.translate((0, -fet-height - 2cm));
    draw-fet(fet-configs.at(2));
  });
  draw.group({
    draw.translate((1.5 * cpp, -fet-height - 2cm));
    draw-fet(fet-configs.at(3), swap: swap);
  });
}

#let draw-placements(gaps) = {
  if gaps < 3 {
    draw.circle((0, 0), stroke: none);
    return;
  }
  if gaps == 3 {
    draw-placement((
      (fet-configs.at(0), 0, false),
      (fet-configs.at(1), 1, true),
      (fet-configs.at(2), 3, false),
      (fet-configs.at(3), 5, true),
    ));
  } else {
    draw-placement((
      (fet-configs.at(0), 0, false),
      (fet-configs.at(1), 1, true),
      (fet-configs.at(2), 3, false),
      (fet-configs.at(3), 4, false),
    ));
  }
}

#let draw-graph(state) = {
  draw-node((0, 0), 4);
  let space = 5 * node-radius;
  draw-node((-space, 0), 0);
  draw-node((0, space), 1);
  draw-node((space, 0), 2);
  draw-node((0, -space), 3);
  draw-edge(0, 4);
  let draw-if(condition, content) = {
    if condition {
      content;
    } else {
      draw.hide(content, bounds: true);
    }
  };
  draw-if(state < 3, draw-edge(1, 4, dashed: true));
  draw-if(state == 3, draw-edge(1, 1));
  draw-if(state == 4, draw-edge(4, 4));
  draw-edge(2, 4);
  draw-edge(3, 4);
}
