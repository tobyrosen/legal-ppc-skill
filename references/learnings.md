# Learnings — Validated Patterns from Session History

This file accumulates diagnostic patterns that have been observed in real sessions and validated as worth encoding. It supplements the knowledge base and diagnosis trees with empirically-observed, account-tested patterns.

**How entries get here:** After a synthesis session reviews accumulated session logs, patterns that appear in 2+ sessions and aren't already in the diagnosis trees are proposed here. Toby reviews and approves before anything is added.

**How this file is used:** Read at session start (Toby version) after the knowledge base and before beginning analysis. Treat entries as additional priors — things worth checking that experience has shown to be common, even if not in the main trees.

**Format:** Each entry should include: the pattern observed, which accounts it appeared in, the session log dates it came from, and what it implies for diagnosis.

---

---

## Provisional Entries (1 session — confirm against second account)

These patterns were observed in the 2026-03-28 Client A session. They are strong enough to record but have not yet appeared in a second account. Mark as confirmed once observed in a second session.

---

### P1 — search_term_view Coverage Is an API Ceiling, Not a Privacy Threshold

**Source:** 2026-03-28-Client A | **Status:** Provisional (1 session)

**Pattern:** `search_term_view` consistently returns ~50% of actual campaign spend. This is not Google's privacy threshold — it is a hard row cap imposed at the API level. It is not improvable through query granularity (per-campaign, per-ad-group splits), because GAQL has no OFFSET and the cap operates at the query result level.

**Implications for diagnosis:**

- Always pull actual campaign spend from `FROM campaign` before presenting search term findings
- State the coverage ratio explicitly before any waste estimates
- Scale waste estimates by coverage ratio (visible waste ÷ coverage pct)
- Per-campaign splitting is still required (all-campaigns query hits a 500-row display cap much sooner), but expect convergence at ~50% regardless

---

### P2 — "Legal Aid" Consolidation Pattern

**Source:** 2026-03-28-Client A | **Status:** Provisional (1 session)

**Pattern:** Accounts often accumulate hundreds of specific reactive exact-match negative strings (e.g., "legal aid clinic statesville nc", "legal aid divorce nc", "legal aid family law") instead of a single phrase-match categorical that covers all variants.

**Observed case:** Client A had 535 specific "legal aid [variant]" strings in campaign-level negatives. Zero phrase-match `"legal aid"` at account level. Adding one phrase match term makes all 535 strings redundant and catches future variants.

**Implication:** When reviewing negative keyword structure, count how many strings share a common 2-3 word root. If a root appears 20+ times, a phrase match categorical at account level is almost always higher leverage than maintaining the reactive list.

---

### P3 — DDA Decimal Fingerprint for Duplicate Conversion Detection

**Source:** 2026-03-28-Client A | **Status:** Provisional (1 session)

**Pattern:** When Data-Driven Attribution (DDA) distributes conversion credit across touchpoints, the fractional values assigned to a given conversion ID are deterministic — the same event always produces the same fractional tails. If two conversion actions report identical fractional tails (e.g., both show 6.272...), they are almost certainly tracking the same underlying event through different attribution paths (e.g., GA4 form view + HubSpot form submission capturing the same user form fill).

**How to detect:** Pull GAQL 2.2 (conversion volume by action). If two actions consistently show matching non-integer conversion counts with identical decimal components across multiple reporting windows, treat this as confirmation of duplicate tracking.

**Implication:** This is one of the most reliable ways to detect same-event double-counting without needing to audit the tracking implementation directly. Flag immediately — inflated conversion counts degrade smart bidding signal and make CPA appear artificially lower than reality.

---

### P4 — Long Consideration Window Markets (NC Separation Period Example)

**Source:** 2026-03-28-Client A | **Status:** Provisional (1 account — NC family law specific, but framework generalizes)

**Pattern:** Some legal markets have structurally long consideration windows where informational/research queries represent real prospects at an earlier stage of the funnel, not irrelevant traffic.

**NC-specific case:** North Carolina has a mandatory 1-year separation period before divorce can be filed. This creates a 12-month window where prospects research extensively, consult multiple attorneys, and may switch representation mid-separation. Informational queries ("how long does divorce take in NC", "do I need a lawyer for legal separation") represent real prospective clients at earlier funnel stages. Blocking them cuts off top-of-funnel traffic that converts over weeks or months.

**General framework for market exceptions:**
Before applying Section 4 (informational intent) negatives from the negative keyword library, ask:

1. Does this market have a structural event that prolongs the consideration window?
2. Do informational queries from this area actually convert in account data, even at lower rates?
3. Are competitors running on informational terms and converting them?

If yes to any: hold on blocking informational intent; analyze actual search term data first.

**Implication for Section 4 of negative keyword library:** The library's caveat ("consider whether your account has budget and landing pages to nurture this traffic") is understated for markets like NC family law. It should be a near-default exception rather than an optional consideration.

---

### P5 — Competitor Name Searches May Be Intentional Targets (NC Example)

**Source:** 2026-03-28-Client A | **Status:** Provisional (1 session)

**Pattern:** In long consideration window markets, prospects research multiple providers over an extended period. Competitor name searches — even for direct competing attorneys — may represent prospects who consulted that competitor earlier in their funnel and are now considering alternatives.

**Observed case:** Competitor names (baity, joe delk, carmen brown — other NC family law attorneys) were converting in Client A's account. Consistent with the NC separation period: prospects consulting multiple attorneys over a year.

**Implication:** In high-competitor-density, long-consideration markets, competitor keywords may be worth intentionally targeting rather than neutrally ignoring. Evaluate whether competitor terms are converting before recommending them as negatives. This is the opposite of the typical legal PPC default (avoid competitor terms to stay clean).

---

---

## Confirmed Entries (2+ sessions)

---

### P6 — Both ad_group_criterion and keyword_view Return Positive and Negative Keywords

**Source:** 2026-04-01-Client A, 2026-04-19-Client A, 2026-04-27-Client Cjenkins | **Status:** Confirmed (3 sessions, multiple accounts)

**Pattern:** GAQL queries against `ad_group_criterion` AND `keyword_view` both return positive and negative keywords in the same result set. If the `negative` field is not filtered, the two types are indistinguishable from the response. This caused confirmed misdiagnosis in multiple sessions — negative keywords were flagged as active BROAD match problems or active targeting issues.

**Observed cases:**

- `cheap` (BROAD) in a Client A Child Custody ad group — flagged as a positive keyword needing conversion. It was an ad-group-level negative. (2 sessions)
- `5 signs`, `elder`, `dallas`, `pro bono` in a Client C LA+ campaign — flagged as active junk positive keywords. All were ad group-level negatives. Caught via `ad_group_criterion` direct query after the `keyword_view` query returned them without the filter.

**Secondary:** `ad_group.status` omission caused a keyword in Client A Brand's PAUSED "Male Divorce Lawyer" ad group to be flagged as an active BROAD match issue. It was not serving.

**Implication:** Before flagging ANY keyword from ANY resource as an active positive issue, verify `negative = False` AND `ad_group.status = ENABLED`. This applies to both `ad_group_criterion` AND `keyword_view` queries. The negative filter is now required in all library queries using either resource. If a query result is missing the `negative` column, the query is incomplete — do not proceed with analysis.

---

### P8 — search_term_view Returns Historical Data Without status = NONE Filter

**Source:** 2026-04-20-Client D, 2026-04-27-Client B | **Status:** Confirmed (2 sessions, 2 accounts)

**Pattern:** `search_term_view` has two distinct mechanisms that produce false active findings:

1. **Paused ad group data:** Queries return historical records from ALL ad groups — including PAUSED and REMOVED ones — unless `ad_group.status = 'ENABLED'` is in the WHERE clause. Caused confirmed misdiagnosis in Client D: terms from PAUSED SKAG - Probate - Broad ("estate planning attorney near me" at $0.20/click) presented as active waste.

2. **Expired keyword matches (status = NONE):** Even with `ad_group.status = 'ENABLED'`, a term can appear with `search_term_view.status = NONE`, meaning it matched historically via a now-paused or tightened keyword (e.g., a BROAD that was converted to phrase match) and is no longer actively served. Caused confirmed misdiagnosis in Client B: "partition action nevada" (2 clicks, $23.46, 1 conv) flagged as active waste — it was status NONE, triggered by a BROAD keyword that had since been paused.

**Same root cause as P6:** The API returns all matching records for a given account/date range regardless of current serving status. Explicit field-level checks are the only defense.

**Implication:**

- Every `search_term_view` query must SELECT `search_term_view.status` — if the field is not in the result, the query is incomplete, do not proceed
- Every `search_term_view` query must include `AND ad_group.status = 'ENABLED'` in the WHERE clause
- Never flag a term with `status = NONE` as an active finding — it is not currently serving
- Before flagging any search term as an active waste source, confirm `status ≠ NONE`

---

### P7 — search_rank_lost_impression_share ≠ Budget Constraint

**Source:** 2026-04-19-Client B | **Status:** Provisional (1 session)

**Pattern:** `metrics.search_rank_lost_impression_share` measures impressions lost because Ad Rank was too low — a QS, bid, or landing page problem. It is not a budget signal. `metrics.search_budget_lost_impression_share` is the separate field that measures impressions lost to budget exhaustion. Conflating the two produces wrong recommendations: OC's 67% rank-lost IS was misread as "budget constrained" when it actually indicated a landing page / QS problem requiring creative and LP work, not more budget.

**Implication:** Always pull both fields when assessing IS. Label them accurately. "Rank lost" → QS/LP/bid quality fix. "Budget lost" → budget increase. Never recommend budget reallocation based on rank-lost IS alone.

---

### P9 — Thin-Signal + High-CPC Smart Bidding → Switch to Max Clicks With a CPC Cap

**Source:** 2026-06-11 + 2026-06-15 walkthroughs (elder abuse account, heaviest-spend campaign) | **Status:** Confirmed (2 sessions, same account; pattern generalizes)

**Pattern:** A campaign on Maximize Conversions whose conversion volume sits *below* the ~15–20/30d reliability floor AND that carries a high avg CPC bids blind and burns budget. Maximize Conversions has no usable signal to optimize against (lumpy, sub-floor weekly conversions), so every auction it wins at a high CPC is a near-random spend of budget. The classic instinct — adjust the target or wait for the algorithm to "learn" — does not apply, because there is nothing to learn from.

**Observed case:** Heaviest-spend campaign at 30-day = 57 clicks, 9 conv, ~$4,187 spend, **$73 avg CPC**, **$465 CPL**, with 25% of impressions lost to budget. 9 conv/30d is under the floor; weekly conv was 4/1/0/4 (lumpy). Switched from Maximize Conversions to **Maximize Clicks with a CPC cap** to rebuild click volume and cap runaway auction prices while a real conversion signal accumulates.

**Implications for diagnosis:**

- When a smart-bidding campaign shows sub-floor conversion volume AND a high avg CPC for the practice area, the play is Maximize Clicks + CPC cap — not a target tweak, not "let it learn." The cap stops single auctions from eating the daily budget; Max Clicks buys the volume needed to rebuild signal.
- This is the bridge between the "Smart Bidding — Post-Tracking-Fix Protocol" low-volume flag (which already says *consider switching to Maximize Conversions* when volume drops below the floor) and the **Campaign-Level CPC Anomaly** routing: when the campaign is BOTH below the floor AND running an anomalously high CPC, Maximize Conversions is not the safe harbor — Max Clicks + cap is.
- Trade-off to flag every time: Max Clicks optimizes for clicks, not conversions. Set a revisit window (3–4 weeks) and watch CVR — if click volume comes back but conversion rate craters, the cleaner volume has done its job and it's time to move back toward a conversion-based strategy.

---

### P10 — A Term That Has Converted Is Never Auto-Negated, However "Wrong" It Looks

**Source:** 2026-06-15 walkthrough (nonprofit-referral term kept) | **Status:** Confirmed (generalizes; reinforces existing search-term integrity rules)

**Pattern:** A search term can *look* like obvious waste — a nonprofit/referral name, an apparent geo mismatch, an off-practice-area string — and still be a real source of converted business. Pattern-matching a term to a "negate" category on appearance alone, without pulling its conversion data, throws away converting traffic.

**Observed case:** A nonprofit-referral term that read as a clean negative ("referral mismatch") had in fact drawn spend AND a conversion in a sibling campaign. Standing decision: **KEEP — do not negative, do not re-flag in future checks.** The earlier "looks like a referral mismatch" flag was wrong because it was made on the term's shape, not its conversion record.

**Implication:** Before excluding ANY term — including ones that match a negative-library category by appearance — check whether it has converted. A converting term is not waste, full stop. This is the positive-intent complement to the existing search-term integrity rules (P6/P8): those stop you flagging *non-serving* history as active; this one stops you negating *actively-converting* traffic because it pattern-matches a junk category. When a prior session has already ruled "keep" on a converting term, that ruling stands — do not re-litigate it each check.

---

### P11 — Geo-Mismatch Negation: Negate the Geo Token, Never the Core Service Term

**Source:** 2026-06-15 walkthrough (geo-mismatched query containing the core service term) | **Status:** Confirmed (generalizes)

**Pattern:** When a query is geo-mismatched (a location the account does not serve) but *also contains the firm's core service term*, a naive negative on the whole phrase — or worse, on the service words — would block exactly the traffic the firm wants. The fix is surgical: negate the GEO token only.

**Observed case:** A query combined the firm's core service ("[core service term]") with a non-target city ("[city]"). Resolution: add the **city** as the negative, **keep** the core service term serving. Negating the service term would have suppressed the firm's primary intent across every other geo.

**Implication:** On any geo-mismatched query, decompose it before negating. Identify the geo token vs. the service token. Negate the geo; never the service. A phrase-level or service-token negative is collateral damage — it removes good traffic to solve a location problem. This is a precision rule that sits under the negative-keyword decision tree: match-the-negative-to-the-actual-problem, not to the whole offending phrase.

---

### P12 — A "Structural" CPA Ceiling Can Lift From Creative Alone — Re-Pull Before Assuming It Still Binds

**Source:** 2026-06-15 walkthrough (standing CPA-gap item resolved by ad refresh) | **Status:** Confirmed (generalizes; reinforces "Account Notes vs. Live Data")

**Pattern:** A long-standing high-CPA item gets blamed on a landing-page or structural limit and parked as "can't fix without the LP / out of scope." That standing flag then persists across sessions as accepted fact. But a creative-level change (ad refresh + near-me / intent-matched headlines) can close the gap on its own — and if nobody re-pulls, the account keeps carrying a *stale* structural flag that no longer reflects reality.

**Observed case:** An ad group ran a standing ~$125 CPA gap vs. its sibling (problem AG ~$157 CPA vs. sibling ~$32), long attributed to a landing-page-quality ceiling controlled by a third party (out of scope). After an ad refresh + near-me headlines, the freshest window showed the gap fully closed (~$100 CPA vs. ~$89 sibling) with **no LP change**. The "structural LP ceiling" thesis had eased; the standing flag was stale.

**Implication:** A "structural" / "out-of-scope" / "LP-gated" CPA flag is a hypothesis with a shelf life, not a permanent fact. Before re-asserting it in a new session, re-pull live data — the gap may already have closed via creative. This is a direct application of **Account Notes vs. Live Data**: the note records *prior* state; the current CPA must come from a live query. Do not let a standing structural flag persist unverified, and explicitly retire it when the data shows it no longer binds. (Corollary: when low conversion volume makes the sibling's CPA unreliable, treat the comparison as directional — see the 15–20 conv reliability threshold.)

---

### P13 — Judge a Volume-Driving Ad Group on Marginal Contribution, Not CPA-vs-Sibling

**Source:** 2026-06-15 walkthrough (expansion ad group KEEP decision) | **Status:** Confirmed (generalizes)

**Pattern:** An expansion / test ad group that runs at a small CPA premium over its incumbents but drives a large share of the campaign's conversions is a KEEP, not a kill. Killing it to "save" the per-conversion premium loses the volume it generates — trading real conversions for pennies of CPA efficiency. The premium is the cost of the marginal volume, and that volume is usually worth more than the spread.

**Observed case:** An expansion ad group running ~$10–20/conv above the two incumbents was the **#1 conversion driver — ~50% of the campaign's ad-group conversions** (~23 conv, ~$110 CPA since launch). Its weekly trend climbed hard (0 → 4 → 12). Early dead weeks (0-conv launch period) had dragged its blended since-launch CPA upward, making the standing average look worse than the current marginal performance. Decision: **KEEP + monitor**; revisit only if its weekly CPA detaches upward from the incumbents for 2–3 consecutive weeks.

**Implications for diagnosis:**

- Evaluate a volume-driving ad group on its **marginal contribution** (how much volume it adds, at what marginal CPA) — not on a static CPA-vs-sibling comparison. A KEEP at a small premium that supplies half the conversions beats a "clean" account that lost that volume.
- **Weight the trend, and discount early dead weeks.** A test's blended since-launch CPA is dragged by its zero-conversion launch period; the relevant signal is the recent weekly trajectory, not the launch-inclusive average. A climbing weekly trend on a still-young ad group argues KEEP even when the lifetime average looks middling.
- Set an explicit kill condition rather than killing on the spot: e.g., "revisit only if weekly CPA detaches upward from incumbents for 2–3 consecutive weeks." This protects volume while keeping a real off-ramp.

---

*Next synthesis session: after 4–8 total sessions. At that point, review all session logs, confirm which provisional entries appear cross-account, and remove the provisional marker.*
