# prepare_cmos.py -- retain the source material legend, with English labels.
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent/'assets'
subprocess.run(['rsvg-convert','--accept-language=en','-f','pdf',str(P/'cmos-cross-section.svg'),'-o',str(P/'cmos-cross-section.pdf')],check=True)
