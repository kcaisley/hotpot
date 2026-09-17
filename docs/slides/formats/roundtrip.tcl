# roundtrip.tcl
set here [file dirname [file normalize [info script]]]
set pdk [file join $env(HOME) Documents libs OpenROAD-flow-scripts flow platforms nangate45]
read_lef $pdk/lef/NangateOpenCellLibrary.tech.lef
read_lef $pdk/lef/NangateOpenCellLibrary.macro.lef
read_def $here/top.def
write_db $here/top.odb
write_def $here/top-roundtrip.def
set block [ord::get_db_block]
if {[llength [$block getInsts]] != 2} {error "Expected two instances"}
if {[llength [$block getBTerms]] != 3} {error "Expected three signal ports"}
puts "CHECK: two instances, three block terminals, [llength [$block getNets]] nets"
exit
