"""Export the four self-contained presentation decks into a public checkout.

Run on the development branch. This copies only TeX, presentation PDFs, used
images; generators, databases and simulations stay here.
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
print(f'Exported {len(DECKS)} decks, 2 shared TeX files and {len(images)} images to {out}')
