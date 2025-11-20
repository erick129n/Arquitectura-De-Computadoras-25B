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
	//INSTRUCCIONES DE TIPO R
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
	//INSTRUCCION DE CARGA PALABRA
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
	//INSTRUCCION DE STORE WORD
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
	//INSTRUCCION BQE (BRANCH TO EQUAL)
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
	//INSTRUCCION DE TIPO I (SUMA)
		6'b001000:
		begin
			RegDest = 1'b0;
			ALUSrc = 1'b1;
			MemtoReg = 1'b0;
			RegWrite = 1'b1;
			MemRead = 1'b0;
			MemWrite = 1'b0;
			Branch = 1'b0;
			ALUOp = 2'b00;
		end
	//INSTRUCCION J
		6'b000010:
		begin
			RegDest = 1'bX;
			ALUSrc = 1'bX;
			MemtoReg = 1'bX;
			RegWrite = 1'bx;
			MemRead = 1'bx;
			MemWrite = 1'bx;
			Branch = 1'bx;
			ALUOp = 2'b00;
		end
		default:
		begin
			RegDest = 1'b0;
			ALUSrc = 1'b0;
			MemtoReg = 1'b0;
			RegWrite = 1'b0;
			MemRead = 1'b0;
			MemWrite = 1'b0;
			Branch = 1'b0;
			ALUOp = 2'b10;
		end
	endcase
end

endmodule
