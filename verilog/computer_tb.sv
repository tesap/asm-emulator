
`include "computer.sv"

//----------------------------------------------------------------------------
// Testbench
//----------------------------------------------------------------------------

module tb_computer;

    parameter TIME_PERIOD = 10;

    // Inputs
    logic clk;
    logic reset;

    // Outputs
    logic ended;

    computer computer_dut (
        .*
    );

    always #TIME_PERIOD clk = ~clk;

    initial begin
        clk = 0;
        reset = 1;

        #TIME_PERIOD reset = 0;
          
        // for (int i = 0; i < 100; i ++) begin
        while (!ended) begin
            @ (negedge clk);
        end
          
        $display("%s: PASS", `__FILE__);
        $finish;
	end
endmodule
