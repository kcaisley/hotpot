set tech $env(OPENROAD_ROOT)/test/Nangate45
read_lef $tech/Nangate45_tech.lef
read_lef $tech/Nangate45_stdcell.lef
read_def results/floorplanning/04_pins.def
if {[gui::enabled]} {gui::fit}
