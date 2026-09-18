.PHONY: all figures overview recap stages finishing
all: intro.pdf filetypes.pdf lib.pdf def.pdf floorplanning.pdf

floorplanning.pdf: floorplanning.tex style.tex $(wildcard assets/floorplanning/*.png)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@

.PHONY: floorplanning-figures
floorplanning-figures:
	python3 render_floorplanning.py

intro.pdf filetypes.pdf lib.pdf def.pdf: %.pdf: %.tex style.tex $(wildcard assets/extension/*.pdf) assets/nxp-die-slide.jpg assets/lefdef-cover.png assets/spice-homepage.png $(wildcard examples/*) $(wildcard assets/*.pdf) $(wildcard layout/*_labeled.pdf) assets/openroad-flow.png assets/dmc65-layout.png assets/arithmeum-house.jpg $(wildcard assets/fabs/*.pdf)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@

figures:
	python3 build_digital.py
	python3 annotate_top.py
	rsvg-convert -f pdf -o assets/top-detail.pdf assets/top-detail.svg
	rsvg-convert -f pdf -o assets/top-opendb.pdf assets/top-opendb.svg
	pdflatex -interaction=batchmode -halt-on-error -output-directory assets assets/inverter-cmos.tex
	pdflatex -interaction=batchmode -halt-on-error -output-directory assets assets/nand-cmos.tex

.PHONY: layouts
layouts:
	cd ../.. && QT_QPA_PLATFORM=offscreen klayout -b -r docs/slides/layout/build_layout.py
	python3 layout/render_layout.py
	python3 layout/annotate_layout.py

.PHONY: fabs
fabs:
	python3 build_fabs.py
	python3 prepare_cmos.py

.PHONY: extensions
extensions:
	python3 formats/build_design.py
	openroad -exit formats/roundtrip.tcl > formats/roundtrip.log 2>&1
	openroad -exit formats/reload.tcl > formats/reload.log 2>&1
	openroad -exit formats/timing_session.tcl > formats/timing_session.log 2>&1
	openroad -exit formats/recap_import.tcl > formats/recap_import.log 2>&1
	python3 layout/vector_abstract.py
	python3 build_extension.py
	cd simulation && ngspice -b inverter_test.sp > simulation.log 2>&1
	python3 simulation/plot_results.py
	python3 layout/vector_abstract.py
	python3 build_extension.py
	pdflatex -interaction=batchmode -halt-on-error -output-directory assets assets/loaded-inverter.tex

overview:
	python3 build_overview.py

stages:
	python3 render_stages.py

finishing:
	python3 build_finished_layout.py

recap:
	python3 build_recap.py
