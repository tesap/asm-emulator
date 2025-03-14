
`include "jmp_handle.sv"

//----------------------------------------------------------------------------
// Testbench
//----------------------------------------------------------------------------

module jmp_handle_tb;
    logic opcode, j1, j2, j3, zr, ng;
    logic out_load, out_inc;

    jmp_handle jmp_handle_inst
    (
        .*
    );

    task test
    (
        input t_opcode,
        input t_j1,
        input t_j2,
        input t_j3,
        input t_zr,
        input t_ng,

        input t_out_load,
        input t_out_inc
    );

    { opcode, j1, j2, j3, zr, ng } = { t_opcode, t_j1, t_j2, t_j3, t_zr, t_ng };

    # 1;

    $display ("TEST opcode=%b, j1=%b, j2=%b, j3=%b, zr=%b, ng=%b, out_load=%b, out_inc=%b", opcode, j1, j2, j3, zr, ng, out_load, out_inc);

    if (out_load !== t_out_load || out_inc !== t_out_inc)
        begin
            $display ("FAIL: EXPECTED %d, %b", t_out_load, t_out_inc);
            $finish;
        end
    endtask

    initial begin
        //    opcode  j1  j2  j3  zr  ng out_load out_inc
        test (     0,  0,  0,  1,  0,  0,       0,     1);
        test (     0,  1,  1,  1,  1,  0,       0,     1);

        test (     1,  0,  0,  1,  0,  0,       1,     0);
        test (     1,  0,  1,  0,  1,  0,       1,     0);
        test (     1,  0,  1,  1,  1,  0,       1,     0);
        test (     1,  0,  1,  1,  0,  0,       1,     0);

        $display ("%s: PASS", `__FILE__);
        $finish;
    end
endmodule


