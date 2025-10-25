module BR(
      input [19:0] bus
);
//wire [4:0] Aw = bus[4:0];  
//wire [4:0] AR1 = bus[9:5];   
//wire [4:0] AR2  = bus[14:10]; 
//wire [4:0] op  = bus[19:15]; 
wire [31:0] res;
wire [31:0] DR1;
wire [31:0] DR2;
wire WReg = 1'b1;
wire over;
reg_bank inst_reg(
    .AR1(bus[9:5]),
    .AR2(bus[14:10]),
    .Awrite(bus[4:0]),
    .DataIn(res), 
    .WReg(WReg), 
    .DR1(DR1), 
    .DR2(DR2));

alu inst_alu(
    .a(DR1),
    .b(DR2),
    .sel(bus[19:15]),
    .s(res),
    .overflow(over)
    );


endmodule