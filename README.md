# HIP3Radar

Early warning for Hyperliquid perp risk. Real-time surveillance of every HL native + HIP-3 perp market.

Live site: https://edgardextra-lang.github.io/hip3radar-site/
Live dashboard: https://competent-beach-notre-meter.trycloudflare.com/hip3radar/

## What it does

Polls every Hyperliquid perp dex (native + 8 HIP-3 dexes, ~300+ markets) every 60s and scores each market 0–100 on five risk signals:

- **Oracle drift** — HL oracle price vs Binance/OKX/Bybit median
- **Mark-oracle spread** — HL mark price vs oracle price (manipulation tell)
- **OI velocity** — open interest growth 1h / 24h
- **OI / volume ratio** — thin-float indicator
- **Funding extremity** — extreme funding rates

## API

```
GET /hip3radar/api/state   # top 25 highest risk
GET /hip3radar/api/all     # every market
GET /hip3radar/api/dex/:id # per-dex slice
```

CORS enabled. No auth. Free.

## Why

Built after the JELLY incident (March 2025) — $12M socialized loss from a single whale-dump on a thin-float meme perp. Every signal in this radar would have fired hours before the wipe.
