// design.v
module design (
  input  wire in1,
  input  wire in2,
  output wire out
);
  wire wire1;

  NAND2_X1 inst1 (
    .A1(in1), .A2(in2), .ZN(wire1)
  );
  INV_X1 inst2 (
    .A(wire1), .ZN(out)
  );
endmodule
