import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start 4-bit counter test")

    # Clock (same style as manual: set a clock and start it)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Initialize
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Reset (active-low)
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # After reset, counter must be 0
    assert int(dut.uo_out.value) & 0x0F == 0

    # Enable counting (ui[0] = 1)
    dut.ui_in[0].value = 1

    # Check first few counts
    for expected in range(1, 6):
        await ClockCycles(dut.clk, 1)
        count = int(dut.uo_out.value) & 0x0F
        assert count == (expected & 0x0F), f"Expected {expected}, got {count}"

    # Disable counting (hold)
    dut.ui_in[0].value = 0
    held = int(dut.uo_out.value) & 0x0F
    await ClockCycles(dut.clk, 3)
    count2 = int(dut.uo_out.value) & 0x0F
    assert count2 == held, f"Counter should hold at {held}, got {count2}"
