`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    10:45:17 10/04/2025 
// Design Name: 
// Module Name:    Banco 
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
module Banco(
    input [31:0] instruccion
    );


wire [31:0] DatoA;
wire [31:0] DatoB;
wire [31:0] Res;


Registros instReg (
    .ARead1(instruccion[25:21]), 
    .ARead2(instruccion[20:16]), 
    .AWR(instruccion[15:11]), 
    .DataIn(Res), 
    .WE(1), 
    .DRead1(DatoA), 
    .DRead2(DatoB)
    );



ALU instance_alu (
    .a(DatoA), 
    .b(DatoB), 
    .operador(instruccion[5:0]), 
    .resultado(Res)
    );


	
endmodule
