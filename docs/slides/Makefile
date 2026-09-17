.PHONY: all figures
all: background.pdf

background.pdf: background.tex extension_slides.tex $(wildcard assets/extension/*.pdf) assets/nxp-die-slide.jpg assets/lefdef-cover.png assets/spice-homepage.png $(wildcard examples/*) $(wildcard assets/*.pdf) $(wildcard layout/*_labeled.pdf) assets/openroad-flow.png assets/dmc65-layout.png $(wildcard assets/fabs/*.pdf)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build background.tex
	cp build/background.pdf background.pdf

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
	python3 formats/build_top.py
	openroad -exit formats/roundtrip.tcl > formats/roundtrip.log 2>&1
	openroad -exit formats/reload.tcl > formats/reload.log 2>&1
	openroad -exit formats/timing_session.tcl > formats/timing_session.log 2>&1
	python3 build_extension.py
	cd simulation && ngspice -b inverter_test.sp > simulation.log 2>&1
	python3 simulation/plot_results.py
	python3 build_extension.py
	pdflatex -interaction=batchmode -halt-on-error -output-directory assets assets/loaded-inverter.tex
