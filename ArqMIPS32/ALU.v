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


module ALU #(
	parameter SIZEDATA = 32, OP=4)
	(
    input [SIZEDATA-1 :0] a,
    input [SIZEDATA-1 :0] b,
    input [OP-1 :0] operador,
	output zero,
    output reg[SIZEDATA-1 :0] resultado
    );

	always@* begin
	
		case(operador)
			4'b0000:
				begin
					resultado = a & b;
				end
			4'b0001:
				begin
					resultado = a | b;
				end
			4'b0010:
				begin
					resultado = a + b;
				end
			4'b0110:
				begin
					resultado = a - b;
				end
			4'b0111:
				begin
					resultado = a < b ? 1 : 0;
				end
			4'b1100:
				begin
					resultado = ~a || ~b;
				end
			endcase
	end
	
	assign zero = resultado ? 1 : 0;

endmodule
