module memoryInstructions
	#(parameter WORD = 32, S_MEM = 8, DIR_MEM = 1024)
	(
    input [S_MEM-1:0] address,
    output [WORD-1:0] instruction
);


reg [S_MEM-1:0] memory [0:DIR_MEM-1];

initial begin
    $readmemb("Instrucciones.txt", memory);
end

  assign instruction = address;
endmodule