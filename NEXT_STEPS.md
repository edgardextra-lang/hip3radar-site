# HIP3Radar — Next Steps Playbook

**Positioning:** The independent Safety Score for every Hyperliquid perp. Trustpilot for HIP-3 markets + wholesale data API for every HL dashboard.

**Revenue model (three lines):**
1. **Consumer (free)** — public scoreboard. Drives traffic, builds authority. Never monetized directly.
2. **Deployer-side** — Verified Badge ($299/mo) + Verified Pro ($899/mo). Deployers pay for trust signals + private control.
3. **API-side** — API Starter $99 / API Pro $499 / API Enterprise $2K+/mo. Dashboards and bots pay for production-rate data access.

---

## Week 1 — Ship and measure

### Day 1–2: Landing page refresh
- [x] Copy rewritten to dual-audience ("Every HL perp, graded")
- [x] Pricing expanded to 6 tiers across 2 audiences
- [ ] **Manual check:** load `index.html` locally, click every CTA, verify the Supabase waitlist still writes with new plan labels (`verified`, `api_pro`, etc.)
- [ ] Run Lighthouse on the live site — confirm no regressions in mobile score

### Day 2–3: Build the SEO backbone (the thing nobody else has)
For EVERY tracked market, a public URL: `hip3radar.xyz/market/<dex>/<symbol>`.

Each page MUST include:
- Live Safety Score (big number, 0–100, color-coded)
- 30-day score history chart
- Signal breakdown (oracle drift, OI velocity, funding, spread)
- Deployer context (which deployer runs this market, link to deployer page)
- "Last incident" and flag history
- Shareable OG image for Twitter previews
- `<meta name="description">` targeting "is [symbol] safe on hyperliquid"

**Why:** Every time someone Googles a new HIP-3 market to see if it's safe, you want to be the first result. This is the SEO moat nothing else has.

### Day 3: Build the badge endpoint
`https://hip3radar.xyz/badge/<dex>/<symbol>.svg` returns a live-colored SVG showing the Safety Score. Deployers paste one `<img>` tag. Done.

**Free variant:** auto-cached, 15-min stale allowed.
**Verified variant:** real-time, customizable color theme, links back to deployer profile.

### Day 4–5: Instrument everything
- Umami event tracking on every pricing CTA (already partial)
- Add `waitlist-submit` events with `plan` dimension — know which tier converts
- Add `badge-view` event on the per-market pages — know which markets attract interest

---

## Week 2 — Outreach (the real revenue comes from this)

### Primary target: 5 tool builders for the API deal
These are the people who will pay $499/mo without flinching because it makes their product better.

| Target | Contact approach | Pitch angle |
|---|---|---|
| **Buildix** (buildix.trade) | Twitter DM + email via contact form | "Your users search for orderflow. Add 'is this market safe' and you become the full answer." |
| **Hyperdash** (hyperdash.com) / pvp.trade | Twitter (they're active), DM founder | "You're the execution UX. We're the risk UX. One column in your terminal." |
| **Loris.tools** | Email via site | "You cover funding. We cover oracle integrity. Your HIP-3 page is missing safety scores." |
| **ASXN** (data.asxn.xyz) | Twitter + warm intro if possible | "Official-feel dashboard should have official-feel safety scores. Free pilot to prove volume." |
| **Coinalyze** | Business email on footer | "CEX traders now dabbling in HL — they want the safety cue they get from TradingView asset badges." |

**Email template (use literally, swap brackets):**

> **Subject:** Adding a "Safety Score" column to [Buildix]?
>
> Hey [first name],
>
> I run HIP3Radar — we score every Hyperliquid perp (324 markets across 9 dexes) on oracle integrity, manipulation exposure, and liquidity health. All public at hip3radar.xyz.
>
> Watching your coverage, I think a "Safety Score" column would be a genuine differentiator — none of the other HL dashboards have it, and after JELLY, traders care. It's one API call per market.
>
> Here's a live example badge: `<img src="https://hip3radar.xyz/badge/vntl/ANTHROPIC.svg">` renders as [screenshot].
>
> API Pro is $499/mo, 100K requests/day, real-time webhook for score changes. Happy to set up a free 30-day trial so you can A/B test whether users actually engage with it.
>
> Free call this week? 20 min, I'll show you exactly where to plug it in.
>
> — Edgard
> HIP3Radar · edgard.extra@gmail.com

**Hit-rate expectation:** 5 sends → 2-3 replies → 1 paying customer in 2 weeks. That's $499/mo, one customer. Stack 3-5 of them and API-side is $1,500–2,500/mo alone.

### Secondary target: 10 deployers for the Verified Badge

The HIP-3 deployer list isn't public, but these are known from research. Start with names you can find on Twitter/Discord:

1. **Trade.xyz (Hyperunit)** — equity perps, biggest HIP-3 deployer
2. **Ventuals** — pre-IPO perps (Anthropic, OpenAI, SpaceX, etc.)
3. **Aura** — US Treasuries perps
4. **Kinetiq Research** — Launch protocol
5. **ChainSight** — variance perpetuals
6. **Hyperbeat** — VLP vault for Ventuals
7. **Pyth's own HIP-3 markets** (if any) — probably won't buy but good for benchmarking
8. **XChange** if they exist
9. **Any deployer running a meme-coin-style market** — these need the badge most (the "is this a trap?" question is loudest here)
10. **Any deployer scoring poorly** on your public scoreboard right now — they NEED to show they're improving

**Email template for deployers:**

> **Subject:** Your markets are already graded. Want the badge?
>
> Hey [team name],
>
> HIP3Radar publishes an independent Safety Score for every Hyperliquid perp market, including [their market name(s)]. Your current score: **[X/100]** (live at hip3radar.xyz/market/[their slug]).
>
> Traders check scores before they touch new HIP-3 markets. If you get Verified, you can display the HIP3Radar badge on your app — same idea as "Certified Secure" on a login page. Score changes notify your team via Telegram/Slack before they go public, so you have a heads-up to respond.
>
> $299/mo, includes a monthly audit report PDF and a shareable verification URL for marketing.
>
> Worth a 15-min call? Happy to walk through what the score captures for [their market] specifically.
>
> — Edgard
> HIP3Radar

**Hit-rate expectation:** 10 sends → 3-4 replies → 1-2 deployers signed up in 3 weeks. $299-600/mo deployer revenue within a month.

### Tertiary: Twitter visibility loop

1. **Weekly "lowest-scoring market of the week" thread** — autogenerated, high-engagement ("look at this sketchy HIP-3 market" gets retweets).
2. **Alert posts when a market's score drops significantly** — free content, viral hook.
3. **Monthly "safest deployers" leaderboard** — gives deployers reason to promote you.
4. **Thread every time there's an incident** — be the first source of analysis.

Goal: 500 followers in 30 days. Every follower is a potential deployer intro.

---

## Month 2 — Product deepening

Once 2-3 paying customers exist on each side, expand:

### Deployer side
- **Verified Pro tier usage**: custom thresholds, PagerDuty integration
- **White-label Safety Score widget** for deployers to embed on their own docs
- **Deployer CRM**: track which deployers are on which tier, upsell from Verified → Verified Pro
- **Audit trail export** — this is the compliance angle that wins enterprise upgrades later

### API side
- **Usage dashboard** for API customers — helps them see value, justifies upgrades
- **SDK packages** (TypeScript, Python) so integration is 30 seconds not 30 minutes
- **Webhook delivery** upgraded to support score-change streams (WebSocket)
- **Co-marketing**: "Powered by HIP3Radar" credit in exchange for logo placement on your homepage

### Consumer side (indirect revenue)
- **Personalized alerts** ($29/mo tier IF demand shows up — don't build preemptively)
- **Watchlists + portfolio integration** — wait for user demand
- **Chrome extension** that overlays scores on Hyperliquid.xyz / pvp.trade frontends

---

## What could kill this

### Risk 1: Pyth launches a public scoreboard of their own
**Probability:** medium. They have the data and the incentive.
**Defense:** ship faster. Own the brand ("HIP3Radar" is the neutral name) before they try. Pyth is perceived as an oracle vendor — you're perceived as an independent auditor. That brand distinction is hard for them to replicate.

### Risk 2: Deployers view the public score as hostile / refuse to engage
**Probability:** medium-high. Low-scoring deployers will not like this.
**Mitigation:** offer a "grace window" where newly-deployed markets aren't scored for 7 days. Offer a feedback form so deployers can correct data before a bad score goes public. Frame Verified Badge as "right of reply" not "paying for a good score."

**Explicitly DO NOT** let deployers pay to change their score. The moment you do, you lose the independence that is the whole product.

### Risk 3: Tool builders build it themselves
**Probability:** low in short term. The infrastructure (325 markets × 9 DEXes × 60s polling) is non-trivial.
**Defense:** focus on wholesale pricing that's cheaper than they could build. Add signals they can't easily replicate (cross-CEX oracle consensus, which requires CEX API access at scale).

### Risk 4: HL Foundation launches an official "HL Verified" program
**Probability:** low-medium. HL Foundation has not shown inclination to centralize this.
**Defense:** apply for an HL Foundation grant or partnership. Becoming "the" neutral scoreboard under a grant is a bigger win than competing against one.

---

## 30-day revenue projection (honest)

| Source | Optimistic | Realistic | Pessimistic |
|---|---|---|---|
| API Pro customers | 3 × $499 = $1,497 | 1 × $499 = $499 | 0 |
| Verified deployers | 3 × $299 = $897 | 1 × $299 = $299 | 0 |
| API Starter | 5 × $99 = $495 | 2 × $99 = $198 | 0 |
| **MRR total** | **$2,889** | **$996** | **$0** |

Break-even vs infra cost: ~$200/mo (VPS + HL RPC). Realistic month-1 leaves $800/mo contribution. Most of the value isn't dollar-today, it's **owning the category before Pyth notices**.

---

## If nothing works in 60 days

Call it. The infrastructure is valuable even if the business model isn't. Options:
- Open source the scoring engine, become the *reference* that tools implement against — monetize via consulting / speaking.
- Fold into another HL tool as acqui-hire or technology license.
- Pivot again — use the same infrastructure for a different product (e.g., HIP-3 market launch consultancy, where "HIP3Radar Safety Score" is a service baked into launching a new market).

The technology has optionality. The business thesis is what gets tested.

---

## Your concrete next action (this afternoon)

1. Open `index.html` in a browser, click through every CTA, screenshot anything broken or off-brand.
2. Send the 5 tool-builder cold emails above (literally copy-paste, change one name each).
3. Tweet once: "Every Hyperliquid perp now has an independent Safety Score. 324 markets. 9 dexes. Free. → hip3radar.xyz"
4. Post the same in /r/Hyperliquid and any HL Discord you're in.
5. Come back tomorrow and measure what the cold outreach produced.

The tech is done. This is a distribution problem from here.
