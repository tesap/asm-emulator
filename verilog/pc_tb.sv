
`include "pc.sv"

//----------------------------------------------------------------------------
// Testbench
//----------------------------------------------------------------------------

module tb_pc;

    parameter TIME_PERIOD = 10;

    logic clk, reset, inc, load;
    logic [15:0] in_data, out_data;

    pc pc_dut (
        .clk(clk),
        .reset(reset),
        .in(in_data),
        .load(load),
        .inc(inc),
        .out(out_data)
    );

    always #TIME_PERIOD clk = ~clk;

    initial begin
        $monitor("Time=%0t clk=%b reset=%b load=%b inc=%b in_data=%h out_data=%h",
        $time, clk, reset, load, inc, in_data, out_data);
    end

    initial begin
        clk = 0;
        reset = 1;
        load = 0;
        inc = 0;
        in_data = 16'h0000;

        #TIME_PERIOD reset = 0;

        // ================================ 1
        @ (negedge clk);
        in_data = 16'hABCD;
        load = 1;

        @ (negedge clk);
        load = 0;
        if (out_data !== 16'hABCD) begin
            $display("ERROR: Output mismatch at time %0t", $time);
            $finish;
        end

        @ (negedge clk);
        if (out_data !== 16'hABCD) begin
            $display("ERROR: Output mismatch at time %0t", $time);
            $finish;
        end

        // ================================ 2
        @ (negedge clk);
        in_data = 16'h1111;
        load = 1;

        @ (negedge clk);
        load = 0;
        if (out_data !== 16'h1111) begin
            $display("ERROR: Output mismatch at time %0t", $time);
            $finish;
        end

        // ================================ 3
        @ (negedge clk);
        inc = 1;

        @ (negedge clk);
        inc = 0;
        if (out_data !== 16'h1112) begin
            $display("ERROR: Output mismatch at time %0t", $time);
            $finish;
        end

        // ================================ 4
        @ (negedge clk);
        inc = 1;

        @ (negedge clk);
        inc = 0;
        if (out_data !== 16'h1113) begin
            $display("ERROR: Output mismatch at time %0t", $time);
            $finish;
        end

        $display("pc.sv: PASS");
        $finish;
    end
endmodule
