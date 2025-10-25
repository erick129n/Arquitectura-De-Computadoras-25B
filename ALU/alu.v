`timescale 1ns/1ns
module alu (
    input [31:0] a,
    input [31:0] b,
    input [4:0] sel,
    output reg [31:0] s,
    output reg overflow
    

);

always @(sel) begin 
    case (sel)
    5'd1:
        begin
            s = a + b;
        end
    5'd2:
        begin
            s = a & b;
        end
    5'd3:
        begin
            s = a == b?1:0;
        end
    5'd4:
        begin
            s = a > b?1:0;
        end
    5'd5:
        begin
            s = a << 1;
        end
    5'd6:
        begin
            s = a >> 1;
        end
    5'd7:
        begin
            s = a * b;
        end
    endcase
end


endmodule
