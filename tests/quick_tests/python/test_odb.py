from siliconcompiler import odb

import os

def test_readlef():
    db = odb.dbDatabase.create()
    testdir = os.path.dirname(os.path.abspath(__file__))
    lef = odb.read_lef(db, f'{testdir}/test_odb/test.lef') 
    macro = lef.getMasters()[0]
    assert macro.getName() == 'test'
    assert macro.getWidth() == 5000
    assert macro.getHeight() == 5000
