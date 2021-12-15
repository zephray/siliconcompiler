import importlib
import os

# Hack to make sure we don't try to import migen.py in this directory.
import sys
cwd = sys.path.pop(0)
from migen.fhdl.verilog import convert
from migen import Signal
sys.path.insert(0, cwd)

import siliconcompiler

chip = siliconcompiler.Chip()
chip.read_manifest('sc_manifest.json')
design = chip.get('design')

design_dir = os.path.join(os.getcwd(), 'inputs', f'{design}.py')

spec = importlib.util.spec_from_file_location(design, design_dir)
imported = importlib.util.module_from_spec(spec)
spec.loader.exec_module(imported)

design_module = getattr(imported, design)
output = os.path.join('outputs', f'{design}.v')

instance = design_module()
convert(instance, set(instance.ios), name=design).write(output)
