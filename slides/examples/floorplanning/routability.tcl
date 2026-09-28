read_db results/floorplanning/04_pins.odb
read_liberty $env(OPENROAD_ROOT)/test/Nangate45/Nangate45_typ.lib
set_global_routing_layer_adjustment metal2-metal10 0.5
set_routing_layers -signal metal2-metal10 -clock metal6-metal10
global_placement -routability_driven -density 0.80 -pad_left 2 -pad_right 2
write_db results/floorplanning/06_routability.odb
