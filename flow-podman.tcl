read_lef ../OpenROAD/test/Nangate45/Nangate45_tech.lef
read_lef ../OpenROAD/test/Nangate45/Nangate45_stdcell.lef
read_liberty ../OpenROAD/test/Nangate45/Nangate45_typ.lib
read_verilog ../OpenROAD/test/gcd_nangate45.v
link_design gcd
