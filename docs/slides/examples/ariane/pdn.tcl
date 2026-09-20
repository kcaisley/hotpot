add_global_connection -net VDD -inst_pattern {.*} -pin_pattern {^VDD$} -power
add_global_connection -net VSS -inst_pattern {.*} -pin_pattern {^VSS$} -ground
global_connect
set_voltage_domain -name CORE -power VDD -ground VSS
define_pdn_grid -name core -voltage_domains CORE -pins {metal7}
add_pdn_stripe -grid core -layer metal1 -width 0.17 -followpins
add_pdn_stripe -grid core -layer metal4 -width 0.48 -pitch 56 -offset 2
add_pdn_stripe -grid core -layer metal7 -width 1.4 -pitch 30 -offset 2
add_pdn_connect -grid core -layers {metal1 metal4}
add_pdn_connect -grid core -layers {metal4 metal7}
define_pdn_grid -name macros -voltage_domains CORE -macro -orient {R0 R180 MX MY} -halo {2 2 2 2} -default
add_pdn_stripe -grid macros -layer metal5 -width 0.93 -pitch 10 -offset 2
add_pdn_stripe -grid macros -layer metal6 -width 0.93 -pitch 10 -offset 2
add_pdn_connect -grid macros -layers {metal4 metal5}
add_pdn_connect -grid macros -layers {metal5 metal6}
add_pdn_connect -grid macros -layers {metal6 metal7}
pdngen
