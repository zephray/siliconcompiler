import math
import os

from siliconcompiler.floorplan import Floorplan

def generate_floorplan(chip, freepdk45_cellarea, pins, target_util=0.15, coremargin=10, dir=None):
    # Use FreePDK45 placement site size as a normalization factor for scaling
    # area for other PDKs
    freepdk45_site_area = 0.266

    fp = Floorplan(chip)
    site_area = fp.stdcell_width * fp.stdcell_height
    area = freepdk45_cellarea / target_util  * (site_area / freepdk45_site_area)
    sidelength = math.sqrt(area)

    corewidth = fp.snap(sidelength, fp.stdcell_width)
    coreheight = fp.snap(sidelength, fp.stdcell_height)

    coremargin_w = fp.snap(coremargin, fp.stdcell_width)
    coremargin_h = fp.snap(coremargin, fp.stdcell_height)

    die_width = corewidth + 2 * coremargin_w
    die_height = coreheight + 2 * coremargin_h

    fp.create_diearea([(0, 0), (die_width, die_height)],
                      corearea=[(coremargin_w, coremargin_h),
                                (corewidth + coremargin_w, coreheight + coremargin_h)])

    in_pins = []
    out_pins = []
    for iodir, pinname, buswidth in pins:
        if buswidth == 1:
            pins = [pinname]
        else:
            pins = [f'{pinname}[{i}]' for i in range(buswidth)]

        if iodir == 'input':
            in_pins.extend(pins)
        else:
            out_pins.extend(pins)

    layer = chip.get('asic', 'hpinlayer')
    width = fp.layers[layer]['width']
    depth = 3 * width

    in_spacing = (die_height - len(in_pins) * width) / (len(in_pins) + 1)
    fp.place_pins(in_pins, 0, in_spacing, 0, in_spacing + width, depth, width, layer, snap=True)

    out_spacing = (die_height - len(out_pins) * width) / (len(out_pins) + 1)
    fp.place_pins(out_pins, die_width-depth, out_spacing, 0, out_spacing + width, depth, width, layer, snap=True)

    design = chip.get('design')
    if dir is None:
        dir = design
    mydir = os.path.dirname(__file__)
    outfile = os.path.join(mydir, dir, f'{design}.def')
    fp.write_def(outfile)

    return outfile

