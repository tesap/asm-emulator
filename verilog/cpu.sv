
`include "alu.sv"
`include "pc.sv"
`include "jmp_handle.sv"

module cpu
(
    input clk,
    input reset,

    input [15:0] inM,
    input [15:0] instruction,

    output [15:0] outM,
    output writeM,
    output [15:0] addressM,
    output [15:0] pc
);

    wire opcode 	= instruction[15];
    // wire ... 	= instruction[13];
    // wire ... 	= instruction[14];
    wire alu_a  	= instruction[12];
    wire alu_zx 	= instruction[11];
    wire alu_nx 	= instruction[10];
    wire alu_zy 	= instruction[9];
    wire alu_ny 	= instruction[8];
    wire alu_f  	= instruction[7];
    wire alu_no		= instruction[6];
    wire a_dest 	= instruction[5];
    wire d_dest 	= instruction[4];
    wire m_dest 	= instruction[3];
    wire j1 			= instruction[2];
    wire j2 			= instruction[1];
    wire j3 			= instruction[0];

    wire [15:0] y = (opcode && alu_a) ? inM : a_reg_out;
    wire [15:0] alu_out;
    wire [15:0] a_reg_input = (opcode) ? alu_out : instruction;
    wire [15:0] a_reg_out;
    wire signed [15:0] d_reg_out;
    reg signed [15:0] out_m;
    
    wire a_write = (!opcode) || a_dest;
    wire d_write = opcode && d_dest;
    
    assign writeM = opcode && m_dest;
    assign addressM = a_reg_out;
    assign outM = out_m;
    
    always @(posedge clk) begin
            out_m <= alu_out;
    end
    
    register a_register_inst
    (
            .in 	(a_reg_input),
            .write 	(a_write),
            .clk 	(clk),
            .reset 	(reset),
            .out 	(a_reg_out)
    );

    register d_register_inst
    (
            .in 	(alu_out),
            .write 	(d_write),
            .clk 	(clk),
            .reset 	(reset),
            .out 	(d_reg_out)
    );

    alu alu_inst
    (
            .x  (d_reg_out),
            .y  (y),
            .zx (alu_zx),
            .nx (alu_nx),
            .zy (alu_zy),
            .ny (alu_ny),
            .f  (alu_f),
            .no (alu_no),
            .out (alu_out),
            .zr (alu_zr),
            .ng (alu_ng)
    );

    jmp_handle jmp_handle_inst
    (
            .opcode(opcode),
            .j1(j1),
            .j2(j2),
            .j3(j3),
            .zr(alu_zr),
            .ng(alu_ng),
            .out_load(jmp_handle_load),
            .out_inc(jmp_handle_inc)
    );

    pc pc_inst
    (
            .clk(clk),
            .reset(reset),
            .in(a_reg_out),
            .load(jmp_handle_load),
            .inc(jmp_handle_inc),
            .out(pc)
    );
endmodule
