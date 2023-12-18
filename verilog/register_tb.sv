
`include "register.sv"

//----------------------------------------------------------------------------
// Testbench
//----------------------------------------------------------------------------

module tb_register;

    parameter TIME_PERIOD = 10;

    logic clk, reset, write;
    logic [15:0] in_data, out_data;

    register dut (
        .clk(clk),
        .reset(reset),
        .in(in_data),
        .write(write),
        .out(out_data)
    );

    always #TIME_PERIOD clk = ~clk;

    initial begin
        $monitor("Time=%0t clk=%b reset=%b write=%b in_data=%h out_data=%h",
        $time, clk, reset, write, in_data, out_data);
    end

    initial begin
        clk = 0;
        reset = 1;
        write = 0;
        in_data = 16'h0000;

        #TIME_PERIOD reset = 0;

        @ (negedge clk);
        in_data = 16'hABCD;
        write = 1;

        @ (negedge clk);
        write = 0;
        if (out_data !== 16'hABCD) begin
            $display("ERROR: Output mismatch at time %0t", $time);
            $finish;
        end

        @ (negedge clk);
        if (out_data !== 16'hABCD) begin
            $display("ERROR: Output mismatch at time %0t", $time);
            $finish;
        end

        @ (negedge clk);
        in_data = 16'h1111;
        write = 1;

        @ (negedge clk);
        if (out_data !== 16'h1111) begin
            $display("ERROR: Output mismatch at time %0t", $time);
            $finish;
        end

        @ (negedge clk);
        reset = 1;
        write = 0;

        @ (negedge clk);
        reset = 0;
        if (out_data !== 0) begin
            $display("ERROR: Output mismatch at time %0t", $time);
            $finish;
        end

        $display("register.sv: PASS");
        $finish;
    end

endmodule
