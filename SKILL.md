---
name: google-ads-analysis
description: Expert Google Ads analysis and optimization for law firm PPC accounts. Use when analyzing Google Ads performance, running account audits, diagnosing campaign issues, reviewing search terms, checking conversion tracking, or managing negative keywords for legal marketing clients. Trigger phrases: "analyze this account", "Google Ads audit", "why is performance down", "check campaigns", "search term review", "run a GAQL query", "this account feels off".
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
- **`references/learnings.md`** *(Toby version only)* — Validated patterns extracted from past session logs. Read this after the knowledge base to supplement with empirically-observed patterns.
- **`account-notes/[account].md`** *(Toby version only)* — Account-specific context, history, and prior findings. Read the relevant file for the account being analyzed.

---

## Reference Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `references/gaql-query-library.md` | Pre-built GAQL queries organized by diagnostic task | Any time live account data is needed |
| `references/negative-keyword-library.md` | Master negative keyword lists by category | Search term reviews, account audits, new account setup |
| `references/diagnosis-trees.md` | Diagnostic frameworks for the most common account problems | Performance diagnosis, account review, issue investigation |
| `account-audit-checklist.md` | Structured first-review audit checklist (Sections A–I, pass/fail, output format) | First-contact account review (Tree 5) |

---

## MCP Tool Note

Queries in `references/gaql-query-library.md` are pure GAQL and MCP-agnostic. Execute them using whatever GAQL execution tool is available in the current environment.

Currently: `run_gaql(customer_id, query, format)` from the `googleAdsServer` MCP.
- Prefer `format="table"` for diagnostic reads
- Use `format="csv"` for large result sets you need to process
- `run_gaql` is preferred over `execute_gaql_query` — it's a superset with output format control

If the MCP changes, update this note only. The query library remains valid.

**Login/MCC customer ID:** 0000000000
**First step in any new session:** `list_accounts()` — confirms which accounts are accessible.

---

## GAQL Query Integrity — Keywords and Search Terms

### Keyword queries (`ad_group_criterion`)

The API returns **both positive and negative keywords in the same result set**. Failing to distinguish them causes confirmed misdiagnosis.

**Mandatory rules before flagging any keyword as an issue:**

1. **Always SELECT `ad_group_criterion.negative`** when querying keywords from `ad_group_criterion`. If this field is missing from your query result, the query is incomplete — re-run using query 3.1 or 3.2 from the GAQL library before drawing any conclusions.

2. **Check `negative` before flagging.** If `negative = True`, this keyword is a negative. It is working correctly. Do NOT treat it as a positive match type issue, a quality score problem, or a waste source.

3. **Always SELECT and filter `ad_group.status`.** Keywords from paused ad groups are not serving. Do NOT flag them as active optimization targets. The standard keyword queries in the library filter `ad_group.status = 'ENABLED'` — use them.

4. **Also SELECT `campaign.status`** for the same reason. A keyword in a paused campaign is not a live problem.

**Quick check:** if a keyword query result doesn't have a `negative` column, stop. Re-run the correct query from the library. Do not proceed with analysis on an incomplete result.

### Search term queries (`search_term_view`)

`search_term_view` returns historical search term records from **all ad groups — including PAUSED and REMOVED ones**. Without filtering, results will include data from groups that are no longer serving, producing false findings.

**Mandatory rules before presenting any search term finding:**

1. **Always include `ad_group.status = 'ENABLED'` in the WHERE clause.** Same rule as keyword queries — different query type, same root cause.

2. **Check which ad group a term came from before flagging it.** If `ad_group.status = PAUSED` or `REMOVED`, that term is historical. Do NOT flag it as an active waste source or a current keyword structure problem.

3. **Status field confirms active serving.** The `search_term_view.status` field shows `NONE` for terms from paused groups — another signal to check.

**Root cause of both rules:** Google's API scopes data by account and date, not by serving status. Paused ad groups still have historical records. Always filter explicitly.

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

---

## Impression Share — Two Separate Metrics

`search_rank_lost_impression_share` and `search_budget_lost_impression_share` are not the same thing.

- **Rank-lost IS** — impressions lost because Ad Rank was too low. Fix: QS improvement, ad relevance, landing page quality, or bid adjustment. Adding budget does not help.
- **Budget-lost IS** — impressions lost because the daily budget ran out. Fix: increase budget.

**Rule:** When assessing IS, always pull GAQL 5.1 which includes both fields. Never characterize a campaign as "budget-constrained" based on rank-lost IS alone — that is a QS/LP problem requiring creative work, not spend.

---

## Using Sub-Agents for Heavy Analysis

For tasks that involve pulling and analyzing large search term datasets across multiple campaigns, spawn parallel sub-agents — one per campaign — using the `Agent` tool with `subagent_type: "general-purpose"`. This:
- Prevents search term files from consuming the main context window
- Enables parallel data pulls (faster wall-clock time)
- Keeps each agent's analysis focused on one campaign

**Pattern:**
```
Main agent → fires N sub-agents in parallel (one per campaign)
Each sub-agent → pulls search terms, runs intent categorization, returns structured summary:
  { campaign, spend_visible, spend_actual, waste_terms[], converting_terms[], flags[] }
Main agent → synthesizes all summaries into findings + action list
```

Use this pattern any time a search term review spans more than 2 campaigns.

---

## Skill Dependencies

This skill works best alongside other installed skills. Check availability at session start and use them when relevant:

| Skill | Use for | Required? |
|-------|---------|-----------|
| `xlsx` | Negative keyword upload files, bulk change sheets, structured exports | Recommended |
| `pptx` / `docx` | Client-facing reports | Optional |
| *(data skill — future)* | Statistical aggregation, complex analysis | Planned |

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
- **Conversion tracking audit** — Verify that what's being tracked is correct and complete.

**Brief clarity gate:** Before pulling any data, assess whether the brief is specific enough to target the session. A clear brief (explicit concern, named campaign, defined scope) → proceed. A vague brief ("run a review", "check performance", "see what's going on", "[account] feels off") → do two things before pulling any data:

1. **State the diagnostic entry point.** Name which Tree in `references/diagnosis-trees.md` applies — e.g., "This looks like a Tree 4 (performance drop) entry point, pending clarification" or "Defaulting to Tree 5 (account review) since no specific concern was named." Say this out loud in your response. Don't silently assume an entry point and start pulling queries.

2. **Ask 1–2 focused clarifying questions:**
   - "Is there a specific concern driving this — performance drop, budget issue, something the client flagged?"
   - "Is there a campaign or time period you want to prioritize?"

This isn't gatekeeping — it's targeting. Naming the entry point surfaces your diagnostic reasoning before any data pull and lets the user redirect you if it's wrong. Don't start pulling large datasets before knowing where to look.

### Step 2 — Verify prior session's pending actions *(Toby version only)*
Before any new analysis, read `account-notes/[account].md` and check the `## Pending Actions` section.

**If the file doesn't exist:** This is a new account with no prior session history. Note this, skip the verification step, and plan to create the file at session end using the template in the session log section. Proceed to Step 3.

For each pending item, pull current account state via GAQL and verify whether it was implemented:

- **Implemented correctly** → mark done, note the date, move to session log
- **Not implemented** → re-flag as pending, surface to user at start of session
- **Implemented incorrectly** → flag specifically with what's wrong

This closes the feedback loop. The skill recommended the action; now it confirms whether it happened and can begin attributing performance changes to specific interventions. Don't skip this even if the user hasn't mentioned it — it's how the skill builds a reliable thesis about what works in this account.

### Step 3 — Run pre-flight checks
Before any symptom-specific diagnosis, run the three pre-flight checks from `references/diagnosis-trees.md`:
- PF-1: Conversion tracking verification
- PF-2: Structural red flags
- PF-3: Change history read

All three are mandatory and none are deferred by a vague brief. Run PF-1, PF-2, and PF-3 before any symptom-specific diagnosis, regardless of brief clarity. PF-1 is the most urgent — conversion tracking issues invalidate every other finding and should be checked first. PF-2 and PF-3 follow immediately after, not after the brief is clarified. A vague brief about "performance feeling off" is still a brief. All three pre-flights run.

### Step 4 — Pull data, flag everything
Run the relevant queries from the GAQL library. Don't draw conclusions yet — read the account broadly and flag anything that deviates from knowledge base standards or known good-account patterns. A flag is a candidate for investigation, not a confirmed finding.

When you hit something you can't see via the API, use the blind spot protocol from `references/diagnosis-trees.md`:
> ⚠️ **BLIND SPOT — [what cannot be seen]**
> → Please share a screenshot of [exact location, with applicable filters/date range].

**For search term reviews across more than 2 campaigns:** suggest the sub-agent pattern before pulling data (see "Using Sub-Agents" above). This is the default approach for multi-campaign pulls — don't wait for the user to ask.

### Step 5 — Maintain a running action list
This is the most important habit in multi-section sessions. As each analysis section completes, immediately append its action items to a running list — don't wait until the end. Items from section A must still be present when section C is done.

At session end, the action list is the union of every section's items. Nothing gets dropped because a later section produced its own list.

Format each item as:
```
- [ACTION] [target] — [one-line rationale] | [scope: account/campaign/ad-group]
```

Update `account-notes/[account].md → ## Pending Actions` with the full list before closing.

### Step 6 — Prioritize flags by impact
Prioritize by: estimated spend impact × confidence it's a real problem. Structural issues affecting budget allocation every day rank ahead of cosmetic issues.

### Step 7 — Diagnose priority flags
For each priority flag, work through the relevant diagnosis tree. A flag becomes a finding when you can state: what is wrong, why it matters, what likely caused it, and what should be done.

### Step 8 — Produce output
- **Internal analysis** → prioritized findings list with context and recommendations
- **Client communication** → translated into plain language, focused on business impact
- **Reporting** → handled separately via AgencyAnalytics, not this skill

### Step 9 — Write session log *(Toby version only)*
Before closing the session, generate a session log using the template below and save to `session-logs/YYYY-MM-DD-[account-name].md`.

---

## Accounts

Add your accounts here. The `login_customer_id` is your MCC ID (if using a manager account).

| Account | ID | Notes |
|---------|-----|-------|
| Example — Family Law | 1234567890 | See `account-notes/example-family-law.md`. |
| MCC/Login | 0000000000 | Use as login_customer_id when querying sub-accounts |

*(Replace with your own accounts. One row per account. Add an account-notes file for each.)*

---

## Session Log Template *(Toby version)*

Copy this template and fill it out at the end of every session. Save to `session-logs/YYYY-MM-DD-[account-name].md`.

```markdown
# Session Log — [YYYY-MM-DD] — [Account Name]

## Brief
[One or two sentences: what triggered this session, what the stated objective was]

## Entry Point
[Which diagnostic tree was the primary starting point]
- [ ] Conversions low
- [ ] CPA too high
- [ ] Budget not spending
- [ ] Performance dropped
- [ ] Inherited account / first review
- [ ] Search term review
- [ ] Other: ___

## Diagnostic Path
[Ordered account of what was checked and why — not a polished narrative, just what actually happened]
1. [What was pulled] → [What it showed] → [What that led to]
2. ...

## Flags Raised
[Everything that looked wrong before prioritization]
- [Flag] | [Why flagged] | [Severity: High / Medium / Low]

## Confirmed Findings
[Flags that became actual findings after investigation]
- [Finding] | [Root cause if identified] | [Recommended action]

## Actions Taken This Session
[What was actually changed, not just recommended. "None" is a valid answer.]

## Blind Spots Hit
[What couldn't be diagnosed via API and whether a screenshot was obtained]
- [What] | [Screenshot obtained? Y/N] | [Outcome / what it showed]

## Open Questions
[What couldn't be resolved and why — for follow-up in next session]

## Session Observations
[The most important field. Anything surprising. Anything the current skill doesn't account for. New diagnostic patterns. Client context that matters for future sessions. If nothing is surprising, say so explicitly.]
```

---

## Skill Development Loop *(Toby version)*

Session logs accumulate in `session-logs/`. After approximately 4–8 sessions with substantive findings, run a synthesis session:

1. Read all session logs, focusing on `Session Observations` and `Diagnostic Path` fields
2. Identify patterns that appear in 2+ sessions and aren't already in the diagnosis trees
3. Propose additions or revisions to the relevant skill files
4. Review and approve before any file is updated
5. Add validated patterns to `references/learnings.md` with the date and source session log(s)

This is the mechanism by which the skill improves. The model doesn't learn — the files learn.
