read_lef ../libs/OpenROAD/test/Nangate45/Nangate45_tech.lef
read_lef ../libs/OpenROAD/test/Nangate45/Nangate45_stdcell.lef
read_liberty ../libs/OpenROAD/test/Nangate45/Nangate45_typ.lib
read_verilog ../libs/OpenROAD/test/gcd_nangate45.v
link_design gcd
initialize_floorplan \
  -site FreePDK45_38x28_10R_NP_162NW_34O \
  -die_area {0 0 60 40} \
  -core_area {2 2 58 38}

make_tracks

#Make Power Grid and Nets
add_global_connection \
  -net VDD \
  -inst_pattern {.*} \
  -pin_pattern {^VDD$} \
  -power

add_global_connection \
 -net VSS \
 -inst_pattern {.*} \
 -pin_pattern {^VSS$} \
 -ground

set_voltage_domain \
 -name CORE \
 -power VDD \
 -ground VSS

define_pdn_grid \
 -name core_grid \
 -voltage_domain CORE

add_pdn_stripe \
 -grid core_grid \
 -layer metal1 \
 -followpins

add_pdn_stripe \
  -grid core_grid \
  -layer metal4 \
  -width 1 \
  -pitch 10 \
  -offset 2
  #-number_of_straps 2

add_pdn_stripe \
  -grid core_grid \
  -layer metal7 \
  -width 1 \
  -pitch 20 \
  -offset 3
# -number_of_straps 2

add_pdn_connect \
 -grid core_grid \
 -layers {metal1 metal4}

add_pdn_connect \
 -grid core_grid \
 -layers {metal4 metal7}

pdngen

#Place Pins/Ports
place_pins \
 -hor_layers metal3 \
 -ver_layers metal2 \
 -annealing

set_io_pin_constraint \
 -direction input \
 -region left:*

set_io_pin_constraint \
  -pin_names {resp_msg[*]} \
  -region right:* \
  -group

place_pins \
 -hor_layers metal3 \
 -ver_layers metal2 \
 -min_distance 0.8

#check_power_grid \
# -net VDD \
# check_power_grid \
# -net VSS \



set_input_delay 0.102 -clock core_clock \
  [lsearch -inline -all -not -exact [all_inputs] [get_ports clk]]

set_output_delay 0.102 -clock core_clock \
 [all_outputs]

set_global_routing_layer_adjustment \
  metal2-metal10 0.5

set_wire_rc -signal -layer metal3
set_wire_rc -clock -layer metal6
estimate_parasitics -placement



set_routing_layers \
 -signal metal2-metal10 \
 -clock metal6-metal10



global_placement \
 -timing_driven \
 -density 0.8 \
 -pad_left 2 -pad_right 2

#set_layer_rc -layer metal1 metal2 metal3 metal4 metal10


repair_design

set_placement_padding -global \
 -left 1 -right 1

detailed_placement \
 -max_displacement 10



check_placement -verbose

#Clock Tree Synthesis
create_clock -name core_clock -period 0.51 \
 [get_port clk]

repair_clock_inverters

clock_tree_synthesis -root_buf BUF_X4 \
 -buf_list BUF_X4 -sink_clustering_enable \
 -sink_clustering_max_diameter 100

repair_clock_nets

detailed_placement
set_propagated_clock [all_clocks]
estimate_parasitics -placement
repair_timing -skip_gate_cloning
detailed_placement

report_clock_skew -digits 3
report_worst_slack -max digits 3
report_worst_slack -min digits 3

#gui::set_display_controls "Nets/*" visible true
#gui::set_display_controls \
# "Instances/StdCells/Clock tree/*" visible true
#gui::set_display_controls \
#"Instances/StdCells/Sequential" visible true

#Global routing


set_global_routing_layer_adjustment * 0.3

set_routing_alpha 0.0

#global_route_debug -net signal \
# -st -rst -tree2D -tree3D

global_route \
 -guide_file results/route.guide \
 -congestion_iterations 100 \
 -critical_nets_percentage 10

read_guides results/route.guide

report_wire_length -global_route \
 -summary

estimate_parasitics -global_routing
report_checks -path_delay max

repair_antennas -iterations 5
pin_access
detailed_route
