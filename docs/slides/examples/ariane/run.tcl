set here [file dirname [file normalize [info script]]]
set root [file normalize [file join $here ../../../..]]
if {![file exists $root/flow_ariane.tcl]} {set root [file normalize [file join $here ../../..]]}
source $root/flow_ariane.tcl
