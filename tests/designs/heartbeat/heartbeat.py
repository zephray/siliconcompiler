import math

import siliconcompiler
from siliconcompiler.floorplan import Floorplan

def generate_floorplan(chip):
    fp = Floorplan(chip)
    site_area = fp.stdcell_width * fp.stdcell_height
    area = 67 * 5 * (site_area / 0.266)
    sidelength = math.sqrt(area)

    corewidth = fp.snap(sidelength, fp.stdcell_width)
    coreheight = fp.snap(sidelength, fp.stdcell_height)

    coremargin = 10
    coremargin_w = fp.snap(coremargin, fp.stdcell_width)
    coremargin_h = fp.snap(coremargin, fp.stdcell_height)

    die_width = corewidth + 2 * coremargin_w
    die_height = coreheight + 2 * coremargin_h

    fp.create_diearea([(0, 0), (die_width, die_height)],
                      corearea=[(coremargin_w, coremargin_h),
                                (corewidth + coremargin_w, coreheight + coremargin_h)])

    in_pins = ['clk', 'nreset']
    out_pins = ['out']

    layer = chip.get('asic', 'hpinlayer')
    width = fp.layers[layer]['width']
    depth = 3 * width

    in_spacing = (die_height - len(in_pins) * width) / (len(in_pins) + 1)
    fp.place_pins(in_pins, 0, in_spacing, 0, in_spacing + width, depth, width, layer, snap=True)

    out_spacing = (die_height - len(out_pins) * width) / (len(out_pins) + 1)
    fp.place_pins(out_pins, die_width-depth, out_spacing, 0, out_spacing + width, depth, width, layer, snap=True)

    outfile = 'heartbeat.def'
    fp.write_def(outfile)

    return outfile

def heartbeat(target):
    chip = siliconcompiler.Chip()
    chip.set('source', 'heartbeat.v')
    chip.set('design', 'heartbeat')

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
    elif mode == 'fpga':
        partname = chip.get('fpga', 'partname')
        if partname == 'ice40up5k-sg48':
            chip.add('constraint', 'heartbeat_ice40.pcf')

    return chip

if __name__ == '__main__':
    targets = ['asicflow_freepdk45', 'asicflow_skywater130', 'fpgaflow_ice40up5k-sg48']

    for target in targets:
        chip = heartbeat(target)
        chip.set('jobname', f'job_{target}')
        chip.set('quiet', True)
        chip.run()
        chip.summary()
