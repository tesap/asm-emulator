
`include "cpu.sv"

//----------------------------------------------------------------------------
// Testbench
//----------------------------------------------------------------------------

module tb_cpu;
    parameter TIME_PERIOD = 10;

    // Inputs
    logic clk;
    logic reset;
	 
    logic [15:0] inM;
    logic [15:0] instruction;
	 
    // Outputs
    logic [15:0] outM;
    logic writeM;
    logic [15:0] addressM;
    logic [15:0] pc;

    cpu cpu_dut (
         .*
    );

    always #TIME_PERIOD clk = ~clk;

    initial begin
        $monitor(
            "Time=%0t clk=%b reset=%b inM=%h instruction=%b reset=%b | outM=%h writeM=%b addressM=%h pc=%d",
            $time, clk, reset, inM, instruction, reset, outM, writeM, addressM, pc
        );
    end
	 
    initial begin
        clk = 0;
        reset = 1;
        inM = 16'h0000;
        instruction = 16'h0000;
		 
        #TIME_PERIOD reset = 0;

        @ (negedge clk);
		  
        inM = 0;
        instruction = 16'h0AA1; // @AA1
        @ (negedge clk);
        if (addressM !== 16'h0AA1) begin
            $display("%s: ERROR: Output mismatch at time %0t", `__FILE__, $time);
            $finish;
        end
		  
        instruction = 16'b1000111111001000; // M=1
        @ (negedge clk);
        if (addressM !== 16'h0AA1 || outM !== 16'h001 || writeM !== 1) begin
            $display("%s: ERROR: Output mismatch at time %0t", `__FILE__, $time);
            $finish;
        end
		  
        instruction = 16'b1110110000001000; // M=A
        @ (negedge clk);
        if (addressM !== 16'h0AA1 || outM !== 16'h0AA1 || writeM !== 1) begin
            $display("%s: ERROR: Output mismatch at time %0t", `__FILE__, $time);
            $finish;
        end
        inM = 16'h0AA1;
		  
        instruction = 16'b1110110111100000; // A=A+1
        @ (negedge clk);
        if (addressM !== 16'h0AA2 || writeM !== 0) begin
            $display("%s: ERROR: Output mismatch at time %0t", `__FILE__, $time);
            $finish;
        end
		  
        instruction = 16'b1110110010100000; // A=A-1
        @ (negedge clk);
        if (addressM !== 16'h0AA1 || writeM !== 0) begin
            $display("%s: ERROR: Output mismatch at time %0t", `__FILE__, $time);
            $finish;
        end
		  
        instruction = 16'b1111110111101000; // AM=M+1
        @ (negedge clk);
        if (addressM !== 16'h0AA2 || outM !== 16'h0AA2 || writeM !== 1) begin
            $display("%s: ERROR: Output mismatch at time %0t", `__FILE__, $time);
            $finish;
        end
		  
        instruction = 16'h0005; // @5
        @ (negedge clk);
        if (addressM !== 16'h0005) begin
            $display("%s: ERROR: Output mismatch at time %0t", `__FILE__, $time);
            $finish;
        end
		  
        instruction = 16'b1110110000010000; // D=A
        @ (negedge clk);
		  
        instruction = 16'b1110011111100000; // A=D+1
        @ (negedge clk);
        if (addressM !== 16'h0006 || writeM !== 0) begin
            $display("%s: ERROR: Output mismatch at time %0t", `__FILE__, $time);
            $finish;
        end
		  
        instruction = 16'b1110101010000111; // 0;JMP
        @ (negedge clk);
        if (addressM !== 16'h0006 || pc !== 16'h0006) begin
            $display("%s: ERROR: Output mismatch at time %0t", `__FILE__, $time);
            $finish;
        end
		  
        $display("%s: PASS", `__FILE__);
        $finish;
    end
endmodule
