/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_nasser_hadi_counter (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,    // Dedicated outputs
    input  wire [7:0] uio_in,    // IOs: Input path
    output wire [7:0] uio_out,   // IOs: Output path
    output wire [7:0] uio_oe,    // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,       // always 1 when the design is powered, can ignore
    input  wire       clk,       // clock
    input  wire       rst_n       // reset_n - low to reset
);

    // ui_in mapping
    wire en = ui_in[0];          // enable counting when 1

    reg [3:0] count;

    // Synchronous logic (posedge clock), async reset via rst_n (active-low)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 4'b0000;
        end else if (en) begin
            count <= count + 4'b0001;
        end
    end

    // Optional terminal count flag (1 when count == 15)
    wire tc = (count == 4'hF);

    // Outputs
    assign uo_out[0] = count[0];
    assign uo_out[1] = count[1];
    assign uo_out[2] = count[2];
    assign uo_out[3] = count[3];
    assign uo_out[4] = tc;
    assign uo_out[5] = 1'b0;
    assign uo_out[6] = 1'b0;
    assign uo_out[7] = 1'b0;

    // No bidirectional IO used
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // Prevent unused warnings (pattern shown in manual)
    wire _unused = &{ena, ui_in[7:1], uio_in, 1'b0};

endmodule
