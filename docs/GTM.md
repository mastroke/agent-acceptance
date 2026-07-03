# GTM — Traction + Sales Velocity

`agent-acceptance` combines two shipped OSS eval tools into one paid sign-off artifact. The goal the user set: **a lot of traction, sell with velocity.** This is the concrete plan to produce the numbers that get an accelerator to say yes (see [ACCELERATORS.md](ACCELERATORS.md)).

## The unit economics

- **Wedge ICP:** AI agencies shipping $10–30k agentic builds (already `agent-handoff`'s ICP). ~hundreds in the UK/EU/US. They lose deals at handoff because buyers won't sign without proof. We hand them the proof artifact → they close faster → they pay.
- **Second ICP (upmarket):** Agentic AI vendors selling into regulated buyers (credit/insurance/triage — the scout's thesis-20260629 ICP). EU AI Act Art. 25 makes them jointly liable; a signed governance pack is the bilateral Art. 26(5) attachment. WTP $15–110K/system/yr (scout dossier).
- **Pricing (land + expand):**
  - **Free:** OSS CLI (`pip install`), full behavioral gate, public report. Top-of-funnel + GitHub stars.
  - **$49 once:** Agency Pack — procurement-ready report templates, client-onboarding/SOW snippets, example scenarios, "how to run acceptance" runbook (already drafted in `agent-handoff/pack/procurement/`). **List on Gumroad today.**
  - **$490/mo:** Governed Eval add-on — GateMem-aligned MGS scoring, the EU AI Act acceptance pack template, priority scenarios. For agencies doing regulated work.
  - **Design-partner (enterprise):** $5–15k pilot — custom golden scenarios for their stack + a signed acceptance report their buyer accepts. The path to $1M ARR.

## Traction flywheel (the thing accelerators fund)

The bar: **$1K MRR + 5–10% WoW growth for 6 weeks.** Every step below moves one of those numbers.

### Week 1 — ship the landing + list the pack (velocity = speed from launch to revenue)

- [ ] List the **$49 Agency Pack on Gumroad** (`mastroke.gumroad.com/l/agency-handoff-pack`) — the zip script + listing copy already exist in `agent-handoff/pack/procurement/` and `ops/gumroad-listing.md`. This is the single highest-leverage 15-min task; it's been parked at "$0 until you do #5". **Do it today.**
- [ ] Add a buy link + "star on GitHub" CTA to the `agent-acceptance` and `agent-handoff` READMEs.
- [ ] Set up a **traction counter** (a simple `trajectories`/CSV log): week, GitHub stars, Gumroad sales, MRR, waitlist signups. The engineer's `masoob_contributions.csv` already logs Growth rows; add a `docs/TRACTION.md` updated weekly.

### Week 1–2 — top-of-funnel (free OSS → stars → agency awareness)

- [ ] Post a **"how AI agencies prove an agent is safe to hand off"** writeup to: r/SaaS, r/AI_Agents, Indie Hackers, HN (Show HN: "agent-acceptance — one acceptance report for agentic AI"). Lead with the artifact (a sample `acceptance.md`), not the architecture.
- [ ] Cross-link the three repos (`agent-acceptance` ↔ `agent-handoff` ↔ `verified-memory-gate`) so a star on one funnels to the others.
- [ ] Add a 30-second asciinema/GIF of `agent-acceptance run` producing the report. READMEs with a visible run convert 3–5×.

### Week 2–4 — outbound to the wedge (sales velocity = agencies close faster with this)

- [ ] Build a list of **20 AI agencies** (LinkedIn / Clutch / agencies building LangChain/agent builds). Outbound each with: their client's handoff problem → a sample acceptance report → free pack if they run it on one build and send feedback. **Ask for the feedback, not the sale** — feedback is the trojan horse for a paid pack + design partner.
- [ ] Target outcome: 3 agencies running it on a real build → 1 paid pack + 1 design-partner conversation.
- [ ] Each agency that uses it = a measurable "weekly active" + a logo. Logos are the traction that compounds.

### Week 4–6 — convert to MRR + the growth curve

- [ ] From the 3 agency pilots, close **≥1 design-partner pilot ($5–15k)** and **≥10 $49 packs** → clears $1K MRR.
- [ ] Now the metric exists: *"Launched 6 weeks ago, 10 agencies use it, $X MRR growing W% WoW."* → **apply to Seedcamp (rolling) + EF (by 4 Aug)** with the traction-first one-pager from ACCELERATORS.md.

## Sales-velocity tactics (why buyers say yes fast)

1. **Sell the artifact, not the tool.** The deliverable a buyer signs is `acceptance.md`. Demo ends with that file in their hands. Agencies that hand over a signed acceptance report close; agencies that hand over a demo don't.
2. **Free OSS removes procurement friction.** The agency's engineer can run it today without a credit card. The paid pack is an *upgrade*, not a gate.
3. **Anchor on the regulation.** EU AI Act Art. 25 + PLD Dec-2026 = the buyer *has* to have this. We're not creating demand, we're the compliance artifact they're already being asked for.
4. **One number, repeated.** MGS = U·(1−A)·(1−F). One governance score buyers can compare across vendors. Simpler than observability = faster yes.

## What NOT to do (slop-avoidance, per the reward fix)

- **Don't claim results we haven't generated.** The `claims_backed` reward gate now penalizes README results tables with no backing artifact. Until the GateMem baselines actually run (t2–t5 on `verified-memory-gate`), the README must say "behavioral-only / memory not assessed" honestly, not advertise an MGS we haven't computed.
- **Don't build breadth before the wedge closes.** One ICP (agencies), one artifact (acceptance.md), one price ($49 then $490). The platform play comes after design-partner revenue, not before.
- **Don't apply to accelerators pre-traction.** The 55% that get ignored are pre-numbers. Use the weeks to make the number, then lead with it.

## Weekly tracking row (update every Friday)

```
week | github_stars_agent-acceptance | gumroad_packs_sold | mrr_usd | waitlist | design_partners | wow_growth
```

This row IS the application material. The first week it shows ≥$1K MRR + positive WoW, we apply to Seedcamp the same day.
