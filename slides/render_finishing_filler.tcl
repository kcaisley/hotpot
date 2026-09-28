# OpenROAD GUI capture of the routed GCD with filler instances highlighted.
set here [file dirname [file normalize [info script]]]
set root [file normalize [file join $here ..]]
read_db [file join $root results/gcd/gcd_final.odb]
set block [ord::get_db_block]

gui::set_display_controls "Misc/Background" color white
gui::set_display_controls "Tracks/*" visible false
gui::set_display_controls "Rows/*" visible false
gui::set_display_controls "Nets/*" visible false
gui::set_display_controls "Instances/*" visible true
gui::set_display_controls "Layers/*" visible false
gui::set_display_controls "Misc/Scale bar" visible false

set filler_count 0
foreach inst [$block getInsts] {
  if {[string match FILLCELL* [[$inst getMaster] getName]]} {
    gui::highlight_inst [$inst getName] 0
    incr filler_count
  }
}
puts "OpenROAD filler image: $filler_count filler cells highlighted"
save_image -width 2400 -area {0 0 38.045 38.045} \
  [file join $here images/finishing/gcd_fillers_highlighted_openroad.png]
