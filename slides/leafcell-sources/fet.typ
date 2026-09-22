#import "@preview/cetz:0.5.2": canvas, draw

#let draw-fet(conductive) = {
  let p-doped = red.lighten(60%);
  let n-doped = blue.lighten(60%);
  let ca-color = orange.lighten(50%);
  let oxide-color = gray;
  let gate-color = purple.lighten(60%);

  let ca-height = 1cm;
  let body-x = 15cm;
  let body-y = 35mm;

  let source-min = 0.15 * body-x;
  let source-max = 0.35 * body-x;
  let drain-min = 0.65 * body-x;
  let drain-max = 0.85 * body-x;
  let gate-min = 0.4 * body-x;
  let gate-max = 0.6 * body-x;

  // Body
  let body-rect = draw.rect((0, 0), (body-x, body-y), fill: p-doped);
  body-rect;
  draw.content((1cm, 7mm), "P");

  // Tap connection
  draw.line((0, 7mm), (rel: (-1cm, 0)));
  draw.line((rel: (0, 0)), (rel: (0, -1cm)));
  draw.line((-1.5cm, -3mm), (rel: (10mm, 0)));
  draw.line((-1.3cm, -5mm), (rel: (6mm, 0)));
  draw.line((-1.1cm, -7mm), (rel: (2mm, 0)));

  if conductive {
    let channel-height = ca-height;
    draw.rect((source-max, body-y - channel-height), (drain-min, body-y), fill: n-doped.lighten(30%), name: "channel");
    draw.content("channel", ["N"]);
  }

  // source/drain
  let sd-depth = 0.6 * body-y;
  for (min, max, name) in ((source-min, source-max, "Source"), (drain-min, drain-max, "Drain")) {
    draw.boolean(
      body-rect,
      draw.circle(((min + max) / 2, body-y), radius: (max - min, sd-depth)),
      op: "intersection",
      fill: n-doped,
    );
    draw.rect((min, body-y), (max, body-y + ca-height), fill: ca-color, name: name);
    draw.content(name, name);
    draw.content(((min + max) / 2, body-y - sd-depth / 2), "N");
  }

  // Gate
  let oxide-height = 0.1 * body-y;
  let gate-height = ca-height;
  draw.rect(
    (gate-min, body-y),
    (gate-max, body-y + oxide-height),
    fill: oxide-color,
  );
  draw.rect(
    (gate-min, body-y + oxide-height),
    (gate-max, body-y + oxide-height + gate-height),
    fill: gate-color,
    name: "gate"
  );
  draw.content("gate", "Gate=" + if conductive { "1" } else { "0" });
}
