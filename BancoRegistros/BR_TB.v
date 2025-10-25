`timescale 1ns/1ns
module BR_TB(

);

reg[19:0] control_bus;

BR DUT(
    .bus(control_bus));


// ---------------------------
// | OP  |  AR2  | AR1 | Aw  |
// ---------------------------
// |19-15| 14-10 | 9-5 | 4-0 |
// ---------------------------

initial
begin
    #100;
    control_bus = 20'b00001_00000_00000_11111;
    #100;
    // SUMA: 5 + 6 = 11 → guardar en registro 7
    control_bus = 20'b00001_00000_00001_00111;
    #100;
    
    // SUMA: 6 + 10 = 16 → guardar en registro 4
    control_bus = 20'b00001_00100_00010_00001;
    #100;
    
    // AND: 10 AND 11 = 10 → guardar en registro 2
    control_bus = 20'b00010_00010_00011_00010;
    #100;
    
    // COMPARACION: 12 > 11 = 1 → guardar en registro 1
    control_bus = 20'b00100_00001_00011_00100;
    #100;
    
    $stop;
end

endmodule