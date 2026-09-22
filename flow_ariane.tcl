# Run from the repository root after `make inputs` in
# slides/examples/ariane.  All paths below are repository-root-relative.

set_thread_count 8
read_liberty slides/examples/ariane/inputs/NangateOpenCellLibrary_typical.lib
read_liberty slides/examples/ariane/inputs/fakeram45_256x16.lib
read_lef slides/examples/ariane/inputs/NangateOpenCellLibrary.tech.lef
read_lef slides/examples/ariane/inputs/NangateOpenCellLibrary.macro.mod.lef
read_lef slides/examples/ariane/inputs/fakeram45_256x16.lef
read_verilog slides/examples/ariane/inputs/ariane.v
link_design ariane

create_clock -name core_clock -period 10.0 [get_ports clk_i]
set_power_activity -input -activity 0.1 -duty 0.5

# Build the initial floorplan from utilization, aspect ratio, and site rules.
initialize_floorplan -site FreePDK45_38x28_10R_NP_162NW_34O -utilization 50 -aspect_ratio 1 -core_space 5
make_tracks

# We place without global cell placement, so we assume all cells in center
place_pins -hor_layers metal5 -ver_layers metal6
rtl_macro_placer -halo_width 8 -halo_height 8
write_db results/ariane/macros.odb

# Add tap and endcap cells before constructing the power grid.
tapcell -distance 120 -tapcell_master TAPCELL_X1 -endcap_master TAPCELL_X1

# Connect cell power pins to the CORE voltage domain.
add_global_connection -net VDD -inst_pattern {.*} -pin_pattern {^VDD$} -power
add_global_connection -net VSS -inst_pattern {.*} -pin_pattern {^VSS$} -ground
global_connect
set_voltage_domain -name CORE -power VDD -ground VSS

# Define the standard-cell power grid on metal1, metal4, and metal7.
define_pdn_grid -name core -voltage_domains CORE -pins {metal7}
add_pdn_stripe -grid core -layer metal1 -width 0.17 -followpins
add_pdn_stripe -grid core -layer metal4 -width 0.48 -pitch 56 -offset 2
add_pdn_stripe -grid core -layer metal7 -width 1.4 -pitch 30 -offset 2
add_pdn_connect -grid core -layers {metal1 metal4}
add_pdn_connect -grid core -layers {metal4 metal7}

# Define a macro grid with a halo, then connect it up through metal7.
define_pdn_grid -name macros -voltage_domains CORE -macro -orient {R0 R180 MX MY} -halo {2 2 2 2} -default
add_pdn_stripe -grid macros -layer metal5 -width 0.93 -pitch 10 -offset 2
add_pdn_stripe -grid macros -layer metal6 -width 0.93 -pitch 10 -offset 2
add_pdn_connect -grid macros -layers {metal4 metal5}
add_pdn_connect -grid macros -layers {metal5 metal6}
add_pdn_connect -grid macros -layers {metal6 metal7}
pdngen
write_db results/ariane/floorplan.odb

# RC values let timing repair estimate wire delay before routing.
set_layer_rc -layer metal1 -resistance 5.4286e-03 -capacitance 7.41819E-02
set_layer_rc -layer metal2 -resistance 3.57167E-03 -capacitance 8.33611E-02
set_layer_rc -layer metal3 -resistance 3.57147E-03 -capacitance 1.03981E-01
set_layer_rc -layer metal4 -resistance 1.50001E-03 -capacitance 1.19150E-01
set_layer_rc -layer metal5 -resistance 1.50000E-03 -capacitance 1.09256E-01
set_layer_rc -layer metal6 -resistance 1.50000E-03 -capacitance 1.14168E-01
set_layer_rc -layer metal7 -resistance 1.87501E-04 -capacitance 1.17491E-01
set_layer_rc -layer metal8 -resistance 1.87501E-04 -capacitance 9.45346E-02
set_layer_rc -layer metal9 -resistance 3.74996E-05 -capacitance 1.06091E-01
set_layer_rc -layer metal10 -resistance 3.75000E-05 -capacitance 7.37095E-01
set_wire_rc -signal -layer metal3
set_wire_rc -clock -layer metal5

# Keep global routing aware of the available signal and clock metal.
set_global_routing_layer_adjustment metal2-metal3 0.5
set_global_routing_layer_adjustment metal4-metal10 0.25
set_routing_layers -signal metal2-metal10 -clock metal4-metal10
set_macro_extension 0
set_dont_use {CLKBUF_* AOI211_X1 OAI211_X1}

# Remove synthesis-only buffers, place cells, and legalize them in rows.
repair_tie_fanout -separation 5 LOGIC0_X1/Z
repair_tie_fanout -separation 5 LOGIC1_X1/Z
remove_buffers
global_placement -routability_driven -density 0.55 -pad_left 2 -pad_right 2
estimate_parasitics -placement
repair_design
set_placement_padding -global -left 1 -right 1
detailed_placement
place_pins -hor_layers metal5 -ver_layers metal6 -min_distance 2
write_db results/ariane/placed.odb
write_def results/ariane/placed.def

# Check the power grid before building the clock tree.
check_power_grid -net VDD
check_power_grid -net VSS

# Build and repair the physical clock network.
repair_clock_inverters
clock_tree_synthesis -root_buf BUF_X4 -buf_list {BUF_X4 BUF_X8 BUF_X16} -sink_clustering_enable -sink_clustering_max_diameter 100
repair_clock_nets
detailed_placement
set_propagated_clock [all_clocks]
estimate_parasitics -placement
repair_timing -skip_gate_cloning
detailed_placement
global_connect
write_db results/ariane/cts.odb

# Reserve routing resources and estimate parasitics from the global routes.
pin_access
global_route -guide_file results/ariane/route.guide -congestion_iterations 100 -congestion_report_file results/ariane/congestion.rpt -verbose
repair_antennas -iterations 5
write_db results/ariane/global_route.odb

# Convert global guides into exact wire and via shapes.
detailed_route -output_drc results/ariane/route_drc.rpt -output_maze results/ariane/maze.log -no_pin_access -verbose 1
write_db results/ariane/routed.odb
check_antennas
design_is_routed -verbose
detailed_route_num_drvs

# Complete standard-cell rows, validate the result, and save final outputs.
filler_placement {FILLCELL_X32 FILLCELL_X16 FILLCELL_X8 FILLCELL_X4 FILLCELL_X2 FILLCELL_X1}
global_connect
check_placement -verbose
check_power_grid -net VDD
check_power_grid -net VSS
write_db results/ariane/final.odb
write_def results/ariane/final.def
write_verilog results/ariane/final.v
write_sdc results/ariane/final.sdc
define_process_corner -ext_model_index 0 X
extract_parasitics -ext_model_file slides/examples/ariane/inputs/rcx_patterns.rules
write_spef results/ariane/final.spef
read_spef results/ariane/final.spef
report_power
report_worst_slack -max
report_worst_slack -min
