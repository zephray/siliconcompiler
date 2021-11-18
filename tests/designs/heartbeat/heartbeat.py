from tests.designs import common

import siliconcompiler

def generate_floorplan(chip):
    pins = [
        ('input', 'clk', 1),
        ('input', 'nreset', 1),
        ('output', 'out', 1),
    ]

    return common.generate_floorplan(chip, 67, pins)

def heartbeat(target):
    chip = siliconcompiler.Chip()
    chip.set('source', 'heartbeat.v')
    chip.set('design', 'heartbeat')

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
            chip.clock(name='clk', pin='clk', period=1.0)
        elif process == 'skywater130':
            chip.clock(name='clk', pin='clk', period=6.5)

    return chip

if __name__ == '__main__':
    targets = ['asicflow_freepdk45', 'asicflow_skywater130', 'fpgaflow_ice40up5k-sg48']

    for target in targets:
        chip = heartbeat(target)
        chip.set('jobname', f'job_{target}')
        chip.set('quiet', True)
        chip.run()
        chip.summary()
