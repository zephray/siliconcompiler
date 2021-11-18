import os

from tests.designs import common

import siliconcompiler

SC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DESIGN_ROOT = os.path.join(SC_ROOT, 'third_party', 'designs', 'picorv32')

def generate_floorplan(chip):
    pins = [
        ('input', 'clk', 1),
        ('input', 'resetn', 1),
        ('input', 'mem_ready', 1),
        ('input', 'mem_rdata', 32),
        ('input', 'pcpi_wr', 1),
        ('input', 'pcpi_rd', 32),
        ('input', 'pcpi_wait', 1),
        ('input', 'pcpi_ready', 1),
        ('input', 'irq', 32),

        ('output', 'trap', 1),
        ('output', 'mem_valid', 1),
        ('output', 'mem_instr', 1),
        ('output', 'mem_addr', 32),
        ('output', 'mem_wdata', 32),
        ('output', 'mem_wstrb', 4),
        ('output', 'mem_la_read', 1),
        ('output', 'mem_la_write', 1),
        ('output', 'mem_la_addr', 32),
        ('output', 'mem_la_wdata', 32),
        ('output', 'mem_la_wstrb', 32),
        ('output', 'pcpi_valid', 1),
        ('output', 'pcpi_insn', 32),
        ('output', 'pcpi_rs1', 32),
        ('output', 'pcpi_rs2', 32),
        ('output', 'eoi', 32),
        ('output', 'trace_valid', 1),
        ('output', 'trace_data', 36)
    ]

    return common.generate_floorplan(chip, 16407, pins)

def picorv32(target):
    chip = siliconcompiler.Chip()
    chip.set('design', 'picorv32')
    chip.set('source', os.path.join(DESIGN_ROOT, 'picorv32.v'))

    flow, tech = target.split('_')
    if flow == 'asicflow' and tech != 'freepdk45':
        chip.set('flowarg', 'verify', 'true')

    chip.target(target)
    mode = chip.get('mode')

    if mode == 'asic':
        fp_path = generate_floorplan(chip)
        chip.set('asic', 'def', fp_path)

        process = chip.get('pdk', 'process')
        if process == 'freepdk45':
            chip.clock(name='clk', pin='clk', period=20)
        elif process == 'skywater130':
            chip.clock(name='clk', pin='clk', period=40)
    else:
        partname = chip.get('fpga', 'partname')
        if partname == 'fpgaflow_ice40up5k-sg48':
            chip.set('design', 'icebreaker')
            chip.add('source', os.path.join(DESIGN_ROOT, 'picosoc', 'icebreaker.v'))
            chip.add('source', os.path.join(DESIGN_ROOT, 'picosoc', 'picosoc.v'))
            chip.add('source', os.path.join(DESIGN_ROOT, 'picosoc', 'simpleuart.v'))
            chip.add('source', os.path.join(DESIGN_ROOT, 'picosoc', 'spimemio.v'))
            chip.add('constraint', os.path.join(DESIGN_ROOT, 'picosoc', 'icebreaker.pcf'))

    return chip

if __name__ == '__main__':
    targets = ['asicflow_freepdk45', 'asicflow_skywater130', 'fpgaflow_ice40up5k-sg48']

    for target in targets:
        chip = picorv32(target)
        chip.set('jobname', f'job_{target}')
        chip.set('quiet', True)
        chip.run()
        chip.summary()
