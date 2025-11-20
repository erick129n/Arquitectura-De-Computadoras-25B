module memoriaDatos
	#(parameter SIZE = 32, SIZE_MEM = 32'h7FF, SIZE_WORD_MEM = 8)
	(
	input[SIZE-1:0] address,
	input[SIZE-1:0] dato,
	input MemWrite,
	input MemRead,
	output reg[SIZE-1:0] datoLeido
);


reg[SIZE_WORD_MEM-1:0] memory [0:SIZE_MEM-1];

always@(MemWrite, MemRead) begin
	if(MemWrite) begin
		//{memory[address], memory[address+1], memory[address+2], memory[address+3]} = dato;
		memory[address] = dato[31:23];
		memory[address+1] = dato[22:15];
		memory[address+2] = dato[14:7];
		memory[address+3] = dato[7:0];
	end
	if(MemRead) begin
		datoLeido = {memory[address], memory[address+1], memory[address+2], memory[address+3]} ;
	end
end

endmodule
