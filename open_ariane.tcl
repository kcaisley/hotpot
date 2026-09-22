# Open the completed Ariane run for inspection.
# Run from anywhere with:
#   openroad -gui -no_init open_ariane.tcl

set root [file dirname [file normalize [info script]]]
cd $root

# Load the final routed database, timing libraries, constraints, and SPEF.
read_db results/ariane/final.odb
read_liberty slides/examples/ariane/inputs/NangateOpenCellLibrary_typical.lib
read_liberty slides/examples/ariane/inputs/fakeram45_256x16.lib
read_sdc results/ariane/final.sdc

# Match the RC and power setup used by the Ariane flow before reporting.
foreach {layer resistance capacitance} {
  metal1  5.4286e-03 7.41819E-02
  metal2  3.57167e-03 8.33611E-02
  metal3  3.57147e-03 1.03981E-01
  metal4  1.50001e-03 1.19150E-01
  metal5  1.50000e-03 1.09256E-01
  metal6  1.50000e-03 1.14168E-01
  metal7  1.87501e-04 1.17491E-01
  metal8  1.87501e-04 9.45346E-02
  metal9  3.74996e-05 1.06091E-01
  metal10 3.75000e-05 7.37095E-01
} {
  set_layer_rc -layer $layer -resistance $resistance -capacitance $capacitance
}
set_wire_rc -signal -layer metal3
set_wire_rc -clock -layer metal5
read_spef results/ariane/final.spef
set_power_activity -input -activity 0.1 -duty 0.5

puts "=== Ariane timing ==="
report_worst_slack -min -digits 3
report_worst_slack -max -digits 3
report_tns -digits 3
# The Clock Tree Viewer below exposes the skew details without running the
# expensive full skew report on the large routed Ariane database.
puts "=== Ariane power and area ==="
report_power -digits 3
report_design_area

if {[gui::enabled]} {
  gui::set_title "HOTPOT - final routed Ariane RISC-V"
  gui::set_display_controls "Misc/Background" color white
  gui::set_display_controls "Layers/*" visible true
  gui::set_display_controls "Instances/*" visible true
  gui::set_display_controls "Nets/*" visible true
  gui::set_display_controls "Nets/Clock" visible true
  gui::set_display_controls "Instances/StdCells/Clock tree/*" visible true
  gui::set_display_controls "Instances/StdCells/Sequential" visible true
  gui::set_display_controls "Nets/Power" visible true
  gui::set_display_controls "Nets/Ground" visible true
  gui::set_display_controls "Heat Maps/*" visible true
  gui::set_display_controls "Misc/Module view" visible true
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
