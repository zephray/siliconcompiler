from migen import *
from migen.fhdl.verilog import convert

class heartbeat(Module):
  def __init__(self, N=8):
    self.out = Signal()
    self.counter_reg = Signal(N)
    self.ios = [self.out]

    ###

    self.sync += self.counter_reg.eq(self.counter_reg + 1)
    self.sync += self.out.eq(self.counter_reg == Cat(Replicate(0, N-1), 1))
