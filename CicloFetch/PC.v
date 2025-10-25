module PC(
    input clk,
    input reset,
    input [31:0] pc_in,
    output reg [31:0] pc_out
);

always @(posedge clk or posedge reset) begin
    if (reset) begin
        pc_out <= 32'b0;
    end else begin
        pc_out <= pc_in + 4;
    end
end

endmodule