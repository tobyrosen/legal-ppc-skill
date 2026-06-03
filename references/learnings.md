# Learnings — Validated Patterns from Session History

This file accumulates diagnostic patterns that have been observed in real sessions and validated as worth encoding. It supplements the knowledge base and diagnosis trees with empirically-observed, account-tested patterns.

**How entries get here:** After a synthesis session reviews accumulated session logs, patterns that appear in 2+ sessions and aren't already in the diagnosis trees are proposed here. Toby reviews and approves before anything is added.

**How this file is used:** Read at session start (Toby version) after the knowledge base and before beginning analysis. Treat entries as additional priors — things worth checking that experience has shown to be common, even if not in the main trees.

**Format:** Each entry should include: the pattern observed, which accounts it appeared in, the session log dates it came from, and what it implies for diagnosis.

---

---

## Provisional Entries (1 session — confirm against second account)

These patterns were observed in the 2026-03-28 McCrary session. They are strong enough to record but have not yet appeared in a second account. Mark as confirmed once observed in a second session.

---

### P1 — search_term_view Coverage Is an API Ceiling, Not a Privacy Threshold

**Source:** 2026-03-28-mccrary | **Status:** Provisional (1 session)

**Pattern:** `search_term_view` consistently returns ~50% of actual campaign spend. This is not Google's privacy threshold — it is a hard row cap imposed at the API level. It is not improvable through query granularity (per-campaign, per-ad-group splits), because GAQL has no OFFSET and the cap operates at the query result level.

**Implications for diagnosis:**

- Always pull actual campaign spend from `FROM campaign` before presenting search term findings
- State the coverage ratio explicitly before any waste estimates
- Scale waste estimates by coverage ratio (visible waste ÷ coverage pct)
- Per-campaign splitting is still required (all-campaigns query hits a 500-row display cap much sooner), but expect convergence at ~50% regardless

---

### P2 — "Legal Aid" Consolidation Pattern

**Source:** 2026-03-28-mccrary | **Status:** Provisional (1 session)

**Pattern:** Accounts often accumulate hundreds of specific reactive exact-match negative strings (e.g., "legal aid clinic statesville nc", "legal aid divorce nc", "legal aid family law") instead of a single phrase-match categorical that covers all variants.

**Observed case:** McCrary had 535 specific "legal aid [variant]" strings in campaign-level negatives. Zero phrase-match `"legal aid"` at account level. Adding one phrase match term makes all 535 strings redundant and catches future variants.

**Implication:** When reviewing negative keyword structure, count how many strings share a common 2-3 word root. If a root appears 20+ times, a phrase match categorical at account level is almost always higher leverage than maintaining the reactive list.

---

### P3 — DDA Decimal Fingerprint for Duplicate Conversion Detection

**Source:** 2026-03-28-mccrary | **Status:** Provisional (1 session)

**Pattern:** When Data-Driven Attribution (DDA) distributes conversion credit across touchpoints, the fractional values assigned to a given conversion ID are deterministic — the same event always produces the same fractional tails. If two conversion actions report identical fractional tails (e.g., both show 6.272...), they are almost certainly tracking the same underlying event through different attribution paths (e.g., GA4 form view + HubSpot form submission capturing the same user form fill).

**How to detect:** Pull GAQL 2.2 (conversion volume by action). If two actions consistently show matching non-integer conversion counts with identical decimal components across multiple reporting windows, treat this as confirmation of duplicate tracking.

**Implication:** This is one of the most reliable ways to detect same-event double-counting without needing to audit the tracking implementation directly. Flag immediately — inflated conversion counts degrade smart bidding signal and make CPA appear artificially lower than reality.

---

### P4 — Long Consideration Window Markets (NC Separation Period Example)

**Source:** 2026-03-28-mccrary | **Status:** Provisional (1 account — NC family law specific, but framework generalizes)

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

**Source:** 2026-03-28-mccrary | **Status:** Provisional (1 session)

**Pattern:** In long consideration window markets, prospects research multiple providers over an extended period. Competitor name searches — even for direct competing attorneys — may represent prospects who consulted that competitor earlier in their funnel and are now considering alternatives.

**Observed case:** Competitor names (baity, joe delk, carmen brown — other NC family law attorneys) were converting in McCrary's account. Consistent with the NC separation period: prospects consulting multiple attorneys over a year.

**Implication:** In high-competitor-density, long-consideration markets, competitor keywords may be worth intentionally targeting rather than neutrally ignoring. Evaluate whether competitor terms are converting before recommending them as negatives. This is the opposite of the typical legal PPC default (avoid competitor terms to stay clean).

---

---

## Confirmed Entries (2+ sessions)

---

### P6 — Both ad_group_criterion and keyword_view Return Positive and Negative Keywords

**Source:** 2026-04-01-mccrary, 2026-04-19-mccrary, 2026-04-27-cowdreyjenkins | **Status:** Confirmed (3 sessions, multiple accounts)

**Pattern:** GAQL queries against `ad_group_criterion` AND `keyword_view` both return positive and negative keywords in the same result set. If the `negative` field is not filtered, the two types are indistinguishable from the response. This caused confirmed misdiagnosis in multiple sessions — negative keywords were flagged as active BROAD match problems or active targeting issues.

**Observed cases:**

- `cheap` (BROAD) in McCrary Catawba - Child Custody ad group — flagged as a positive keyword needing conversion. It was an ad-group-level negative. (2 sessions)
- `5 signs`, `elder`, `dallas`, `pro bono` in Cowdrey Jenkins LA+ — flagged as active junk positive keywords. All were ad group-level negatives. Caught via `ad_group_criterion` direct query after the `keyword_view` query returned them without the filter.

**Secondary:** `ad_group.status` omission caused a keyword in McCrary Brand's PAUSED "Male Divorce Lawyer" ad group to be flagged as an active BROAD match issue. It was not serving.

**Implication:** Before flagging ANY keyword from ANY resource as an active positive issue, verify `negative = False` AND `ad_group.status = ENABLED`. This applies to both `ad_group_criterion` AND `keyword_view` queries. The negative filter is now required in all library queries using either resource. If a query result is missing the `negative` column, the query is incomplete — do not proceed with analysis.

---

### P8 — search_term_view Returns Historical Data Without status = NONE Filter

**Source:** 2026-04-20-kirschbaum, 2026-04-27-underwood | **Status:** Confirmed (2 sessions, 2 accounts)

**Pattern:** `search_term_view` has two distinct mechanisms that produce false active findings:

1. **Paused ad group data:** Queries return historical records from ALL ad groups — including PAUSED and REMOVED ones — unless `ad_group.status = 'ENABLED'` is in the WHERE clause. Caused confirmed misdiagnosis in Kirschbaum: terms from PAUSED SKAG - Probate - Broad ("estate planning attorney near me" at $0.20/click) presented as active waste.

2. **Expired keyword matches (status = NONE):** Even with `ad_group.status = 'ENABLED'`, a term can appear with `search_term_view.status = NONE`, meaning it matched historically via a now-paused or tightened keyword (e.g., a BROAD that was converted to phrase match) and is no longer actively served. Caused confirmed misdiagnosis in Underwood: "partition action nevada" (2 clicks, $23.46, 1 conv) flagged as active waste — it was status NONE, triggered by a BROAD keyword that had since been paused.

**Same root cause as P6:** The API returns all matching records for a given account/date range regardless of current serving status. Explicit field-level checks are the only defense.

**Implication:**

- Every `search_term_view` query must SELECT `search_term_view.status` — if the field is not in the result, the query is incomplete, do not proceed
- Every `search_term_view` query must include `AND ad_group.status = 'ENABLED'` in the WHERE clause
- Never flag a term with `status = NONE` as an active finding — it is not currently serving
- Before flagging any search term as an active waste source, confirm `status ≠ NONE`

---

### P7 — search_rank_lost_impression_share ≠ Budget Constraint

**Source:** 2026-04-19-underwood | **Status:** Provisional (1 session)

**Pattern:** `metrics.search_rank_lost_impression_share` measures impressions lost because Ad Rank was too low — a QS, bid, or landing page problem. It is not a budget signal. `metrics.search_budget_lost_impression_share` is the separate field that measures impressions lost to budget exhaustion. Conflating the two produces wrong recommendations: OC's 67% rank-lost IS was misread as "budget constrained" when it actually indicated a landing page / QS problem requiring creative and LP work, not more budget.

**Implication:** Always pull both fields when assessing IS. Label them accurately. "Rank lost" → QS/LP/bid quality fix. "Budget lost" → budget increase. Never recommend budget reallocation based on rank-lost IS alone.

---

*Next synthesis session: after 4–8 total sessions. At that point, review all session logs, confirm which provisional entries appear cross-account, and remove the provisional marker.*
