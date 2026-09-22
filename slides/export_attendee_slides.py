"""Export presentation decks, images and workshop examples to the public checkout."""
from pathlib import Path
import argparse
import re
import shutil

P = Path(__file__).resolve().parent
DECKS = ['intro', 'filetypes', 'def', 'lib', 'floorplanning',
         'placement', 'cts', 'routing', 'finishing']
DEV_ONLY = (
    'flow_gcd.tcl', 'flow_ariane.tcl',
    'open_gcd.tcl', 'open_ariane.tcl',
)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('checkout', type=Path, help='Checkout of the attendee main branch')
parser.add_argument('--deck', action='append', choices=DECKS)
args = parser.parse_args()
selected = args.deck or DECKS
out = args.checkout.resolve() / 'slides'
out.mkdir(parents=True, exist_ok=True)
if 'floorplanning' in selected:
    shutil.rmtree(out/'images/floorplanning', ignore_errors=True)
images = set()

def graphic(match):
    src = Path(match[2])
    assert (P/src).is_file(), src
    dest = src if src.parts[0] == 'images' else Path('images') / src
    (out/dest).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(P/src, out/dest)
    images.add(dest.as_posix())
    return r'\includegraphics' + (match[1] or '') + '{' + dest.as_posix() + '}'

def listing(match):
    code = (P/match[2]).read_text().rstrip()
    return '\n' + r'\begin{lstlisting}' + (match[1] or '') + '\n' + code + '\n' + r'\end{lstlisting}' + '\n'

for name in selected + ['style']:
    source = (P/f'{name}.tex').read_text()
    source = re.sub(r'\\includegraphics(\[[^\]]*\])?\{([^}]+)\}', graphic, source)
    source = re.sub(r'\\lstinputlisting(\[[^\]]*\])?\{([^}]+)\}', listing, source)
    # Beamer needs fragile frames for the now-embedded, editable listings.
    def frame(match):
        content = match[0]
        if r'\begin{lstlisting}' in content and not re.match(r'\\begin\{frame\}\[[^]]*fragile', content):
            content = content.replace(r'\begin{frame}', r'\begin{frame}[fragile]', 1)
        return content
    source = re.sub(r'\\begin\{frame\}.*?\\end\{frame\}', frame, source, flags=re.S)
    (out/f'{name}.tex').write_text(source)
for name in selected:
    shutil.copy2(P/f'{name}.pdf', out/f'{name}.pdf')

# Preserve standalone contributor decks that live beside the named workshop
# decks (for example openroad_global_routing.pdf).
for companion in P.glob('*.pdf'):
    shutil.copy2(companion, out/companion.name)

if 'floorplanning' in selected:
    checkpoint = args.checkout.resolve()/'checkpoints/ariane'
    shutil.copytree(P/'examples/ariane/checkpoint', checkpoint, dirs_exist_ok=True)
    shutil.rmtree(out/'examples', ignore_errors=True)
    shutil.copy2(P/'examples/floorplanning/flow.tcl', args.checkout.resolve()/'flow.tcl')

# The public checkout is derived from dev.  Remove stale dev-only artifacts
# even when the destination was exported previously.
for dev_only in DEV_ONLY:
    (args.checkout.resolve()/dev_only).unlink(missing_ok=True)
shutil.rmtree(args.checkout.resolve()/'results', ignore_errors=True)
shutil.rmtree(out/'results', ignore_errors=True)

(out/'Makefile').unlink(missing_ok=True)
(out/'.gitignore').write_text('build/\nresults/\n*.aux\n*.log\n*.out\n*.nav\n*.snm\n*.toc\n*.vrb\n*.fls\n*.fdb_latexmk\n')
print(f'Exported {len(selected)} decks, 1 shared style file and {len(images)} images to {out}')
