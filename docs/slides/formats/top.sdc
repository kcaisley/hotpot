# top.sdc
create_clock -name virtual -period 1.0
set_input_delay -clock virtual 0.05 [get_ports {in1 in2}]
set_output_delay -clock virtual 0.05 [get_ports out]
set_input_transition 0.02 [get_ports {in1 in2}]
set_load 10 [get_ports out]
