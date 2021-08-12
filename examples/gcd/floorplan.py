import math

def setup_floorplan(fp, chip):
    fp.db_units = 1000

    cell_h = fp.std_cell_height
    die_w = 72 * cell_h
    die_h = 72 * cell_h
    margin = 8 * cell_h
    fp.create_die_area(die_w, die_h, core_area=(margin, margin, die_w - margin, die_h - margin))

    in_pins = ['clk']
    in_pins += [f'req_msg[{i}]' for i in range(32)]
    in_pins += ['req_val', 'reset', 'resp_rdy']

    out_pins = ['req_rdy']
    out_pins += [f'resp_msg[{i}]' for i in range(16)]
    out_pins += ['resp_val']

    metal = chip.get('asic', 'hpinlayer')
    width = 3 * fp.layers[metal]['width']
    height = 1 * fp.layers[metal]['width']

    spacing_we = die_h / (len(in_pins) + 1)
    fp.place_pins(in_pins, 0, spacing_we - height/2, 0, spacing_we, width, height, metal, snap=True) # west

    spacing_ea = die_h / (len(out_pins) + 1)
    fp.place_pins(out_pins, die_w - width, spacing_ea - height/2, 0, spacing_ea, width, height, metal, snap=True) # east

    metal = chip.get('asic', 'vpinlayer')
    width = 1 * fp.layers[metal]['width']
    height = 3 * fp.layers[metal]['width']
    fp.place_pins(['vdd', 'vss'], die_w / 2 - 2 * width, die_h - height, 2 * width, 0, width, height, metal, snap=True)

    # PDN
    fp.add_viarule('via_1600x480', 'M1M2_PR', (0.15, 0.15), ('m1', 'via', 'm2'), (.17, .17), (.245,  .165, .055, .165), rowcol=(1,4))
    fp.add_viarule('via2_1600x480', 'M2M3_PR', (0.2, 0.2), ('m2', 'via2', 'm3'), (.2, .2), (.04,  .140, .1, .065), rowcol=(1,4))
    fp.add_viarule('via3_1600x480', 'M3M4_PR', (0.2, 0.2), ('m3', 'via3', 'm4'), (.2, .2), (.1,  .06, .1, .14), rowcol=(1,4))
    fp.add_viarule('via4_1600x1600', 'M4M5_PR', (0.8, 0.8), ('m4', 'via4', 'm5'), (.8, .8), (.04,  .04, .04, .04))

    hpitch = 10
    hwidth = 5
    hlayer = 'm5'
    vpitch = 10
    vwidth = 5
    vlayer = 'm4'

    fp.configure_net('vdd', 'vpwr', 'power')
    fp.configure_net('vss', 'vgnd', 'ground')

    core_w = die_w - 2 * margin

    ## Horizontal straps
    n = int(core_w // (hpitch + hwidth)) + 1
    fp.place_wires(['vdd', 'vss'] * (n // 2),
        margin, margin,
        0, hpitch + hwidth,
        core_w, hwidth, hlayer, 'STRIPE')

    ## Vertical straps
    n = int(core_w // (vpitch + hwidth)) + 1
    fp.place_wires(['vdd', 'vss'] * (n // 2),
        margin, margin,
        vpitch + vwidth, 0,
        vwidth, core_w, vlayer, 'STRIPE')

    # Vias connecting vdd straps
    x = margin + vwidth / 2
    y = margin + hwidth / 2
    for _ in range(n//2):
        fp.place_vias(['vdd'] * (n//2), x, y, 2 * (vpitch + vwidth), 0, 'm4', 'via4_1600x1600')
        y += 2 * (hpitch + hwidth)

    # Vias connecting vss straps
    x = margin + vwidth / 2 + (vpitch + vwidth)
    y = margin + hwidth / 2 + (hpitch + hwidth)
    for _ in range(n//2):
        fp.place_vias(['vss'] * (n//2), x, y, 2 * (vpitch + vwidth), 0, 'm4', 'via4_1600x1600')
        y += 2 * (hpitch + hwidth)

    npwr = 1 + math.floor(len(fp.rows) / 2)
    ngnd = math.ceil(len(fp.rows) / 2)

    # Vias connecting vdd straps to std cell stripes
    x = margin + vwidth / 2
    y = margin
    for _ in range(npwr):
        fp.place_vias(['vdd'] * (n//2), x, y, 2 * (vpitch + vwidth), 0, 'm3', 'via3_1600x480')
        fp.place_vias(['vdd'] * (n//2), x, y, 2 * (vpitch + vwidth), 0, 'm2', 'via2_1600x480')
        fp.place_vias(['vdd'] * (n//2), x, y, 2 * (vpitch + vwidth), 0, 'm1', 'via1_1600x480')
        y += 2 * fp.std_cell_height

    # Vias connecting vss straps to std cell stripes
    x = margin + vwidth / 2 + (vpitch + vwidth)
    y = margin + fp.std_cell_height
    for _ in range(ngnd):
        fp.place_vias(['vss'] * (n//2), x, y, 2 * (vpitch + vwidth), 0, 'm3', 'via3_1600x480')
        fp.place_vias(['vss'] * (n//2), x, y, 2 * (vpitch + vwidth), 0, 'm2', 'via2_1600x480')
        fp.place_vias(['vss'] * (n//2), x, y, 2 * (vpitch + vwidth), 0, 'm1', 'via1_1600x480')
        y += 2 * fp.std_cell_height

    return fp
