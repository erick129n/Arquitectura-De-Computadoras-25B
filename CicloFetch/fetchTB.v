`timescale 1ns / 1ns
module fetchTB(

);

reg clk;
reg reset;
reg [31:0] pc_in;

fetch fetch_unit (
    .clk(clk),
    .reset(reset),
    .pc_in(pc_in)
);
initial begin
    clk = 0;
    forever #2 clk = ~clk; // Cambia el estado cada 2 unidades de tiempo
end
initial begin
    // Initialize signals
    reset = 1;
    pc_in = 32'b0;

    // Release reset after some time
    #50;
    reset = 0;

    // Test different PC values
    #100; pc_in = 32'd0;
    #100; pc_in = 32'd1;
    #100; pc_in = 32'd3;
    #100; pc_in = 32'd2;

    // Finish simulation after some time
    #100;
    $stop;
end
endmodule