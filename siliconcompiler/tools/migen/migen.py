import os
import siliconcompiler

#####################################################################
# Make Docs
#####################################################################

def make_docs():
    '''
    The Migen FHDL library replaces the event-driven paradigm with the notions
    of combinatorial and synchronous statements, has arithmetic rules that make
    integers always behave like mathematical integers, and most importantly
    allows a design's logic to be constructed by a Python program.

    Documentation: https://m-labs.hk/migen/manual/

    Sources: https://github.com/m-labs/migen

    Installation: ``pip install migen``

    '''

    chip = siliconcompiler.Chip()
    chip.set('arg','step','import')
    chip.set('arg','index','<index>')
    setup_tool(chip)
    return chip

################################
# Setup Tool (pre executable)
################################

def setup_tool(chip):
    ''' Per tool function that returns a dynamic options string based on
    the dictionary settings.
    '''

    # Standard Setup
    tool = 'migen'
    clobber = False

    refdir = os.path.join('tools', tool)

    step = chip.get('arg','step')
    index = chip.get('arg','index')

    chip.set('eda', tool, step, index, 'threads', '4', clobber=clobber)
    chip.set('eda', tool, step, index, 'copy', False, clobber=clobber)
    chip.set('eda', tool, step, index, 'exe', 'python', clobber=clobber)
    chip.set('eda', tool, step, index, 'script', 'tools/migen/scdriver.py', clobber=clobber)
    chip.set('eda', tool, step, index, 'refdir', refdir, clobber=clobber)
    chip.set('eda', tool, step, index, 'format', 'json')
    chip.set('eda', tool, step, index, 'vswitch', '-m pip show migen', clobber=clobber)
    chip.set('eda', tool, step, index, 'version', '0.9.2', clobber=clobber)

################################
#  Custom runtime options
################################

def runtime_options(chip):
    ''' Custom runtime options, returns list of command line options.
    '''

    return []

################################
# Version Check
################################

def parse_version(stdout):
    ''' Output:
    Name: migen
    Version: 0.9.2
    Summary: Python toolbox for building complex digital hardware
    ...
    '''
    prefix = 'Version:'
    for line in stdout.split('\n'):
        if line.startswith(prefix):
            version = line[len(prefix):]
            return version.strip()

    return ''

################################
# Post_process (post executable)
################################

def post_process(chip):
    ''' Tool specific function to run after step execution
    '''

    return 0
