module memInstru(
	input [7:0] operacion,
	output reg [31:0] instruccion
	);

reg[7:0] Inst [0:31];

always@* begin
	instruccion = Inst[operacion];
end

endmodule