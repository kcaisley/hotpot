set here [file dirname [file normalize [info script]]]
read_db $here/results/placed.odb
source $here/libraries.tcl
create_clock -name core_clock -period 1.0 [get_ports clk_i]
set_power_activity -input -activity 0.1 -duty 0.5
set_wire_rc -signal -layer metal3
set_wire_rc -clock -layer metal5
estimate_parasitics -placement
gui::set_heatmap Power rebuild
gui::set_heatmap Power ShowLegend 1
gui::set_title "HOTPOT - Ariane RISC-V"
gui::set_display_controls "Misc/Module view" visible true
gui::show_widget "Hierarchy Browser"
gui::show_widget "Inspector"
gui::fit
