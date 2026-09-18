"""Readable vector overviews of actual floorplan rows and placed-cell boundaries.

Geometry is exported by render_stages.tcl from the saved OpenDB checkpoints.
These are placement abstractions; cell internals are deliberately omitted.
"""
from pathlib import Path
import subprocess

P = Path(__file__).resolve().parent / 'assets/stages'
for stage in ['floorplan', 'global_placement', 'detailed_placement']:
    rows = [line.split('\t') for line in (P/f'{stage}_geometry.tsv').read_text().splitlines()]
    x0, y0, x1, y1 = map(float, rows[0][1:])
    scale = 850 / max(x1-x0, y1-y0)
    def box(coords, fill, stroke, width):
        x, y, X, Y = map(float, coords)
        return (f'<rect x="{25+(x-x0)*scale}" y="{875-(Y-y0)*scale}" '
                f'width="{(X-x)*scale}" height="{(Y-y)*scale}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="900" viewBox="0 0 900 900">',
           '<rect width="900" height="900" fill="white"/>',
           box((x0,y0,x1,y1),'none','#D8DEE9',2)]
    for row in rows[1:]:
        if row[0] == 'ROW':
            svg.append(box(row[1:5], '#EDF2E8', '#A3BE8C', 1.8))
        else:
            svg.append(box(row[3:7], '#81A1C1', '#FFFFFF', 1.0))
    svg.append('</svg>')
    path = P/f'{stage}.svg'
    path.write_text('\n'.join(svg))
    subprocess.run(['rsvg-convert','-f','pdf','-o',str(path.with_suffix('.pdf')),str(path)],check=True)
    print(stage, len(rows)-1, 'actual row/cell boundaries')
