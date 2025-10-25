module Control
	#(parameter SIZE_INS = 6,
	  parameter SIZE_ALU_OP = 2)
	(
	input [SIZE_INS-1:0] instruccion,
	output reg RegDest,
	output reg Branch,
	output reg MemRead,
	output reg MemtoReg,
	output reg [SIZE_ALU_OP-1:0] ALUOp,
	output reg MemWrite,
	output reg ALUSrc,
	output reg RegWrite
	);
	
always@(instruccion) begin
	case(instruccion)
		6'b000000:
		begin
			RegDest = 1'b1;
			ALUSrc = 1'b0;
			MemtoReg = 1'b0;
			RegWrite = 1'b1;
			MemRead = 1'b0;
			MemWrite = 1'b0;
			Branch = 1'b0;
			ALUOp = 2'b10;
		end
		6'b100011:
		begin	
			RegDest = 1'b0;
			ALUSrc = 1'b1;
			MemtoReg = 1'b1;
			RegWrite = 1'b1;
			MemRead = 1'b1;
			MemWrite = 1'b0;
			Branch = 1'b0;
			ALUOp = 2'b00;
		end
		6'b101011:
		begin
			RegDest = 1'bX;
			ALUSrc = 1'b1;
			MemtoReg = 1'bX;
			RegWrite = 1'b0;
			MemRead = 1'b0;
			MemWrite = 1'b1;
			Branch = 1'b0;
			ALUOp = 2'b00;
		end
		6'b000100:
		begin
			RegDest = 1'bX;
			ALUSrc = 1'b0;
			MemtoReg = 1'bX;
			RegWrite = 1'b0;
			MemRead = 1'b0;
			MemWrite = 1'b0;
			Branch = 1'b1;
			ALUOp = 2'b01;
		end
	endcase
end

endmodule
