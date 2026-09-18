# render_stages.tcl -- native OpenROAD images from the saved workshop checkpoints.
set here [file dirname [file normalize [info script]]]
set root [file normalize [file join $here ../..]]
set stage $env(HOTPOT_SLIDE_STAGE)
set checkpoints [dict create floorplan 1_floorplan global_placement 3_global_placement detailed_placement 4_repaired cts 5_cts global_routing 6_global_route detailed_routing gcd_final finishing gcd_final]
read_db $root/results/[dict get $checkpoints $stage].odb
read_liberty $env(HOME)/Documents/libs/OpenROAD/test/Nangate45/Nangate45_typ.lib
create_clock -name core_clock -period 0.485 [get_ports clk]
set_propagated_clock [all_clocks]
gui::set_display_controls "Misc/Background" color white
foreach control {"Tracks/*" "Rows/*" "Nets/*" "Instances/*" "Heat Maps/*" "Misc/Instances/Pins" "Misc/Instances/Names" "Misc/Instances/Pin Names" "Misc/Instances/Blockages" "Misc/GCell grid" "Misc/Scale bar" "Misc/Labels" "Layers/*"} {
  gui::set_display_controls $control visible false
}
switch $stage {
  floorplan {
    gui::set_display_controls "Rows/*" visible true
  }
  global_placement - detailed_placement {
    gui::set_display_controls "Instances/*" visible true
    gui::set_display_controls "Misc/Instances/Pins" visible true
    gui::set_display_controls "Layers/metal1" visible true
  }
  cts {
    gui::set_display_controls "Instances/*" visible true
    foreach net [[ord::get_db_block] getNets] {
      if {[$net getSigType] eq "CLOCK"} {gui::highlight_net [$net getName] 7}
    }
  }
  global_routing {
    gui::set_display_controls "Instances/*" visible true
    gui::set_display_controls "Layers/*" visible true
    read_guides $root/results/6_global_route.guide
    draw_route_segments {*}
  }
  detailed_routing - finishing {
    gui::set_display_controls "Instances/*" visible true
    gui::set_display_controls "Layers/*" visible true
    gui::set_display_controls "Nets/*" visible true
    gui::set_display_controls "Nets/Power" visible false
    gui::set_display_controls "Nets/Ground" visible false
    gui::set_display_controls "Misc/Instances/Pins" visible true
    if {$stage eq "detailed_routing"} {
      gui::set_display_controls "Instances/Physical/Fill cell" visible false
    }
  }
}
set block [ord::get_db_block]
set die [$block getDieArea]
set units [$block getDbUnitsPerMicron]
set area [list [expr {double([$die xMin])/$units-0.8}] [expr {double([$die yMin])/$units-0.8}] [expr {double([$die xMax])/$units+0.8}] [expr {double([$die yMax])/$units+0.8}]]
puts "STAGE: $stage; bounds $area; [llength [$block getInsts]] instances"
file mkdir $here/assets/stages
save_image -area $area -width 1400 $here/assets/stages/$stage.png
if {$stage in {floorplan global_placement detailed_placement}} {
  # Exact row/cell boundaries for readable vector thumbnails.
  set file [open $here/assets/stages/${stage}_geometry.tsv w]
  puts $file "DIE\t[$die xMin]\t[$die yMin]\t[$die xMax]\t[$die yMax]"
  if {$stage eq "floorplan"} {
    foreach row [$block getRows] {
      set box [$row getBBox]
      puts $file "ROW\t[$box xMin]\t[$box yMin]\t[$box xMax]\t[$box yMax]\t[[$row getSite] getWidth]"
    }
  } else {
    foreach inst [$block getInsts] {
      set box [$inst getBBox]
      puts $file "CELL\t[$inst getName]\t[[$inst getMaster] getName]\t[$box xMin]\t[$box yMin]\t[$box xMax]\t[$box yMax]"
    }
  }
  close $file
}
if {$stage eq "cts"} {
  # Export real placement and clock pin coordinates for the legible vector
  # overview. Lines in that figure are connectivity fly-lines, not routes.
  set file [open $here/assets/stages/cts_geometry.tsv w]
  puts $file "DIE\t[$die xMin]\t[$die yMin]\t[$die xMax]\t[$die yMax]"
  foreach inst [$block getInsts] {
    set box [$inst getBBox]
    puts $file "CELL\t[$inst getName]\t[[$inst getMaster] getName]\t[$box xMin]\t[$box yMin]\t[$box xMax]\t[$box yMax]"
  }
  foreach net [$block getNets] {
    if {[$net getSigType] ne "CLOCK"} {continue}
    foreach term [$net getITerms] {
      lassign [$term getAvgXY] valid x y
      if {!$valid} {error "Missing clock pin coordinate"}
      puts $file "PIN\t[$net getName]\t[[$term getInst] getName]\t[$term getIoType]\t$x\t$y"
    }
    foreach term [$net getBTerms] {
      set pin [lindex [$term getBPins] 0]
      set box [lindex [$pin getBoxes] 0]
      set x [expr {([$box xMin]+[$box xMax])/2}]
      set y [expr {([$box yMin]+[$box yMax])/2}]
      puts $file "PORT\t[$net getName]\t[$term getName]\t[$term getIoType]\t$x\t$y"
    }
  }
  close $file
}
exit
