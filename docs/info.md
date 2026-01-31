<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## Project: 4-bit Digital Counter (tt10)

**Author:** nasser hadi

## How it works
This design is a synchronous **4-bit up counter**.
- The counter increments on each rising edge of **clk** when **en = ui[0] = 1**
- When **rst_n = 0**, the counter resets to 0
- Outputs:
  - `uo[3:0]` = counter value (LSB to MSB)
  - `uo[4]` = terminal count flag (1 when counter == 15)

## How to test
1. Hold reset low (`rst_n=0`) for a few cycles → counter should be 0
2. Set `en=1` → counter increments each clock: 0,1,2,3,...
3. Set `en=0` → counter holds its value (no counting)
4. Let it wrap after 15 → returns to 0

## External hardware
None

