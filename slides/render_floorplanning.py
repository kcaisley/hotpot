from pathlib import Path
import os
import subprocess

HERE = Path(__file__).resolve().parent
root = os.environ.get("OPENROAD_ROOT")
if not root or not (Path(root) / "test/Nangate45/Nangate45_tech.lef").is_file():
    raise SystemExit("Set OPENROAD_ROOT to an OpenROAD source checkout containing test/Nangate45.")
env = dict(os.environ, OPENROAD_ROOT=str(Path(root).resolve()), QT_QPA_PLATFORM="offscreen")
logs = HERE / "build/floorplanning"
logs.mkdir(parents=True, exist_ok=True)


def run(name, script, gui=False, stage=None):
    command = ["openroad", "-no_init", "-exit"]
    if gui:
        command.append("-gui")
    result = subprocess.run(
        command + [str(script)], cwd=HERE,
        env=dict(env, HOTPOT_FP_STAGE=stage or ""),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    (logs / f"{name}.log").write_text(result.stdout)
    if result.returncode or "[ERROR" in result.stdout:
        raise RuntimeError(f"{name} failed; see {logs / (name + '.log')}")
    print(name, "OK", flush=True)


run("flow", HERE / "examples/floorplanning/floorplan.tcl")
run("macro_setup", HERE / "examples/floorplanning/macros.tcl")
for stage in """floorplan compact wide margin explicit rows tracks taps rails
                straps pdn vias placed pins_auto pins_sides pins_close
                pins_anneal pin_fixed pins_group macros macros_halo macros_auto routability""".split():
    run(stage, HERE / "render_floorplanning.tcl", gui=True, stage=stage)
