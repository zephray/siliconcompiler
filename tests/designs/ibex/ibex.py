import os

from tests.designs import common

import siliconcompiler

SC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DESIGN_ROOT = os.path.join(SC_ROOT, 'third_party', 'designs', 'ibex')

def generate_floorplan(chip):

    pins = [
        ('input', 'clk_i', 1),
        ('input', 'rst_ni', 1),
        ('input', 'hart_id_i', 32),
        ('input', 'boot_addr_i', 32),

        ('output', 'instr_req_o', 1),
        ('input', 'instr_gnt_i', 1),
        ('input', 'instr_rvalid_i', 1),
        ('output', 'instr_addr_o', 32),
        ('input', 'instr_rdata_i', 32),
        ('input', 'instr_err_i', 1),

        ('output', 'data_req_o', 1),
        ('input', 'data_gnt_i', 1),
        ('input', 'data_rvalid_i', 1),
        ('output', 'data_we_o', 1),
        ('output', 'data_be_o', 4),
        ('output', 'data_addr_o', 32),
        ('output', 'data_wdata_o', 32),
        ('input', 'data_rdata_i', 32),
        ('input', 'data_err_i', 1),

        ('output', 'dummy_instr_id_o', 1),
        ('output', 'rf_raddr_a_o', 5),
        ('output', 'rf_raddr_b_o', 5),
        ('output', 'rf_waddr_wb_o', 5),
        ('output', 'rf_we_wb_o', 1),
        ('output', 'rf_wdata_wb_ecc_o', 32),
        ('input', 'rf_rdata_a_ecc_i', 32),
        ('input', 'rf_rdata_b_ecc_i', 32),

        ('output', 'ic_tag_req_o', 2),
        ('output', 'ic_tag_write_o', 1),
        ('output', 'ic_tag_addr_o', 8),
        ('output', 'ic_tag_wdata_o', 22),
        ('input',  'ic_tag_rdata_i', 44),
        ('output', 'ic_data_req_o', 2),
        ('output', 'ic_data_write_o', 1),
        ('output', 'ic_data_addr_o', 8),
        ('output', 'ic_data_wdata_o', 64),
        ('input',  'ic_data_rdata_i', 128),

        ('input', 'irq_software_i', 1),
        ('input', 'irq_timer_i', 1),
        ('input', 'irq_external_i', 1),
        ('input', 'irq_fast_i', 15),
        ('input', 'irq_nm_i', 1),
        ('output', 'irq_pending_o', 1),

        ('input', 'debug_req_i', 1),
        ('output', 'crash_dump_o', 128),

        ('input',  'fetch_enable_i', 1),
        ('output', 'alert_minor_o', 1),
        ('output', 'alert_major_o', 1),
        ('output', 'core_busy_o', 1)
    ]

    return common.generate_floorplan(chip, 25160, pins, dir='ibex')

def ibex(target):
    chip = siliconcompiler.Chip()
    chip.set('design', 'ibex_core')
    chip.add('source', os.path.join(DESIGN_ROOT, 'rtl', 'ibex_core.sv'))
    chip.add('ydir', os.path.join(DESIGN_ROOT, 'rtl'))
    chip.add('idir', os.path.join(DESIGN_ROOT, 'vendor', 'lowrisc_ip', 'ip', 'prim', 'rtl'))
    chip.add('idir', os.path.join(DESIGN_ROOT, 'vendor', 'lowrisc_ip', 'dv', 'sv', 'dv_utils'))

    chip.set('flowarg', 'sv', 'true')

    chip.target(target)
    mode = chip.get('mode')

    if mode == 'asic':
        fp_path = generate_floorplan(chip)
        chip.set('asic', 'def', fp_path)

        process = chip.get('pdk', 'process')
        if process == 'freepdk45':
            chip.clock(name='clk', pin='clk_i', period=20)
        elif process == 'skywater130':
            chip.clock(name='clk', pin='clk_i', period=40)

    return chip

if __name__ == '__main__':
    # targets = ['asicflow_freepdk45', 'asicflow_skywater130', 'fpgaflow_ice40up5k-sg48']
    targets = ['asicflow_skywater130', 'fpgaflow_ice40up5k-sg48']

    for target in targets:
        chip = ibex(target)
        chip.set('jobname', f'job_{target}')
        chip.set('quiet', True)
        chip.run()
        chip.summary()
