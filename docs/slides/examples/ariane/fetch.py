from pathlib import Path
from urllib.request import urlopen
import hashlib
import gzip
import shutil

files = [('ariane.v',
  'https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD/14b1ef13293b2a4c165d67cd81b4c48a4be9c5f4/src/par/examples/timing-aware-partitioning/ariane.v',
  'e65e29f430db4bc5cf21d39edeedad00e816b3aa6982891a8916d062bab350f6'),
 ('NangateOpenCellLibrary.tech.lef',
  'https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD-flow-scripts/3a964e13f/flow/platforms/nangate45/lef/NangateOpenCellLibrary.tech.lef',
  '834a79295054cd4209178d1bade67c353863c47bb4b3c22ee38b862b7cec37f2'),
 ('NangateOpenCellLibrary.macro.mod.lef',
  'https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD-flow-scripts/3a964e13f/flow/platforms/nangate45/lef/NangateOpenCellLibrary.macro.mod.lef',
  'a43aea339f12a57a63497783e508ba16f3da2dc056d3247dec7d99707c2dedef'),
 ('fakeram45_256x16.lef',
  'https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD-flow-scripts/3a964e13f/flow/platforms/nangate45/lef/fakeram45_256x16.lef',
  '963800bda44bd5f13c1f6ee9ecf1f51b3805d58c2780d922b129bbaa7eb5f775'),
 ('NangateOpenCellLibrary_typical.lib',
  'https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD-flow-scripts/3a964e13f/flow/platforms/nangate45/lib/NangateOpenCellLibrary_typical.lib',
  '8d540a4d4cf6d09d27c87ad067857a9c0c2eeb023ab7a56e058cd3113db4e9b1'),
 ('fakeram45_256x16.lib',
  'https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD-flow-scripts/3a964e13f/flow/platforms/nangate45/lib/fakeram45_256x16.lib',
  '1226b624618d90376b0af26ed788adcfe8e8a57e78e2c10b3583f656f7a039e0'),
 ('rcx_patterns.rules',
  'https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD-flow-scripts/3a964e13f/flow/platforms/nangate45/rcx_patterns.rules',
  '2f65fafbe2c704b378563c53a680b93cef080c2799997019d43df7d1e5a563e9')]
inputs = Path(__file__).resolve().parent / "inputs"
inputs.mkdir(exist_ok=True)
for name, url, digest in files:
    target = inputs / name
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == digest:
        continue
    with urlopen(url, timeout=120) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != digest:
        raise RuntimeError(f"Checksum mismatch: {name}")
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(target)
    print(f"Downloaded {name}")

checkpoint = inputs.parent / "checkpoint"
root = next(parent for parent in Path(__file__).resolve().parents if (parent / "flow_ariane.tcl").is_file())
results = root / "results" / "ariane"
results.mkdir(exist_ok=True)
for archive in checkpoint.glob("*.gz"):
    target = results / archive.stem
    if not target.exists():
        temporary = target.with_suffix(target.suffix + ".tmp")
        with gzip.open(archive, "rb") as source, temporary.open("wb") as output:
            shutil.copyfileobj(source, output)
        temporary.replace(target)
        print(f"Unpacked {target.name}")
