import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles, Timer

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start 4-bit counter test")

    # Start clock
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    # Init inputs
    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Hold reset low for a few full cycles (very important)
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 3)

    # Release reset cleanly between edges
    dut.rst_n.value = 1
    await Timer(1, units="ns")

    # Sanity print after reset release
    dut._log.info(f"After reset release: rst_n={dut.rst_n.value} ui_in={dut.ui_in.value} uo_out={dut.uo_out.value}")

    # Enable counting and settle before the next edge
    dut.ui_in.value = 1
    await Timer(1, units="ns")

    dut._log.info(f"Before counting edge: rst_n={dut.rst_n.value} ui_in={dut.ui_in.value} uo_out={dut.uo_out.value}")

    # Wait one rising edge: should increment 0 -> 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")  # let signals update after edge
    count = int(dut.uo_out.value) & 0x0F

    dut._log.info(f"After 1st count edge: uo_out={dut.uo_out.value} count={count}")

    assert count == 1, f"Expected 1, got {count}"

    # Next few counts
    for expected in range(2, 6):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        count = int(dut.uo_out.value) & 0x0F
        dut._log.info(f"Expected {expected}, got {count}, uo_out={dut.uo_out.value}")
        assert count == expected, f"Expected {expected}, got {count}"
