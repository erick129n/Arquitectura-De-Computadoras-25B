module reg_bank(
    input[4:0] AR1,
    input[4:0] AR2,
    input[4:0] Awrite,
    input[31:0] DataIn,
    input WReg,
    output reg[31:0] DR1,
    output reg[31:0] DR2

);


reg[31:0] Banco [0:31];

initial
begin
    $readmemb("Datos.txt",Banco);
end

always@*
begin
    DR1 = Banco[AR1];
    DR2 = Banco[AR2];

    if(WReg && Awrite != 0) begin  // Evita escribir en registro 0
        Banco[Awrite] = DataIn;
        // Actualizar salidas si estamos leyendo el registro que se escribe
        if(AR1 == Awrite) DR1 = DataIn;
        if(AR2 == Awrite) DR2 = DataIn;
    end
end
/*always@(WReg or Awrite or DataIn) begin
    if(WReg) begin
        Banco[Awrite] = DataIn;
    end
end*/


endmodule