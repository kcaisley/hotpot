check_power_grid -net VDD
check_power_grid -net VSS
repair_clock_inverters
clock_tree_synthesis -root_buf BUF_X4 -buf_list {BUF_X4 BUF_X8 BUF_X16} -sink_clustering_enable -sink_clustering_max_diameter 100
repair_clock_nets
detailed_placement
set_propagated_clock [all_clocks]
estimate_parasitics -placement
repair_timing -skip_gate_cloning
detailed_placement
global_connect
write_db $work/cts.odb
pin_access
global_route -guide_file $work/route.guide -congestion_iterations 100 -congestion_report_file $work/congestion.rpt -verbose
repair_antennas -iterations 5
write_db $work/global_route.odb
detailed_route -output_drc $work/route_drc.rpt -output_maze $work/maze.log -no_pin_access -verbose 1
write_db $work/routed.odb
for {set attempt 0} {[check_antennas] && $attempt < 5} {incr attempt} {
  repair_antennas
  detailed_route -output_drc $work/route_drc.rpt -output_maze $work/maze.log -no_pin_access -verbose 1
}
if {[check_antennas]} {error "Antenna violations remain"}
if {![design_is_routed -verbose]} {error "Unrouted nets remain"}
set drvs [detailed_route_num_drvs]
puts "FINAL routing violations: $drvs"
if {$drvs != 0} {error "Detailed routing has $drvs violations"}
filler_placement {FILLCELL_X32 FILLCELL_X16 FILLCELL_X8 FILLCELL_X4 FILLCELL_X2 FILLCELL_X1}
global_connect
check_placement -verbose
check_power_grid -net VDD
check_power_grid -net VSS
write_db $work/final.odb
write_def $work/final.def
write_verilog $work/final.v
write_sdc $work/final.sdc
define_process_corner -ext_model_index 0 X
extract_parasitics -ext_model_file $inputs/rcx_patterns.rules
write_spef $work/final.spef
read_spef $work/final.spef
report_power
report_worst_slack -max
report_worst_slack -min
