// nand.v
module NAND2_X1 (
  input  wire A1,
  input  wire A2,
  output wire ZN
);
  assign ZN = ~(A1 & A2);
endmodule
