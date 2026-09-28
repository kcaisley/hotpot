read_lef $env(OPENROAD_ROOT)/test/Nangate45/Nangate45_tech.lef
read_lef $env(OPENROAD_ROOT)/test/Nangate45/Nangate45_stdcell.lef
read_liberty $env(OPENROAD_ROOT)/test/Nangate45/Nangate45_typ.lib
read_verilog $env(OPENROAD_ROOT)/test/gcd_nangate45.v
link_design gcd
