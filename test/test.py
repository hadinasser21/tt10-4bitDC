import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start 4-bit counter test")

    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    dut.ena.value = 1
    dut.uio_in.value = 0

    # Hold enable low during reset
    dut.ui_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1

    # Wait one rising edge so reset is fully released on a clock edge
    await RisingEdge(dut.clk)

    # Confirm reset state
    assert (int(dut.uo_out.value) & 0x0F) == 0

    # Enable counting: bit0 = 1
    dut.ui_in.value = 1

    # Wait one rising edge, then it should increment to 1
    await RisingEdge(dut.clk)
    count = int(dut.uo_out.value) & 0x0F
    assert count == 1, f"Expected 1, got {count}"

    # Run a few more cycles
    for expected in range(2, 6):
        await RisingEdge(dut.clk)
        count = int(dut.uo_out.value) & 0x0F
        assert count == expected, f"Expected {expected}, got {count}"

    # Disable counting (hold)
    dut.ui_in.value = 0
    held = int(dut.uo_out.value) & 0x0F
    await ClockCycles(dut.clk, 3)
    count2 = int(dut.uo_out.value) & 0x0F
    assert count2 == held, f"Counter should hold at {held}, got {count2}"
