import siliconcompiler
import os

microwatt_wd = "../../third_party/designs/microwatt/"

def add_sources(chip):
    chip.add('input', 'vhdl', microwatt_wd + 'decode_types.vhdl')
    chip.add('input', 'vhdl', microwatt_wd + 'common.vhdl')
    chip.add('input', 'vhdl', microwatt_wd + 'wishbone_types.vhdl')
    chip.add('input', 'vhdl', microwatt_wd + 'fetch1.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'utils.vhdl')
    chip.add('input', 'vhdl', microwatt_wd + 'plru.vhdl') # keep
    # chip.add('input', 'vhdl', microwatt_wd + 'cache_ram.vhdl') # keep
    chip.add('input', 'vhdl', 'cache_ram.vhdl')
    chip.add('input', 'vhdl', 'ram/sram_0rw1r1w_64_512_freepdk45.vhdl')
    chip.add('input', 'vhdl', microwatt_wd + 'icache.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'decode1.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'helpers.vhdl')
    chip.add('input', 'vhdl', microwatt_wd + 'insn_helpers.vhdl')
    chip.add('input', 'vhdl', microwatt_wd + 'control.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'decode2.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'register_file.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'cr_file.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'crhelpers.vhdl')
    chip.add('input', 'vhdl', microwatt_wd + 'ppc_fx_insns.vhdl')
    chip.add('input', 'vhdl', microwatt_wd + 'rotator.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'logical.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'countzero.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'multiply.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'divider.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'execute1.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'loadstore1.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'mmu.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'dcache.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'writeback.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'core_debug.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'core.vhdl') # keep
    chip.add('input', 'vhdl', microwatt_wd + 'fpu.vhdl') # keep
    # chip.add('input', 'vhdl', microwatt_wd + 'wishbone_arbiter.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'wishbone_bram_wrapper.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'sync_fifo.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'wishbone_debug_master.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'xics.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'syscon.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'gpio.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'soc.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'spi_rxtx.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'spi_flash_ctrl.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'fpga/soc_reset.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'fpga/pp_fifo.vhd')
    # chip.add('input', 'vhdl', microwatt_wd + 'fpga/pp_soc_uart.vhd')
    # chip.add('input', 'vhdl', microwatt_wd + 'fpga/main_bram.vhdl')
    chip.add('input', 'vhdl', microwatt_wd + 'nonrandom.vhdl') # keep
    # chip.add('input', 'vhdl', microwatt_wd + 'fpga/clk_gen_ecp5.vhd')
    # chip.add('input', 'vhdl', microwatt_wd + 'fpga/top-generic.vhdl')
    # chip.add('input', 'vhdl', microwatt_wd + 'dmi_dtm_dummy.vhdl')

def setup_ram(chip):
    ram = siliconcompiler.Chip('sram_0rw1r1w_64_512_freepdk45')
    stackup = chip.get('asic', 'stackup')
    ram.set('model', 'layout', 'gds', stackup,
        'ram/sram_0rw1r1w_64_512_freepdk45.gds')
    ram.set('model', 'layout', 'lef', stackup,
        'ram/sram_0rw1r1w_64_512_freepdk45.lef')

    chip.add('asic', 'macrolib', 'sram_0rw1r1w_64_512_freepdk45')
    chip.import_library(ram)

def main():
    chip = siliconcompiler.Chip('core')
    add_sources(chip)

    cwd = os.getcwd() + '/' + microwatt_wd
    chip.add('option', 'define', 'MEMORY_SIZE=8192')
    chip.add('option', 'define', 'RAM_INIT_FILE='+cwd+'/hello_world/hello_world.hex')
    chip.add('option', 'define', 'RESET_LOW=true')
    chip.add('option', 'define', 'CLK_INPUT=50000000')
    chip.add('option', 'define', 'CLK_FREQUENCY=40000000')

    chip.set('option', 'frontend', 'vhdl')
    chip.set('option', 'steplist', ['physyn', 'floorplan', 'place'])
    chip.load_target('freepdk45_demo')
    setup_ram(chip)

    chip.run()

if __name__ == '__main__':
    main()
