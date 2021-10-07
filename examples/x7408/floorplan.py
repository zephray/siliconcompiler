import math

from siliconcompiler.core import Chip
from siliconcompiler.floorplan import Floorplan

GPIO = 'sky130_ef_io__gpiov2_pad_wrapped'
VDD = 'sky130_ef_io__vccd_hvc_pad'
VDDIO = 'sky130_ef_io__vddio_hvc_pad'
VSS = 'sky130_ef_io__vssd_hvc_pad'
VSSIO = 'sky130_ef_io__vssio_hvc_pad'
CORNER = 'sky130_ef_io__corner_pad'
FILL_CELLS = ['sky130_ef_io__com_bus_slice_1um',
              'sky130_ef_io__com_bus_slice_5um',
              'sky130_ef_io__com_bus_slice_10um',
              'sky130_ef_io__com_bus_slice_20um']

def calculate_even_spacing(fp, pads, distance, start):
    n = len(pads)
    pads_width = sum(fp.available_cells[pad].width for pad in pads)
    spacing = (distance - pads_width) // (n + 1)

    pos = start + spacing
    io_pos = []
    for pad in pads:
        io_pos.append((pad, pos))
        pos += fp.available_cells[pad].width + spacing

    return io_pos

def core_floorplan(fp, chip):
    place_w = 240 * fp.stdcell_width
    place_h = 40 * fp.stdcell_height
    margin_left = 24 * fp.stdcell_width
    margin_bottom = 4 * fp.stdcell_height
    core_w = place_w + (2 * margin_left)
    core_h = place_h + (2 * margin_bottom)

    #gpio_h = fp.available_cells[GPIO].height
    gpio_w = margin_left
    gpio_h = margin_bottom

    top_w = math.ceil(core_w + 2 * gpio_h)
    top_h = math.ceil(core_h + 2 * gpio_h)
    core_w = top_w - 2 * gpio_h
    core_h = top_h - 2 * gpio_h

    chip.set('asic', 'diearea', [(0,0), (core_w, core_h)])
    chip.set('asic', 'corearea', [(margin_left,margin_bottom), (place_w+margin_left,place_h+margin_bottom)])
    fp.create_diearea([(0, 0), (core_w, core_h)],
                     corearea=[(margin_left, margin_bottom),
                               (place_w + margin_left, place_h + margin_bottom)])

    gpio_Lb = margin_left + gpio_h/2
    gpio_Bb = margin_bottom + gpio_h
    chip.logger.info(f'DIE  X: 0 Y: 0 W: {core_w} H: {core_h}')
    chip.logger.info(f'CORE X: {margin_left} Y: {margin_bottom} W: {place_w} H: {place_h}')
    chip.logger.info(f'X: {gpio_Lb} Y: {gpio_Bb} W: {gpio_h} H: {gpio_h}')

    fp.place_pins(['A1', 'B1', 'A2', 'B2'], 0, margin_bottom + gpio_h, 0, gpio_h*2, gpio_w, gpio_h, 'm5', direction='input')
    fp.place_pins(['A3', 'B3', 'A4', 'B4'], core_w - margin_left, margin_bottom + gpio_h, 0, gpio_h*2, gpio_w, gpio_h, 'm5', direction='input')
    fp.place_pins(['Y1', 'Y2', 'Y3', 'Y4'], margin_left + gpio_w, 0, gpio_w*2, 0, gpio_w, gpio_h, 'm5', direction='output')

    # Setup power nets and pins
    fp.add_net('_vdd', ['VPWR'], 'power')
    fp.add_net('_vss', ['VGND'], 'ground')
    fp.place_pins(['_vdd', '_vss', '_vdd', '_vss'], margin_left + gpio_w, core_h - margin_bottom, gpio_w*2, 0, gpio_w, gpio_h, 'm5', direction='inout')

    '''
    # PDN
    place_min_x = margin_left
    place_min_y = margin_bottom
    place_max_x = margin_left + place_w
    place_max_y = margin_bottom + place_h
    corner_w = fp.available_cells[CORNER].width
    corner_h = fp.available_cells[CORNER].height
    we_io = [GPIO] * 4
    no_io = [VDD, VSS, VDD, VSS]
    ea_io = [GPIO] * 4
    so_io = [GPIO] * 4
    we_pads = calculate_even_spacing(fp, we_io, top_h - corner_h - corner_w, corner_h)
    so_pads = calculate_even_spacing(fp, so_io, top_w - corner_h - corner_w, corner_w)
    no_pads = calculate_even_spacing(fp, no_io, top_w - corner_h - corner_w, corner_w)
    ea_pads = calculate_even_spacing(fp, ea_io, top_h - corner_h - corner_w, corner_h)

    #fp.place_pins(['A1', 'B1', 'A2', 'B2'], margin_left, margin_bottom + gpio_h, 0, gpio_h, gpio_h, gpio_h, 'm5', direction='input')
    #fp.place_pins(['A3', 'B3', 'A4', 'B4'], core_w - margin_left, margin_bottom + gpio_h, 0, gpio_h, gpio_h, gpio_h, 'm5', direction='input')
    #fp.place_pins(['Y1', 'Y2', 'Y3', 'Y4'], margin_left + gpio_h, margin_bottom, gpio_h, 0, gpio_h, gpio_h, 'm5', direction='output')
    #for y in we_pads:

    n_vert = 2 # how many vertical straps to place
    vwidth = 5 # width of vertical straps in microns
    n_hori = 4 # how many horizontal straps to place
    hwidth = 5 # width of horizontal straps
    vlayer = 'm4' # metal layer for vertical straps
    hlayer = 'm5' # metal layer for horizontal straps
    vpitch = (core_w - n_vert * vwidth) / (n_vert + 1)
    hpitch = (core_h - n_hori * hwidth) / (n_hori + 1)

    # Power ring
    vss_ring_left_x = place_min_x - 4 * vwidth
    vss_ring_bottom_y = place_min_y - 4 * hwidth
    vss_ring_width = place_w + 9 * vwidth
    vss_ring_height = place_h + 9 * hwidth
    vss_ring_right_x = vss_ring_left_x + vss_ring_width
    vss_ring_top_y = vss_ring_bottom_y + vss_ring_height
    vdd_ring_left_x = vss_ring_left_x + 2 * vwidth
    vdd_ring_bottom_y = vss_ring_bottom_y + 2 * hwidth
    vdd_ring_width = vss_ring_width - 4 * vwidth
    vdd_ring_height = vss_ring_height - 4 * hwidth
    vdd_ring_right_x = vdd_ring_left_x + vdd_ring_width
    vdd_ring_top_y = vdd_ring_bottom_y + vdd_ring_height
    chip.logger.info
    fp.place_ring('_vdd', vdd_ring_left_x, vdd_ring_bottom_y, vdd_ring_width, vdd_ring_height, hwidth, vwidth, hlayer, vlayer)
    fp.place_ring('_vss', vss_ring_left_x, vss_ring_bottom_y, vss_ring_width, vss_ring_height, hwidth, vwidth, hlayer, vlayer)

    # Place horizontal power straps
    fp.place_wires(['_vdd'] * (n_hori // 2), vdd_ring_left_x, margin_bottom + hpitch, 0, 2 * (hpitch + hwidth), vdd_ring_width, hwidth, hlayer, 'STRIPE')
    fp.place_wires(['_vss'] * (n_hori // 2), vss_ring_left_x, margin_bottom + hpitch + (hpitch + hwidth), 0, 2 * (hpitch + hwidth), vss_ring_width, hwidth, hlayer, 'STRIPE')

    # Place vertial power straps
    fp.place_wires(['_vdd'] * (n_vert // 2),
        place_min_x + vpitch, vdd_ring_bottom_y,
        2 * (vpitch + vwidth), 0,
        vwidth, vdd_ring_height, vlayer, 'STRIPE')
    fp.place_wires(['_vss'] * (n_vert // 2),
        place_min_x + vpitch + (vpitch + vwidth), vss_ring_bottom_y,
        2 * (vpitch + vwidth), 0,
        vwidth, vss_ring_height, vlayer, 'STRIPE')

    gpio_h = fp.available_cells[GPIO].height
    pow_h = fp.available_cells[VDD].height
    pow_gap = gpio_h - pow_h

    # Place wires connecting power pads to the power ring
    for pad_type, y in we_pads:
        y -= gpio_h
        if pad_type == VDD:
            fp.place_wires(['_vdd'], 0, y + 0.495, 0, 0, vdd_ring_left_x + vwidth, 23.9, 'm3', 'followpin')
            fp.place_pins (['_vdd'], 0, y + 0.495, 0, 0, vdd_ring_left_x + vwidth, 23.9, 'm3')
        elif pad_type == VSS:
            fp.place_wires(['_vss'], 0, y + 0.495, 0, 0, vss_ring_left_x + vwidth, 23.9, 'm3', 'followpin')
            fp.place_pins( ['_vss'], 0, y + 0.495, 0, 0, vss_ring_left_x + vwidth, 23.9, 'm3')
        else:
            continue

    # Insert power vias.
    fp.insert_vias(layers=[('m1', 'm4'), ('m3', 'm4'), ('m3', 'm5'), ('m4', 'm5')])
    '''

def generate_core_floorplan(chip):
    fp = Floorplan(chip)
    core_floorplan(fp, chip)
    fp.write_def('asic_core.def')
    fp.write_lef('asic_core.lef')
