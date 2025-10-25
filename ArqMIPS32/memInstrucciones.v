module memoryInstructions
	#(parameter SIZE = 32, S_MEM = 256, DIR_MEM = 8)
	(
    input [DIR_MEM-1:0] address,
    output reg [SIZE-1:0] instruction
);


reg [DIR_MEM-1:0] memory [0:S_MEM-1];

initial begin
    $readmemb("Instrucciones.txt", memory);
end

always @(*) begin
    instruction = {memory[address], memory[address+1], memory[address+2], memory[address+3]};
end
endmodule