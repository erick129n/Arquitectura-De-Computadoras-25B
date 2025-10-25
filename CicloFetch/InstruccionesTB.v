`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   10:55:18 10/04/2025
// Design Name:   Banco
// Module Name:   D:/Users/Lenovo/Documents/Codigo/designCompPCW10/Nueva carpeta/Instrucciones/InstruccionesTB.v
// Project Name:  Instrucciones
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: Banco
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module InstruccionesTB;

	// Inputs
	reg [31:0] instruccion;

	// Instantiate the Unit Under Test (UUT)
	Banco uut (
		.instruccion(instruccion)
	);

	initial begin
	#100;
		// Initialize Inputs
		instruccion = 32'b00000_00000_00001_00101; //modificar para 32

		// Wait 100 ns for global reset to finish
		#100;
        
		instruccion = 32'b00000_00100_00010_00110; //modificar para 32
		// Add stimulus here
		#100;
		
		instruccion = 32'b00100_00110_00011_00111; //modificar para 32
		
		#100;

	end
      
endmodule

