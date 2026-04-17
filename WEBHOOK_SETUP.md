# Supabase → Email Alert Setup

**Status:** Flask endpoint **deployed and tested**. Only the Supabase-side configuration below is pending.

When a new verification application is submitted via `verify.html`, Supabase will POST to our Flask webhook, which sends a formatted email to `hello@hip3radar.xyz` with all application details.

---

## 1. Add the Supabase Database Webhook (one-time setup)

### Steps in the Supabase dashboard:

1. Log in to https://supabase.com/dashboard/project/rrowmfxcfeegtazmkvtf
2. Go to **Database → Webhooks** (left sidebar, under Database)
3. Click **Create a new hook**
4. Fill in the form:

| Field | Value |
|---|---|
| **Name** | `verification_application_alert` |
| **Table** | `hip3radar_waitlist` |
| **Events** | ☑ Insert  (uncheck Update + Delete) |
| **Type** | `HTTP Request` |
| **HTTP method** | `POST` |
| **URL** | `https://hip3radar.xyz/api/hooks/verification-application` |
| **HTTP Headers** | Add one header → name: `Authorization`, value: `Bearer 46e9f4cb7a62895a08cf564bfed580a2ec3c291ff59fb659` |
| **HTTP Parameters** | *(leave empty)* |
| **Timeout** | `5000 ms` (default 1000 is too tight for Resend) |

5. Click **Create webhook**.

---

## 2. Verify it works

### Smoke-test the endpoint directly

```bash
curl -X POST https://hip3radar.xyz/api/hooks/verification-application \
  -H "Authorization: Bearer 46e9f4cb7a62895a08cf564bfed580a2ec3c291ff59fb659" \
  -H "Content-Type: application/json" \
  -d '{
    "record": {
      "id": 999,
      "email": "you@your-email.com",
      "plan": "verification_application",
      "created_at": "2026-04-17T18:45:00Z",
      "metadata": {
        "deployer": "SMOKE TEST",
        "wallet": "0x1111111111111111111111111111111111111111",
        "markets": "test-market",
        "notes": "Verifying webhook end-to-end."
      }
    }
  }'
```

Expected response:
```json
{"deployer":"SMOKE TEST","notified":"hello@hip3radar.xyz","ok":true}
```

Check your `hello@hip3radar.xyz` inbox — the email arrives within ~2 seconds.

### End-to-end test with real form submission

1. Open https://hip3radar.xyz/verify.html in incognito
2. Fill the form (use a real test wallet address, any email you control)
3. Submit
4. You should get the alert email at `hello@hip3radar.xyz` within 10 seconds

---

## 3. The email you'll receive looks like

```
Subject: HIP3Radar · New verification application — <Deployer Name>
From:    HIP3Radar <hello@hip3radar.xyz>
Reply-To: <applicant's email>     ← hit reply to go straight to them
To:      hello@hip3radar.xyz

New HIP3Radar verification application received.

Deployer: Ventuals
Wallet:   0x7d3f0000000000000000000000000000000000a291
Email:    ops@ventuals.com
Markets:  vntl:ANTHROPIC, vntl:OPENAI, vntl:SPACEX
Notes:    Interested in onboarding before our SPACEX launch next week.

Submitted: 2026-04-17T18:45:00Z
Record ID: 12847

Review in Supabase:
https://supabase.com/dashboard/project/rrowmfxcfeegtazmkvtf/editor/

Reply to the applicant at ops@ventuals.com.

— hip3radar.xyz webhook
```

---

## 4. Security notes

- **Shared secret is in `.env` on the cloud server** — `/home/ubuntu/HyperBot/HIP3Radar/.env` line: `HIP3RADAR_WEBHOOK_SECRET=46e9f4...`
- **Also stored locally** at `/Users/eddy/Arbitrage/HyperBot/HIP3Radar-site/.webhook_secret` (chmod 600, gitignored)
- **Never commit the secret to git.** If it ever leaks:
  ```bash
  # 1. Generate a new one
  NEW=$(openssl rand -hex 24)
  # 2. Update the Supabase webhook's Authorization header in the dashboard
  # 3. Update the server's .env
  ssh ... 'sed -i "s/^HIP3RADAR_WEBHOOK_SECRET=.*/HIP3RADAR_WEBHOOK_SECRET=$NEW/" /home/ubuntu/HyperBot/HIP3Radar/.env'
  # 4. Restart the Flask app
  ssh ... 'pkill -f hip3radar_app.py; sleep 2; bash /home/ubuntu/HyperBot/HIP3Radar/start_app.sh'
  ```

---

## 5. What the endpoint does (behavior summary)

| Condition | Response |
|---|---|
| No `Authorization: Bearer <secret>` header (or wrong secret) | `401 Unauthorized` |
| `record.plan != "verification_application"` (e.g. regular waitlist) | `200 OK` with `{"skipped": "not a verification application"}` — no email sent |
| `record.plan == "verification_application"` with any `record` payload | `200 OK`, email dispatched to `hello@hip3radar.xyz` via Resend, `reply_to` set to the applicant |
| Resend API fails | `502 Bad Gateway` with error body — Supabase will retry per its retry policy |

The endpoint is **idempotent-tolerant** — if Supabase retries, you'll get duplicate emails (which is fine; you get a clear flag that something odd is happening).

---

## 6. Failover / polling fallback (optional, not yet set up)

If the webhook ever stops working (e.g. Cloudflare tunnel down), there's no automatic fallback yet. To add one, a `cron` job on the HyperBot server could query the Supabase REST API every hour for unread verification applications and email them. ~30 lines of Python. Build it only if the webhook proves unreliable over 30 days.

---

## Status summary

- [x] Flask endpoint deployed to `https://hip3radar.xyz/api/hooks/verification-application`
- [x] Webhook secret generated + stored in `.env`
- [x] Resend email template written and smoke-tested (email received)
- [x] Authentication working (401 on missing/wrong token)
- [x] Plan filter working (non-verification applications skipped)
- [ ] **You: create the Supabase webhook in the dashboard (steps in §1 above)**
- [ ] **You: submit a test through verify.html to confirm end-to-end**
