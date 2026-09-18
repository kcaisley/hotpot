set deck_dir [file dirname [file normalize [info script]]]
set out $deck_dir/assets/floorplanning
file mkdir $out
set work results/floorplanning
set site FreePDK45_38x28_10R_NP_162NW_34O
set stage $env(HOTPOT_FP_STAGE)

proc base_view {} {
  global deck_dir
  source $deck_dir/examples/floorplanning/view.tcl
  gui::set_display_controls "Rows/*" visible false
  gui::set_display_controls "Misc/Scale bar" visible false
  foreach {layer color} {metal1 #5E81AC metal2 #B48EAD metal3 #BF616A metal4 #5E81AC metal7 #B48EAD} {
    gui::set_display_controls "Layers/$layer" color $color
  }
}
proc shot {name {area {}}} {
  global out
  if {$area eq {}} {
    set b [ord::get_db_block]
    set d [$b getDieArea]
    set u [$b getDbUnitsPerMicron]
    set area [list [expr {double([$d xMin])/$u-1}] [expr {double([$d yMin])/$u-1}] [expr {double([$d xMax])/$u+1}] [expr {double([$d yMax])/$u+1}]]
  }
  save_image -width 2400 -area $area $out/$name.png
}

switch $stage {
  macros - macros_halo - macros_auto {
    if {$stage eq "macros_auto"} {
      source $deck_dir/examples/floorplanning/macros_auto.tcl
    } else {
      source $deck_dir/examples/floorplanning/macros.tcl
      if {$stage eq "macros"} {make_rows -site $site -core_area {5 5 175 105}}
    }
    base_view
    gui::set_display_controls "Rows/*" visible true
    gui::set_display_controls "Instances/Macro" visible true
    gui::set_display_controls "Layers/metal3" visible true
    gui::set_display_controls "Misc/Instances/Pins" visible true
    gui::set_display_controls "Misc/Instances/Blockages" visible true
    gui::set_display_controls "Misc/Instances/Names" visible true
    gui::set_display_controls "Misc/Instances/Names" color #2E3440
    shot $stage
  }
  floorplan - compact - wide - margin - explicit {
    source $deck_dir/examples/floorplanning/start.tcl
    set cases [dict create floorplan {40 1 1} compact {65 1 1} wide {40 0.5 1} margin {40 1 4}]
    if {$stage eq "explicit"} {
      initialize_floorplan -site $site -die_area {0 0 60 40} -core_area {2 2 58 38}
    } else {
      lassign [dict get $cases $stage] util ratio margin
      initialize_floorplan -site $site -utilization $util -aspect_ratio $ratio -core_space $margin
    }
    make_tracks
    base_view
    gui::set_display_controls "Rows/*" visible true
    if {$stage in {floorplan compact}} {
      shot $stage {-1 -1 39.045 39.045}
    } else {shot $stage}
  }
  rows - tracks {
    read_db $work/01_floorplan.odb
    base_view
    if {$stage eq "rows"} {
      gui::set_display_controls "Rows/*" visible true
    } else {
      gui::set_display_controls "Layers/metal2" visible true
      gui::set_display_controls "Layers/metal3" visible true
      gui::set_display_controls "Tracks/Pref" visible true
    }
    shot $stage {1 1 5 5}
  }
  taps - rails - straps - pdn - vias {
    read_db $work/02_power.odb
    base_view
    gui::set_display_controls "Layers/metal1" visible true
    if {$stage eq "taps"} {
      gui::set_display_controls "Instances/*" visible true
      gui::set_display_controls "Misc/Instances/Pins" visible true
      shot taps {0 0 5 7}
    } else {
      gui::set_display_controls "Nets/Power" visible true
      gui::set_display_controls "Nets/Ground" visible true
      if {$stage in {straps pdn vias}} {gui::set_display_controls "Layers/metal4" visible true}
      if {$stage in {pdn vias}} {gui::set_display_controls "Layers/metal7" visible true}
      if {$stage eq "vias"} {
        gui::set_display_controls "Layers/*" visible true
        shot vias {1 1 7 7}
      } else {shot $stage}
    }
  }
  placed - pins_auto - pins_sides - pins_close - pins_anneal - pin_fixed - pins_group - routability {
    if {$stage eq "routability"} {
      source $deck_dir/examples/floorplanning/routability.tcl
    } elseif {$stage eq "pins_auto"} {
      read_db $work/04_pins.odb
    } elseif {$stage in {pins_sides pins_close}} {
      source $deck_dir/examples/floorplanning/pins_sides.tcl
    } else {
      read_db $work/03_before_pins.odb
      if {$stage eq "pins_anneal"} {place_pins -hor_layers metal3 -ver_layers metal2 -annealing}
      if {$stage eq "pin_fixed"} {
        place_pin -pin_name clk -layer metal3 -location {0 10} -pin_size {0.14 0.14} -force_to_die_boundary
        place_pins -hor_layers metal3 -ver_layers metal2
      }
      if {$stage eq "pins_group"} {
        set_io_pin_constraint -pin_names {resp_msg[*]} -region right:* -group -order
        place_pins -hor_layers metal3 -ver_layers metal2
      }
    }
    base_view
    gui::set_display_controls "Instances/*" visible true
    gui::set_display_controls "Misc/Instances/Pins" visible true
    gui::set_display_controls "Layers/metal1" color #5E81AC
    gui::set_display_controls "Layers/metal1" visible true
    gui::set_display_controls "Nets/Signal" visible true
    gui::set_display_controls "Nets/Clock" visible true
    gui::set_display_controls "Shape Types/Pins" visible true
    gui::set_display_controls "Shape Types/Pin Names" visible true
    gui::set_display_controls "Layers/metal2" visible true
    gui::set_display_controls "Layers/metal3" visible true
    if {$stage eq "pins_close"} {
      shot $stage {-1 1 5 15}
    } elseif {$stage eq "pin_fixed"} {
      select -type BTerm -name clk
      shot $stage {-1 5 5 15}
    } else {shot $stage}
  }
}
exit
