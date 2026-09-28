# Render one real GCD global route with the workshop's Nord layer palette.
set here [file dirname [file normalize [info script]]]
set root [file dirname $here]
read_db $root/results/gcd/6_global_route.odb
set_routing_layers -signal metal2-metal10 -clock metal6-metal10
set_global_routing_layer_adjustment metal2-metal10 0.5
global_route -congestion_iterations 100
gui::set_display_controls "Misc/Background" color white
foreach control {"Tracks/*" "Rows/*" "Nets/*" "Instances/*" "Heat Maps/*" "Misc/Module view" "Misc/Instances/Names" "Misc/Instances/Pins" "Layers/*"} {
  gui::set_display_controls $control visible false
}
foreach {layer color} {
  metal1 #81A1C1 metal2 #BF616A metal3 #A3BE8C
  metal4 #EBCB8B metal5 #B48EAD metal6 #88C0D0
  metal7 #D08770 metal8 #5E81AC metal9 #8FBCBB
  metal10 #EBCB8B
} {
  gui::set_display_controls "Layers/$layer" color $color
}
gui::set_display_controls "Instances/*" visible true
gui::set_display_controls "Instances/*" color #D8DEE9
draw_route_segments {_188_}
gui::set_display_controls "Layers/*" visible true
set block [ord::get_db_block]
set die [$block getDieArea]
set u [$block getDbUnitsPerMicron]
set area [list [expr {double([$die xMin])/$u}] [expr {double([$die yMin])/$u}] [expr {double([$die xMax])/$u}] [expr {double([$die yMax])/$u}]]
save_image -area $area -width 1800 [file join $here images/routing/gcd_one_global_route.png]
