import math
import os

import siliconcompiler
from siliconcompiler.floorplan import Floorplan

SC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DESIGN_ROOT = os.path.join(SC_ROOT, 'third_party', 'designs', 'picorv32')

def generate_floorplan(chip):
    fp = Floorplan(chip)
    site_area = fp.stdcell_width * fp.stdcell_height
    area = 16407 * 7 * (site_area / 0.266)
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

    in_pins = ['clk', 'resetn', 'mem_ready']
    in_pins += [f'mem_rdata[{n}]' for n in range(32)]
    in_pins += ['pcpi_wr']
    in_pins += [f'pcpi_rd[{n}]' for n in range(32)]
    in_pins += ['pcpi_wait', 'pcpi_ready']
    in_pins += [f'irq[{n}]' for n in range(32)]

    out_pins = ['trap', 'mem_valid', 'mem_instr']
    out_pins += [f'mem_addr[{n}]' for n in range(32)]
    out_pins += [f'mem_wdata[{n}]' for n in range(32)]
    out_pins += [f'mem_wstrb[{n}]' for n in range(4)]
    out_pins += ['mem_la_read', 'mem_la_write']
    out_pins += [f'mem_la_addr[{n}]' for n in range(32)]
    out_pins += [f'mem_la_wdata[{n}]' for n in range(32)]
    out_pins += [f'mem_la_wstrb[{n}]' for n in range(32)]
    out_pins += ['pcpi_valid']
    out_pins += [f'pcpi_insn[{n}]' for n in range(32)]
    out_pins += [f'pcpi_rs1[{n}]' for n in range(32)]
    out_pins += [f'pcpi_rs2[{n}]' for n in range(32)]
    out_pins += [f'eoi[{n}]' for n in range(32)]
    out_pins += ['trace_valid']
    out_pins += [f'trace_data[{n}]' for n in range(36)]

    layer = chip.get('asic', 'hpinlayer')
    width = fp.layers[layer]['width']
    depth = 3 * width

    in_spacing = (die_height - len(in_pins) * width) / (len(in_pins) + 1)
    fp.place_pins(in_pins, 0, in_spacing, 0, in_spacing + width, depth, width, layer, snap=True)

    out_spacing = (die_height - len(out_pins) * width) / (len(out_pins) + 1)
    fp.place_pins(out_pins, die_width-depth, out_spacing, 0, out_spacing + width, depth, width, layer, snap=True)

    outfile = 'picorv32.def'
    fp.write_def(outfile)

    return outfile

def picorv32(target):
    chip = siliconcompiler.Chip()
    chip.set('design', 'picorv32')
    chip.set('source', os.path.join(DESIGN_ROOT, 'picorv32.v'))

    chip.target(target)
    mode = chip.get('mode')

    if mode == 'asic':
        fp_path = generate_floorplan(chip)
        chip.set('asic', 'def', fp_path)

        process = chip.get('pdk', 'process')
        if process == 'freepdk45':
            chip.clock(name='clk', pin='clk', period=4)
        elif process == 'skywater130':
            chip.clock(name='clk', pin='clk', period=10)

    return chip

if __name__ == '__main__':
    chip = picorv32('asicflow_freepdk45')
    chip.set('quiet', True)
    chip.run()
    chip.summary()
