import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start 4-bit counter test")

    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)   # ensure at least one real edge happens in reset
    dut.rst_n.value = 1

    # Give 1ns to settle after changing rst_n (important for some sims)
    await Timer(1, units="ns")

    # Enable counting (bit0 = 1) and let it settle BEFORE the next edge
    dut.ui_in.value = 1
    await Timer(1, units="ns")

    # Now this rising edge should increment 0 -> 1
    await RisingEdge(dut.clk)
    count = int(dut.uo_out.value) & 0x0F
    assert count == 1, f"Expected 1, got {count}"

    # Next few counts
    for expected in range(2, 6):
        await RisingEdge(dut.clk)
        count = int(dut.uo_out.value) & 0x0F
        assert count == expected, f"Expected {expected}, got {count}"
