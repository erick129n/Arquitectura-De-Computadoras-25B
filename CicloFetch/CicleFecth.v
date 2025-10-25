module fetch(
    input clk,
    input reset,
    input [31:0] pc_in
);

wire [31:0] instruction;
wire [31:0] DatoA, DatoB;
wire [31:0] Res, Dato_next1, Dato_next2, Res_next;
wire [31:0] pc_out; 
PC pc_unit (
    .clk(clk),
    .reset(reset),
    .pc_in(pc_in),
    .pc_out(pc_out)
);

memoryInstructions mem_inst (
    .address(pc_out),
    .instruction(instruction)
);


buffer buffer_memInstruc_reg(
    .clk(clk),
    .data_in(instruction),
    .data_in2(32'b0), 
    .data_out(), 
    .data_out2() 
);


Registros reg_unit(
    .ARead1(instruction[20:16]),
    .ARead2(instruction[25:21]),
    .AWR(instruction[15:11]),
    .DataIn(Res_next),
    .WE(1),
    .DRead1(DatoA),
    .DRead2(DatoB) 
);

buffer buffer_reg_alu(
    .clk(clk),
    .data_in(DatoA),
    .data_in2(DatoB),
    .data_out(Dato_next1),
    .data_out2(Dato_next2)
);

ALU alu_unit (
    .a(Dato_next1),
    .b(Dato_next2), 
    .operador(instruction[5:0]), 
    .resultado(Res)
);

buffer buffer_alu_reg(
    .clk(clk),
    .data_in(Res),
    .data_in2(32'b0), 
    .data_out(Res_next), 
    .data_out2() 
);

endmodule
