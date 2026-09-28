# DEF to GDS script

`def2stream.py` was downloaded on 2026-09-23 from the official
[OpenROAD Flow Scripts source](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/util/def2stream.py).
It is kept unmodified. `convert_nangate45.py` supplies this repository's
Nangate45 technology and library paths.

Run `python3 scripts/convert_nangate45.py gcd` for a complete cell merge.
Run `python3 scripts/convert_nangate45.py ariane --allow-empty-fakeram` for a
preview GDS. The Ariane design contains `fakeram45_256x16`, whose LEF exists
here but whose physical GDS does not. The preview leaves that macro empty and
must not be used as a complete GDS for DRC, LVS, or fabrication.
