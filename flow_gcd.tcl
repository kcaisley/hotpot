# BSD-3-Clause
# Portions adapted from OpenROAD's BSD-3-Clause test flow and Nangate45
# configuration. Copyright (c) 2019-2026, The OpenROAD Authors.
#
# HOTPOT, aka Hands-On Tutorial: Physical Design with Open-Source Tools
#
# Run from this directory with OPENROAD_ROOT set to an OpenROAD checkout:
#   mkdir -p results/gcd
#   openroad -gui -threads max -no_init -log results/gcd/run.log -metrics results/gcd/metrics.json flow_gcd.tcl

###########################################################################
# 0. Output directories

file mkdir results/gcd
file mkdir results/gcd/images
if {[info exists env(OPENROAD_ROOT)]} {
  set openroad_root [file normalize $env(OPENROAD_ROOT)]
} elseif {[file isdirectory ../OpenROAD/test/Nangate45]} {
  set openroad_root [file normalize ../OpenROAD]
} else {
  set openroad_root [file normalize ../libs/OpenROAD]
}
if {![file isdirectory $openroad_root/test/Nangate45]} {
  error "Set OPENROAD_ROOT to an OpenROAD source checkout"
}

# Screenshot-only GUI formatting is kept here so the flow stages stay readable.
proc screenshot {view filename} {
  gui::set_display_controls "Misc/Background" color white
  gui::set_display_controls "Tracks/*" visible false
  gui::set_display_controls "Rows/*" visible false
  gui::set_display_controls "Misc/Instances/Pins" visible true
  gui::set_display_controls "Nets/*" visible false
  gui::set_display_controls "Instances/*" visible false
  gui::set_display_controls "Heat Maps/*" visible false
  gui::set_display_controls "Misc/Instances/Blockages" visible false
  gui::set_display_controls "Misc/GCell grid" visible false
  gui::set_display_controls "Misc/Scale bar" visible true

  switch $view {
    floorplan {
      gui::set_display_controls "Rows/*" visible true
      gui::set_display_controls "Misc/Instances/Pins" visible false
    }
    power_grid {
      gui::set_display_controls "Nets/*" visible true
    }
    placement {
      gui::set_display_controls "Instances/*" visible true
      gui::set_display_controls "Nets/*" visible true
    }
    clock_tree {
      gui::set_display_controls "Instances/*" visible true
      gui::set_display_controls "Nets/Clock" visible true
      gui::set_display_controls "Instances/StdCells/Clock tree/*" visible true
      gui::set_display_controls "Instances/StdCells/Sequential" visible true
    }
    default {
      error "Unknown screenshot view: $view"
    }
  }

  gui::fit
  save_image -width 1920 $filename
}

puts "OpenROAD executable: [info nameofexecutable]"
puts "OpenROAD version: [string trim [exec [info nameofexecutable] -version]]"
puts "Input checkout: $openroad_root"
puts "Input revision: [exec git -C $openroad_root rev-parse HEAD]"

utl::metric "TUTORIAL::experiment" tutorial
utl::metric "TUTORIAL::openroad_version" [string trim [exec [info nameofexecutable] -version]]
utl::metric "TUTORIAL::input_revision" [exec git -C $openroad_root rev-parse HEAD]
utl::metric "TUTORIAL::clock_period" 0.510
utl::metric "TUTORIAL::place_density" 0.80

###########################################################################
# 1. Read the technology and design

read_lef $openroad_root/test/Nangate45/Nangate45_tech.lef
read_lef $openroad_root/test/Nangate45/Nangate45_stdcell.lef
read_liberty $openroad_root/test/Nangate45/Nangate45_typ.lib
read_verilog $openroad_root/test/gcd_nangate45.v
link_design gcd

utl::metric "TUTORIAL::input_instances" [sta::network_instance_count]

###########################################################################
# 2. Timing constraints

create_clock -name core_clock -period 0.510 [get_ports clk]
set_input_delay 0.102 -clock core_clock [lsearch -inline -all -not -exact [all_inputs] [get_ports clk]]
set_output_delay 0.102 -clock core_clock [all_outputs]

report_checks -path_delay min_max -digits 3

###########################################################################
# 3. Floorplan and routing tracks

# OpenROAD computes the square floorplan and snaps it to legal Nangate45 sites.
initialize_floorplan -site FreePDK45_38x28_10R_NP_162NW_34O -utilization 40 -aspect_ratio 1 -core_space 1

# OpenROAD reads the exact routing pitches and offsets from the technology LEF.
make_tracks

# Remove purely electrical buffers inserted by synthesis so that placement
# and timing repair can rebuild them using physical information.
remove_buffers

write_db results/gcd/1_floorplan.odb
write_def results/gcd/1_floorplan.def

screenshot floorplan results/gcd/images/1_floorplan.png

###########################################################################
# 4. Tap/endcap cells and the power distribution network

tapcell -distance 120 -tapcell_master TAPCELL_X1 -endcap_master TAPCELL_X1

add_global_connection -net VDD -inst_pattern {.*} -pin_pattern {^VDD$} -power
add_global_connection -net VDD -inst_pattern {.*} -pin_pattern {^VDDPE$}
add_global_connection -net VDD -inst_pattern {.*} -pin_pattern {^VDDCE$}
add_global_connection -net VSS -inst_pattern {.*} -pin_pattern {^VSS$} -ground
add_global_connection -net VSS -inst_pattern {.*} -pin_pattern {^VSSE$}

set_voltage_domain -name CORE -power VDD -ground VSS
define_pdn_grid -name core_grid -voltage_domains CORE -pins {metal7}
add_pdn_stripe -grid core_grid -layer metal1 -followpins
# Dense vertical VSS/VDD straps.
add_pdn_stripe -grid core_grid -layer metal4 -width 1 -pitch 7 -offset 2
# Four horizontal rails: VSS, VDD, VSS, VDD, centered inside the core.
add_pdn_stripe -grid core_grid -layer metal7 -width 1 -pitch 20 -offset 3 -number_of_straps 2
add_pdn_connect -grid core_grid -layers {metal1 metal4}
add_pdn_connect -grid core_grid -layers {metal4 metal7}
pdngen

write_db results/gcd/2_power_grid.odb

screenshot power_grid results/gcd/images/2_power_grid.png

###########################################################################
# 5. Global placement and pin placement

set_global_routing_layer_adjustment metal2-metal10 0.5
set_routing_layers -signal metal2-metal10 -clock metal6-metal10
set_macro_extension 2

# First place cells while ports are still unconstrained, then place the ports
# and repeat with routability in the objective.
global_placement -density 0.80 -pad_left 2 -pad_right 2 -skip_io

screenshot placement results/gcd/images/3_global_placement_without_pins.png

place_pins -hor_layers metal3 -ver_layers metal2
global_placement -routability_driven -density 0.80 -pad_left 2 -pad_right 2

write_db results/gcd/3_global_placement.odb
write_def results/gcd/3_global_placement.def

screenshot placement results/gcd/images/3_global_placement_with_pins.png

###########################################################################
# 6. Parasitic model, design repair, and legalization

set_layer_rc -layer metal1 -resistance 5.432e-03 -capacitance 8.494e-02
set_layer_rc -layer metal2 -resistance 3.574e-03 -capacitance 8.081e-02
set_layer_rc -layer metal3 -resistance 3.574e-03 -capacitance 7.516e-02
set_layer_rc -layer metal4 -resistance 1.502e-03 -capacitance 9.663e-02
set_layer_rc -layer metal5 -resistance 1.502e-03 -capacitance 8.394e-02
set_layer_rc -layer metal6 -resistance 1.502e-03 -capacitance 7.298e-02
set_layer_rc -layer metal7 -resistance 1.883e-04 -capacitance 1.112e-01
set_layer_rc -layer metal8 -resistance 1.883e-04 -capacitance 8.528e-02
set_layer_rc -layer metal9 -resistance 3.780e-05 -capacitance 9.063e-02
set_layer_rc -layer metal10 -resistance 3.780e-05 -capacitance 6.635e-02

set_wire_rc -signal -layer metal3
set_wire_rc -clock -layer metal6
set_dont_use {CLKBUF_* AOI211_X1 OAI211_X1}

estimate_parasitics -placement
repair_design
repair_tie_fanout -separation 5 LOGIC0_X1/Z
repair_tie_fanout -separation 5 LOGIC1_X1/Z

set_placement_padding -global -left 1 -right 1
detailed_placement
check_placement -verbose

write_db results/gcd/4_repaired.odb

screenshot placement results/gcd/images/4_repaired_and_legalized.png

###########################################################################
# 7. Clock-tree synthesis and timing repair

repair_clock_inverters
clock_tree_synthesis -root_buf BUF_X4 -buf_list BUF_X4 -sink_clustering_enable -sink_clustering_max_diameter 100
repair_clock_nets
detailed_placement

set_propagated_clock [all_clocks]
estimate_parasitics -placement
repair_timing -skip_gate_cloning
detailed_placement

report_clock_skew -digits 3
report_worst_slack -min -digits 3
report_worst_slack -max -digits 3

write_db results/gcd/5_cts.odb

screenshot clock_tree results/gcd/images/5_clock_tree.png

###########################################################################
# 8. Global routing

pin_access
global_route -guide_file results/gcd/6_global_route.guide -congestion_iterations 100 -verbose
estimate_parasitics -global_routing

report_wire_length -summary -global_route
report_worst_slack -min -digits 3
report_worst_slack -max -digits 3

write_db results/gcd/6_global_route.odb

###########################################################################
# 9. Detailed routing

detailed_route -output_drc results/gcd/7_detailed_route_drc.rpt -output_maze results/gcd/7_detailed_route_maze.log -no_pin_access -verbose 0

utl::metric "TUTORIAL::detailed_route_violations" [detailed_route_num_drvs]
if {![design_is_routed]} {
  error "Detailed routing finished with unrouted nets"
}

screenshot placement results/gcd/images/7_detailed_route.png

###########################################################################
# 10. Fill, extraction, deliverables, and benchmark metrics

filler_placement {FILLCELL*}
check_placement -verbose

screenshot placement results/gcd/images/8_filled_design.png

define_process_corner -ext_model_index 0 X
extract_parasitics -ext_model_file $openroad_root/test/Nangate45/Nangate45.rcx_rules
write_spef results/gcd/gcd.spef
read_spef results/gcd/gcd.spef

write_db results/gcd/gcd_final.odb
write_def results/gcd/gcd_final.def
write_verilog -remove_cells {FILLCELL*} results/gcd/gcd_final.v
write_abstract_lef results/gcd/gcd_abstract.lef

report_checks -path_delay min_max -format full_clock_expanded -fields {input_pin slew capacitance} -digits 3
report_worst_slack -min -digits 3
report_worst_slack -max -digits 3
report_tns -digits 3
report_check_types -max_slew -max_capacitance -max_fanout -violators -digits 3
report_clock_skew -digits 3
report_power
report_design_area

# Do not silently report success when the final setup contract is violated.
set final_setup_slack [sta::worst_slack -max]
if {$final_setup_slack < 0.0} {
  error "Final setup timing failed: WNS $final_setup_slack"
}

utl::metric "TUTORIAL::utilization_percent" [expr 100.0 * [rsz::utilization]]
utl::metric "TUTORIAL::worst_slack_min" [sta::worst_slack -min]
utl::metric "TUTORIAL::worst_slack_max" [sta::worst_slack -max]
utl::metric "TUTORIAL::tns_max" [sta::total_negative_slack -max]
utl::metric "TUTORIAL::clock_skew" [expr abs([sta::worst_clock_skew -setup])]

puts ""
puts "Completed tutorial flow"
puts "Results: results/gcd"
puts "Detailed-route violations: [detailed_route_num_drvs]"

# Leave the completed design and its clock-tree data open for inspection.
gui::set_display_controls "Instances/*" visible true
gui::set_display_controls "Nets/*" visible false
gui::set_display_controls "Nets/Clock" visible true
gui::set_display_controls "Instances/StdCells/Clock tree/*" visible true
gui::set_display_controls "Instances/StdCells/Sequential" visible true
gui::set_display_controls "Tracks/*" visible false
gui::set_display_controls "Rows/*" visible false
gui::set_display_controls "Misc/GCell grid" visible false
gui::set_display_controls "Misc/Scale bar" visible true
gui::fit
gui::show_widget "Clock Tree Viewer"
gui::select_clockviewer_clock core_clock

puts "The final routed design and Clock Tree Viewer are open in the GUI."
puts "Close the GUI when you are finished inspecting the results."
