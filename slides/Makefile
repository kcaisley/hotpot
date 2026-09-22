.PHONY: all figures overview recap stages finishing placement cts routing gui-evidence gui-screenshots
all: intro.pdf filetypes.pdf lib.pdf def.pdf floorplanning.pdf placement.pdf cts.pdf routing.pdf finishing.pdf

floorplanning.pdf: floorplanning.tex style.tex $(wildcard images/floorplanning/*.png)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@

.PHONY: floorplanning-figures
floorplanning-figures:
	python3 render_floorplanning.py

intro.pdf filetypes.pdf lib.pdf def.pdf: %.pdf: %.tex style.tex $(wildcard images/extension/*.pdf) images/nxp-die-slide.jpg images/lefdef-cover.png images/spice-homepage.png $(wildcard examples/*) $(wildcard images/*.pdf) $(wildcard layout/*_labeled.pdf) images/openroad-flow.png images/dmc65-layout.png images/arithmeum-house.jpg $(wildcard images/fabs/*.pdf)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@

placement.pdf: placement.tex style.tex $(wildcard images/placement/*)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@

cts.pdf: cts.tex style.tex $(wildcard images/placement/*) $(wildcard images/cts/*) $(wildcard images/routing/*) $(wildcard images/floorplanning/*)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@

gui-evidence:
	QT_QPA_PLATFORM=offscreen HOTPOT_GUI_DESIGN=gcd HOTPOT_GUI_VIEW=clock_layout openroad -gui -no_init -exit render_gui_evidence.tcl
	QT_QPA_PLATFORM=offscreen HOTPOT_GUI_DESIGN=gcd HOTPOT_GUI_VIEW=timing openroad -gui -no_init -exit render_gui_evidence.tcl
	QT_QPA_PLATFORM=offscreen HOTPOT_GUI_DESIGN=gcd HOTPOT_GUI_VIEW=clock_viewer openroad -gui -no_init -exit render_gui_evidence.tcl
	QT_QPA_PLATFORM=offscreen HOTPOT_GUI_DESIGN=ariane HOTPOT_GUI_VIEW=clock_layout openroad -gui -no_init -exit render_gui_evidence.tcl
	QT_QPA_PLATFORM=offscreen HOTPOT_GUI_DESIGN=ariane HOTPOT_GUI_VIEW=timing openroad -gui -no_init -exit render_gui_evidence.tcl
	QT_QPA_PLATFORM=offscreen HOTPOT_GUI_DESIGN=ariane HOTPOT_GUI_VIEW=clock_viewer openroad -gui -no_init -exit render_gui_evidence.tcl
	QT_QPA_PLATFORM=offscreen HOTPOT_GUI_DESIGN=ariane HOTPOT_GUI_VIEW=power_heatmap openroad -gui -no_init -exit render_gui_evidence.tcl
	QT_QPA_PLATFORM=offscreen HOTPOT_GUI_DESIGN=ariane HOTPOT_GUI_VIEW=routing_heatmap openroad -gui -no_init -exit render_gui_evidence.tcl

gui-screenshots:
	bash capture_timing_gui.sh ariane

routing.pdf: routing.tex style.tex $(wildcard images/routing/*) $(wildcard images/finishing/*)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@

finishing.pdf: finishing.tex style.tex $(wildcard images/finishing/*) $(wildcard images/cts/*)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build $<
	cp build/$@ $@

figures:
	python3 build_digital.py
	python3 annotate_top.py
	rsvg-convert -f pdf -o images/top-detail.pdf images/top-detail.svg
	rsvg-convert -f pdf -o images/top-opendb.pdf images/top-opendb.svg
	pdflatex -interaction=batchmode -halt-on-error -output-directory images images/inverter-cmos.tex
	pdflatex -interaction=batchmode -halt-on-error -output-directory images images/nand-cmos.tex

.PHONY: layouts
layouts:
	cd .. && QT_QPA_PLATFORM=offscreen klayout -b -r slides/layout/build_layout.py
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
	pdflatex -interaction=batchmode -halt-on-error -output-directory images images/loaded-inverter.tex

overview:
	python3 build_overview.py

stages:
	python3 render_stages.py

finishing:
	python3 build_finished_layout.py

recap:
	python3 build_recap.py
