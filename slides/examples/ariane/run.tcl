set here [file dirname [file normalize [info script]]]
source $here/libraries.tcl
set work $here/results
file mkdir $work
set_thread_count 8
read_lef $inputs/NangateOpenCellLibrary.tech.lef
read_lef $inputs/NangateOpenCellLibrary.macro.mod.lef
read_lef $inputs/fakeram45_256x16.lef
read_verilog $inputs/ariane.v
link_design ariane
create_clock -name core_clock -period 1.0 [get_ports clk_i]
set_power_activity -input -activity 0.1 -duty 0.5
initialize_floorplan -site FreePDK45_38x28_10R_NP_162NW_34O -die_area {0 0 1500 1500} -core_area {10 12 1448 1448}
make_tracks
place_pins -hor_layers metal3 -ver_layers metal2
rtl_macro_placer -halo_width 5 -halo_height 5
write_db $work/macros.odb
set_wire_rc -signal -layer metal3
set_wire_rc -clock -layer metal5
global_placement -density 0.55
detailed_placement
write_db $work/placed.odb
write_def $work/placed.def
estimate_parasitics -placement
report_power
