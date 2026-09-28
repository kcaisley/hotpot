# OpenROAD view for the finishing slide. The metal fill recipe is illustrative
# for the Nangate45 workshop design, not a foundry signoff rule deck.
set here [file dirname [file normalize [info script]]]
set root [file normalize [file join $here ..]]
read_db [file join $root results/gcd/gcd_final.odb]
set block [ord::get_db_block]
set filler_count 0
foreach inst [$block getInsts] {
  if {[string match FILLCELL* [[$inst getMaster] getName]]} {
    incr filler_count
  }
}
density_fill -rules [file join $here examples/finishing/metal_fill_demo.json]
set metal_fill_count [llength [$block getFills]]
puts "OpenROAD finishing image: $filler_count filler cells, $metal_fill_count metal fill shapes"
write_db [file join $root results/gcd/gcd_metal_fill_demo.odb]

gui::set_display_controls "Misc/Background" color white
gui::set_display_controls "Tracks/*" visible false
gui::set_display_controls "Rows/*" visible false
gui::set_display_controls "Nets/*" visible false
gui::set_display_controls "Instances/*" visible false
gui::set_display_controls "Instances/Physical/Fill cell" visible true
gui::set_display_controls "Instances/Physical/Fill cell" color #B48EAD
gui::set_display_controls "Layers/*" visible false
gui::set_display_controls "Layers/metal5" visible true
gui::set_display_controls "Layers/metal5" color #5E81AC
gui::set_display_controls "Shape Types/Fills" visible true
gui::set_display_controls "Misc/Scale bar" visible true
gui::fit
set out [file join $here images/finishing]
file mkdir $out
save_image -width 2400 -area {0 0 38.045 38.045} [file join $out gcd_filler_metal_fill_openroad.png]
