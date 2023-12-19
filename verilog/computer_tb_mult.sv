
/*
* Checks "test/mult.hack" that writes multiply of RAM[0] and RAM[1] to RAM[2]
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

module computer_tb_mult;

    parameter TIME_PERIOD = 10;
    parameter rom_size = 22;
    parameter ram_size = 32;
    parameter rom_file = "test/hack/mult.hack";
    parameter ram_init_file = "test/ram_mult_init.mem";
    parameter ram_final_file = "test/ram_mult_final.mem";

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

    integer a = 13, b = 8;

    initial begin
        clk = 0;
        reset = 1;

        // Setup input memory
        if (a * b > 2 ** 16) begin
            $display("%s: FAIL: Too big values", `__FILE__);
            $finish;
        end

        ram_in[0] = a;
        ram_in[1] = b;
        $writememb(ram_init_file, ram_in);
          
        #TIME_PERIOD reset = 0;

        // Run Computer
        // for (int i = 0; i < 100; i ++) begin
        while (!ended) begin
            @ (negedge clk);
        end

        // Check final memory
        $readmemb(ram_final_file, ram_out);

        `assert(ram_out[2], a * b);

        $display("%s: PASS", `__FILE__);
        $finish;
    end
endmodule
