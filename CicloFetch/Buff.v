module buffer(
    input clk,
    input [31:0] data_in,
    input [31:0] data_in2,
    output reg [31:0] data_out,
    output reg [31:0] data_out2
);

always @(posedge clk) begin
    data_out <= data_in;
    data_out2 <= data_in2;
end

endmodule
