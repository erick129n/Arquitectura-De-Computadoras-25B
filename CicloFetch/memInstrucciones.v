module memoryInstructions(
    input [31:0] address,
    output reg [31:0] instruction
);


reg [31:0] memory [0:255];

initial begin
    $readmemb("Instrucciones.txt", memory);
end

always @(*) begin
    instruction = memory[address];
end
endmodule