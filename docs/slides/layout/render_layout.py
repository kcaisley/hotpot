# render_layout.py -- render GDS directly with KLayout and the local technology.
from pathlib import Path
import os
import subprocess
ROOT = Path(__file__).resolve().parent
subprocess.run(['klayout', '-zz', '-r', str(ROOT/'render_klayout.py')],
               check=True, env={**os.environ, 'QT_QPA_PLATFORM': 'offscreen'})
