
/*
* Just runs "test/main.hack" without any checks
*/

`include "computer.sv"

`define assert(signal, value) \
    if (signal !== value) begin \
        $display("ASSERTION FAILED in %m: signal (%d) != value (%d)", signal, value); \
        $finish; \
    end
//----------------------------------------------------------------------------
// Testbench
//----------------------------------------------------------------------------

module computer_run_main;

    parameter TIME_PERIOD = 10;
    parameter rom_size = 45;
    parameter ram_size = 32;
    parameter rom_file = "test/main.hack";
    parameter ram_init_file = "test/ram_32_init.mem";
    parameter ram_final_file = "test/ram_main_final.mem";

    integer i = 0;

    // Inputs
    logic clk;
    logic reset;

    // Outputs
    logic ended;


    computer #(
        .rom_size(rom_size),
        .ram_size(ram_size),
        .rom_file(rom_file),
        .ram_init_file(ram_init_file),
        .ram_final_file(ram_final_file)
    ) computer_dut (
        .*
    );

    reg [15:0] ram_out [0:ram_size - 1];
    reg [15:0] ram_in  [0:ram_size - 1];

    always #TIME_PERIOD clk = ~clk;

    initial begin
        clk = 0;
        reset = 1;

        // $writememb(ram_init_file, ram_in);

        #TIME_PERIOD reset = 0;

        // Run Computer
        // for (int i = 0; i < 100; i ++) begin
        while (!ended) begin
            @ (negedge clk);
            i += 1;

            if (i >= 1000) begin
                // $display("%s: FAIL: endless loop");
                $finish;
            end
        end

        $display("%s: PASS (No checks)", `__FILE__);
        $finish;
    end
endmodule
