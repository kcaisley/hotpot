set here [file dirname [file normalize [info script]]]
set tech $env(OPENROAD_ROOT)/test/Nangate45
set site FreePDK45_38x28_10R_NP_162NW_34O
read_lef $tech/Nangate45_tech.lef
read_lef $tech/Nangate45_stdcell.lef
read_lef $tech/fakeram45_64x32.lef
read_liberty $tech/Nangate45_typ.lib
read_liberty $tech/fakeram45_64x32.lib
read_verilog $env(OPENROAD_ROOT)/test/gcd_nangate45.v
read_verilog $here/macros.v
link_design macro_demo
initialize_floorplan -site $site -die_area {0 0 180 110} -core_area {5 5 175 105}
make_tracks
file mkdir results/floorplanning
write_db results/floorplanning/macros_base.odb
place_macro -macro_name ram0 -location {15 20} -orientation R0
place_macro -macro_name ram1 -location {100 20} -orientation MY
cut_rows -halo_width_x 5 -halo_width_y 5
file mkdir results/floorplanning
write_db results/floorplanning/macros.odb
