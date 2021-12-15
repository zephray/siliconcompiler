import os
import siliconcompiler
import pytest

@pytest.mark.eda
@pytest.mark.quick
def test_migen(datadir):
    design = 'heartbeat'
    src = os.path.join(datadir, f'{design}.py')
    step = 'import'

    chip = siliconcompiler.Chip(loglevel="INFO")

    chip.add('source', src)
    chip.set('design', design)
    chip.set('mode', 'sim')
    chip.set('arg', 'step', step)
    chip.set('vercheck', True)
    chip.target('migen')

    chip.run()

    assert chip.find_result('v', step=step) is not None
