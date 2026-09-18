read_db results/floorplanning/macros_base.odb
set tech $env(OPENROAD_ROOT)/test/Nangate45
read_liberty $tech/Nangate45_typ.lib
read_liberty $tech/fakeram45_64x32.lib
set_macro_halo -macro_name ram0 -halo {5 5}
set_macro_halo -macro_name ram1 -halo {5 5}
rtl_macro_placer
cut_rows -halo_width_x 5 -halo_width_y 5
write_db results/floorplanning/macros_auto.odb
