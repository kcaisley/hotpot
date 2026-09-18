# recap_import.tcl -- verify the Verilog entry path shown on the recap slide.
set here [file dirname [file normalize [info script]]]
set pdk [file join $env(HOME) Documents libs OpenROAD-flow-scripts flow platforms nangate45]
read_lef $pdk/lef/NangateOpenCellLibrary.tech.lef
read_lef $pdk/lef/NangateOpenCellLibrary.macro.lef
read_liberty $pdk/lib/NangateOpenCellLibrary_typical.lib
read_verilog $here/../examples/design.v
link_design -hier design
read_sdc $here/design.sdc
set block [ord::get_db_block]
if {[$block getName] ne "design"} {error "Unexpected block name"}
foreach {method expected} {getInsts 2 getBTerms 3 getNets 4} {
  if {[llength [$block $method]] != $expected} {error "Unexpected $method count"}
}
foreach inst [$block getInsts] {
  puts "LINKED: [$inst getName] [[$inst getMaster] getName]"
}
puts "PASS: LEF, Liberty and design.v link; cells.v remains a functional simulation view"
exit
