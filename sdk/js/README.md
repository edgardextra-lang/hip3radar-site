# hip3radar — JavaScript SDK

Real-time risk surveillance for every Hyperliquid native + HIP-3 perpetual market.

```bash
npm install hip3radar
```

## Usage

```js
import { HIP3Radar, safetyGrade } from "hip3radar";

const client = new HIP3Radar();  // free public tier — no key

// Top 25 highest-risk markets right now
const state = await client.state();
for (const m of state.top_risk) {
  const g = safetyGrade(m.risk_score);
  console.log(`${m.name.padEnd(25)} ${g.grade.padStart(3)} (${g.rating}/100)`);
}

// Full snapshot
const snap = await client.allMarkets();
console.log(`${snap.market_count} markets across ${snap.dex_count} dexes`);

// One dex
const xyz = await client.dex("xyz");

// One market
const btc = await client.market("hl", "BTC");

// 24h history
const hist = await client.history("hl", "BTC", 24);

// Recent alerts
const alerts = await client.alerts({ level: "critical", limit: 20 });

// Incident archive
const jelly = await client.incident("jelly-2025");

// Verified deployers
const verified = await client.verifiedDeployers();
```

## Authenticated tier

```js
const client = new HIP3Radar({ apiKey: "hr_pro_..." });
```

See [hip3radar.xyz/api-key](https://hip3radar.xyz/api-key) for tiers and pricing.

## Letter grade utility

```js
safetyGrade(12.4);  // { rating: 87.6, grade: "A" }
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

## Browser-side embed

```html
<script type="module">
  import { HIP3Radar, safetyGrade } from "https://hip3radar.xyz/sdk/js/hip3radar.js";
  const client = new HIP3Radar();
  const state = await client.state();
  document.body.textContent = `Top risk: ${state.top_risk[0].name}`;
</script>
```

## Links

- [Live scoreboard](https://hip3radar.xyz/hip3radar/)
- [API docs](https://hip3radar.xyz/docs)
- [OpenAPI spec](https://hip3radar.xyz/openapi.json)
- [Changelog](https://hip3radar.xyz/changelog)
- [Status](https://hip3radar.xyz/status)

MIT licensed.
