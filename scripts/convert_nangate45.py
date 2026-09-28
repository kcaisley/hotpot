#!/usr/bin/env python3
"""Merge a routed Nangate45 DEF with standard-cell GDS using ORFS def2stream.

Run from anywhere with ``python3 scripts/convert_nangate45.py gcd`` or
``python3 scripts/convert_nangate45.py ariane --allow-empty-fakeram``.
The Ariane option permits its LEF-only teaching SRAM to remain an empty cell;
the resulting GDS is useful for viewing, not physical signoff.
"""

import argparse
import os
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ORFS = ROOT.parent / "libs" / "OpenROAD-flow-scripts" / "flow"
INPUTS = ROOT / "slides" / "examples" / "ariane" / "inputs"
DESIGNS = {
    "gcd": (ROOT / "results/gcd/gcd_final.def", ROOT / "results/gcd/gcd_final.gds"),
    "ariane": (ROOT / "results/ariane/final.def", ROOT / "results/ariane/final.gds"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("design", choices=DESIGNS)
    parser.add_argument("--allow-empty-fakeram", action="store_true")
    parser.add_argument("--orfs-flow", type=Path, default=ORFS)
    args = parser.parse_args()
    if args.design == "ariane" and not args.allow_empty_fakeram:
        parser.error("Ariane has no fakeram45_256x16 GDS; pass --allow-empty-fakeram for a preview GDS")

    platform = args.orfs_flow / "platforms" / "nangate45"
    gds = platform / "gds" / "NangateOpenCellLibrary.gds"
    tech = platform / "FreePDK45.lyt"
    source_def, output_gds = DESIGNS[args.design]
    for path in (gds, tech, source_def):
        if not path.is_file():
            parser.error(f"missing input: {path}")

    tree = ET.parse(tech)
    lefdef = tree.find(".//reader-options/lefdef")
    if lefdef is None:
        parser.error(f"technology file has no LEF/DEF reader options: {tech}")
    for child in list(lefdef):
        if child.tag == "lef-files":
            lefdef.remove(child)
    for name in (
        "NangateOpenCellLibrary.tech.lef",
        "NangateOpenCellLibrary.macro.mod.lef",
        "fakeram45_256x16.lef",
    ):
        path = INPUTS / name
        if not path.is_file():
            parser.error(f"missing LEF: {path}")
        ET.SubElement(lefdef, "lef-files").text = str(path)

    env = os.environ.copy()
    env["GDS_ALLOW_EMPTY"] = "^fakeram45_256x16$" if args.allow_empty_fakeram else ""
    with tempfile.TemporaryDirectory(prefix="nangate45_lyt_") as tmp:
        configured_tech = Path(tmp) / "FreePDK45.lyt"
        tree.write(configured_tech, encoding="utf-8", xml_declaration=True)
        command = [
            "klayout", "-b", "-r", str(ROOT / "scripts/def2stream.py"),
            "-rd", f"tech_file={configured_tech}",
            "-rd", "layer_map=",
            "-rd", f"in_def={source_def}",
            "-rd", f"design_name={args.design}",
            "-rd", f"in_files={gds}",
            "-rd", "seal_file=",
            "-rd", f"out_file={output_gds}",
        ]
        subprocess.run(command, check=True, env=env)
    print(f"Wrote {output_gds}")


if __name__ == "__main__":
    main()
