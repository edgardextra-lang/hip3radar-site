# HIP3Radar — X.com Rebrand Kit

Everything needed to align your X presence with the new positioning.

---

## 1. Profile assets

### Banner (1500×500)
Regenerated file: `brand/hip3radar-banner-twitter.png`

Contents:
- Eyebrow: `● INDEPENDENT · NEUTRAL · PUBLIC`
- Wordmark: **HIP3Radar**
- Headline: *Every Hyperliquid perp, **graded**.*
- Subtitle: *324 markets · 9 perp dexes · scored every 60 seconds*
- URL: `hip3radar.xyz`
- Right side: JELLY risk curve chart with "WE BUILT THIS AFTER JELLY · $12M HLP LOSS · MARCH 2025"

Upload via X → Edit profile → Change header photo → select `hip3radar-banner-twitter.png`.

### Profile picture (400×400)
Use existing `brand/hip3radar-logo-400.png` — the pink radar dot on dark background. No change needed; it's on-brand with the new direction.

### Display name
`HIP3Radar` (no change — keep short, brand-first)

### @ handle
Keep whatever it currently is. Never change an established handle.

---

## 2. Bio (choose one)

X bio limit: **160 characters**. Three drafts, pick whichever fits your voice.

### Option A — scoreboard-first (149 chars)
```
Safety scores for every Hyperliquid perp. 324 markets · 9 dexes · graded every 60s. Free for traders · Verified for deployers · API for dashboards.
```

### Option B — pain-first (153 chars)
```
Don't trade a rugged perp. Independent safety score for every Hyperliquid market. 324 perps · 9 dexes · public · neutral · free. hip3radar.xyz
```

### Option C — founder-voice (142 chars)
```
Grading every perp on Hyperliquid so traders don't get rugged and deployers don't get slashed. 324 markets, 9 dexes, scored 24/7. Neutral · public · free.
```

**My recommendation: Option A.** It names all three audiences in one line. Option B is punchier but reads as adversarial to deployers (who we want to sell to).

### Location
Leave blank, or `Hyperliquid` as a wink.

### Website
`https://hip3radar.xyz`

### Birthday
Leave blank — irrelevant for a product account.

---

## 3. Pinned tweet

The tweet people see first on your profile. Should establish the product in 5 seconds and give a reason to click through.

### Primary option (280-char single tweet)

> Built after JELLY lost HLP $12M in 30 minutes.
>
> Now every perp on Hyperliquid gets a Safety Score 0–100, updated every 60 seconds.
>
> 324 markets · 9 dexes · independent · public · free
>
> Trader? Check before you ape.
> Deployer? Get verified.
> Dashboard? Embed the API.
>
> hip3radar.xyz

Character count: 278.

### Alternative — 3-tweet thread

**Thread 1/3:**
```
Every HIP-3 market has a deployer with $20M staked.

Every HIP-3 market can be the next JELLY.

No one was publishing a safety score for them.

So we built HIP3Radar →
```

**2/3:**
```
Every Hyperliquid perp now has a Safety Score 0–100, updated every 60 seconds on oracle integrity, manipulation exposure, and liquidity health.

324 markets · 9 dexes · neutral · public · free.

hip3radar.xyz
```

**3/3:**
```
Three ways to use it:

🔴 Trader — check the score before you click buy
🟢 Deployer — get Verified, display the badge on your app
🔷 Dashboard — drop in our API, add a Safety Score column to your UI

Built independent from Pyth, BlockSec, Chaos Labs.
No clients to protect. Every market graded.
```

Pick the single tweet for immediate clarity, or the thread for an engagement hook. Both work.

---

## 4. First 7 days of posts (the content that actually moves the needle)

All of these tweets should come from the HIP3Radar account, not your personal one. Publish roughly one per day. Most are auto-generatable from your existing data.

### Day 1 — announcement
```
HIP3Radar 2.0 is live.

Every Hyperliquid perp now gets a public Safety Score. Updated every 60 seconds. Free forever.

324 markets across 9 dexes. One number per market. Rate your next meme perp before you trade it.

→ hip3radar.xyz
```

### Day 2 — "scariest market right now"
Pick the real lowest-scoring market from your dashboard. Screenshot the score card. Caption:
```
The lowest-scoring Hyperliquid perp this hour:

[MARKET NAME] — [SCORE]/100

Oracle drift: [X%]  
OI / daily vol: [Y×]  
Funding percentile: [Z]  

This is the shape JELLY had. Trade accordingly.

→ hip3radar.xyz/[slug]
```

### Day 3 — deployer pitch (tag them)
```
@Ventuals @TradeXYZ @hyperbeat 

You now have public Safety Scores on HIP3Radar.

Want the Verified badge on your app?
Monthly audit + shareable URL + custom ops alerts.

4-step application: hip3radar.xyz/verify
```

### Day 4 — dashboard / API pitch (tag tool builders)
```
@Buildix @hyperdash_com @loris_tools

Add a Safety Score column to your dashboard in 5 minutes:

<img src="hip3radar.xyz/badge/SLUG.svg">

324 markets · live · free tier up to 10K req/day.

API docs: hip3radar.xyz/#api
```

### Day 5 — trader-facing educational thread
```
5 signs a Hyperliquid perp is about to get wrecked:

1. Oracle drift > 5% vs CEX median
2. OI / 24h volume > 10×
3. Funding rate p99 for multiple hours
4. Sudden OI spike on low volume
5. Deployer has no verification badge

All 5 are on HIP3Radar, live.
```

### Day 6 — social proof (when/if a score predicts an event)
```
24 hours ago, HIP3Radar scored [MARKET] a [SCORE].

Today, it [ROUND-TRIPPED 40% / GOT DELISTED / SAW A CASCADE].

Not magic. Just math + five public signals + nobody else watching.

Every HL perp graded: hip3radar.xyz
```

### Day 7 — "how it works" (pinnable thread)
Plain-language explainer of the five signals. Post as 6-tweet thread. High-value content for building authority with devs.

---

## 5. Ongoing cadence (weeks 2+)

**Daily automation (recommended):**
- Auto-tweet top-3 highest-risk markets every 12 hours (build from `/api/state` endpoint)
- Auto-tweet "market of the week" (most dramatic score move) every Monday

**Weekly manual:**
- 1 thread explaining a signal in depth
- 1 tweet replying to/commenting on a Hyperliquid ecosystem development (not self-promotion)

**Monthly:**
- A "state of HIP-3 markets" thread with aggregate stats — which dexes are healthiest, which deployers have improved scores, etc.

---

## 6. What NOT to do

- **Don't hashtag-spam.** `#Crypto #Hyperliquid #HIP3` adds nothing and looks retail.
- **Don't reply to every Hyperliquid mention with "check your Safety Score!"** — you'll get muted.
- **Don't post inspiration porn or motivational quotes.** B2B infra account, not a hustle guru.
- **Don't @-mention Hyperliquid Labs repeatedly asking for retweets.** Let them find you through quality content.
- **Never, ever, under any circumstance, let a deployer pay to change their score.** One leaked DM and the brand dies.

---

## 7. Action checklist

- [ ] Upload `brand/hip3radar-banner-twitter.png` as header
- [ ] Confirm `hip3radar-logo-400.png` is current profile picture
- [ ] Replace bio with Option A (or B/C)
- [ ] Set website to `hip3radar.xyz`
- [ ] Post Day 1 announcement tweet
- [ ] Pin the primary pinned tweet (or thread 1/3)
- [ ] Schedule Day 2-7 tweets in your tool of choice (Typefully, X's native scheduler, or post manually)
- [ ] After Day 3: start monitoring replies/DMs from tagged deployers and tool builders — those are your first real customer conversations
