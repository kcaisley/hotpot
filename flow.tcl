set tech $env(OPENROAD_ROOT)/test/Nangate45
set netlist $env(OPENROAD_ROOT)/test/gcd_nangate45.v
set site FreePDK45_38x28_10R_NP_162NW_34O

read_lef $tech/Nangate45_tech.lef
read_lef $tech/Nangate45_stdcell.lef
read_liberty $tech/Nangate45_typ.lib
read_verilog $netlist
link_design gcd
