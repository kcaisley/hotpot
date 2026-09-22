# Generate GUI evidence from the completed GCD checkpoint.
# Run from the repository root with OpenROAD's GUI build:
#   QT_QPA_PLATFORM=offscreen openroad -gui -no_init -exit slides/render_cts_gui.tcl

set root [file normalize [file join [file dirname [file normalize [info script]]] ..]]
set openroad_root [file normalize [file join $root ../libs/OpenROAD]]
set out [file join $root slides images cts]
file mkdir $out

read_db [file join $root results gcd gcd_final.odb]
read_liberty [file join $openroad_root test Nangate45 Nangate45_typ.lib]

# Recreate the GCD timing contract and activate extracted RC.
create_clock -name core_clock -period 0.510 [get_ports clk]
set_input_delay 0.102 -clock core_clock \
  [lsearch -inline -all -not -exact [all_inputs] [get_ports clk]]
set_output_delay 0.102 -clock core_clock [all_outputs]
set_propagated_clock [all_clocks]
read_spef [file join $root results gcd gcd.spef]

gui::set_title "HOTPOT - GCD timing path"
gui::set_display_controls "Misc/Background" color white
gui::set_display_controls "Instances/*" visible true
gui::set_display_controls "Instances/StdCells/Clock tree/*" visible true
gui::set_display_controls "Instances/StdCells/Sequential" visible true
gui::set_display_controls "Nets/*" visible false
gui::set_display_controls "Nets/Clock" visible true
gui::set_display_controls "Nets/Signal" visible true
gui::set_display_controls "Layers/*" visible true
gui::set_display_controls "Misc/Instances/Pins" visible true
gui::set_display_controls "Heat Maps/*" visible false
gui::set_display_controls "Misc/Scale bar" visible true

# Populate and select the worst setup path in the GUI.
gui::show_widget "Timing Report"
gui::update_timing_report
gui::show_worst_path -setup
gui::fit
set block [ord::get_db_block]
set die [$block getDieArea]
set units [$block getDbUnitsPerMicron]
gui::save_image [file join $out gcd_timing_path.png] \
  [expr {double([$die xMin]) / $units}] \
  [expr {double([$die yMin]) / $units}] \
  [expr {double([$die xMax]) / $units}] \
  [expr {double([$die yMax]) / $units}] 1920

# Save the actual Clock Tree Viewer diagram for core_clock.
gui::show_widget "Clock Tree Viewer"
gui::select_clockviewer_clock core_clock
save_clocktree_image -clock core_clock -width 1600 -height 1000 \
  [file join $out gcd_clock_tree_viewer.png]

exit
