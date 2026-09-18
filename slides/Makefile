DECKS := intro filetypes def lib
.PHONY: all
all: $(addsuffix .pdf,$(DECKS))

%.pdf: %.tex slide_style.tex extension_slides.tex $(shell find images -type f)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@
