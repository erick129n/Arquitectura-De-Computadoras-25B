module desplazar
	#(parameter SIZE=32, 
	  parameter SIZE_OUT = 32)
	(
	input [SIZE-1:0] dato,
	output [SIZE_OUT-1:0] datoOut
	);
	
	
	assign datoOut = dato >> 2;
	
endmodule
