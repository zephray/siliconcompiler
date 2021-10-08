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

// Top-level module for core logic.
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
  inout _vss0,
  inout _vdd0,
  inout _vss1,
  inout _vdd1
);
  // Power pad connections.
  wire _vdd;
  wire _vss;
  assign _vss0 = _vss;
  assign _vss1 = _vss;
  assign _vdd0 = _vdd;
  assign _vdd1 = _vdd;
  // Instantiate 4 AND2 gates with the top module's signals.
  and_2in and1(A1, B1, Y1);
  and_2in and2(A2, B2, Y2);
  and_2in and3(A3, B3, Y3);
  and_2in and4(A4, B4, Y4);
endmodule

// Top-level module including padring.
module x7408_top
(
  inout _vdd,
  inout _vss,
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
  output wire Y4
);
  // GPIO standard cell signals.
  wire [2:0] n_pad;
  wire [2:0] n_din;
  wire [2:0] n_dout;
  wire [23:0] n_cfg;
  wire [2:0] n_ie;
  wire [2:0] n_oen;
  wire [47:0] n_tech_cfg;
  wire [2:0] e_pad;
  wire [2:0] e_din;
  wire [2:0] e_dout;
  wire [23:0] e_cfg;
  wire [2:0] e_ie;
  wire [2:0] e_oen;
  wire [47:0] e_tech_cfg;
  wire [2:0] s_pad;
  wire [2:0] s_din;
  wire [2:0] s_dout;
  wire [23:0] s_cfg;
  wire [2:0] s_ie;
  wire [2:0] s_oen;
  wire [47:0] s_tech_cfg;
  wire [2:0] w_pad;
  wire [2:0] w_din;
  wire [2:0] w_dout;
  wire [23:0] w_cfg;
  wire [2:0] w_ie;
  wire [2:0] w_oen;
  wire [47:0] w_tech_cfg;

  // Core signal wiring. A/B signals are inputs, Ys are outputs.
  assign n_cfg = 24'b0;
  assign e_cfg = 24'b0;
  assign s_cfg = 24'b0;
  assign w_cfg = 24'b0;
  // A1: NE, B1: N, Y1: NW. (_vss0: NWW)
  assign Y1 = n_pad[0];
  assign n_pad[1] = B1;
  assign n_pad[2] = A1;
  // A2: EN, B2: E, Y2: ES. (_vdd1: ESS)
  assign Y2 = e_pad[0];
  assign e_pad[1] = B2;
  assign e_pad[2] = A2;
  // A3: SW, B3: S, Y3: SE. (_vss1: SEE)
  assign s_pad[0] = A3;
  assign s_pad[1] = B3;
  assign Y3 = s_pad[2];
  // A4: WS, B4: W, Y4: WN. (_vdd0: WNN)
  assign w_pad[0] = A4;
  assign w_pad[1] = B4;
  assign Y4 = w_pad[2];

  // Core module.
  x7408 core (
    A1, B1, A2, B2,
    A3, B3, A4, B4,
    Y1, Y2, Y3, Y4,
    _vss, _vdd, _vss, _vdd
  );

  // Main padring.
  oh_padring #(
    .TYPE("SOFT"),
    .NO_DOMAINS(1),
    .NO_GPIO(3),
    .NO_VDDIO(0),
    .NO_VSSIO(0),
    .NO_VDD(0),
    .NO_VSS(1),
    .SO_DOMAINS(1),
    .SO_GPIO(3),
    .SO_VDDIO(0),
    .SO_VSSIO(0),
    .SO_VDD(0),
    .SO_VSS(1),
    .EA_DOMAINS(1),
    .EA_GPIO(3),
    .EA_VDDIO(0),
    .EA_VSSIO(0),
    .EA_VDD(1),
    .EA_VSS(0),
    .WE_DOMAINS(1),
    .WE_GPIO(3),
    .WE_VDDIO(0),
    .WE_VSSIO(0),
    .WE_VDD(1),
    .WE_VSS(0),
  ) padring (
    .vdd(_vdd),
    .vss(_vss),
    .no_vddio(_vdd),
    .no_vssio(_vss),
    .no_pad(n_pad),
    .no_din(n_din),
    .no_dout(n_dout),
    .no_cfg(n_cfg),
    .no_ie(n_ie),
    .no_oen(n_oen),
    .no_tech_cfg(n_tech_cfg),
    .so_vddio(_vdd),
    .so_vssio(_vss),
    .so_pad(s_pad),
    .so_din(s_din),
    .so_dout(s_dout),
    .so_cfg(s_cfg),
    .so_ie(s_ie),
    .so_oen(s_oen),
    .so_tech_cfg(s_tech_cfg),
    .we_vddio(_vdd),
    .we_vssio(_vss),
    .we_pad(w_pad),
    .we_din(w_din),
    .we_dout(w_dout),
    .we_cfg(w_cfg),
    .we_ie(w_ie),
    .we_oen(w_oen),
    .we_tech_cfg(w_tech_cfg),
    .ea_vddio(_vdd),
    .ea_vssio(_vss),
    .ea_pad(e_pad),
    .ea_din(e_din),
    .ea_dout(e_dout),
    .ea_cfg(e_cfg),
    .ea_ie(e_ie),
    .ea_oen(e_oen),
    .ea_tech_cfg(e_tech_cfg)
  );

  // Padring corners.
  oh_pads_corner corner_sw (
    .vdd(_vdd),
    .vss(_vss),
    .vddio(_vdd),
    .vssio(_vss)
  );
  oh_pads_corner corner_nw (
    .vdd(_vdd),
    .vss(_vss),
    .vddio(_vdd),
    .vssio(_vss)
  );
  oh_pads_corner corner_se (
    .vdd(_vdd),
    .vss(_vss),
    .vddio(_vdd),
    .vssio(_vss)
  );
  oh_pads_corner corner_ne (
    .vdd(_vdd),
    .vss(_vss),
    .vddio(_vdd),
    .vssio(_vss)
  );
endmodule
