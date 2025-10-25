`timescale 1ns / 1ps
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
module Registros(
    input [4:0] ARead1,
    input [4:0] ARead2,
    input [4:0] AWR,
    input [31:0] DataIn,
    input WE,
    output [31:0] DRead1,
    output [31:0] DRead2
    );


	reg[31:0] Registro [0:31];
	
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
