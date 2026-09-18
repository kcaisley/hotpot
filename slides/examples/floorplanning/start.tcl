set tech $env(OPENROAD_ROOT)/test/Nangate45
set netlist $env(OPENROAD_ROOT)/test/gcd_nangate45.v
set site FreePDK45_38x28_10R_NP_162NW_34O
set work results/floorplanning
file mkdir $work

read_lef $tech/Nangate45_tech.lef
read_lef $tech/Nangate45_stdcell.lef
read_liberty $tech/Nangate45_typ.lib
read_verilog $netlist
link_design gcd

create_clock -name core_clock -period 0.485 [get_ports clk]
set data_inputs [lsearch -inline -all -not -exact [all_inputs] [get_ports clk]]
set_input_delay 0.097 -clock core_clock $data_inputs
set_output_delay 0.097 -clock core_clock [all_outputs]
write_db $work/00_linked.odb
