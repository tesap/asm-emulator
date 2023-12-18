
`include "alu.sv"

//----------------------------------------------------------------------------
// Testbench
//----------------------------------------------------------------------------

module testbench;
    logic signed [15:0] x, y;
    logic zx, nx, zy, ny, f, no;

    logic signed [15:0] out;
    logic zr, ng;

    alu alu_test
    (
        .x  (x),
	.y  (y),
	.zx (zx),
	.nx (nx),
	.zy (zy),
	.ny (ny),
	.f  (f),
	.no (no),
	.out (out),
	.zr (zr),
	.ng (ng)
    );

    task test
    (
        input [15:0] t_x,
        input [15:0] t_y,
        input t_zx,
        input t_nx,
        input t_zy,
        input t_ny,
        input t_f,
        input t_no,

        input [15:0] t_out,
        input t_zr,
        input t_ng
    );

    { x, y, zx, nx, zy, ny, f, no } = { t_x, t_y, t_zx, t_nx, t_zy, t_ny, t_f, t_no };

    # 1;

    $display ("TEST      x,      y, zx, nx, zy, ny, f, no");
    $display ("TEST %d, %d,  %b,  %b,  %b,  %b, %b,  %b", x, y, zx, nx, zy, ny, f, no);
    $display ("RES:             out, zr, ng");
    $display ("RES:          %d, %b,  %b", out, zr, ng);

    if (out !== t_out || zr !== t_zr || ng !== t_ng)
        begin
            $display ("FAIL: EXPECTED %d, %b,  %b", t_out, t_zr, t_ng);
            $finish;
        end
    endtask

    initial
        begin
        //        x   y   zx  nx  zy  ny  f   no  out zr  ng
        test (    1,  2,  0,  0,  0,  0,  1,  0,  3,  0,  0);
        test (    10, 20, 0,  0,  0,  0,  1,  0,  30, 0,  0);
        test (    10, 20, 0,  0,  0,  0,  1,  0,  30, 0,  0);
        test (    51, 32, 0,  0,  0,  0,  1,  0,  83, 0,  0);

        test (     1,  1, 0,  0,  0,  0,  0,  0,   1, 0,  0);
        test (     0,  1, 0,  0,  0,  0,  0,  0,   0, 1,  0);
        test (     1,  0, 0,  0,  0,  0,  0,  0,   0, 1,  0);

        test (    15, 18, 1,  0,  0,  0,  1,  0,  18, 0,  0);
        test (    15, 18, 0,  0,  1,  0,  1,  0,  15, 0,  0);
        test (    15, 18, 1,  0,  1,  0,  1,  0,   0, 1,  0);

        // test (    15, 18, 0,  1,  0,  0,  1,  0,   3, 0,  0);
        // test (    15, 18, 0,  1,  0,  0,  1,  1,  -3, 0,  1);
        // test (    15, 18, 0,  1,  0,  1,  1,  0, -33, 0,  1);
        // test (    15, 18, 0,  1,  0,  1,  1,  1,  33, 0,  0);
        test (    15, 18, 1,  1,  1,  1,  1,  1,  1, 0,  0);


        $display ("%s PASS", `__FILE__);
        $finish;
    end
endmodule

