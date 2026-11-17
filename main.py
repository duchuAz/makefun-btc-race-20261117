"""CBBTC buy-and-hold bot for the agent-fun/bars-replay/v1 protocol.

Strategy v1: on the first tradeable batch, spend the whole cash balance on CBBTC with a
250 bps slippage cap, then hold until the harness flattens the position at the end of the
window. If the buy is rejected, try once more on the next tradeable batch.

The shim owns the wire; this module only decides the orders for each batch.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars  # noqa: E402

SYMBOL = "CBBTC"
MAX_SLIPPAGE_BPS = 250

# Set once the market confirms our buy filled (state persists across batches).
bought = False


def on_batch(state, batch):
    """Return the orders decided on this batch; every order fills at the next bar's open."""
    global bought

    # Remember a confirmed fill so the buy is never sent twice.
    for fill in batch.get("fills", ()):
        if fill.get("side") == "buy" and fill.get("status") == "filled" and fill.get("symbol") == SYMBOL:
            bought = True

    # Warm-up bars are history only: every order decided on one is rejected.
    if state.warming_up:
        return []

    if bought or SYMBOL in state.positions:
        return []
    if state.close(SYMBOL) is None or state.cash <= 0:
        return []

    return [
        {
            "side": "buy",
            "symbol": SYMBOL,
            "notional_quote_units": state.cash,
            "max_slippage_bps": MAX_SLIPPAGE_BPS,
        }
    ]


if __name__ == "__main__":
    makefun_bars.run(on_batch)
