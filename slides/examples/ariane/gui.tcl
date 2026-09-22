# The flattened flow and its inputs use repository-root-relative paths.
cd ../../..
read_db results/ariane/final.odb
read_liberty slides/examples/ariane/inputs/NangateOpenCellLibrary_typical.lib
read_liberty slides/examples/ariane/inputs/fakeram45_256x16.lib
set_layer_rc -layer metal1 -resistance 5.4286e-03 -capacitance 7.41819E-02
set_layer_rc -layer metal2 -resistance 3.57167e-03 -capacitance 8.33611E-02
set_layer_rc -layer metal3 -resistance 3.57147e-03 -capacitance 1.03981E-01
set_layer_rc -layer metal4 -resistance 1.50001e-03 -capacitance 1.19150E-01
set_layer_rc -layer metal5 -resistance 1.50000e-03 -capacitance 1.09256E-01
set_layer_rc -layer metal6 -resistance 1.50000e-03 -capacitance 1.14168E-01
set_layer_rc -layer metal7 -resistance 1.87501e-04 -capacitance 1.17491E-01
set_layer_rc -layer metal8 -resistance 1.87501e-04 -capacitance 9.45346E-02
set_layer_rc -layer metal9 -resistance 3.74996e-05 -capacitance 1.06091E-01
set_layer_rc -layer metal10 -resistance 3.75000e-05 -capacitance 7.37095E-01
set_wire_rc -signal -layer metal3
set_wire_rc -clock -layer metal5
read_sdc results/ariane/final.sdc
read_spef results/ariane/final.spef
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
