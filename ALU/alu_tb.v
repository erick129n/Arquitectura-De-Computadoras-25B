`timescale 1ns/1ns
module aluTB(

);


reg [31:0] A;
reg [31:0] B;
reg [4:0]selTb;

wire [31:0] out;
wire over;

alu DUT(.a(A), .b(B), .sel(selTb), .s(out), .overflow(over));


initial begin
A = 32'd4;
B = 32'd6; 
selTb = 5'd0; //suma a con b
#100;
    selTb = 5'd1; //operacion a and b
#100;
selTb = 5'd2; // a igual b
#100;
selTb = 5'd3; // a mayor que b
#100;
selTb = 5'd4; // a corrido a la izquierda
#100;
selTb = 5'd5; // a corrido a la derecha
#100;
selTb = 5'd6; // a por b
#100;

$stop;
end
endmodule