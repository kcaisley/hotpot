.PHONY: inputs run gui help
inputs:
	python3 fetch.py
run: inputs
	openroad -no_init -exit run.tcl
gui:
	openroad -no_init -gui gui.tcl
help:
	@printf '%s\n' 'Dependencies: OpenROAD with GUI; Python 3 for downloads.' 'make run: download pinned inputs, place Ariane, and save ODB + DEF.' 'make gui: open the placed checkpoint with timing and power libraries.' 'Power estimates assume 0.1 input transitions/cycle, 50% duty, and a 1 ns clock; no workload trace.'
