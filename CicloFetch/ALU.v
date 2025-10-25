`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:27:02 10/03/2025 
// Design Name: 
// Module Name:    ALU 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module ALU(
    input [31:0] a,
    input [31:0] b,
    input [3:0] operador,
    output reg[31:0] resultado
    );

	always@* begin
	
		case(operador)
			4'd0:
				begin
					resultado = a + b;
				end
			4'd1:
				begin
					resultado = a & b;
				end
			4'd2:
				begin
					resultado = a == b ? 1:0;
				end
			4'd3:
				begin
					resultado = a > b ? 1:0;
				end
			4'd4:
				begin
					resultado = a << 1;
				end
			4'd5:
				begin
					resultado = a >> 1;
				end
			4'd6:
				begin
					resultado = a - b;
				end
			endcase
	end

endmodule
