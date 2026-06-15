---
name: google-ads-analysis
description: Use this skill when analyzing, auditing, or diagnosing Google Ads accounts for law firms. Triggers include explicit requests (account audit, search term review, GAQL query, conversion tracking check, negative keyword review, impression share analysis) and implicit ones (why is CPA high, leads are down, this campaign feels off, something changed this week, why is this not spending, performance is down). Use even if the user doesn't say "Google Ads" — phrases like "check the campaigns", "run an audit", "performance seems off", or "why are leads down" should all activate it. Does NOT cover: campaign creation, Facebook/Meta ads, SEO, keyword research for new accounts, or client reporting via AgencyAnalytics.
compatibility: Requires googleAdsServer MCP with run_gaql tool (Google Ads API access). Designed for Claude Code.
---

# Google Ads Analysis Skill — Rosen Advertising

## Purpose

This skill enables autonomous analysis and optimization of Google Ads accounts for law firms. It encodes expert-level knowledge about legal PPC and provides structured tools for diagnosis, auditing, and optimization without requiring step-by-step direction.

---

## Version Note

This skill operates in two modes:

**Toby version (internal):** At session start, read `references/learnings.md` (if it has entries) and the relevant `account-notes/[account].md` file. At session end, generate a session log using the template at the bottom of this file. This version has historical context that accumulates over time.

**Public version:** Read skill reference files only. No session logging. No account notes. No `learnings.md`. This version is derived from the Toby version when there is something worth publishing — it does not need to be maintained separately in the meantime.

---

## Knowledge Foundation

Read these before any analysis:

- **`references/google-ads-knowledge-base.md`** — Core philosophy and principles. The lens through which all findings are evaluated. Non-negotiable starting point.
- **`references/learnings.md`** _(Toby version only)_ — Validated patterns extracted from past session logs. Read this after the knowledge base to supplement with empirically-observed patterns.
- **`account-notes/[account].md`** _(Toby version only)_ — Account-specific context, history, and prior findings. Read the relevant file for the account being analyzed.

---

## Account Macro Context — Mandatory Reasoning Input

Every audit, optimization, or diagnostic session must establish account macro context **before** any item-level work. Macro context is mandatory input to the reasoning, even when it is not surfaced in the output.

**What "macro context" means:**

- Spend trend: current period vs prior 90-day baseline
- Conversion volume trend: current period vs prior 90-day baseline
- Lead volume trend: from CRM where available, otherwise primary conversion action volume
- CPL / CPA trend: current period vs prior 90-day baseline
- Year-over-year comparison where the data spans long enough

Pull this **before** running symptom-specific diagnosis. Every recommendation must be evaluated against the macro state of the account — recommending "raise bids on the Women campaign" lands differently when total account spend is already up 40% this month with conversions down. Tactical recommendations made in isolation from the macro frame are tunnel vision, even when the items themselves are correct.

**Output rule — surface conditionally, not every session:**

- The macro snapshot is NOT included in the user-facing output by default. Users do not need to see a trend dump every session.
- Surface a **flag** in the output only when the macro signal is material enough to warrant attention:
  - Material trend shift (e.g., conversion volume down 25%+ vs prior period)
  - Trend reversal (account was trending up, now reversing)
  - **Contradiction** with the tactical recommendation about to be made (e.g., recommending bid-up when spend is already up 40% MoM)
  - Pattern that explains other findings (e.g., a sudden YoY drop alongside structural changes that may be the cause)
- When surfacing a flag, frame it as a question or observation tied to the broader account direction — not as a separate audit section.

**Format when flagging:**

```text
[MACRO FLAG] [one-line description of the trend]
[Why it matters in the context of the work being done]
```

Example: a session optimizing keyword structure finds the work tactically correct, but conversions are down 35% MoM. The macro flag surfaces because the proposed keyword expansion may amplify spend in a period where the account is already underperforming — worth pausing to investigate the conversion drop before scaling.

---

## Reference Files

| File                                     | Purpose                                                                          | When to Use                                                |
| ---------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `references/gaql-query-library.md`       | Pre-built GAQL queries organized by diagnostic task                              | Any time live account data is needed                       |
| `references/negative-keyword-library.md` | Master negative keyword lists by category                                        | Search term reviews, account audits, new account setup     |
| `references/diagnosis-trees.md`          | Diagnostic frameworks for the most common account problems                       | Performance diagnosis, account review, issue investigation |
| `references/creative-audit.md`           | Creative / image-asset audit — what to pull (sidecar tools), what to look for, API-sourceable vs manual | Every periodic check (creative pass in Step 4); any creative/display review |
| `account-audit-checklist.md`             | Structured first-review audit checklist (Sections A–I, pass/fail, output format) | First-contact account review (Tree 5)                      |

---

## MCP Tool Note

Queries in `references/gaql-query-library.md` are pure GAQL and MCP-agnostic. Execute them using whatever GAQL execution tool is available in the current environment.

Currently: `run_gaql(customer_id, query, format)` from the `googleAdsServer` MCP.

- Prefer `format="table"` for diagnostic reads
- Use `format="csv"` for large result sets you need to process
- `run_gaql` is preferred over `execute_gaql_query` — it's a superset with output format control

If the MCP changes, update this note only. The query library remains valid.

**Login/MCC customer ID:** _(set in your MCP config — replace with your own MCC/manager account ID)_
**First step in any new session:** `list_accounts()` — confirms which accounts are accessible.

---

## GAQL Query Integrity — Keywords and Search Terms

### Keyword queries (`ad_group_criterion` and `keyword_view`)

The API returns **both positive and negative keywords in the same result set** — this applies to both `ad_group_criterion` AND `keyword_view` queries. Failing to distinguish them causes confirmed misdiagnosis.

**Mandatory rules before flagging any keyword as an issue:**

1. **Always filter `ad_group_criterion.negative = FALSE` in the WHERE clause** of any keyword query, regardless of whether the resource is `ad_group_criterion` or `keyword_view`. If this filter is missing, the result contains negatives mixed with positives — re-run before drawing any conclusions.

2. **Check `negative` before flagging.** If `negative = True`, this keyword is a negative. It is working correctly. Do NOT treat it as a positive match type issue, a quality score problem, or a waste source.

3. **Always SELECT and filter `ad_group.status`.** Keywords from paused ad groups are not serving. Do NOT flag them as active optimization targets. The standard keyword queries in the library filter `ad_group.status = 'ENABLED'` — use them.

4. **Also SELECT `campaign.status`** for the same reason. A keyword in a paused campaign is not a live problem.

**Quick check:** if a keyword query — from either `ad_group_criterion` or `keyword_view` — does not include `ad_group_criterion.negative = FALSE` in the WHERE clause, stop. Re-run the correct query from the library. Do not proceed with analysis on an incomplete result.

### Search term queries (`search_term_view`)

`search_term_view` returns historical search term records from **all ad groups — including PAUSED and REMOVED ones**. Without filtering, results will include data from groups that are no longer serving, producing false findings.

**Mandatory rules before presenting any search term finding:**

1. **Always include `ad_group.status = 'ENABLED'` in the WHERE clause.** Same rule as keyword queries — different query type, same root cause.

2. **Always SELECT `search_term_view.status` in every search term query.** If this field is missing from the result, the query is incomplete — re-run using the library query before drawing any conclusions. Do not flag any term as a finding without this field present.

3. **Never flag a term with `status = NONE` as an active finding.** `NONE` means the term matched historically but is no longer actively served by any keyword. It may be from a period when a broader keyword (e.g., BROAD match) was active and has since been tightened or paused. It is not a current waste source. Confirmed misdiagnosis: "partition action nevada" in Client B (2026-04-27) — flagged as active, was status NONE from a paused BROAD keyword.

4. **Check which ad group a term came from before flagging it.** If `ad_group.status = PAUSED` or `REMOVED`, that term is historical. Do NOT flag it as an active waste source or a current keyword structure problem.

**Quick check:** If a search term query result does not include `search_term_view.status`, stop. Re-run the correct query from the library. Do not proceed with analysis on an incomplete result.

**Root cause:** Google's API scopes data by account and date, not by serving status. Paused ad groups and expired keyword matches still have historical records. Always filter and verify explicitly.

### Auditing search term data you are handed

The rules above govern queries you run. The same logic applies when someone **gives** you search term data (a pasted table, a CSV, a screenshot). You didn't run the query — you don't know if the `ad_group.status = ENABLED` filter was applied.

**Before flagging any handed search term as waste, check CPC plausibility:**

Legal PPC CPCs are typically $5–50+ per click for competitive terms (probate, family law, personal injury, elder law). If a handed result shows a legal search term at under ~$2/click, that is anomalously cheap for the practice area.

Cheap CPC on a competitive legal term is a red flag that the data includes paused ad group history — paused ad groups accumulate low-cost historical impressions/clicks from when CPCs were lower, or from test periods.

**Protocol for handed search term data:**

1. Before drawing any conclusions, scan the CPC column. If you see legal-intent terms at under $2/click (especially under $1), flag this immediately: "These CPCs look anomalously low for legal PPC — typical range is $5–50+. This may include data from paused ad groups."
2. Ask: "Can you confirm which ad groups these terms came from, and whether the query filtered for ENABLED ad groups only?"
3. Do NOT present terms with suspicious CPCs as active waste findings until the source is confirmed.
4. If the source is confirmed as a paused ad group, they are historical — no action needed.

---

## Smart Bidding — Post-Tracking-Fix Protocol

When conversion tracking contamination is fixed on an account running tCPA or any smart bidding strategy, the **bidding model is now invalid** — it was trained on inflated or incorrect conversion data. The following protocol is mandatory.

**Do NOT adjust the tCPA target immediately after fixing tracking.**

This is the single most common mistake made after a tracking cleanup. The instinct to "correct" the target to match new, cleaner CPA numbers is wrong. Here's why: the algorithm hasn't learned what the clean-data CPA actually is yet. Any target you set is still anchored to contaminated history. Setting a new target before relearning completes just gives the algorithm a new wrong number instead of the old wrong number.

**The correct sequence:**

1. **Fix the tracking.** Confirm it's clean.
2. **Hold the current tCPA target.** Do not change it yet.
3. **Announce a 2–4 week lockdown.** No bid strategy changes, no target changes, no budget changes. Treat it like a standard learning phase — because it is one.
4. **Expect apparent CPA to rise.** This is not the account getting worse. It's the tracking getting accurate. Previously reported CPA was artificially low because conversions were double-counted. The "new" higher CPA is the real number. Do not react to it.
5. **After 2–4 weeks of clean data**, evaluate whether the target needs adjustment. Now you have a real baseline. Adjust based on that — not on the pre-fix numbers.

**What to monitor during relearning:**

- Learning status in the campaign settings (should show "Learning" initially, then clear)
- 14-day rolling CPA (expect rise, then stabilization)
- Impression share (may drop as algorithm recalibrates auction bids)
- Absolute conversion volume (will appear to drop — this is the duplicate count disappearing)

**Low-volume flag:** If the account was already near the 15–20 conversion/month reliability threshold before the fix, the cleaned-up volume may fall below it. If this happens, consider switching to Maximize Conversions rather than tCPA until volume recovers.

**Low-volume flag — already on Maximize Conversions + high CPC.** Maximize Conversions is not always the safe harbor. When a campaign is **already on Maximize Conversions, running below the ~15–20 conv/month reliability floor, AND carrying a high avg CPC for its practice area**, the algorithm is bidding blind on thin signal and burning budget per click. The fix is **Maximize Clicks with a CPC cap** — buy volume and rebuild conversion signal while capping runaway auctions — not another target tweak. Set a 3–4 week revisit and watch CVR (Max Clicks optimizes for clicks, not conversions). See learnings P9.

---

## tCPA Direction Rule

**Only lower tCPA when actual cost/conv is already comfortably below the current target.** Lowering tCPA when CPA is at or above target restricts campaign volume — it signals to the algorithm to win fewer auctions, which reduces conversion opportunities when the account is already struggling to generate them.

**Decision framework:**

- **cost/conv well below target** (e.g., target $150, actual $90): Safe to lower tCPA to capture efficiency. Move in 10–15% increments, not all at once.
- **cost/conv near target** (e.g., target $150, actual $140): Hold. Insufficient headroom. Lowering risks volume loss without efficiency gain.
- **cost/conv above target** (e.g., target $150, actual $210): Do NOT lower tCPA. Fix root causes first — QS, ad relevance, LP conversion rate, negative keyword gaps. Lowering further restricts an already underperforming campaign.
- **cost/conv well above target AND low impression share:** Root cause is almost always QS/bid quality, not budget. Adding budget does not fix a tCPA campaign that's losing impressions to rank. Diagnose rank-lost IS (use GAQL 5.1).

**The instinct to "tighten" tCPA when CPA is high is wrong.** When the algorithm is already under pressure to find converting traffic, lowering the target tells it to spend less per conversion — which means it enters fewer auctions and gets fewer conversions, not cheaper ones. This is the most common bidding mistake in legal PPC.

**Exception:** If budget is clearly not the constraint (budget-lost IS is near 0) and rank-lost IS is very high, the issue is bid quality — tCPA can be raised to give the algorithm room to compete, not lowered.

---

## Target Setting — Targets Come From Firm Economics, Not Account Data

A bidding target (tCPA, target CPL, target cost per signed case) is an **external input** — not something you back-solve from the account's own numbers. The account's current CPA tells you how performance compares to the target; it is never the _source_ of the target.

**Where a target comes from, in priority order:**

1. **Firm economics in `account-notes/[account].md`.** The firm's average case value, lead-to-signed rate, and acceptable cost per signed case give you the target CPL/CPA. These are operator-recorded business inputs — use them.
2. **An explicit operator override.** If the operator states a target (or different economics) for the task at hand, that supersedes the notes.
3. **If neither exists, ask.** Request the firm's economics — average signed-case value, lead-to-signed rate, acceptable cost per signed case. Do not set a target without them.

**Never back-solve a target from the account's own current CPA or spend.** Averaging what the account currently pays per conversion and calling that "the target" is circular: the current CPA reflects the account's current performance, including whatever is broken about it, so a target derived from it merely ratifies the status quo. It is a loop that can never improve the account — every "target" is just last period's result wearing a new label. This is the one forbidden move in target setting.

**Why the instinct is wrong:** a target is a business decision about what a signed case is worth and what the firm will pay to win one. That decision lives with the firm, not in the auction data. Pull the account's CPA to _measure against_ the target; pull the target itself from the firm's economics.

**Worked logic:** average signed-case value $12,000 × a 15% acquisition budget = $1,800 target cost per signed case; at a 30% lead-to-signed rate that is a ~$540 target CPL. If the account's current CPL is $900, it is 67% over the external target — that is a finding. You did not learn $540 by looking at the account; you brought it from the firm's economics.

**When the external target sits well below current performance,** that gap is the finding — not a reason to abandon the target. Fix the drivers first (QS, landing page, structure). If you then move the live tCPA toward the economics target, step it down in increments (see the tCPA Direction Rule above) so the algorithm does not oscillate. The economics number is the destination; the increments are how you reach it without thrashing. "Realistic target" means achievable in steps, never "back-solved from current CPA."

---

## Campaign-Level CPC Anomaly — Routing Protocol

When campaign-level avg CPC looks anomalous (not search term level — the campaign performance summary), route the diagnosis based on direction:

**Anomalously LOW avg CPC for the practice area:**

Legal PPC typical ranges: family law $8–25, elder law $10–35, personal injury $20–80, partition/real estate $15–40, elder abuse $60–150+.

If campaign avg CPC is well below these ranges (e.g., $3.20 in a Medicaid campaign, or $2.50 in a divorce campaign):

1. **First check: tracking integrity.** Low avg CPC on competitive legal terms is a red flag for data contamination — possibly includes historical data from paused ad groups or test periods when CPCs were lower, or a conversion tracking issue that is inflating apparent traffic.
2. **Do NOT route to keyword targeting as the first frame.** The instinct to explain cheap clicks as "wrong match type" or "low-intent keywords" is secondary. Check data integrity first.
3. Pull campaign history (PF-3) and confirm the avg CPC trajectory. If it was historically normal and recently dropped, something changed — conversion tracking, keyword structure, or bid strategy reset.
4. If search term data confirms the clicks are coming from low-intent queries at low CPC, then keyword/match type diagnosis applies. But only after ruling out data contamination.

**Anomalously HIGH avg CPC:**

For high-value practice areas (elder abuse, complex commercial litigation), $80–150/click is normal — do not flag as problematic by default. Context: case values in elder abuse can be $500K–$2M+; a $120 CPC acquiring one case is exceptional ROI.

Flag as potentially problematic only when HIGH avg CPC is combined with: (a) zero or near-zero conversions over 14+ days, AND (b) impression share is adequate (>30%). This combination suggests the algorithm is bidding high for clicks that don't convert — possible LP issue, wrong audience, or conversion tracking failure.

**Third condition — high CPC + sub-floor (not zero) conversions + budget-lost IS → bidding-strategy fix, not the LP/tracking diagnosis.** Distinct from the zero-conversion case above: when avg CPC is high, the campaign **is** converting but **below** the ~15–20 conv/month reliability floor, and it is losing impression share to budget, the problem is that smart bidding has too little signal to bid well on expensive auctions. Route this to the bidding-strategy fix — Maximize Clicks with a CPC cap (see the Smart Bidding low-volume flag and learnings P9) — rather than the LP/audience/tracking diagnosis. The zero-conversion branch points at LP/tracking; this thin-but-nonzero branch points at the bidding model.

---

## Search Term Data — Coverage Ceiling

`search_term_view` typically shows **~50% of actual campaign spend**. This is a Google Ads API limitation — the API withholds low-volume search terms and has a hard row cap per query. It is not fixable through query splitting or pagination (GAQL does not support OFFSET).

**Coverage check is mandatory before presenting any search term findings.** Do this first, before analysis, before findings, before recommendations:

1. Pull actual campaign spend for the period via `FROM campaign`
2. Sum total cost from your `search_term_view` results
3. Report the ratio: "Search term data covers $X of $Y actual spend (Z%)"

Do not present findings, waste estimates, or negative keyword recommendations until this ratio is on the table. The user needs to know what they're working with before deciding how much weight to give any finding. If coverage is low, scale estimates accordingly and say so — don't ask whether the user still wants the analysis on bad data. The answer is always to disclose the coverage and proceed transparently, not to ask permission.

**Per-campaign querying (not per-account)** is still required — pulling all campaigns in one query caps at ~500 rows and will give far worse coverage than querying per campaign. But even per-campaign or per-ad-group querying converges at ~50% coverage — this is the ceiling.

**What this means for analysis:** waste estimates and conversion totals from search term data represent the visible portion only. Scale dollar figures by the coverage ratio when reporting (e.g., if visible waste is $244 at 54% coverage, estimated total waste is ~$452). Patterns and categories observed in the visible 50% are representative — the hidden 50% is randomly distributed, not systematically different.

**Never recommend blocking a term category solely based on search term data showing zero conversions.** Account-level conversion data (from `FROM campaign`) is authoritative for spend; search term data is a sampling.

**Negative-keyword precision — two decision rules:**

- **Never negate a term that has converted**, no matter how much it looks like junk, a referral/nonprofit name, or a geo/category mismatch. Check the term's conversion data before excluding it — a converting term is a customer, not waste. (A term that looks like a nonprofit-referral mismatch can still be a real lead source.)
- **On a geo-mismatched query that contains your core service term, negate the geo token only — never the service term.** Decompose the query first: for a city-mismatched query like `[core service term] [wrong city]`, negate `[wrong city]`, not `[core service term]`, so the campaign keeps serving the service term in its real geo. See learnings P10–P11.

---

## QS Throttling — All-BELOW_AVERAGE + Zero Impressions

The Google Ads UI displays a "limited by quality score" label for severely underperforming keywords. The API does not expose this label as a field — `system_serving_status` returns `ELIGIBLE` even for throttled keywords. To diagnose QS throttling via API, use this heuristic:

**Throttled keyword pattern:** QS ≤ 2, AND all three components BELOW_AVERAGE (`search_predicted_ctr`, `creative_quality_score`, `post_click_quality_score`), AND zero or near-zero impressions over the most recent 7-14 days on an active campaign with available budget.

When all three conditions are present, the keyword has been effectively removed from auction consideration by Google. This is categorically different from a keyword with QS 4-6 and one weak component.

**Standard QS optimization does not recover a throttled keyword.** Improving ad copy, landing page, or CTR applies to underperforming keywords that are still entering auctions. For a throttled keyword, Google is not entering it into auctions at all — incremental quality improvements cannot recover it from this baseline.

**The correct intervention is structural replacement:**

1. Pause the throttled keyword
2. Create a new keyword variant in a new or reorganized ad group with dedicated ad copy and a landing page that precisely matches the query intent
3. A fresh keyword gives Google a clean quality signal with no prior history

State the heuristic explicitly when diagnosing — do not present `system_serving_status = ELIGIBLE` as confirmation that the keyword is serving normally.

---

## BROAD Match Keyword Remediation — Default Path

When a BROAD match keyword is flagged for cleanup (high CPA, waste, or match type tightening), the default recommendation is **convert to phrase match first** — not delete, not pause, not jump directly to exact.

**Why phrase, not exact:** BROAD → exact skips the intermediate step that preserves near-intent query variants while filtering the looser ones. Exact match may lose reach unnecessarily. Phrase match is the standard intermediate step.

**Why not delete or pause:** If a BROAD keyword has conversion history, it carries smart bidding signal. Deleting or pausing removes that signal. Phrase match conversion preserves the signal while tightening control.

**When hard delete is appropriate:** Only for irrelevant terms — wrong practice area, wrong geography, competitor brand names. Relevant keywords that are simply too broad get converted to phrase, not deleted.

**Sequence:**

1. Convert BROAD to phrase match
2. Monitor search terms for 2-4 weeks
3. If CPA remains above target after phrase conversion, identify specific waste terms to negative or evaluate tightening to exact

---

## Search Partners CPA Distortion — Network Segmentation Required

When a brief presents a CPA figure for a campaign running on **both Search and Search Partners**, that figure is a blended average across two networks with different traffic quality. Search Partners traffic typically converts at a lower rate and higher CPA than Google Search traffic in legal PPC.

**Before drawing any CPA conclusion or recommending any bid change, flag whether the campaign includes Search Partners:**

Pull: GAQL 6.4 or `segments.network` — segment campaign performance by `SEARCH` vs. `SEARCH_PARTNERS`.

If network data is not provided and Search Partners status is unknown:

- State explicitly: the reported CPA may be a blended figure that includes Search Partners
- Do not diagnose "CPA is high" or recommend a tCPA change until network split is confirmed
- The required next step is: pull performance by `segments.network` (clicks, conversions, cost, CPA) for each network separately

**Smart bidding signal risk:** Excluding Search Partners is not a simple win. Removing the Partners network reduces the total conversion signal available to the smart bidding algorithm. If the campaign is near the 15-20 conv/month reliability threshold, excluding Partners may push it into Sub-tree D territory. Always check conversion volume contribution before recommending exclusion.

**Decision framework after pulling network data:**

- If Search Partners CPA is above target AND Partners conversion volume is small relative to Search → exclusion is reasonable; signal loss is minimal
- If Search Partners CPA is above target BUT Partners is contributing significant conversion volume → exclusion risk is real; consider whether blended CPA is still on-target if Partners is removed
- If Search CPA is already on-target → the issue is contained to Partners; exclusion is the likely fix, but confirm volume contribution first

---

## Handling Comparative and Premise-Based Questions

When a question contains a stated premise — "Why is X so high?", "X is at $284, should we pause it?", "X is performing worse than Y" — **verify the premise before diagnosing it.**

Do not accept a stated CPA, performance comparison, or benchmark as given. Pull actual data first.

**Cross-account comparisons require extra scrutiny.** A CPA comparison between two accounts is only meaningful if the accounts are comparable: same practice area, same geography type, same conversion volume range, and same conversion definition. In legal PPC, elder law vs. family law, small market vs. metro, 3 conversions/month vs. 30 — these are not comparable even if both accounts run Google Search.

**Conversion volume threshold for reliable CPA.** A CPA figure requires at least 15-20 conversions to be statistically meaningful. Below that threshold, CPA is noise — a single high-cost conversion in a low-volume account can shift the reported CPA by 40–60%. When conversion volume is below 15-20/month per campaign (or over a 90-day period for a narrow campaign), explicitly flag: this CPA is not a reliable signal. The threshold comes from smart bidding minimums — tCPA requires this volume to function — but applies equally to manual interpretation.

**Reasons lists must follow, not precede, verification.** Producing a list of "reasons CPA is high" before confirming that CPA is actually high (via live data) treats a premise as confirmed fact. This pattern produces plausible-sounding but ungrounded analysis. If live data isn't available, frame conditionally: "If the data confirms CPA is elevated, likely causes include..." is different from "CPA is high because..."

---

## Account Notes vs. Live Data

**Account notes describe prior state. They are not a substitute for current data.**

`account-notes/[account].md` records what was true at the time of past sessions — prior CPA figures, pending actions, observations from weeks or months ago. Before drawing any diagnostic conclusion about the current state of the account, pull live data via GAQL.

**The rule:** If a conclusion requires knowing current account state (keyword status, current CPA, current conversion volume, current campaign settings), it must come from a live GAQL query — not from account notes alone.

Account notes are used for:

- Understanding prior context before pulling data
- Knowing what to look for and what changed since the last session
- Applying market-specific priors and account history

Account notes are NOT used for:

- Determining whether a keyword is currently active
- Stating current CPA or performance numbers
- Confirming whether a prior recommendation was implemented
- Drawing any conclusion that requires knowing current account state

If MCP tools are available, use them. Don't reason from a snapshot when you can query the live account.

**A standing "structural" flag has a shelf life.** A note that a CPA gap is "LP-gated," "structural," or "out of scope" is a *hypothesis recorded at a point in time* — not a permanent truth. Re-pull live data before re-asserting it, and retire it when the data shows the gap has closed. Creative or ad changes (a refresh, new headlines) can lift a ceiling long blamed on structure; don't let a stale standing flag keep an ad group on the problem list after it has recovered. See learnings P12.

---

## Impression Share — Two Separate Metrics

`search_rank_lost_impression_share` and `search_budget_lost_impression_share` are not the same thing.

- **Rank-lost IS** — impressions lost because Ad Rank was too low. Fix: QS improvement, ad relevance, landing page quality, or bid adjustment. Adding budget does not help.
- **Budget-lost IS** — impressions lost because the daily budget ran out. Fix: increase budget.

**Rule:** When assessing IS, always pull GAQL 5.1 which includes both fields. Never characterize a campaign as "budget-constrained" based on rank-lost IS alone — that is a QS/LP problem requiring creative work, not spend.

**Rank-lost IS on Maximize Conversions = QS issue only.** On campaigns using Maximize Conversions (no tCPA), the algorithm already bids as high as it calculates optimal for each auction. If rank-lost IS is high on a Max Conv campaign, the algorithm is not "holding back" — it is losing auctions because Ad Rank is insufficient. The fix is QS and landing page quality, not a bid strategy change. Never diagnose rank-lost IS as a bid constraint on a Max Conv campaign — there is no bid ceiling to raise.

**Budget-lost IS can occur without hitting the daily cap.** BROAD match keywords can consume budget disproportionately early in the day — serving on high-volume, lower-intent queries before more targeted phrase/exact keywords compete. This produces budget-lost IS even when daily spend is below the budget ceiling. If a campaign has budget-lost IS and a BROAD keyword consuming most of the daily budget before 10am, the fix is converting the BROAD to phrase match — not increasing budget. Increasing budget gives the BROAD more to consume early-day and does not solve the problem.

---

## Creative / Image-Asset Audit — Standing Periodic Check

A creative pass is a **standing part of every periodic (Monday/Thursday) check**, not an optional add-on. Rosen Advertising accounts are shifting heavily toward image, and all running accounts move toward display soon — so image-asset coverage and quality are now a first-class account-health dimension. Run the creative pass every periodic session; keep it proportionate (a focused pass, not a forensic teardown).

**Tooling — sidecar only.** The image-asset tools live **only in the incumbent `googleAdsServer` sidecar** (the official MCP lacks them — that's why the sidecar is retained). Use these four tools and only these; do not substitute or invent others:

- `get_image_assets` — list image assets in the account (inventory)
- `get_asset_usage` — map which campaigns / ad groups use which assets (coverage)
- `download_image_asset` — fetch the image file (for inspection / vision)
- `analyze_image_assets` — vision analysis of image content / quality

**What the pass covers (full detail in `references/creative-audit.md`):**

- **(a) Coverage** — map every ENABLED campaign against `get_asset_usage`; flag campaigns thin or missing image assets. As accounts move to display, a campaign with no image coverage cannot fill its inventory — the highest-priority creative finding. Don't flag pure Search campaigns for lacking display creative.
- **(b) Quality + content** — `analyze_image_assets` (with `download_image_asset` to confirm) against three bars: on-brand, legible, and message-matched to the ad group's intent. Vision is a strong first read; the final brand/compliance call on a legal client is a manual review.
- **(c) Usage gaps** — assets uploaded but attached to nothing (`get_image_assets` minus `get_asset_usage`), and campaigns with no coverage.
- **(d) Fatigue** — long-running unchanged assets (cross-reference change history, GAQL §8) and declining signals; where per-asset performance is thin, fall back to ad-group/campaign CTR proxy and say so. Don't over-call fatigue on low volume.

**API-sourceable vs. manual — be explicit (skill convention).** Inventory, usage mapping, coverage gaps, and the file download are **API-sourceable** via the four sidecar tools. Image content is **API-assisted via vision** (`analyze_image_assets`) — a strong read, not a final verdict. The **on-brand / compliance / message-match call is a manual/visual review**, per-asset performance is only **partially API-sourceable**, and how an asset renders in a live placement is a **blind spot** — request a screenshot via the standard protocol. Mark the source tier on every creative finding; never present a brand/compliance verdict that rests only on vision as auto-confirmed.

This section is the methodology pointer — it wires into "How to Approach a Session" Step 4 as a creative sub-step. Full procedure, the source-tier table, and the blind-spot wording are in `references/creative-audit.md`.

---

## Using Sub-Agents for Heavy Analysis

For tasks that involve pulling and analyzing large search term datasets across multiple campaigns, spawn parallel sub-agents — one per campaign — using the `Agent` tool with `subagent_type: "general-purpose"`. This:

- Prevents search term files from consuming the main context window
- Enables parallel data pulls (faster wall-clock time)
- Keeps each agent's analysis focused on one campaign

**Pattern:**

```text
Main agent → fires N sub-agents in parallel (one per campaign)
Each sub-agent → pulls search terms, runs intent categorization, returns structured summary:
  { campaign, spend_visible, spend_actual, waste_terms[], converting_terms[], flags[] }
Main agent → synthesizes all summaries into findings + action list
```

Use this pattern any time a search term review spans more than 2 campaigns.

**Compatibility:** Requires Claude Code with the `Agent` tool available. If running in an environment where the `Agent` tool is not available, run each campaign's search term pull sequentially in the same session rather than in parallel.

---

## Skill Dependencies

This skill works best alongside other installed skills. Check availability at session start and use them when relevant:

| Skill                   | Use for                                                               | Required?   |
| ----------------------- | --------------------------------------------------------------------- | ----------- |
| `xlsx`                  | Negative keyword upload files, bulk change sheets, structured exports | Recommended |
| `pptx` / `docx`         | Client-facing reports                                                 | Optional    |
| _(data skill — future)_ | Statistical aggregation, complex analysis                             | Planned     |

If a dependency is missing and the user asks for output that skill would handle, note what's missing and suggest installing it rather than producing a lower-quality substitute.

---

## How to Approach a Session

### Step 1 — Establish the brief

Every session has a brief. It may be explicit (client concern, specific issue) or self-directed (monthly review, regular optimization). The brief determines where to focus. There is no universal starting point.

Common brief types:

- **Performance review** — What happened over the last period? What changed?
- **Issue investigation** — Something is wrong. Diagnose and explain.
- **Account audit** — First look at an account or periodic structural review.
- **Search term review** — Mine search terms for negatives and keyword opportunities.
- **Ad copy review** — Assess creative performance and identify refresh candidates.
- **Creative / image-asset audit** — Image-asset coverage, quality, usage gaps, and fatigue. Runs as a standing creative pass in every periodic check (see Step 4b and the "Creative / Image-Asset Audit" section); also a brief in its own right as accounts move to display.
- **Conversion tracking audit** — Verify that what's being tracked is correct and complete.

**Brief clarity gate:** Assess whether the brief is specific enough to target the session. A clear brief (explicit concern, named campaign, defined scope) → proceed directly. A vague brief ("run a review", "check performance", "see what's going on", "[account] feels off") → do the following:

1. **State the diagnostic entry point.** Name which Tree in `references/diagnosis-trees.md` applies — e.g., "This looks like a Tree 4 (performance drop) entry point" or "Defaulting to Tree 5 (account review) since no specific concern was named." Say this out loud in your response. Don't silently assume an entry point.

2. **Proceed to Steps 2 and 3.** Pre-flight checks run regardless of brief clarity — do not wait for clarification before running them. See Step 3.

3. **Ask 1–2 focused clarifying questions after pre-flight**, using what you found as context:
   - "Is there a specific concern driving this — performance drop, budget issue, something the client flagged?"
   - "Is there a campaign or time period you want to prioritize?"

This isn't gatekeeping — it's targeting. Pre-flight data makes clarifying questions more precise. Name the entry point, run pre-flight, then ask.

### Step 2 — Verify prior session's pending actions _(Toby version only)_

Before any new analysis, read `account-notes/[account].md` and check the `## Pending Actions` section.

**If the file doesn't exist:** This is a new account with no prior session history. Note this, skip the verification step, and plan to create the file at session end using the template in the session log section. Proceed to Step 3.

For each pending item, pull current account state via GAQL and verify whether it was implemented:

- **Implemented correctly** → mark done, note the date, move to session log
- **Not implemented** → re-flag as pending, surface to user at start of session
- **Implemented incorrectly** → flag specifically with what's wrong

This closes the feedback loop. The skill recommended the action; now it confirms whether it happened and can begin attributing performance changes to specific interventions. Don't skip this even if the user hasn't mentioned it — it's how the skill builds a reliable thesis about what works in this account.

### Step 3 — Run pre-flight checks

Before any symptom-specific diagnosis, run the pre-flight checks from `account-audit-checklist.md` and `references/diagnosis-trees.md`:

- **PF-0: Account macro context** (reasoning input — surface as flag only when material; see "Account Macro Context" section above)
- PF-1: Conversion tracking verification
- PF-2: Structural red flags
- PF-3: Change history read

All four are mandatory and none are deferred by a vague brief. PF-0 grounds every subsequent recommendation in the account's actual direction — it does not produce a user-facing section by default, but its findings inform whether and how to surface a macro flag. PF-1 is the most urgent symptom-specific check — conversion tracking issues invalidate every other finding. A vague brief about "performance feeling off" is still a brief. All four pre-flights run.

### Step 4 — Pull data, flag everything

Run the relevant queries from the GAQL library. Don't draw conclusions yet — read the account broadly and flag anything that deviates from knowledge base standards or known good-account patterns. A flag is a candidate for investigation, not a confirmed finding.

When you hit something you can't see via the API, use the blind spot protocol from `references/diagnosis-trees.md`:

> ⚠️ **BLIND SPOT — [what cannot be seen]**
> → Please share a screenshot of [exact location, with applicable filters/date range].

**For search term reviews across more than 2 campaigns:** suggest the sub-agent pattern before pulling data (see "Using Sub-Agents" above). This is the default approach for multi-campaign pulls — don't wait for the user to ask.

**Step 4b — Creative pass (run every periodic Monday/Thursday check).** As part of pulling data, run the creative / image-asset audit — it is a standing part of every periodic check, not an optional add-on (RA accounts are moving to image/display). Keep it proportionate: inventory + usage mapping for the whole account, then vision-analyze only the subset the coverage map flags.

1. `get_image_assets` — pull the account's image-asset inventory.
2. `get_asset_usage` — map assets → campaigns/ad groups; cross-reference the ENABLED campaign list (GAQL `FROM campaign`) to find campaigns thin or missing image coverage.
3. `analyze_image_assets` (+ `download_image_asset` to confirm) — vision read on in-use assets the map flagged: on-brand, legible, message-matched to ad-group intent.
4. Flag the four checks — coverage gaps, quality/content, usage gaps (uploaded-but-unused), fatigue candidates — into the running action list (Step 5), marking each finding's source tier (API-sourceable vs. manual/visual review).

These four tools live **only in the `googleAdsServer` sidecar**; the official MCP lacks them. Full procedure, source-tier table, and blind-spot wording: `references/creative-audit.md` and the "Creative / Image-Asset Audit" section above.

### Step 5 — Maintain a running action list

This is the most important habit in multi-section sessions. As each analysis section completes, immediately append its action items to a running list — don't wait until the end. Items from section A must still be present when section C is done.

At session end, the action list is the union of every section's items. Nothing gets dropped because a later section produced its own list.

Format each item as:

```text
- [ACTION] [target] — [one-line rationale] | [scope: account/campaign/ad-group]
```

_(Toby version only)_ Update `account-notes/[account].md → ## Pending Actions` with the full list before closing.

### Step 6 — Prioritize flags by impact

Prioritize by: estimated spend impact × confidence it's a real problem. Structural issues affecting budget allocation every day rank ahead of cosmetic issues.

### Step 7 — Diagnose priority flags

For each priority flag, work through the relevant diagnosis tree. A flag becomes a finding when you can state: what is wrong, why it matters, what likely caused it, and what should be done.

### Step 8 — Produce output

- **Internal analysis** → prioritized findings list with context and recommendations
- **Client communication** → translated into plain language, focused on business impact
- **Reporting** → handled separately via AgencyAnalytics, not this skill

**Campaign → Ad Group path is mandatory in every finding.** Every keyword, search term, ad, or ad group finding must lead with the full path so the user can navigate to it in the Google Ads UI:

```text
Campaign: [campaign name] | Ad Group: [ad group name] | [keyword or term]
```

Without the campaign name, a finding is unactionable — the user cannot locate the item. This applies to every finding in every output format, without exception. A finding that omits the path is incomplete.

### Step 9 — Write session log _(Toby version only)_

Before closing the session, generate a session log using the template below. Create the `session-logs/` directory if it does not already exist, then save to `session-logs/YYYY-MM-DD-[account-name].md`.

---

## Accounts

Add your accounts here. The `login_customer_id` is your MCC ID (if using a manager account).

| Account              | ID         | Notes                                               |
| -------------------- | ---------- | --------------------------------------------------- |
| Example — Family Law | 1234567890 | See `account-notes/example-family-law.md`.          |
| MCC/Login            | 0000000000 | Use as login_customer_id when querying sub-accounts |

_(Replace with your own accounts. One row per account. Add an account-notes file for each.)_

---

## Session Log Template and Skill Development Loop _(Toby version only)_

See `references/session-management.md` for the session log template and skill development loop instructions.

---

## Audit Mode & Search-Query Mining (agency-agents mine 2026-06-02)

Net-new capability added from the paid-search division of the agency-agents mine — the highest-RA-revenue item in that mine. Turns Google Ads account access into a sellable deliverable (new-account takeover, win-back pitch, pre-scale readiness, account-health diagnosis, client-facing roadmap). **ra-clients owns scoping this against the existing eval harness and confirming googleAdsServer MCP data availability per section before treating any audit as client-ready.**

### Audit posture (PAID-1..14)

- No setting unchecked, no dollar unaccounted for.
- Automated data pull first, strategic analysis second.
- Every finding maps to business impact and is graded by severity.

### Forensic audit sections

1. **Executive Summary** — account-health verdict, top 3 risks, top 3 opportunities, expected business impact.
2. **Account Structure** — taxonomy, granularity, naming, labels, geo/device/dayparting.
3. **Bidding & Budget** — strategy fit, learning-period violations, budget-constrained campaigns, floor/ceiling issues.
4. **Keyword & Targeting** — match-type distribution, negative coverage, quality-score distribution, audience observation vs targeting.
5. **Competitive Positioning** — impression-share gaps + top-of-page metrics (API-sourced via GAQL). Auction-insights competitor breakdown + overlap rate are a known API blind spot — NOT available via GAQL; request a UI screenshot per the blind-spot protocol and never present them as auto-pulled. See `account-audit-checklist.md` §7.
6. **Landing-Page Fit** — assessed manually or with external tools (the rendered page, PageSpeed Insights, a crawler), not from the Google Ads API. Never present landing-page findings as auto-pulled.
7. **Compliance** — legal-services policy, bar-advertising claim risk, prohibited/absolute claims.
8. **Historical/Change-History Forensics** — when degradation started, what changed before/after.
9. **Recommendation Roadmap** — severity, expected impact, owner, 30/60/90-day sequencing. Add impact estimation (PAID-9) and technical→business executive translation (PAID-10).

### Search-query mining / n-gram waste (PAID-40..47)

Augments the existing negative-keyword library:

- Spend-weighted irrelevant-query detection; n-gram frequency analysis for recurring modifiers.
- Zero-conversion / high-CPC low-value query flags; query→ad→LP alignment scoring.
- Negative-keyword decision tree; tiered negatives (account / campaign / ad-group / shared lists) with conflict detection.
- Query sculpting to route searches to the right ad groups; brand vs non-brand leakage detection; competitor interception/defense.
- Output: waste table, n-gram table, recommended negatives by level, conflicts/risks, query-sculpting recs, business-impact estimate.

### Tracking-QA gate (PAID-48) — runs BEFORE any audit result is trusted

- If conversion tracking is broken/suspicious, the analysis is provisional.
- Check Ads vs GA4 / CRM / call-tracking consistency where available; flag enhanced-conversion match-rate + discrepancy benchmarks for ra-clients to validate.
- Output must say "tracking unreliable" loudly when applicable. ("Bad tracking is worse than no tracking.")

### Secondary adjuncts (not first priority)

- **RSA builder (PAID-16..18):** headline buckets, coherent combinations, character limits — cross-linked with ads-creative-development.
- **Paid-social diagnostic appendix (PAID-25..31):** funnel structure, audience engineering, frequency, SKAN/privacy mitigation, CRM tracking, MQL lead-quality KPI (PAID-31) — only if ra-clients wants legal-ppc (or a sibling) to own paid-social.
- **Algorithm-recovery module (MKTA-42):** penalty/update identification + remediation for SEO/PPC-adjacent account review.
- **ROI reporting with a spend threshold (SUP-18).**

### Eval-harness note

ra-clients to add eval cases under `evals/` for audit-mode + query-mining before this is client-facing — left to ra-clients because the harness format and Google Ads MCP data availability are theirs to confirm (per INTEGRATION-PLAN acceptance criteria 3.6).
