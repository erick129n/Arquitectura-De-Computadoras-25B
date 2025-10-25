module memoriaDatos
	#(parameter SIZE = 32, SIZE_MEM = 256)
	(
	input[SIZE-1:0] address,
	input[SIZE-1:0] dato,
	input MemWrite,
	input MemRead,
	output reg[SIZE-1:0] datoLeido
);


reg[SIZE-1:0] memory [0:SIZE_MEM-1];

always@* begin
	if(MemWrite) begin
		memory[address] = dato;
	end
	if(MemRead) begin
		datoLeido = memory[address];
	end
end

endmodule
