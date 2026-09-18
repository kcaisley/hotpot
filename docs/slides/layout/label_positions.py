"""Shared label anchors in cell-local micrometers, inside actual LEF metal.

Rotated output labels fit the narrow vertical M1 fingers. Signal labels avoid
the dark via cuts so black type remains readable in all three physical views.
"""
PIN_LABELS = {
    'NAND2_X1': [('A1', .4475, .55, 0), ('A2', .1225, .665, 0),
                 ('ZN', .285, 1.10, -90)],
    'INV_X1': [('A', .1125, .665, 0), ('ZN', .2775, .90, -90)],
}
NET_LABELS = [('in1', -.10, .91), ('in2', -.10, .595),
              ('wire1', .48, .46), ('out', 1.075, 1.12)]

def on_shape(x, y, label, size=30, rotation=0):
    return (f'<text x="{x}" y="{y}" fill="#000000" '
            f'font-family="DejaVu Sans,sans-serif" font-size="{size}" '
            f'text-anchor="middle" dy="0.35em" '
            f'transform="rotate({rotation},{x},{y})">{label}</text>')
