
`include "cpu.sv"

module computer
# (
    parameter rom_size,
    parameter ram_size,

    parameter rom_file,
    parameter ram_init_file,
    parameter ram_final_file
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
        $monitor(
            "================== COMPUTER: Time=%0t clk=%b reset=%b | inM=%d instruction=%b reset=%b | outM=%d writeM=%b addressM=%d pc=%d ended=%b",
            $time, clk, reset, inM, instruction, reset, outM, writeM, addressM, pc, ended
        );
    end
    
    // always @* begin
    //     $display("RAM: 0=%d,\n 1=%d,\n 2=%d,\n sum=%d,\n i=%d", ram[0], ram[1], ram[2], ram[16], ram[17]);
    // end
    
    // Init
    initial @(negedge reset) begin
        $readmemb(rom_file, program_rom);
        $readmemb(ram_init_file, ram);
    end
    
    // Final
    initial @(posedge ended) begin
        $writememb(ram_final_file, ram);
    end
    
    always @(posedge clk) begin
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
