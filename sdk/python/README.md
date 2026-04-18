# hip3radar — Python SDK

Real-time risk surveillance for every Hyperliquid native + HIP-3 perpetual market.

```bash
pip install hip3radar
```

## Usage

```python
from hip3radar import HIP3Radar, safety_grade

# Free public tier — no key needed
client = HIP3Radar()

# Top 25 highest-risk markets
state = client.state()
for m in state["top_risk"]:
    grade = safety_grade(m["risk_score"])
    print(f"{m['name']:25s} {grade['grade']:3s} ({grade['rating']:5.1f}/100)")

# Full snapshot — every market across every dex
snap = client.all_markets()
print(f"{snap['market_count']} markets across {snap['dex_count']} dexes")

# One dex
xyz = client.dex("xyz")  # trade.xyz markets

# One market
btc = client.market("hl", "BTC")

# 24h history
hist = client.history("hl", "BTC", hours=24)

# Recent alerts
alerts = client.alerts(level="critical", limit=20)

# Incident archive
incidents = client.incidents()
jelly = client.incident("jelly-2025")

# Verified deployers
verified = client.verified_deployers()

# System health
print(client.healthz())
```

## Authenticated tier

```python
client = HIP3Radar(api_key="hr_pro_...")
```

See [hip3radar.xyz/api-key](https://hip3radar.xyz/api-key) for tiers and pricing.

## Letter grade utility

```python
from hip3radar import safety_grade

g = safety_grade(risk_score=12.4)
# {"rating": 87.6, "grade": "A"}
```

| Risk score | Rating | Grade |
|---|---|---|
| 0–9 | 91–100 | AA |
| 10–19 | 81–90 | A |
| 20–29 | 71–80 | B+ |
| 30–39 | 61–70 | B |
| 40–49 | 51–60 | C |
| 50–69 | 31–50 | D |
| 70–100 | 0–29 | F |

## Links

- [Live scoreboard](https://hip3radar.xyz/hip3radar/)
- [API docs](https://hip3radar.xyz/docs)
- [OpenAPI spec](https://hip3radar.xyz/openapi.json)
- [Changelog](https://hip3radar.xyz/changelog)
- [Status](https://hip3radar.xyz/status)

MIT licensed.
