set here [file dirname [file normalize [info script]]]
read_db $here/results/final.odb
source $here/libraries.tcl
source $here/rc.tcl
read_sdc $here/results/final.sdc
read_spef $here/results/final.spef
set_power_activity -input -activity 0.1 -duty 0.5
gui::set_heatmap Power rebuild
gui::set_heatmap Power ShowLegend 1
foreach {layer color} {metal1 #81A1C1 via1 #D8DEE9 metal2 #BF616A via2 #D08770 metal3 #A3BE8C via3 #B4D0A4 metal4 #EBCB8B via4 #F3D99B metal5 #B48EAD via5 #C6ABC2 metal6 #88C0D0 via6 #A9D2DE metal7 #D08770 via7 #E4AD9D metal8 #5E81AC via8 #81A1C1 metal9 #8FBCBB via9 #B3D1D0 metal10 #EBCB8B} {
  gui::set_display_controls "Layers/$layer" color $color
}
gui::set_title "HOTPOT - routed Ariane RISC-V"
gui::set_display_controls "Layers/*" visible true
gui::set_display_controls "Instances/*" visible true
gui::set_display_controls "Nets/*" visible true
gui::set_display_controls "Heat Maps/*" visible false
gui::set_display_controls "Misc/Module view" visible true
gui::set_display_controls "Nets/Power" visible true
gui::set_display_controls "Nets/Ground" visible true
gui::show_widget "Inspector"
gui::show_widget "Hierarchy Browser"
gui::fit
