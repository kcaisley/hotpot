source [file join [file dirname [info script]] flow.tcl]
initialize_floorplan -die_area {0 0 60 0 60 30 30 30 30 60 0 60} -core_area {2 2 58 2 58 28 28 28 28 58 2 58} -site FreePDK45_38x28_10R_NP_162NW_34O
make_tracks
file mkdir results/floorplanning
write_db results/floorplanning/polygon.odb
if {[gui::enabled]} {gui::fit}
