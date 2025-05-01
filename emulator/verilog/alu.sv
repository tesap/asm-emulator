
module alu
(
    input [15:0] x,
    input [15:0] y,
    input zx, // zero the x input?
    input nx, // negate the x input?
    input zy, // zero the y input?
    input ny, // negate the y input?
    input f,  // compute out = x + y (if 1) or x & y (if 0)
    input no, // negate the out output?

    output [15:0] out, 	// 16-bit output
    output zr, 		// 1 if (out == 0), 0 otherwise
    output ng 		// 1 if (out < 0),  0 otherwise
);
    wire [15:0] x1;
    wire [15:0] y1;
    wire [15:0] x2;
    wire [15:0] y2;
    wire [15:0] f_res;
    wire signed [15:0] f_res2;

    assign x1 = (zx) ? 0 : x;
    assign y1 = (zy) ? 0 : y;
    
    assign x2 = (nx) ? ~x1 : x1;
    assign y2 = (ny) ? ~y1 : y1;

    assign f_res = (f) ? (x2 + y2) : (x2 & y2);
    assign f_res2 = (no) ? ~f_res : f_res;

    assign zr = (f_res2 == 0);
    assign ng = (f_res2 < 0);
    assign out = f_res2;
endmodule


