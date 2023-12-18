
module register
(
    input clk,
    input reset,

    input [15:0] in,
    input write,

    output [15:0] out
);

    reg [15:0] r;

    always @(negedge clk or posedge reset) begin
        if (reset) begin
            r <= 0;
        end
        else if (write) begin
            r <= in;
        end
    end

    assign out = r;
endmodule


