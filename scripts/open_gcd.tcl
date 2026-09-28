# Open the GCD global-routing congestion heatmap.
# Run from anywhere with:
#   openroad -gui -no_init scripts/open_gcd.tcl

set root [file dirname [file dirname [file normalize [info script]]]]
cd $root

# The global-route checkpoint holds GCell capacity and usage.
# The separate congestion report file is not needed here.
read_db results/gcd/6_global_route.odb

if {[gui::enabled]} {
  gui::set_title "HOTPOT - GCD routing congestion"
  gui::set_display_controls "Misc/Background" color white
  gui::set_display_controls "Misc/Module view" visible false
  gui::set_display_controls "Instances/*" visible true
  gui::set_display_controls "Nets/*" visible false
  gui::set_display_controls "Layers/*" visible true
  gui::set_display_controls "Heat Maps/*" visible true
  gui::set_heatmap Routing rebuild
  gui::set_heatmap Routing ShowLegend 1
  gui::fit
}
