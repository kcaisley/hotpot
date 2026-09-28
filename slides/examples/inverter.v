// inverter.v
module INV_X1 (
  input  wire A,
  output wire ZN
);
  assign ZN = ~A;
endmodule
