# Open the completed GCD run for inspection.
# Run from anywhere with:
#   openroad -gui -no_init open_gcd.tcl

set root [file dirname [file normalize [info script]]]
cd $root

if {[info exists env(OPENROAD_ROOT)]} {
  set openroad_root [file normalize $env(OPENROAD_ROOT)]
} elseif {[file isdirectory ../OpenROAD/test/Nangate45]} {
  set openroad_root [file normalize ../OpenROAD]
} elseif {[file isdirectory ../libs/OpenROAD/test/Nangate45]} {
  set openroad_root [file normalize ../libs/OpenROAD]
} else {
  error "Set OPENROAD_ROOT to an OpenROAD source checkout"
}

# Load the final routed database and the extracted post-route parasitics.
read_db results/gcd/gcd_final.odb
read_liberty $openroad_root/test/Nangate45/Nangate45_typ.lib

# Recreate the timing contract used by the current GCD flow.
create_clock -name core_clock -period 0.510 [get_ports clk]
set_input_delay 0.102 -clock core_clock \
  [lsearch -inline -all -not -exact [all_inputs] [get_ports clk]]
set_output_delay 0.102 -clock core_clock [all_outputs]
set_propagated_clock [all_clocks]
read_spef results/gcd/gcd.spef

puts "=== GCD timing ==="
report_worst_slack -min -digits 3
report_worst_slack -max -digits 3
report_tns -digits 3
report_clock_skew -digits 3
puts "=== GCD power and area ==="
report_power -digits 3
report_design_area

if {[gui::enabled]} {
  gui::set_title "HOTPOT - final routed GCD"
  gui::set_display_controls "Misc/Background" color white
  gui::set_display_controls "Layers/*" visible true
  gui::set_display_controls "Instances/*" visible true
  gui::set_display_controls "Nets/*" visible false
  gui::set_display_controls "Nets/Clock" visible true
  gui::set_display_controls "Instances/StdCells/Clock tree/*" visible true
  gui::set_display_controls "Instances/StdCells/Sequential" visible true
  gui::set_display_controls "Nets/Power" visible false
  gui::set_display_controls "Nets/Ground" visible false
  gui::set_display_controls "Heat Maps/*" visible true
  gui::set_display_controls "Misc/Scale bar" visible true
  gui::set_heatmap Power rebuild
  gui::set_heatmap Power ShowLegend 1
  gui::show_widget "Inspector"
  gui::show_widget "Hierarchy Browser"
  gui::show_widget "Timing Report"
  gui::update_timing_report
  gui::show_worst_path -setup
  gui::show_widget "Clock Tree Viewer"
  gui::select_clockviewer_clock core_clock
  gui::fit
}
