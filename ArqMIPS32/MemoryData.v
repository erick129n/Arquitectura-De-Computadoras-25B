module memoriaDatos #(
    parameter SIZE = 32,
    parameter SIZE_MEM = 32'h7FF,
    parameter SIZE_WORD_MEM = 8
)(
    input [SIZE-1:0] address,
    input [SIZE-1:0] dato,
    input MemWrite,
    input MemRead,
    output reg [SIZE-1:0] datoLeido
);

    reg [SIZE_WORD_MEM-1:0] memory [SIZE_MEM-1:0];
    
    // ESCRIBIR - Sensible a TODAS las señales relevantes
    always @(*) begin
        if (MemWrite === 1'b1 && address < (SIZE_MEM - 3)) begin
            memory[address+3]   <= dato[31:24];
            memory[address+2] <= dato[23:16];
            memory[address+1] <= dato[15:8];
            memory[address] <= dato[7:0];
        end
    end
    
    // LEER - Sensible a TODAS las señales relevantes  
    always @(*) begin
        if (MemRead === 1'b1 && address < (SIZE_MEM - 3)) begin
            datoLeido = {memory[address+3], memory[address+2],
                        memory[address+1], memory[address]};
        end else begin
            datoLeido = 32'h00000000;
        end
    end

endmodule