`timescale 1ns / 1ps

module testbench_puertas;
    reg i_bit1, i_bit2;
    wire o_and, o_nand, o_or, o_nor, o_not, o_xor, o_xnor;
    
    puertas dut (
        .i_bit1(i_bit1),
        .i_bit2(i_bit2),
        .o_and(o_and),
        .o_nand(o_nand),
        .o_or(o_or),
        .o_nor(o_nor),
        .o_not(o_not),
        .o_xor(o_xor),
        .o_xnor(o_xnor)
    );
    
    initial begin
        // Caso 1: 00
        i_bit1 = 0; i_bit2 = 0; #10;
        
        // Caso 2: 01
        i_bit1 = 0; i_bit2 = 1; #10;
        
        // Caso 3: 10
        i_bit1 = 1; i_bit2 = 0; #10;
        
        // Caso 4: 11
        i_bit1 = 1; i_bit2 = 1; #10;
        
        $finish;
    end
    
endmodule