DECKS := intro filetypes def lib
.PHONY: all help
all: $(addsuffix .pdf,$(DECKS))

help:
	@printf '%s\n' 'Build dependencies: TeX Live (Beamer, Latin Modern, listings) and latexmk.' 'Build all decks: make' 'Build one deck: make intro.pdf'

%.pdf: %.tex style.tex $(shell find images -type f)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@
