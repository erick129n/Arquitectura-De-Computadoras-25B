module NucleoTop#(parameter SIZE_DATA = 32,
				  parameter ADD_INST_SIZE = 32,
				  parameter ADD_SIZE = 32,
				  parameter VALOR_SUMADO = 4,
				  parameter SIZE_OP = 6,
				  parameter SIZE_ADDR_BR = 5,
				  parameter SIZE_FUNC = 6,
				  parameter SIZE_HALF_INST = 16,
				  parameter SIZE_ALU_OP=2,
				  parameter S_OP_ALU = 4,
				  parameter S_WB =2,
				  parameter S_M = 3)
	(
		input clk,
		input [ADD_INST_SIZE-1:0 ]pc_in,
		input reset_pc
	);
	
	wire [ADD_INST_SIZE-1 : 0] addr_instruccion_in, addr_instruccion_out, addr_instruccion_to_mux;
	wire [SIZE_DATA-1: 0] instruccion_a_buff, out_instruccion;
	wire [ADD_INST_SIZE-1 :0] ID_addr_instruccion_to_EX;

	// ELIMINAR ESTA LÍNEA: assign addr_instruccion_in = pc_in;
	//assign addr_instruccion_to_mux = addr_instruccion_in;

	PC #(.S_DATA(ADD_INST_SIZE)) PC(
	  .clk(clk),
	  .reset(reset_pc), 
	  .pc_in(addr_instruccion_to_mux), 
	  .pc_out(addr_instruccion_out)
	);
	sumador#(.SIZE(ADD_INST_SIZE)) sumador(
		.A(addr_instruccion_out),
		.B(32'd4),
		.res(addr_instruccion_in)  // ← Esta es la única fuente
	);

	// En el MUX del branch, usa addr_instruccion_in directamente

	
	memoryInstructions memoryInstructions(
		.address(addr_instruccion_out),
		.instruction(instruccion_a_buff)
	);
	
	IF_ID IF_ID(
		.clk(clk),
		.data_in(instruccion_a_buff),
		.data_in2(addr_instruccion_in), //direccion de la instruccion para hacer banch
		.data_out(out_instruccion),
		.data_out2(ID_addr_instruccion_to_EX)
	);
	
	wire [SIZE_OP-1: 0] OP = out_instruccion[31:26];
	wire RegDest;
	wire RegWrite, writeEn;
	wire [SIZE_ALU_OP-1:0]ALUOp;
	wire ALUSrc;
	wire branch;
	wire MemRead;
	wire MemWrite;
	wire Mem_to_Reg;
	Control Control(
		.instruccion(OP),
		.RegDest(RegDest),
		.Branch(branch),
		.MemRead(MemRead),
		.MemtoReg(Mem_to_Reg),
		.ALUOp(ALUOp),
		.MemWrite(MemWrite),
		.ALUSrc(ALUSrc),
		.RegWrite(RegWrite)
	);
	
	wire [SIZE_ADDR_BR-1:0] AR1 = out_instruccion[25:21];
	wire [SIZE_ADDR_BR-1:0] AR2 = out_instruccion[20:16];
	wire [SIZE_ADDR_BR-1:0] AW = out_instruccion[15:11];
	wire [SIZE_OP-1:0] SH = out_instruccion[10:6];
	wire [SIZE_FUNC-1:0] inst_funcion = out_instruccion[5:0];
	wire [SIZE_ADDR_BR-1:0] destinoBr;
	wire [SIZE_HALF_INST-1:0] inst_inmediata = out_instruccion[15:0];
	wire [SIZE_FUNC-1:0] inst_funcion_ex;
	
	wire [SIZE_DATA-1:0] DRead1;
	wire [SIZE_DATA-1:0] DRead2;
	
	wire [SIZE_ADDR_BR-1:0] AWR;
	wire [SIZE_DATA-1:0] Data_Reg;
	Registros BR(
		.ARead1(AR1),
		.ARead2(AR2),
		.AWR(AWR),
		.DataIn(Data_Reg),
		.WE(writeEn),
		.DRead1(DRead1),
		.DRead2(DRead2)
	);
	
	
	wire [SIZE_DATA-1:0] A;
	wire [SIZE_DATA-1:0] B;
	wire [SIZE_ADDR_BR-1:0] AdrrDest1;
	wire [SIZE_ADDR_BR-1:0] AdrrDest2;
	wire [ADD_INST_SIZE-1:0] EX_addr_instr_branch; //instruccion que sera operada con el sumador
	wire alusrc_out, sel_regDes;
	wire [SIZE_ALU_OP-1:0] opeAlu;
	wire [S_WB-1:0] wb_ex_mem;
	wire [S_M-1:0] m_ex_mem;
	wire [ADD_SIZE-1:0] offset_to_desp;
	wire [SIZE_DATA-1:0] dato_extendido;
	
	signed_extention extension(
		.half_word(inst_inmediata),
		.word(dato_extendido)
	);
	
	

	ID_EX ID_EX(
		.WB({RegWrite, Mem_to_Reg}),
		.M({branch, MemRead, MemWrite}),
		.EX({ALUSrc, ALUOp, RegDest}),
		.clk(clk),
		.data_in(DRead1),
		.data_in2(DRead2),
		.data_in3(ID_addr_instruccion_to_EX), //direccion de memoria para hacer branch
		.data_extend_in(dato_extendido),
		.adrWrite1(AR2),
		.adrWrite2(AW),
		.funcion_in(inst_funcion),
		.WB_out(wb_ex_mem),
		.M_out(m_ex_mem),
		.EX_out({alusrc_out, opeAlu, sel_regDes}),
		.data_out(A),
		.data_out2(B),
		.data_out3(EX_addr_instr_branch),
		.data_out_jm(offset_to_desp),
		.funcion(inst_funcion_ex),
		.AWrite1(AdrrDest1),
		.AWrite2(AdrrDest2)
	);
	wire [ADD_INST_SIZE-1:0] instruccion_branch_to_ex_mem;
	wire [ADD_INST_SIZE-1:0] offset_to_adder;
	desplazar desplazador(
		.dato(offset_to_desp),
		.datoOut(offset_to_adder)
	);
	
	sumador#(.SIZE(ADD_INST_SIZE)) sumador_despl(
		.A(EX_addr_instr_branch),
		.B(offset_to_adder),
		.res(instruccion_branch_to_ex_mem)
	);
	
	wire [S_OP_ALU-1:0] selector;
	
	ALUcontrol ALUcontrol(
		.instruccion(inst_funcion_ex),
		.AluOP(opeAlu),
		.outInst(selector)
	);
	
	wire [SIZE_DATA-1:0]operando_B; 
	
	MUX #(.SIZE(SIZE_DATA))mux_in_ALU(
		.dato(offset_to_desp),
		.dato2(B),
		.sel(alusrc_out),
		.datoOut(operando_B)	
	);
	
	wire [SIZE_DATA-1:0] resultadoALU;
	wire flag_zero_to_alu, flag_zero_to_branch;
	ALU ALU(
		.a(A),
		.b(operando_B),
		.operador(selector),
		.zero(flag_zero_to_alu),
		.resultado(resultadoALU)
	);
	
	wire [SIZE_ADDR_BR-1:0] ex_mem_addrDest;
	
	MUX #(.SIZE(5))mux_regDest(
		.dato(AdrrDest2),
		.dato2(AdrrDest1),
		.sel(sel_regDes),
		.datoOut(ex_mem_addrDest)
	);

	wire ex_mem_branch;
	wire [S_WB-1:0] WB_mem_wb;
	wire memoryWrite;
	wire memoryRead;
	wire [SIZE_DATA-1:0]addr_to_memory;
	wire [SIZE_DATA-1:0] dato_escribir;
	wire [SIZE_ADDR_BR-1:0] addr_reg_mem_wb;
	wire [ADD_INST_SIZE-1:0] add_instruccion_to_mux;
	EX_MEM EX_MEM(
		.clk(clk),
		.WB(wb_ex_mem),
		.M(m_ex_mem),
		.zero_in(flag_zero_to_alu),
		.data_in(instruccion_branch_to_ex_mem),
		.data_in2(resultadoALU),
		.AWriteMem_in(B),
		.AWriteReg_in(ex_mem_addrDest),
		.WB_out(WB_mem_wb),
		.M_out({ex_mem_branch, memoryRead, memoryWrite}), //Antes: ex_mem_branch, memoryWrite, memoryRead
		.zero_out(flag_zero_to_branch),
		.data_out(add_instruccion_to_mux),
		.data_out2(addr_to_memory),
		.AWriteMem(dato_escribir),
		.AWriteReg(addr_reg_mem_wb)
	);
	wire [SIZE_DATA-1:0] datoLeido;
	
	wire branchToPC;
	assign branchToPC = 0;
	AND AND(
		.A(ex_mem_branch),
		.B(flag_zero_to_branch),
		.res(branchToPC)
	);
	
	MUX #(.SIZE(32))mux_branch(
		.dato(add_instruccion_to_mux),                    // ← Para el branch no implementado
		.dato2(addr_instruccion_in),     // ← Del sumador (PC+4)
		.sel(branchToPC),
		.datoOut(addr_instruccion_to_mux)
	);
	
	memoriaDatos memoriaDatos(
		.address(addr_to_memory),
		.dato(dato_escribir),
		.MemWrite(memoryWrite),
		.MemRead(memoryRead),
		.datoLeido(datoLeido)
	);
	
	wire [SIZE_DATA-1:0] Dato_MemToReg;
	wire [SIZE_DATA-1:0] Dato_leido1, Dato_leido2;
	wire MemToReg;
	MEM_WB MEM_WB(
		.clk(clk),
		.WB(WB_mem_wb),
		.DatoLeido(datoLeido),
		.direccion(addr_to_memory),
		.direccionRegistro(addr_reg_mem_wb),
		.WB_out({writeEn, MemToReg}),
		.datoLeido_out(Dato_leido1),
		.direccion_out(Dato_leido2),
		.direccionRegistro_out(AWR)
	);
	
	MUX mux_MemoryToReg(
		.dato(Dato_leido1),
		.dato2(Dato_leido2),
		.sel(MemToReg),
		.datoOut(Data_Reg)
	);
endmodule