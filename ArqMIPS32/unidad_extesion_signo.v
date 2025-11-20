module signed_extention #(
		parameter SIZE_WORD = 32,
		parameter SIZE_HALF_WORD = 16
)(
	input [SIZE_HALF_WORD-1:0] half_word,
	output [SIZE_WORD-1:0] word

);
wire dato_signo = half_word[SIZE_HALF_WORD-1];
wire [SIZE_HALF_WORD-1:0]temp;

assign temp = {16{dato_signo}};

assign word = {{16{temp}}, half_word};

endmodule