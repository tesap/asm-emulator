
`include "computer.sv"

`define assert(signal, value) \
    if (signal !== value) begin \
        $display("ASSERTION FAILED in %m: signal != value; %d|%d", signal, value); \
        $finish; \
    end
//----------------------------------------------------------------------------
// Testbench
//----------------------------------------------------------------------------

module tb_computer;

    parameter TIME_PERIOD = 10;
    parameter rom_size = 22;
    parameter ram_size = 32;

    // Inputs
    logic clk;
    logic reset;

    // Outputs
    logic ended;

    computer #(.rom_size(rom_size), .ram_size(ram_size)) computer_dut (
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
            $display("%s: Too big values", `__FILE__);
            $finish;
        end

        ram_in[0] = a;
        ram_in[1] = b;
        $writememb("ram_init.mem", ram_in);
          
        #TIME_PERIOD reset = 0;

        // for (int i = 0; i < 100; i ++) begin
        while (!ended) begin
            @ (negedge clk);
        end

        $readmemb("ram_final.mem", ram_out);

        if (ram_out[2] !== a * b) begin
            $display("%s: ERROR: %d * %d != %d", `__FILE__, a, b, ram_out[2]);
            $finish;
        end

        $display("%s: PASS", `__FILE__);
        $finish;
    end
endmodule
