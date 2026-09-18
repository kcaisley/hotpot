# HOTPOT presentations

| Presentation | PDF | Editable source |
| --- | --- | --- |
| Introduction and logistics | [intro.pdf](intro.pdf) | [intro.tex](intro.tex) |
| Design file types | [filetypes.pdf](filetypes.pdf) | [filetypes.tex](filetypes.tex) |
| DEF | [def.pdf](def.pdf) | [def.tex](def.tex) |
| Liberty | [lib.pdf](lib.pdf) | [lib.tex](lib.tex) |

All decks share `slide_style.tex` and the `images/` folder.
`extension_slides.tex` contains the LEF and timing-concept slides included by
`filetypes.tex`. Code examples are embedded directly in the TeX sources.

To rebuild, install TeX Live with Beamer, Latin Modern, listings and latexmk,
then run `make` here. OpenROAD, KLayout, ngspice and Python are not required to
rebuild these slides: the generated figures are included.

Full development sources and figure generators live on the
[GitHub dev branch](https://github.com/kcaisley/hotpot/tree/dev).
See [SOURCES.md](SOURCES.md) and the TeX speaker notes for figure attribution.
