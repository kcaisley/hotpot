set work results/floorplanning
read_db $work/03_before_pins.odb
clear_io_pin_constraints
set_io_pin_constraint -direction input -region left:*
set_io_pin_constraint -direction output -region right:*
place_pins -hor_layers metal3 -ver_layers metal2 -min_distance 0.8
write_db $work/05_pins_sides.odb
