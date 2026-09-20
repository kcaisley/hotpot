DECKS := intro filetypes def lib floorplanning
.PHONY: all help
all: $(addsuffix .pdf,$(DECKS))

help:
	@printf '%s\n' 'Build dependencies: TeX Live (Beamer, Latin Modern, listings, TikZ) and latexmk.' 'Build all decks: make' 'Build one deck: make intro.pdf' 'Floorplanning exercises: install OpenROAD and set OPENROAD_ROOT to its source checkout.' 'Starter, from repository root: openroad -gui flow.tcl' 'Full example, from slides/: openroad -exit examples/floorplanning/floorplan.tcl' 'Public Ariane GUI example: make -C examples/ariane run gui (OpenROAD + Python 3)'

%.pdf: %.tex style.tex $(shell find images -type f)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@
