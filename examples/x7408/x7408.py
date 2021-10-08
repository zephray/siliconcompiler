# Copyright 2020 Silicon Compiler Authors. All Rights Reserved.
# Build script for a 4x 2-input AND gate chip, like a simple 74x08.
import argparse
import os
import siliconcompiler

from floorplan import generate_core_floorplan

############################
def build_fpga():
    '''
    Helper method to build the design into an iCE40 bitstream.
    '''

    # TODO
    pass

############################
def build_core():
    '''
    Helper method to build the core design, without a top-level padring.
    '''

    #chip = siliconcompiler.Chip(design='x7408_top', loglevel='INFO')
    chip = siliconcompiler.Chip(design='x7408', loglevel='INFO')
    chip.add('source', 'x7408.v')
    chip.add('source', 'oh/padring/hdl/oh_padring.v')
    chip.add('source', 'oh/padring/hdl/oh_pads_domain.v')
    chip.add('source', 'oh/padring/hdl/oh_pads_corner.v')
    chip.add('source', 'asic/sky130/io/asic_iobuf.v')
    chip.add('source', 'asic/sky130/io/asic_iovdd.v')
    chip.add('source', 'asic/sky130/io/asic_iovddio.v')
    chip.add('source', 'asic/sky130/io/asic_iovss.v')
    chip.add('source', 'asic/sky130/io/asic_iovssio.v')
    chip.add('source', 'asic/sky130/io/asic_iocorner.v')
    chip.add('source', 'asic/sky130/io/asic_iopoc.v')
    chip.add('source', 'asic/sky130/io/asic_iocut.v')
    chip.add('source', 'asic/sky130/io/sky130_io.blackbox.v')
    chip.add('constraint', "x7408.sdc")
    chip.set('relax', True)
    #chip.set('quiet', True)
    #chip.set('asic', 'diearea', [(0,0), (40,40)])
    #chip.set('asic', 'corearea', [(5,5), (35,35)])
    chip.target('asicflow_skywater130')
    chip.set('eda', 'openroad', 'place', '0', 'option', 'place_density', ['0.15'])

    # Set up sky130 I/O libs.
    libname = 'io'
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')
    chip.add('library', libname, 'nldm', 'typical', 'lib', 'asic/sky130/io/sky130_dummy_io.lib')
    chip.set('library', libname, 'lef', 'asic/sky130/io/sky130_ef_io.lef')
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_ef_io.gds')
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_fd_io.gds')
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_ef_io__gpiov2_pad_wrapped.gds')
    chip.set('library', libname, 'site', [])
    chip.set('exclude', ['io'])

    chip.set('asic', 'def', 'asic_core.def')
    generate_core_floorplan(chip)

    chip.run()
    chip.summary()

############################
def build_top():
    '''
    Helper method to build the top-level chip, integrating the core design
    with an auto-generated padring.
    '''

    # TODO
    pass

############################
def main():
    '''
    Main build method: parse cmdline args and build the design as requested.
    '''

    parser = argparse.ArgumentParser(description='Build a 4x 2-input AND gate chip.')
    parser.add_argument('--fpga', action='store_true', default=False, help='Build for ice40 FPGA (build ASIC by default)')
    options = parser.parse_args()

    if options.fpga:
        build_fpga()
    else:
        build_core()
        build_top()

############################
if __name__ == '__main__':
    main()
