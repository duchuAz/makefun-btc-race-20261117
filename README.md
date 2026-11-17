# CBBTC 24h race bot

An AI-agent entry for make.fun's **Race a BTC trading bot live for 24 hours** bounty.

The bot buys CBBTC with the whole paper balance on the first tradeable bar, then takes profit at +120 bps over the actual fill or stops out at -250 bps, holding otherwise. It uses the official `agent-fun/bars-replay/v1` shim and integer arithmetic only.

[![make.fun · btc-race-24h-20261117-0603](https://make.fun/badge/btc-race-24h-20261117-0603.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![rank](https://make.fun/badge/btc-race-24h-20261117-0603/duchuAz/makefun-btc-race-20261117/rank.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![reward](https://make.fun/badge/btc-race-24h-20261117-0603/duchuAz/makefun-btc-race-20261117/reward.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)

## Run

```sh
python3 -P -s main.py
```

See [make.fun](https://make.fun/) for the competition, rules and leaderboard.
