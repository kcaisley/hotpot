* inverter_test.sp
.include models/NMOS_VTL.inc
.include models/PMOS_VTL.inc
.include ../examples/inverter.sp
.temp 25
VDD vdd 0 1.1
VIN src 0 PULSE(0 1.1 100p 10p 10p 300p 700p)
RS src A 2k
CIN A 0 5f
Xinv A ZN vdd 0 INV_X1
RL ZN load 1k
CLOAD load 0 10f
.control
set noaskquit
set wr_singlescale
set wr_vecnames
tran 0.2p 1.5n
let psupply = -v(vdd)*i(VDD)
wrdata inverter_waveforms.dat v(src) v(A) v(ZN) v(load) psupply
meas tran tphl TRIG v(A) VAL=0.55 RISE=1 TARG v(ZN) VAL=0.55 FALL=1
meas tran tplh TRIG v(A) VAL=0.55 FALL=1 TARG v(ZN) VAL=0.55 RISE=1
meas tran rise_A TRIG v(A) VAL=0.33 RISE=1 TARG v(A) VAL=0.77 RISE=1
meas tran fall_ZN TRIG v(ZN) VAL=0.77 FALL=1 TARG v(ZN) VAL=0.33 FALL=1
meas tran energy INTEG psupply FROM=700p TO=1.4n
quit
.endc
.end
