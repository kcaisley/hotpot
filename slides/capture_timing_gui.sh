#!/usr/bin/env bash
# Capture the full OpenROAD X11 window for the Timing Report and Charts docks.
# The layout-only images use save_image; these two captures intentionally keep
# the complete GUI so the panels and their controls remain readable.
set -eu

design=${1:-ariane}
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
openroad_bin=${OPENROAD_BIN:-openroad}
display=${DISPLAY:-:0}

capture() {
  view=$1
  output=$2
  tab_x=$3
  log=/tmp/hotpot-${design}-${view}-gui.log

  DISPLAY="$display" HOTPOT_GUI_DESIGN="$design" HOTPOT_GUI_VIEW="$view" \
    HOTPOT_GUI_HOLD_MS=20000 "$openroad_bin" -gui -no_init -exit \
    "$here/render_gui_evidence.tcl" >"$log" 2>&1 &
  pid=$!

  for attempt in $(seq 1 90); do
    if rg -q "GUI_READY $design $view" "$log"; then
      break
    fi
    sleep 1
  done
  if ! rg -q "GUI_READY $design $view" "$log"; then
    cat "$log" >&2
    kill "$pid" 2>/dev/null || true
    return 1
  fi

  window=$(DISPLAY="$display" xdotool search --onlyvisible --name "$design" | head -n 1)
  DISPLAY="$display" xdotool windowactivate "$window" || true
  sleep 1
  if [ "$tab_x" -gt 0 ]; then
    DISPLAY="$display" xdotool mousemove "$tab_x" 998 click 1
    sleep 1
  fi
  DISPLAY="$display" import -window "$window" "$here/$output"
  wait "$pid"
}

capture timing_table "images/cts/${design}_timing_report_gui.png" 1570
capture slack_chart "images/cts/${design}_slack_chart_gui.png" 0
