set here [file dirname [file normalize [info script]]]
source $here/start.tcl

initialize_floorplan -site FreePDK45_38x28_10R_NP_162NW_34O -utilization 40 -aspect_ratio 1 -core_space 1
make_tracks
remove_buffers
write_db $work/01_floorplan.odb

tapcell -distance 120 -tapcell_master TAPCELL_X1 -endcap_master TAPCELL_X1
add_global_connection -net VDD -inst_pattern {.*} -pin_pattern {^VDD$} -power
add_global_connection -net VSS -inst_pattern {.*} -pin_pattern {^VSS$} -ground
set_voltage_domain -name CORE -power VDD -ground VSS
define_pdn_grid -name core_grid -voltage_domains CORE
add_pdn_stripe -grid core_grid -layer metal1 -followpins
add_pdn_stripe -grid core_grid -layer metal4 -width 1 -pitch 7 -offset 2
add_pdn_stripe -grid core_grid -layer metal7 -width 1 -pitch 20 -offset 3 -number_of_straps 2
add_pdn_connect -grid core_grid -layers {metal1 metal4}
add_pdn_connect -grid core_grid -layers {metal4 metal7}
pdngen
write_db $work/02_power.odb

set_global_routing_layer_adjustment metal2-metal10 0.5
set_routing_layers -signal metal2-metal10 -clock metal6-metal10
global_placement -density 0.80 -pad_left 2 -pad_right 2 -skip_io
write_db $work/03_before_pins.odb
place_pins -hor_layers metal3 -ver_layers metal2
write_db $work/04_pins.odb
write_def $work/04_pins.def

if {[gui::enabled]} {source $here/view.tcl}
