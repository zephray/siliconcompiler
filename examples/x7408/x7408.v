// Minimal example for siliconcompiler: a quad 2-input AND gate,
// designed to be similar to (but a bit simpler than) a 74x08 chip.
module and_2in
(
  input wire A1,
  input wire B1,
  output wire Y1
);
  // Use an 'and' primitive to link the inputs and outputs.
  and (Y1, A1, B1);
endmodule

module x7408
(
  input wire A1,
  input wire B1,
  input wire A2,
  input wire B2,
  input wire A3,
  input wire B3,
  input wire A4,
  input wire B4,
  output wire Y1,
  output wire Y2,
  output wire Y3,
  output wire Y4,
  inout _vss,
  inout _vdd
);
  // Instantiate 4 AND2 gates with the top module's signals.
  and_2in and1(A1, B1, Y1);
  and_2in and2(A2, B2, Y2);
  and_2in and3(A3, B3, Y3);
  and_2in and4(A4, B4, Y4);
endmodule
