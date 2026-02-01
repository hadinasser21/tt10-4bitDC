import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


# Helper: in gate-level sim, flops update after UNIT_DELAY (#1), so wait a bit
async def sample_after_edge(delay_ns=2):
    # 2ns is safely > #1 in your flow
    await Timer(delay_ns, units="ns")


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start 4-bit counter test")

    # 10us period clock (matches what you already used)
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    # Init inputs
    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Reset (active-low)
    dut.rst_n.value = 0

    # Hold reset for a couple real clock edges
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    # Release reset
    dut.rst_n.value = 1

    # Let reset release settle
    await Timer(2, units="ns")

    # Enable counting using ui_in[0]
    dut.ui_in.value = 1  # bit0=1 enables counting in your RTL

    # Let ui_in settle before next edge
    await Timer(2, units="ns")

    # Now check counts.
    # IMPORTANT: after each rising edge, wait a tiny bit (gate-level needs it)
    for expected in range(1, 6):
        await RisingEdge(dut.clk)
        await sample_after_edge(delay_ns=2)

        count = int(dut.uo_out.value) & 0x0F
        dut._log.info(f"Expected {expected}, got {count}, uo_out={dut.uo_out.value.binstr}")
        assert count == expected, f"Expected {expected}, got {count}"
