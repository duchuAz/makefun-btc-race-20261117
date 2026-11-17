"""CBBTC take-profit / stop-loss bot for the agent-fun/bars-replay/v1 protocol.

Strategy:
1. On the first tradeable batch, spend the whole cash balance on CBBTC with a 250 bps
   slippage cap (retried on a later batch only if the market rejected the buy).
2. Remember the actual buy fill price reported by the next batch's fills.
3. While the position is held, sell the whole position with the same 250 bps slippage cap
   once the latest close is at least +150 bps above the fill price (take profit) or at
   most -250 bps below it (stop loss).
4. Otherwise hold. The harness flattens any remaining position at the end of the window.

Everything is integer arithmetic on the protocol's scaled prices, so the bot is fully
deterministic: no clock, no environment, no randomness. The shim owns the wire; this
module only decides the orders for each batch.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars  # noqa: E402

SYMBOL = "CBBTC"
MAX_SLIPPAGE_BPS = 250
TAKE_PROFIT_BPS = 120
STOP_LOSS_BPS = 250
BPS = 10_000

# State that persists across batches (the shim calls on_batch once per batch, in order).
bought = False
fill_price = None


def on_batch(state, batch):
    """Return the orders decided on this batch; every order fills at the next bar's open."""
    global bought, fill_price

    # 1. Learn the actual entry price from the fills the market reports.
    for fill in batch.get("fills", ()):
        if (
            fill.get("symbol") == SYMBOL
            and fill.get("side") == "buy"
            and fill.get("status") == "filled"
        ):
            bought = True
            fill_price = int(fill["price"])

    # Warm-up bars are history only: every order decided on one is rejected.
    if state.warming_up:
        return []

    held = state.positions.get(SYMBOL)
    close = state.close(SYMBOL)

    # 2. While the position is open, exit on take profit or stop loss.
    if held is not None and fill_price is not None and close is not None and held.qty > 0:
        above_tp = close * BPS >= fill_price * (BPS + TAKE_PROFIT_BPS)
        below_sl = close * BPS <= fill_price * (BPS - STOP_LOSS_BPS)
        if above_tp or below_sl:
            return [
                {
                    "side": "sell",
                    "symbol": SYMBOL,
                    "qty": held.qty,
                    "max_slippage_bps": MAX_SLIPPAGE_BPS,
                }
            ]
        return []

    # 3. Otherwise hold; only enter once, and only if the buy has not been confirmed yet.
    if bought or fill_price is not None or held is not None:
        return []
    if close is None or state.cash <= 0:
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
