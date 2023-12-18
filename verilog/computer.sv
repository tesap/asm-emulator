
`include "cpu.sv"

module computer
# (
    parameter rom_size,
    parameter ram_size
)
(
    input clk,
    input reset,
    
    output ended
);

    reg [15:0] program_rom [0:rom_size - 1];
    reg [15:0] ram [0:ram_size - 1];
    
    wire [15:0] addressM;
    wire [15:0] outM;
    wire [15:0] pc;
    wire [15:0] instruction = program_rom[pc];
    wire [15:0] inM = ram[addressM];
    
    assign ended = pc >= rom_size;
    
    initial begin
        // $monitor(
        //     "================== COMPUTER: Time=%0t clk=%b reset=%b | inM=%d instruction=%b reset=%b | outM=%d writeM=%b addressM=%d pc=%d",
        //     $time, clk, reset, inM, instruction, reset, outM, writeM, addressM, pc
        // );
    end
    
    // always @* begin
    //     $display("RAM: 0=%d,\n 1=%d,\n 2=%d,\n sum=%d,\n i=%d", ram[0], ram[1], ram[2], ram[16], ram[17]);
    // end
    
    initial @(negedge reset) begin
        $readmemb("main.hack", program_rom);
        $readmemb("ram_init.mem", ram);
    end
    
    final begin
        $writememb("ram_final.mem", ram);
    end
    
    always @(negedge clk) begin
        if (writeM) begin
            ram[addressM] <= outM;
        end
    end

    cpu cpu_inst
    (
        .clk(clk),
        .reset(reset),
        .inM(inM),
        .instruction(instruction),
        .outM(outM),
        .writeM(writeM),
        .addressM(addressM),
        .pc(pc)
    );

endmodule
