//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:30:01 10/04/2025 
// Design Name: 
// Module Name:    Registros 
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
module Registros
	#(parameter S_AD = 5, S_DATA = 32, DIRECCIONES=256)
	(
    input [S_AD-1:0] ARead1,
    input [S_AD-1:0] ARead2,
    input [S_AD-1:0] AWR,
    input [S_DATA-1:0] DataIn,
    input WE,
    output [S_DATA-1:0] DRead1,
    output [S_DATA-1:0] DRead2
    );


	reg[S_DATA-1:0] Registro [0:DIRECCIONES-1];
	
	initial begin
		$readmemb("Datos.txt", Registro);
	end


	assign DRead1 = Registro[ARead1];
	assign DRead2 = Registro[ARead2];
	
	always@(*) begin
		if(WE)begin
			Registro[AWR] = DataIn;
		end
	end
endmodule
