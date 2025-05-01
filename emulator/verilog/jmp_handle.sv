
module jmp_handle
(
    input opcode,
    input j1,
    input j2,
    input j3,
    input zr,
    input ng,

    output out_load,
    output out_inc
);

    wire a1 = !j1 && !j2 &&  j3 && !ng && !zr;
    wire a2 = !j1 &&  j2 && !j3 && zr;
    wire a3 = !j1 &&  j2 &&  j3 && !ng;
    wire a4 =  j1 && !j2 && !j3 &&  ng;
    wire a5 =  j1 && !j2 &&  j3 && !zr;
    wire a6 =  j1 &&  j2 && !j3 && (zr ^ ng);
    wire a7 =  j1 &&  j2 &&  j3;

    wire jmp = a1 || a2 || a3 || a4 || a5 || a6 || a7;
    assign out_load = jmp && opcode;
    assign out_inc = !out_load;

endmodule


