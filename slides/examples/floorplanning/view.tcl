gui::set_display_controls "Misc/Background" color white
foreach control {"Layers/*" "Nets/*" "Instances/*" "Tracks/*" "Rows/*" "Heat Maps/*" "Misc/Instances/Pins" "Misc/Instances/Names" "Misc/Instances/Pin Names" "Misc/Instances/Blockages" "Misc/GCell grid"} {
    gui::set_display_controls $control visible false
}
gui::set_display_controls "Rows/*" color #5E81AC
gui::set_display_controls "Rows/*" visible true
gui::set_display_controls "Misc/Scale bar" visible true
gui::fit
