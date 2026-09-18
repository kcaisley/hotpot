# reload.tcl
set here [file dirname [file normalize [info script]]]
read_db $here/design.odb
set block [ord::get_db_block]
foreach {method expected} {getInsts 2 getBTerms 3 getNets 6} {
  if {[llength [$block $method]] != $expected} {error "Unexpected $method count"}
}
foreach inst [$block getInsts] {puts "RELOADED: [$inst getName] [[$inst getMaster] getName] [$inst getLocation]"}
puts "PASS: binary OpenDB reload preserves instances, ports and nets"
exit
