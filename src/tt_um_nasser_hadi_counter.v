/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_nasser_hadi_counter (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    reg [3:0] count;

    // IMPORTANT: use ui_in[0] directly so it is NOT optimized away
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 4'b0000;
        end else if (ui_in[0]) begin
            count <= count + 4'b0001;
        end
    end

    wire tc = (count == 4'hF);

    assign uo_out = {
        3'b000,
        tc,
        count
    };

    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // Do NOT include ui_in[0] here
    wire _unused = &{ena, ui_in[7:1], uio_in};

endmodule
