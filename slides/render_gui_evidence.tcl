# render_gui_evidence.tcl -- native OpenROAD GUI evidence for the workshop.
#
# Render one design/view at a time, for example:
#   QT_QPA_PLATFORM=offscreen HOTPOT_GUI_DESIGN=ariane \
#     HOTPOT_GUI_VIEW=timing openroad -gui -no_init -exit \
#     slides/render_gui_evidence.tcl
#
# The layout captures intentionally use the same save_image path and Nord
# layer palette as render_floorplanning.tcl.  Clock Tree Viewer is a widget,
# so it uses OpenROAD's native save_clocktree_image command instead.

set here [file dirname [file normalize [info script]]]
set root [file normalize [file join $here ..]]
set design $env(HOTPOT_GUI_DESIGN)
set view $env(HOTPOT_GUI_VIEW)

if {$design ni {gcd ariane}} {
  error "HOTPOT_GUI_DESIGN must be gcd or ariane"
}

set out [file join $here images]
file mkdir [file join $out placement]
file mkdir [file join $out cts]
file mkdir [file join $out routing]
file mkdir [file join $out finishing]

proc set_nord_layers {} {
  foreach {layer color} {
    metal1  #81A1C1
    via1    #D8DEE9
    metal2  #BF616A
    via2    #D08770
    metal3  #A3BE8C
    via3    #B4D0A4
    metal4  #EBCB8B
    via4    #F3D99B
    metal5  #B48EAD
    via5    #C6ABC2
    metal6  #88C0D0
    via6    #A9D2DE
    metal7  #D08770
    via7    #E4AD9D
    metal8  #5E81AC
    via8    #81A1C1
    metal9  #8FBCBB
    via9    #B3D1D0
    metal10 #EBCB8B
  } {
    gui::set_display_controls "Layers/$layer" color $color
  }
}

proc reset_display {} {
  gui::set_display_controls "Misc/Background" color white
  foreach control {
    Tracks/*
    Rows/*
    Nets/*
    Instances/*
    {Heat Maps/*}
    {Misc/Instances/Pins}
    {Misc/Instances/Names}
    {Misc/Instances/Pin Names}
    {Misc/Instances/Blockages}
    {Misc/GCell grid}
    {Misc/Scale bar}
    {Misc/Labels}
    {Misc/Module view}
    Layers/*
  } {
    gui::set_display_controls $control visible false
  }
  set_nord_layers
}

proc show_routed_layout {} {
  # Keep the complete routed design visible, but remove the module overlay
  # and power/ground nets so the timing panels have a real layout beside them.
  gui::set_display_controls "Layers/*" visible true
  gui::set_display_controls "Instances/*" visible true
  gui::set_display_controls "Instances/StdCells/Combinational" visible true
  gui::set_display_controls "Instances/StdCells/Sequential" visible true
  gui::set_display_controls "Instances/StdCells/Clock tree/*" visible true
  gui::set_display_controls "Instances/StdCells/Buffers/Inverters/*" visible true
  gui::set_display_controls "Instances/Macro" visible true
  gui::set_display_controls "Instances/Physical/*" visible true
  gui::set_display_controls "Nets/Signal" visible true
  gui::set_display_controls "Nets/Clock" visible true
  gui::set_display_controls "Nets/Power" visible false
  gui::set_display_controls "Nets/Ground" visible false
  gui::set_display_controls "Misc/Module view" visible false
  gui::set_display_controls "Misc/Instances/Names" visible false
  gui::set_display_controls "Misc/Instances/Pin Names" visible false
  gui::set_display_controls "Misc/Scale bar" visible true
}

proc show_clock_layout {} {
  # Show only the clock network and its endpoints in the physical view.
  gui::set_display_controls "Layers/*" visible true
  gui::set_display_controls "Instances/*" visible false
  gui::set_display_controls "Nets/*" visible false
  gui::set_display_controls "Nets/Clock" visible true
  gui::set_display_controls "Instances/StdCells/Clock tree/*" visible true
  gui::set_display_controls "Instances/StdCells/Sequential" visible true
  gui::set_display_controls "Misc/Module view" visible false
  gui::set_display_controls "Misc/Instances/Pins" visible false
  gui::set_display_controls "Misc/Instances/Names" visible false
  gui::set_display_controls "Misc/Instances/Pin Names" visible false
  gui::set_display_controls "Misc/Scale bar" visible true
}

proc layout_area {} {
  set block [ord::get_db_block]
  set die [$block getDieArea]
  set units [$block getDbUnitsPerMicron]
  return [list \
    [expr {double([$die xMin]) / $units - 0.8}] \
    [expr {double([$die yMin]) / $units - 0.8}] \
    [expr {double([$die xMax]) / $units + 0.8}] \
    [expr {double([$die yMax]) / $units + 0.8}]]
}

proc save_layout {path} {
  set area [layout_area]
  puts "Saving $path with area $area"
  save_image -width 2400 -area $area $path
}

proc hold_gui {} {
  global env
  if {![info exists env(HOTPOT_GUI_HOLD_MS)]} {
    return
  }
  puts "GUI_READY $env(HOTPOT_GUI_DESIGN) $env(HOTPOT_GUI_VIEW)"
  flush stdout
  set ::hotpot_gui_done 0
  after $env(HOTPOT_GUI_HOLD_MS) {set ::hotpot_gui_done 1}
  vwait ::hotpot_gui_done
}

proc hide_timing_panels {} {
  foreach widget {
    Inspector
    {Hierarchy Browser}
    {Timing Report}
    {Clock Tree Viewer}
    Charts
  } {
    gui::hide_widget $widget
  }
}

proc highlight_clock_nets {} {
  foreach net [[ord::get_db_block] getNets] {
    if {[$net getSigType] eq "CLOCK"} {
      gui::highlight_net [$net getName] 7
    }
  }
}

if {$design eq "gcd"} {
  read_db [file join $root results gcd gcd_final.odb]
  if {[info exists env(OPENROAD_ROOT)]} {
    set or_root [file normalize $env(OPENROAD_ROOT)]
  } else {
    set or_root [file normalize [file join $root ../libs/OpenROAD]]
  }
  read_liberty [file join $or_root test Nangate45 Nangate45_typ.lib]
  create_clock -name core_clock -period 0.510 [get_ports clk]
  set_input_delay 0.102 -clock core_clock \
    [lsearch -inline -all -not -exact [all_inputs] [get_ports clk]]
  set_output_delay 0.102 -clock core_clock [all_outputs]
  read_spef [file join $root results gcd gcd.spef]
  set prefix gcd
  set clock_period 0.510
} else {
  read_db [file join $root results ariane final.odb]
  read_liberty [file join $root slides examples ariane inputs NangateOpenCellLibrary_typical.lib]
  read_liberty [file join $root slides examples ariane inputs fakeram45_256x16.lib]
  read_sdc [file join $root results ariane final.sdc]
  foreach {layer resistance capacitance} {
    metal1  5.4286e-03 7.41819E-02
    metal2  3.57167e-03 8.33611E-02
    metal3  3.57147e-03 1.03981E-01
    metal4  1.50001e-03 1.19150E-01
    metal5  1.50000e-03 1.09256E-01
    metal6  1.50000e-03 1.14168E-01
    metal7  1.87501e-04 1.17491E-01
    metal8  1.87501e-04 9.45346E-02
    metal9  3.74996e-05 1.06091E-01
    metal10 3.75000e-05 7.37095E-01
  } {
    set_layer_rc -layer $layer -resistance $resistance -capacitance $capacitance
  }
  set_wire_rc -signal -layer metal3
  set_wire_rc -clock -layer metal5
  set_power_activity -input -activity 0.1 -duty 0.5
  read_spef [file join $root results ariane final.spef]
  set prefix ariane
  set clock_period 10.0
}
set_propagated_clock [all_clocks]

gui::set_title "HOTPOT - $design GUI evidence"
reset_display

set cts_dir [file join $out cts]
set route_dir [file join $out routing]
set finish_dir [file join $out finishing]

switch $view {
  clock_layout {
    show_clock_layout
    highlight_clock_nets
    save_layout [file join $route_dir ${prefix}_clock_tree.png]
  }
  timing {
    show_routed_layout
    gui::show_widget "Timing Report"
    gui::update_timing_report
    gui::show_worst_path -setup
    gui::fit
    save_layout [file join $cts_dir ${prefix}_timing_path.png]
  }
  clock_viewer {
    gui::show_widget "Clock Tree Viewer"
    gui::select_clockviewer_clock core_clock
    save_clocktree_image -clock core_clock -width 1600 -height 1000 \
      [file join $cts_dir ${prefix}_clock_tree_viewer.png]
  }
  power_heatmap {
    gui::set_display_controls "Instances/*" visible true
    gui::set_display_controls "Layers/*" visible true
    gui::set_display_controls "Heat Maps/*" visible true
    gui::set_heatmap Power rebuild
    gui::set_heatmap Power ShowLegend 1
    save_layout [file join $finish_dir ${prefix}_power_heatmap.png]
  }
  routing_heatmap {
    gui::set_display_controls "Instances/*" visible true
    gui::set_display_controls "Layers/*" visible true
    gui::set_display_controls "Heat Maps/*" visible true
    gui::set_heatmap Routing rebuild
    gui::set_heatmap Routing ShowLegend 1
    save_layout [file join $route_dir ${prefix}_routing_congestion.png]
  }
  placement_heatmap {
    gui::set_display_controls "Instances/*" visible true
    gui::set_display_controls "Heat Maps/*" visible true
    gui::set_heatmap Placement rebuild
    gui::set_heatmap Placement ShowLegend 1
    save_layout [file join $out placement ${prefix}_placement_density.png]
  }
  timing_table {
    # Keep the Timing Report dock readable while leaving the routed layout
    # visible beside it.  The selected row/path is shown in that layout.
    show_routed_layout
    hide_timing_panels
    gui::show_widget "Timing Report"
    gui::update_timing_report
    gui::show_worst_path -setup
    gui::fit
    save_layout [file join /tmp hotpot-${prefix}-timing-table-layout.png]
    hold_gui
  }
  slack_chart {
    # The chart widget is separate from the timing-path table.  Selecting
    # Endpoint Slack shows the setup/hold mode menu and the endpoint bins.
    show_routed_layout
    hide_timing_panels
    gui::show_widget "Charts"
    gui::select_chart "Endpoint Slack"
    save_histogram_image [file join $cts_dir ${prefix}_slack_histogram.png] \
      -mode setup -width 1200 -height 800
    save_layout [file join /tmp hotpot-${prefix}-slack-chart-layout.png]
    hold_gui
  }
  default {
    error "HOTPOT_GUI_VIEW must be clock_layout, timing, clock_viewer, power_heatmap, routing_heatmap, placement_heatmap, timing_table, or slack_chart"
  }
}

exit
