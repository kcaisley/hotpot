set root [file dirname [file normalize [info script]]]
set here [file join $root docs/slides/examples/ariane]
if {![file isdirectory $here]} {set here [file join $root slides/examples/ariane]}
source $here/libraries.tcl
set work $root/results/ariane
file mkdir $work
set_thread_count 8
read_lef $inputs/NangateOpenCellLibrary.tech.lef
read_lef $inputs/NangateOpenCellLibrary.macro.mod.lef
read_lef $inputs/fakeram45_256x16.lef
read_verilog $inputs/ariane.v
link_design ariane
create_clock -name core_clock -period 10.0 [get_ports clk_i]
set_power_activity -input -activity 0.1 -duty 0.5
initialize_floorplan -site FreePDK45_38x28_10R_NP_162NW_34O -utilization 50 -aspect_ratio 1 -core_space 5
make_tracks
place_pins -hor_layers metal5 -ver_layers metal6
rtl_macro_placer -halo_width 8 -halo_height 8
write_db $work/macros.odb
tapcell -distance 120 -tapcell_master TAPCELL_X1 -endcap_master TAPCELL_X1
source $here/pdn.tcl
write_db $work/floorplan.odb
source $here/rc.tcl
set_global_routing_layer_adjustment metal2-metal3 0.5
set_global_routing_layer_adjustment metal4-metal10 0.25
set_routing_layers -signal metal2-metal10 -clock metal4-metal10
set_macro_extension 0
set_dont_use {CLKBUF_* AOI211_X1 OAI211_X1}
repair_tie_fanout -separation 5 LOGIC0_X1/Z
repair_tie_fanout -separation 5 LOGIC1_X1/Z
remove_buffers
global_placement -routability_driven -density 0.55 -pad_left 2 -pad_right 2
estimate_parasitics -placement
repair_design
set_placement_padding -global -left 1 -right 1
detailed_placement
place_pins -hor_layers metal5 -ver_layers metal6 -min_distance 2
write_db $work/placed.odb
write_def $work/placed.def
source $here/finish.tcl
