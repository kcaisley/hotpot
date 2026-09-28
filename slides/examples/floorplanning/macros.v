module macro_demo(input clk, input reset, input ce, input we,
                  input [5:0] addr, input [31:0] data,
                  output [31:0] q, output [15:0] result,
                  output ready, output valid);
  wire [31:0] between;
  fakeram45_64x32 ram0 (.clk(clk), .ce_in(ce), .we_in(we),
    .addr_in(addr), .wd_in(data), .w_mask_in(32'hffffffff), .rd_out(between));
  fakeram45_64x32 ram1 (.clk(clk), .ce_in(ce), .we_in(we),
    .addr_in(addr), .wd_in(between), .w_mask_in(32'hffffffff), .rd_out(q));
  gcd logic0 (.clk(clk), .reset(reset), .req_msg(data), .req_val(ce),
    .req_rdy(ready), .resp_msg(result), .resp_val(valid), .resp_rdy(ce));
endmodule
