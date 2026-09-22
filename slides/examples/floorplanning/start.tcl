source [file join [file dirname [info script]] flow.tcl]
set work results/floorplanning
file mkdir $work

create_clock -name core_clock -period 0.510 [get_ports clk]
set data_inputs [lsearch -inline -all -not -exact [all_inputs] [get_ports clk]]
set_input_delay 0.102 -clock core_clock $data_inputs
set_output_delay 0.102 -clock core_clock [all_outputs]
write_db $work/00_linked.odb
