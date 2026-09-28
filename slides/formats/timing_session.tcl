# timing_session.tcl
set here [file dirname [file normalize [info script]]]
set pdk [file join $env(HOME) Documents libs OpenROAD-flow-scripts flow platforms nangate45]
read_liberty $pdk/lib/NangateOpenCellLibrary_typical.lib
read_db $here/design.odb
read_sdc $here/design.sdc
# read_spef design.spef  ;# optional extracted interconnect parasitics
report_checks -path_delay max -fields {slew cap input_pin} -digits 4
exit
