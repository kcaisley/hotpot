# Reproduce the two global-route-guide views used by routing.pdf.
#
# In OpenROAD's Tcl console:
#   source /home/kcaisley/Documents/hotpot/slides/reproduce_global_route_views.tcl
#   hotpot_show_all_global_guides
#   hotpot_show_one_global_guide _188_
#
# The second command accepts any net name in the loaded database.

set ::hotpot_route_script_dir [file dirname [file normalize [info script]]]
set ::hotpot_route_root [file normalize [file join $::hotpot_route_script_dir ..]]
set ::hotpot_route_odb [file join $::hotpot_route_root results gcd 6_global_route.odb]
set ::hotpot_route_guide [file join $::hotpot_route_root results gcd 6_global_route.guide]

proc hotpot_route_display_base {} {
  gui::set_display_controls "Misc/Background" color white

  foreach control {
    Tracks/*
    Rows/*
    Nets/*
    {Heat Maps/*}
    {Misc/Instances/Pins}
    {Misc/Instances/Names}
    {Misc/Instances/Pin Names}
    {Misc/Instances/Blockages}
    {Misc/GCell grid}
    {Misc/Scale bar}
    {Misc/Labels}
    Layers/*
  } {
    gui::set_display_controls $control visible false
  }

  # Keep the placed cells as a faint grey context.
  gui::set_display_controls "Instances/*" visible true
  gui::set_display_controls "Instances/*" color #D8DEE9

  # Keep route segments colored by routing layer.
  foreach {layer color} {
    metal1  #81A1C1
    metal2  #BF616A
    metal3  #A3BE8C
    metal4  #EBCB8B
    metal5  #B48EAD
    metal6  #88C0D0
    metal7  #D08770
    metal8  #5E81AC
    metal9  #8FBCBB
    metal10 #EBCB8B
  } {
    gui::set_display_controls "Layers/$layer" color $color
  }
  gui::set_display_controls "Layers/*" visible true
}

proc hotpot_load_global_route_guides {} {
  global hotpot_route_odb hotpot_route_guide
  read_db $hotpot_route_odb
  read_guides $hotpot_route_guide
}

proc hotpot_show_all_global_guides {} {
  hotpot_route_display_base
  hotpot_load_global_route_guides
  draw_route_segments {*}
  gui::fit
}

proc hotpot_show_one_global_guide {net_name} {
  hotpot_route_display_base
  hotpot_load_global_route_guides
  draw_route_segments [list $net_name]
  gui::fit
}
