"""Export the four self-contained presentation decks into a public checkout.

Run on the development branch. This copies only TeX, presentation PDFs, used
images and attribution files; generators, databases and simulations stay here.
"""
from pathlib import Path
import argparse
import re
import shutil

P = Path(__file__).resolve().parent
DECKS = ['intro', 'filetypes', 'def', 'lib']
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('checkout', type=Path, help='Checkout of the attendee main branch')
args = parser.parse_args()
out = args.checkout.resolve() / 'slides'
out.mkdir(parents=True, exist_ok=True)
images = set()

def graphic(match):
    src = Path(match[2])
    assert (P/src).is_file(), src
    dest = Path('images') / (src.relative_to('assets') if src.parts[0] == 'assets' else src)
    (out/dest).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(P/src, out/dest)
    images.add(dest.as_posix())
    return r'\includegraphics' + (match[1] or '') + '{' + dest.as_posix() + '}'

def listing(match):
    code = (P/match[2]).read_text().rstrip()
    return '\n' + r'\begin{lstlisting}' + (match[1] or '') + '\n' + code + '\n' + r'\end{lstlisting}' + '\n'

for name in DECKS + ['slide_style', 'extension_slides']:
    source = (P/f'{name}.tex').read_text()
    source = re.sub(r'\\includegraphics(\[[^\]]*\])?\{([^}]+)\}', graphic, source)
    source = re.sub(r'\\lstinputlisting(\[[^\]]*\])?\{([^}]+)\}', listing, source)
    # Beamer needs fragile frames for the now-embedded, editable listings.
    def frame(match):
        content = match[0]
        if r'\begin{lstlisting}' in content:
            content = content.replace(r'\begin{frame}', r'\begin{frame}[fragile]', 1)
        return content
    source = re.sub(r'\\begin\{frame\}.*?\\end\{frame\}', frame, source, flags=re.S)
    (out/f'{name}.tex').write_text(source)
for name in DECKS:
    shutil.copy2(P/f'{name}.pdf', out/f'{name}.pdf')

(out/'Makefile').write_text('''DECKS := intro filetypes def lib
.PHONY: all help
all: $(addsuffix .pdf,$(DECKS))

help:
\t@printf '%s\\n' 'Build dependencies: TeX Live (Beamer, Latin Modern, listings) and latexmk.' 'Build all decks: make' 'Build one deck: make intro.pdf'

%.pdf: %.tex slide_style.tex extension_slides.tex $(shell find images -type f)
\tlatexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
\tcp build/$@ $@
''')
(out/'.gitignore').write_text('build/\n*.aux\n*.log\n*.out\n*.nav\n*.snm\n*.toc\n*.vrb\n*.fls\n*.fdb_latexmk\n')
(out/'README.md').write_text('''# HOTPOT presentations

| Presentation | PDF | Editable source |
| --- | --- | --- |
| Introduction and logistics | [intro.pdf](intro.pdf) | [intro.tex](intro.tex) |
| Design file types | [filetypes.pdf](filetypes.pdf) | [filetypes.tex](filetypes.tex) |
| DEF | [def.pdf](def.pdf) | [def.tex](def.tex) |
| Liberty | [lib.pdf](lib.pdf) | [lib.tex](lib.tex) |
''')
(out/'SOURCES.md').write_text('''# Image and source attribution

Original workshop diagrams and simulations are by Kennedy Caisley. Detailed
source links and technical qualifications are retained in each deck's TeX notes.

- CMOS stack: [Cepheiden, Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Cmos-chip_structure_in_2000s_(en).svg), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). English labels retained; rendered/scaled for the slide. The adapted illustration retains CC BY-SA 3.0.
- World map: [Canuckguy and contributors](https://commons.wikimedia.org/wiki/File:BlankMap-World.svg), public domain; recolored and annotated.
- SkyWater building: [Iceone2000](https://commons.wikimedia.org/wiki/File:SkyWater_Building_Exterior.jpg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), scaled without cropping. The adapted image retains CC BY-SA 4.0.
- IHP aerial photograph: [IHP](https://www.ihp-microelectronics.com/fileadmin/user_upload/DJI_0789.JPG), © IHP.
- Singapore campus photograph: [GlobalFoundries](https://gf.com/manufacturing/singapore/), © GlobalFoundries.
- Company logos identify their respective organizations and remain their property.
- Arithmeum: [official building photograph](https://www.arithmeum.uni-bonn.de/fileadmin/user_upload/Arithmeum-Hausfoto.jpg), University of Bonn; retained without cropping. No open license is asserted.
- DMC65: layout rendering from the author's group, 2022; [SiLab Bonn](https://silab-bonn.github.io/).
- Nangate45: [OpenROAD-flow-scripts library files](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/tree/master/flow/platforms/nangate45). Specific GDS, CDL, LEF and Liberty files are linked in slide footers.
- Logic symbols: [netlistsvg](https://github.com/nturley/netlistsvg), modified with the workshop colors; [MIT license](https://github.com/nturley/netlistsvg/blob/master/LICENSE).
- OpenROAD logo: [OpenROAD](https://openroad.org/), rendered in monochrome blue.
- LEF/DEF cover: Cadence, [Language Reference 5.7, November 2009](https://www.ispd.cc/contests/18/lefdefref.pdf).
- SPICE history screenshot: [UC Berkeley](https://bwrcs.eecs.berkeley.edu/Classes/IcBook/SPICE/).

Third-party illustrations and trademarks are not relicensed as workshop code.
''')
print(f'Exported {len(DECKS)} decks, 2 shared TeX files and {len(images)} images to {out}')
