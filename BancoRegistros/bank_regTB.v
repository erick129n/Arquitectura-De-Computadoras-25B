`timescale 1ns/1ns

module bank_regTB();

reg [4:0] ar1;
reg [4:0] ar2;
reg[4:0] aw;
reg [31:0] dIn;
reg writeReg;
wire [31:0]dr1;
wire[31:0]dr2;

reg_bank DUT(.AR1(ar1), .AR2(ar2), .Awrite(aw), .DataIn(dIn), .WReg(writeReg), .DR1(dr1), .DR2(dr2));

initial
begin
    writeReg = 1'b1;
    dIn = 32'd358;
    ar1 = 5'd0;
    ar2 = 5'd1;
    aw = 5'd9;
    #100;
    dIn = 32'd358;
    ar1 = 5'd2;
    ar2 = 5'd4;
    aw = 5'd15;
    #100;
    $stop;
    
end

endmodule