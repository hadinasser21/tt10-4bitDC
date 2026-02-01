import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles, Timer

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start 4-bit counter test")

    # Start clock: 10us period
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    # Initialize inputs
    dut.ena.value = 1          # TinyTapeout project select
    dut.ui_in.value = 0        # user enable = 0
    dut.uio_in.value = 0

    # Let signals settle
    await Timer(1, units="ns")

    # ---- INITIAL SANITY CHECK ----
    dut._log.info(
        f"INIT: ena={dut.ena.value} rst_n={dut.rst_n.value} "
        f"ui_in={dut.ui_in.value} uo_out={dut.uo_out.value}"
    )

    # Fail immediately if ena is not actually high
    assert int(dut.ena.value) == 1, f"ena is NOT 1 (ena={dut.ena.value})"

    # ---- RESET ----
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 3)   # hold reset for multiple real cycles
    dut.rst_n.value = 1
    await Timer(1, units="ns")

    dut._log.info(
        f"After reset release: ena={dut.ena.value} rst_n={dut.rst_n.value} "
        f"ui_in={dut.ui_in.value} uo_out={dut.uo_out.value}"
    )

    # ---- ENABLE COUNTING ----
    dut.ui_in.value = 1             # ui_in[0] = enable
    await Timer(1, units="ns")

    dut._log.info(
        f"Before counting edge: ena={dut.ena.value} rst_n={dut.rst_n.value} "
        f"ui_in={dut.ui_in.value} uo_out={dut.uo_out.value}"
    )

    # ---- FIRST COUNT EDGE ----
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    count = int(dut.uo_out.value) & 0x0F
    dut._log.info(
        f"After 1st count edge: ena={dut.ena.value} "
        f"uo_out={dut.uo_out.value} count={count}"
    )

    assert count == 1, f"Expected 1, got {count}"

    # ---- CONTINUE COUNTING ----
    for expected in range(2, 6):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        count = int(dut.uo_out.value) & 0x0F
        dut._log.info(
            f"Expected {expected}, got {count}, uo_out={dut.uo_out.value}"
        )
        assert count == expected, f"Expected {expected}, got {count}"
