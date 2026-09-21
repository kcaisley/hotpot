# render_finished_layout.py -- native KLayout view of the merged final GDS.
from pathlib import Path
import os
import json
import re
from collections import Counter
import pya

P = Path(__file__).resolve().parent
OUT = P/'assets/stages'
TECH = Path(os.environ.get('NANGATE45_TECH', str(Path.home()/'Documents/asiclab/tech/nangate45')))
view = pya.LayoutView()
for key,value in {'background-color':'#ffffff', 'grid-visible':'false',
                  'text-visible':'false', 'cell-frame-visible':'false'}.items():
    view.set_config(key,value)
index = view.load_layout(str(OUT/'design.gds'),False)
cv = view.cellview(index)
layout = cv.layout()
top = layout.cell('gcd')
assert top is not None
empty = [c.name for c in layout.each_cell() if c.is_empty()]
assert not empty, f'Unresolved GDS cells: {empty}'
components = (P.parent.parent/'results/gcd/gcd_final.def').read_text().split('COMPONENTS ')[1].split('END COMPONENTS')[0]
expected = Counter(re.findall(r'^\s*-\s+\S+\s+(\S+)',components,re.M))
actual = Counter(layout.cell(i.cell_index).name for i in top.each_inst())
assert all(actual[name] == count for name,count in expected.items()), 'GDS/DEF component counts differ'
view.load_layer_props(str(TECH/'nangate45.lyp'))
view.max_hier()
for layer in view.each_layer():
    # Render physical masks; keep annotation/boundary layers out of the thumbnail.
    layer.visible = 1 <= layer.source_layer <= 29 and layer.source_datatype == 0
bounds = top.dbbox().enlarged(0.8)
view.save_image_with_options(str(OUT/'finishing_klayout.png'),1600,1600,1,2,1,bounds,False)
summary = {'top':top.name, 'cells':layout.cells(), 'top_instances':sum(1 for _ in top.each_inst()),
           'def_components':sum(expected.values()), 'matched_master_types':len(expected),
           'filler_instances':{name:count for name,count in actual.items() if name.startswith('FILLCELL_')},
           'filler_total':sum(count for name,count in actual.items() if name.startswith('FILLCELL_')),
           'dbu_um':layout.dbu, 'bounds_um':str(top.dbbox()),
           'layer_style':str(TECH/'nangate45.lyp'), 'empty_cells':empty}
(OUT/'streamout-validation.json').write_text(json.dumps(summary,indent=2)+'\n')
print(summary)
view.destroy()
