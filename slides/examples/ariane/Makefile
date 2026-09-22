.PHONY: inputs run gui help
inputs:
	python3 fetch.py
run: inputs
	openroad -no_init -exit run.tcl
gui: inputs
	openroad -no_init -gui gui.tcl
help:
	@printf '%s\n' 'Dependencies: OpenROAD with GUI; Python 3 for downloads.' 'make gui: unpack and open the included completed checkpoint.' 'Checkpoint generated with OpenROAD 26Q1-2913-gd1719d5edc; make run rebuilds with your binary.' 'make run: rebuild from the mapped netlist through PDN, placement, CTS, routing, fillers, and RC extraction.' 'Power estimates assume 0.1 input transitions/cycle, 50% duty, and a 10 ns clock; no workload trace.'
