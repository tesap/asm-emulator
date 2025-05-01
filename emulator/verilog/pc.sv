
`include "register.sv"

module pc
(
    input clk,
    input reset,

    input [15:0] in,
    input load,
    input inc,

    output [15:0] out
);


    wire [15:0] reg_out;
         wire [15:0] reg_in = (load) ? in : ((inc) ? (reg_out + 1) : 0) ;
    wire write = load || inc || reset;

    register r_inst
    (
        .clk (clk),
        .reset (reset),

        .write (write),
        .in (reg_in),
        .out (reg_out)
    );

    assign out = reg_out;
endmodule

