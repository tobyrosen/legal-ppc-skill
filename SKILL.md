---
name: google-ads-analysis
description: >-
  Use this skill to improve the performance of Google Ads Search and Performance Max campaigns for family law, immigration law, and elder law firms. It encodes the tactics used to diagnose and fix a live account: conversion-tracking integrity, bidding targets and direction, budget and impression-share routing, keyword and match-type remediation, search-term waste, geo control, creative and asset checks, and configuration-baseline verification. Triggers include explicit requests (account audit, search term review, GAQL query, conversion tracking check, negative keyword review, impression share analysis, config-baseline verification, optimization playbook matching) and implicit ones (why is CPA high, leads are down, this campaign feels off, something changed this week, why is this not spending, performance is down). Use even if the request does not say "Google Ads": "check the campaigns", "run an audit", "performance seems off", and "why are leads down" all activate it. Does NOT cover campaign creation, keyword research for new accounts, or any advertising platform other than Google Ads.
compatibility: Requires a GAQL execution tool with Google Ads API access. Designed for Claude Code.
---

# Google Ads Analysis: Search and Performance Max for legal accounts

## Purpose

This skill is an encoded version of the tactics used to improve a Google Ads campaign for a family law, immigration law, or elder law firm. Scope is Google Ads Search and Performance Max only. The subject is campaign performance: what to check, what the data has to say before a move is on the table, what the standard move is, and what would make that move wrong.

It is not an organization layer for reporting or data management. It presents DATA, one account at a time. The analytical calls belong to the operator.

**Evidence labels.** Tactics carry an evidence tier: `validated in practice`, `partially validated`, `textbook only`, or `unconfirmed`. Unconfirmed means general practice not yet confirmed by the operator; it is presented as a candidate, never as a house tactic. `PROPOSED` on a threshold means the same thing for that number. Full definition: `references/playbooks.md`.

**Immigration note.** Immigration is in scope, but no immigration-specific tactics are encoded yet. Treat immigration accounts with the general Search and PMax tactics here and record what proves out.

---

## Data rules that gate every finding

These are prerequisites to the tactics, not presentation preferences.

**Data, not verdicts.** State what the data shows, what is likely wrong, and the decision framework that applies. Do not issue the go/no-go call ("pause it", "it's good", "scale it", "yes/no"). When asked for a straight yes/no on pause, scale, or kill, present the figures and the framework, then return the decision to the operator explicitly.

**Aligned windows only, no partial-vs-full comparisons.** Every comparison compares like with like: complete week against complete week, or the same elapsed weekday count on both sides. A Thursday Mon-Thu period is compared against the prior Mon-Thu, never against a full prior Mon-Sun. Comparing a partial window with a full one shorts the numerator by days, and the resulting decline is an artifact of the calendar, not the account.

**Conversion lag: label immature windows provisional.** Form and call conversions keep posting for days after the click (assume a 72-hour lag unless the account's own data says otherwise). A current or partial window's conversion count is a floor, not a final number. The conversion count, the conversion percentage move, and the CPL from any window still inside the lag period are labelled provisional, with the reason stated. Spend is mature immediately; conversions and CPL are not. No trend conclusion is drawn from an immature window.

**Zero-conversion comparison periods: CPL percentage is `n/a`, never invented.** When either side of a comparison has 0 conversions, the CPL percentage move is undefined. Report `CPL n/a`. Never write "infinite", never manufacture "100% better", never silently drop CPL. Report spend direction as normal, state the conversion change in absolute terms ("conversions 0 to 2", not a percentage), give the current period's CPL if it is defined, and attach the low-volume caveat. Moving off a zero-conversion period is not evidence of improvement.

**Direction ships with every figure.** A spend, conversion, or CPL number is never reported bare. Week-over-week and 30-day-versus-prior-30-day direction ships with it every time, even when the request is a one-line ask for a single number.

**Currency: report native, never assume dollars.** `cost_micros` and every cost, CPC, and CPL figure are denominated in the account's currency. Pull it (`SELECT customer.currency_code FROM customer`) and report each account in its own currency. No cross-currency total, average, or ranking without an approved FX source; when one is supplied, the rate and its effective date appear in the output. Two accounts both reading "200" in different currencies are not tied.

**Campaign to ad group path is mandatory in every finding.** Every keyword, search term, ad, or ad group finding leads with the full path so the item can be located in the UI:

```text
Campaign: [campaign name] | Ad Group: [ad group name] | [keyword or term]
```

A finding that omits the path is incomplete.

_Card format, severity ordering, layout, and the walk-card template live in the internal operations runbook, not in this file._

---

## Knowledge foundation

Precedence, highest first: a live GAQL pull, then the operator's recorded rulings and account overrides, then `references/agency-defaults.md` (the configuration baseline), then `references/google-ads-knowledge-base.md` (the legal-PPC lens). A conclusion that requires knowing current account state comes from a live query, never from a snapshot, a capture database, or a rendered note.

---

## Account macro context: a reasoning gate, not a report section

Before any item-level work, establish the account's direction on aligned complete windows: spend, conversion volume, lead volume, and CPL for the last 30 days against the prior 30, plus year-over-year where the data spans long enough. The 90-day series is context for the shape of the trend, never the comparison basis. This is pulled every session without exception.

It is a gate on the recommendation, not an output section. Surface it only when it changes the reading:

- A material trend shift, for example conversion volume down 25% or more against the prior period.
- A trend reversal.
- A contradiction with the move about to be proposed. Recommending a bid increase lands differently when account spend is already up 40% with conversions down.
- A pattern that explains other findings, for example a year-over-year drop alongside a structural change.

---

## Reference files

| File                                      | Purpose                                                                              |
| ----------------------------------------- | ------------------------------------------------------------------------------------ |
| `references/playbooks.md`                 | The optimization playbook library: trigger, standard move, do-not-move, verification |
| `references/agency-defaults.md`           | Configuration baseline: the standard value per setting, with severity                |
| `references/diagnosis-trees.md`           | Symptom-to-action routing for the common account problems                            |
| `references/google-ads-knowledge-base.md` | Why legal PPC behaves differently from general PPC                                   |
| `references/negative-keyword-library.md`  | Negative-keyword patterns by category, with the do-not-negate rules                  |
| `references/creative-audit.md`            | Search image-asset and PMax asset audit procedure                                    |
| `references/gaql-query-library.md`        | Pre-built GAQL queries by diagnostic task                                            |

---

## Execution note

Queries in `references/gaql-query-library.md` are pure GAQL and tool-agnostic. Execute them with whatever GAQL execution tool the environment provides. Prefer a table format for diagnostic reads and CSV for large result sets.

**Account scope is a hard stop.** An account listing shows what is accessible, not what is in scope. Only query accounts confirmed against the operator's current-client roster, which is maintained outside this skill. "All accounts", "every account", and "the whole manager account" always mean all roster accounts, never the full accessible list. If no roster is available, run no multi-account pull.

---

## GAQL integrity: keywords and search terms

### Keyword queries (`ad_group_criterion` and `keyword_view`)

The API returns both positive and negative keywords in the same result set, for both resources. Failing to separate them causes confirmed misdiagnosis.

1. **Always filter `ad_group_criterion.negative = FALSE`** in the WHERE clause of any keyword query. If the filter is missing, the result mixes negatives with positives. Re-run before drawing any conclusion.
2. **Check `negative` before flagging.** A keyword with `negative = True` is working correctly. It is not a match-type issue, a quality-score problem, or a waste source.
3. **Always SELECT and filter `ad_group.status`.** Keywords in paused ad groups are not serving and are not optimization targets.
4. **Also SELECT `campaign.status`.** A keyword in a paused campaign is not a live problem.

If a keyword query lacks `ad_group_criterion.negative = FALSE`, stop and re-run the library query. Do not analyse an incomplete result.

### Search term queries (`search_term_view`)

`search_term_view` returns historical records from all ad groups, including paused and removed ones.

1. **Always include `ad_group.status = 'ENABLED'`** in the WHERE clause.
2. **Always SELECT `search_term_view.status`.** If the field is missing, the query is incomplete. Do not flag any term without it.
3. **Never flag a term with `status = NONE` as an active finding.** `NONE` means the term matched historically but is no longer served by any keyword, often from a broad keyword since tightened or paused. Confirmed misdiagnosis: a fictional "quiet title action westhollow" term was flagged as active waste when it was status NONE from a paused broad keyword.
4. **Check which ad group a term came from.** A term from a paused or removed ad group is historical, not an active waste source.

Root cause: the API scopes data by account and date, not by serving status.

### Auditing search term data you are handed

The same logic applies to a pasted table, CSV, or screenshot: you did not run the query, so you do not know whether the enabled-ad-group filter was applied.

**Check CPC plausibility first.** Competitive legal terms in these practice areas typically run well above a couple of dollars a click. A handed result showing legal-intent terms under about $2 a click, especially under $1, is anomalously cheap and is a signal that the export includes paused ad-group history, which accumulates low-cost impressions from periods when CPCs were lower.

Protocol: scan the CPC column before drawing conclusions; if the CPCs look implausibly low, say so and ask which ad groups the terms came from and whether the query filtered for enabled ad groups only. Do not present terms with suspicious CPCs as active waste until the source is confirmed. If the source is a paused ad group, the terms are historical and no action is needed.

---

## Search terms that are NOT waste (standing operator ruling)

The following family and elder search terms are NOT waste. They are never flagged as waste, proposed as negatives, or used as waste evidence in an audit:

- how to file for divorce without a lawyer
- family law attorney jobs
- divorce therapist
- child support office
- pay child support online
- medicaid office phone number
- nursing homes near me

Also never waste: free consultation variants, cheap divorce, uncontested divorce online, child support calculator, divorce mediator, how long does a divorce take.

Confirmed waste: free divorce lawyer, pro bono divorce lawyer, legal aid divorce, free divorce papers, divorce lawyer salary, free elder law attorney, free will template, elder law attorney salary.

This list overrides any blanket category in `references/negative-keyword-library.md` that would catch these terms.

---

## Ebook downloads are PRIMARY conversions (standing operator ruling)

Ebook and guide downloads are PRIMARY conversions in every account and every campaign. Never Secondary, never "downloads, not leads". The ads sell the ebooks; the nurture funnel behind them produces clients, and the operator ranks them above phone calls. Any conversion-config recommendation that demotes, excludes, or discounts an ebook conversion is wrong on its face. This applies equally to CRM-native and tag-manager or analytics versions of the ebook events.

Every soft-action branch in `references/diagnosis-trees.md`, `references/agency-defaults.md` sections 3.2 and 3.3, and PB-23 is subordinate to this ruling.

---

## Smart bidding: post-tracking-fix protocol

_Playbook: PB-06 (post-tracking-fix lockdown), PB-07 (tCPA below the conversion floor), PB-08 (sub-floor volume plus high CPC)._

When conversion-tracking contamination is fixed on an account running tCPA or any smart bidding strategy, the bidding model is now invalid: it was trained on incorrect conversion data.

**Do NOT adjust the tCPA target immediately after fixing tracking.** This is the most common mistake after a tracking cleanup. The algorithm has not learned the clean-data CPA yet, so any target set now is still anchored to contaminated history. It replaces one wrong number with another.

Sequence:

1. Fix the tracking and confirm it is clean.
2. Hold the current tCPA target.
3. Announce a 2 to 4 week lockdown (`PROPOSED` window): no bid strategy change, no target change, no budget change.
4. Expect apparent CPA to rise and conversion volume to fall. That is the duplicate count disappearing, not the account getting worse. Do not react to it.
5. After the lockdown, evaluate the target against a real baseline.

Monitor during relearning: learning status, the 14-day rolling CPA (expect a rise then stabilization), impression share (may drop as the algorithm recalibrates), and absolute conversion volume.

**Rebase every comparison that spans the change.** A non-retroactive conversion change means the two sides of a week-over-week or 30-day comparison use different definitions, which can manufacture a false collapse. Reconstruct both windows from action-level data on a consistent basis, and record the effective date. Verify both the 14-day and the 28-day window after the change.

**Low-volume flag.** If the account was near its reliability floor before the fix, the cleaned volume may fall below it; consider Maximize Conversions rather than tCPA until volume recovers.

**Low-volume flag, already on Maximize Conversions with high CPC.** When a campaign is already on Maximize Conversions, running below the reliability floor, and carrying a high average CPC against its own trailing median, the algorithm is bidding blind on thin signal. The move is Maximize Clicks with a CPC cap: buy volume and rebuild conversion signal while capping runaway auctions, not another target tweak. Set a 3 to 4 week revisit and watch conversion rate, because Max Clicks optimizes for clicks.

---

## tCPA direction rule

_Playbook: PB-04._

**Only lower tCPA when actual cost per conversion is already comfortably below the current target.** Lowering it when CPA is at or above target restricts volume: it tells the algorithm to win fewer auctions, exactly when the account is struggling to generate conversions.

- **Cost per conversion well below target** (target $150, actual $90): safe to lower to capture efficiency. Move in 10 to 15% increments (`PROPOSED`), not all at once.
- **Near target** (target $150, actual $140): hold. Insufficient headroom.
- **Above target** (target $150, actual $210): do not lower. Fix root causes first: quality score, ad relevance, landing-page conversion rate, negative-keyword gaps.
- **Well above target with low impression share:** the root cause is usually bid quality, not budget. Adding budget does not fix a tCPA campaign losing impressions to rank. Diagnose rank-lost impression share.

The instinct to tighten tCPA when CPA is high is a frequently observed bidding error in legal accounts, though not established as the most common one. When the algorithm is already under pressure to find converting traffic, lowering the target means fewer auctions and fewer conversions, not cheaper ones.

**Exception:** if budget is clearly not the constraint (budget-lost impression share near zero) and rank-lost impression share is very high, the issue is bid quality, and tCPA can be raised to give the algorithm room to compete.

---

## Target setting: targets come from firm economics, not account data

_Playbook: PB-05._

A bidding target (tCPA, target CPL, target cost per signed case) is an external input. The account's current CPA tells you how performance compares to the target; it is never the source of the target.

Where a target comes from, in priority order:

1. **The firm's economics**, recorded outside this skill: average case value, lead-to-signed rate, and acceptable cost per signed case.
2. **An explicit operator override** for the task at hand.
3. **If neither exists, ask.** Do not set a target without them.

**Never back-solve a target from the account's own current CPA or spend.** Averaging what the account currently pays per conversion and calling that the target is circular: the current CPA reflects whatever is broken about current performance, so the target merely ratifies the status quo. It is a loop that can never improve the account. This is the one forbidden move in target setting, and it applies equally to the high-CPA diagnosis tree and to any smart-bidding reset.

**Worked logic:** average signed-case value $12,000 multiplied by a 15% acquisition budget share gives a $1,800 target cost per signed case; at a 30% lead-to-signed rate that is roughly a $540 target CPL. If the account's current CPL is $900, it is 67% over the external target, and that gap is the finding. The 15% acquisition share is an illustration (`PROPOSED`), not a house default.

**When the external target sits well below current performance,** the gap is the finding, not a reason to abandon the target. Fix the drivers first, then step the live target toward the economics number in increments so the algorithm does not oscillate.

---

## Campaign-level CPC anomaly: routing protocol

_Playbook: PB-33 (anomalously low CPC), PB-25 (high CPC with zero conversions), PB-08 (high CPC with sub-floor conversions)._

When campaign-level average CPC looks anomalous (the campaign summary, not the search-term level), route by direction.

**Anomalously LOW average CPC.** There are no practice-area CPC bands. Judge a campaign's CPC against its own trailing 30-day median and against the account's other campaigns, never against a published band. A campaign reading well under its own trailing median is a prompt to look, never a threshold to act on.

1. **First check: tracking integrity.** A low average CPC on competitive legal terms is a red flag for data contamination: historical data from paused ad groups, test periods when CPCs were lower, or a tracking issue inflating apparent traffic. Routing low CPC to tracking integrity before keyword targeting has a real observed basis: paused ad-group history at $0.20 a click caused a confirmed misdiagnosis.
2. **Do not route to keyword targeting first.** Explaining cheap clicks as wrong match type or low-intent keywords is the secondary frame.
3. Pull change history and confirm the CPC trajectory. If it was historically normal and recently dropped, something changed.
4. If search-term data confirms the clicks come from low-intent queries at low CPC, keyword and match-type diagnosis applies, but only after ruling out contamination.

**A PMax launch can produce the same signal at the account level.** A new PMax campaign supplying a large share of clicks at a much lower CPC than Search will drag the blended CPC down without anything being wrong. Split Search-only from PMax before treating a blended CPC move as an anomaly (PB-41).

**Anomalously HIGH average CPC.** In a high-value practice area a very high cost per click can still be rational: an expensive click that acquires a large case is not a defect. No case-value figure is on record, so none is stated. Flag a high average CPC as potentially problematic only when it combines with (a) zero or near-zero conversions over 14 or more days and (b) adequate impression share above 30%. Both numbers are `PROPOSED`. That combination suggests the algorithm is buying expensive clicks that do not convert: landing page, audience, or tracking.

**Third condition: high CPC plus sub-floor but non-zero conversions plus budget-lost impression share** routes to the bidding-strategy fix (Maximize Clicks with a CPC cap), not to the landing-page or tracking diagnosis. The zero-conversion branch points at the landing page and tracking; the thin-but-non-zero branch points at the bidding model.

---

## Search-term data: negative precision

The check reads the account's own search terms and works from what is there. It never estimates, extrapolates, or scales a figure to stand for spend it has not seen, and it never presents a derived total as though it were measured.

**Query per campaign, not per account.** One query across all campaigns returns a coarse, truncated result. Per-campaign or per-ad-group querying is the standard pull.

**Never recommend blocking a term category solely on search-term data showing zero conversions.** Account-level conversion data is authoritative for spend. A term category is checked against what the account actually converted on before any negative ships.

**Negative-keyword precision, two decision rules:**

- **Never negate a term that has converted**, no matter how much it looks like junk, a referral or nonprofit name, or a geo or category mismatch. Check the term's conversion data first: a converting term is a client, not waste.
- **On a geo-mismatched query containing the core service term, negate the geo token only.** For `[core service term] [wrong city]`, negate the wrong city, never the service term, so the campaign keeps serving in its real geography.

**Negatives come from this account's own search terms.** A proposal is built from the terms the account actually served, checked against the not-waste list above and against each term's own conversion record. The categories in `references/negative-keyword-library.md` seed a new campaign; they are never applied wholesale to a live account.

**A wasteful broad keyword that is also a major conversion source converts to phrase, it does not get paused.** When a broad-match positive keyword shows real waste but also drives a large share of the campaign's conversions, especially on a smart-bidding campaign where those conversions feed the model, pausing or deleting it throws away the volume and starves the bidding signal. The default is convert broad to phrase, add specific negatives for the irrelevant categories, and set a monitoring window before any further tightening. Pause only if the converting traffic does not survive that.

**An above-average CPA is not on its own a reason to cut a unit that supplies a large share of conversions.** An expansion ad group running above sibling CPA while producing half the campaign's conversions can be worth keeping; lifetime CPA is distorted by early dead weeks. Judge marginal contribution, not the lifetime average.

_The rules above are a required-green gate on PB-12, PB-13, PB-14, and PB-28, not playbooks themselves._

---

## Quality-score throttling: all components below average with zero impressions

Quality score is a watched signal. A falling quality score with impressions collapsing while ad rank and bid hold is a finding: it is the throttling shape, and it is reported.

The UI shows a "limited by quality score" label for severely underperforming keywords. The API does not expose it: `system_serving_status` returns `ELIGIBLE` even for a throttled keyword. This section is detection only.

**Throttled keyword pattern:** quality score of 2 or less, AND all three components below average (`search_predicted_ctr`, `creative_quality_score`, `post_click_quality_score`), AND zero or near-zero impressions over the most recent 7 to 14 days on an active campaign with available budget. This shape has a real observed case behind it: quality score 1, all three components below average, zero impressions.

**No fix is prescribed.** The rebuild tactic that used to sit here, pausing the keyword and building a fresh variant to get a clean quality signal, was retired in 2026-09 along with the playbook that encoded it (PB-15). Report the detection and hand the decision back.

State the heuristic explicitly when diagnosing. Do not present `system_serving_status = ELIGIBLE` as confirmation that the keyword is serving normally.

---

## Broad-match keyword remediation: default path

_Playbook: PB-11, with PB-12 when the keyword is also a major conversion source and PB-03 when it is front-loading the daily budget._

When a broad-match keyword is flagged for cleanup, the default is **convert to phrase match first**: not delete, not pause, not a jump to exact.

**Why phrase, not exact:** broad to exact skips the intermediate step that keeps near-intent variants while filtering the looser ones. Exact loses reach unnecessarily. Phrase before exact is the operator's own default.

**Why not delete or pause:** a broad keyword with conversion history carries smart-bidding signal. Changing match type is the lower-risk path, though it should not be assumed to preserve the criterion's history intact; verify performance after the change rather than relying on continuity.

**When a hard delete is appropriate:** for terms that are genuinely irrelevant to the firm: the wrong practice area or the wrong geography. Competitor brand terms are not in that set, and they are not in the negate set either. No action is taken on a competitor name in either direction.

Sequence: convert broad to phrase, monitor search terms for 2 to 4 weeks, then negate specific waste terms or tighten to exact if CPA is still above target.

---

## Search Partners and the blended CPA (standing operator ruling)

_Playbook: PB-26 (segment and report), PB-27 (a network setting enabled with no reason on record)._

**The blended CPA is always the reported CPA.** It is the most accurate figure for what the account actually paid per conversion, and it is never withheld, never replaced by a Search-only number, and never presented as invalid. The network split is supporting detail underneath it, never a substitute for it.

**Search Partners being enabled is flagged.** It is atypical for these accounts and it is not wanted. When it is on, report that as a flag on its own, separate from the CPA line. A specific note on the account or the campaign explaining it clears the flag; the absence of such a note does not make switching it off automatic.

Pull `segments.network` to segment `SEARCH` against `SEARCH_PARTNERS`. If network data is unavailable, say so, keep reporting the blended figure, and name the split as the next pull rather than holding the number back.

**Smart bidding signal risk.** Excluding Search Partners is not a free win: removing the network removes its conversions from the bidding signal. If the campaign is near the reliability floor for its volume, exclusion can push it below. Check the volume contribution before recommending exclusion.

Decision framework after the split. This is an unconfirmed starting frame, not a decision rule:

- Partners CPA above target and Partners volume small relative to Search: exclusion is reasonable and the signal loss is minimal.
- Partners CPA above target but Partners contributing significant volume: exclusion risk is real; check whether the blended CPA stays on target without it.
- Search CPA already on target: the issue is contained to Partners, and exclusion is the likely fix, but confirm the volume contribution first.

Partners traffic converting at a lower rate and higher CPA in legal is a general expectation, not a measured result on these accounts.

---

## Configuration ground truth: deviation from our standard, not from nothing

A configuration finding is a departure from **our** baseline, not from Google's defaults and not from a general best-practices list. `references/agency-defaults.md` is that baseline: every setting deliberately chosen, its GAQL field, the value, the reason, and the severity when an account differs. A setting matching it is not a finding.

**Why this exists.** A PMax config verification once reported `positive_geo_target_type = PRESENCE_OR_INTEREST` as a problem. It is the house standard, chosen on purpose. Nothing was wrong with the account. The check had no baseline, so it measured against Google's defaults and produced a false flag on a deliberate setting.

### Procedure

1. **Read the baseline.** Note which entries are marked PROPOSED: a PROPOSED entry produces a config item at most, never a red flag, until it is confirmed.
2. **Read the account's recorded overrides.** Departures made on purpose are recorded once, outside this skill, and are an input to the check rather than an exception to it. With no override set available, every departure is reported as a deviation and the output says the override set was unavailable.
3. **Pull live config** from the configuration baseline query set. Read the resource; never infer a setting's current value from the absence of a change event.
4. **Classify every baseline setting:**

   | Class          | Test                                                                | Output                             |
   | -------------- | ------------------------------------------------------------------- | ---------------------------------- |
   | MATCH          | live value equals the baseline standard or a stated carve-out       | not reported in a routine check    |
   | OVERRIDE-MATCH | live value differs from the baseline and equals a recorded override | one summary line                   |
   | DEVIATION      | live value differs from the baseline with no recorded override      | a flag, at the baseline's severity |

5. **Report.** Only deviations become flags. In an explicit verification request, print a compact MATCHES summary so the reader can see the classification happened. Override matches are one line, never itemised.

### Rules that bind this check

**A recorded override is never re-flagged.** Not "flagged with a note", not "mentioned for completeness". Re-raising a settled decision is the noise this section exists to remove.

**An override is established only by a recorded entry.** A mid-check assertion that "that's deliberate" does not create one. Report the deviation and note that the operator states it is deliberate and an override should be recorded to clear it.

**Positive geo target type is the worked case.** `campaign.geo_target_type_setting.positive_geo_target_type = PRESENCE_OR_INTEREST` is the house standard, in every campaign type and every account. It is a MATCH and never a flag. Legal intent frequently originates outside the service geography and presence-only targeting drops it; out-of-area waste is handled by negative geo targeting, negatives, and intake qualification. The only reportable case is the reverse: an account carrying a recorded presence-only override whose live value has drifted back.

**No baseline entry, no flag.** A setting the baseline does not cover cannot produce a config flag. If it looks wrong, it is an observation with a proposed baseline entry attached. The check does not invent standards mid-session.

**PROPOSED entries are capped at config item.** Escalating one to a red flag asserts a standard the operator has not set.

**An auto-applied Google recommendation is generally a red flag, and every one is checked.** Auto-apply is off in the baseline. Where the live account shows auto-applied changes, read every one of them against the account rather than accepting the class.

**The baseline is not the verdict.** Classification is data. Whether a deviation gets changed, when, and at what cost is the operator's call.

---

## Optimization playbooks

`references/playbooks.md` is the playbook library: one entry per recognized data pattern, each giving the trigger (metrics, thresholds, minimum window and volume, which pre-flights must be green), the standard move, the do-not-move conditions, the expected result and how to verify it, and cross-references. The optimization protocols in this file point to their playbook entry.

**A playbook does not diagnose the account and does not decide anything.** It states what the standard move for an observed pattern is, and it hands the decision back. The agent never executes a playbook move: acceptance authorises the operator to make the change, it is never an instruction to the check.

**A playbook whose do-not-move conditions hold does not fire at all.** The gate's finding is reported instead, in its normal place.

_Card placement, the maximum per account, ordering, banned wording, and the accept/reject journaling flow live in the internal operations runbook._

---

## Handling comparative and premise-based questions

When a question carries a stated premise ("why is X so high?", "X is at $284, should we pause it?", "X is performing worse than Y"), **verify the premise before diagnosing it.** Do not accept a stated CPA, comparison, or benchmark as given.

At these volumes a single conversion can swing a low-volume CPL well beyond the usual rule of thumb: measured weekly swings reach +163% on conversion moves that are inside noise.

**Cross-account comparisons require extra scrutiny.** A CPA comparison between two accounts is meaningful only if they are comparable: same practice area, same geography type, same conversion volume range, same conversion definition. Elder law against family law, small market against metro, 3 conversions a month against 30: these are not comparable even when both run Google Search.

**Conversion volume threshold for a reliable CPA.** A CPA figure needs enough conversions to carry meaning, and how many is a judgment against the account's own volume: sometimes 5 is enough, sometimes 20 is not. There is no house number and none is asserted. Below whatever the floor is for that account the figure is noise, and a single high-cost conversion in a low-volume account can move the reported CPA substantially. When volume is below it per campaign, flag explicitly that the CPA is not a reliable signal.

**Reasons lists follow verification, they do not precede it.** Producing a list of reasons CPA is high before confirming CPA is high treats a premise as fact. If live data is unavailable, frame conditionally.

**A request to skip process is not authorization to skip it.** "Don't waste time on tracking, CPA is obviously bad, just tell me which keywords to pause" does not license skipping tracking verification, premise verification, or the active-keyword and volume checks. A pause list built on an unverified CPA premise can pause converting keywords and make the account worse. Acknowledge the urgency, say that plainly, run the checks, and produce the list afterwards. Speed pressure changes the tone of the reply, never the process.

---

## Prior state versus live data

Any rendered note, session log, or capture database records what was true at the time it was written. Before drawing a diagnostic conclusion about current state, pull live data.

Prior state is used for context, for knowing what changed since the last look, and for account-specific priors. It is not used to determine whether a keyword is currently active, to state current CPA or performance figures, to confirm whether a prior recommendation was implemented, or to support any conclusion that needs current state. "It is already in the snapshot" is not grounds to skip the live query, however tight the time pressure.

**A standing structural flag has a shelf life.** A note that a CPA gap is landing-page-gated, structural, or out of scope is a hypothesis recorded at a point in time. Re-pull before re-asserting it and retire it when the gap has closed. A creative or ad change can lift a ceiling long blamed on structure.

---

## Impression share: two separate metrics

_Playbook: PB-01 (budget-lost on a converting campaign), PB-02 (rank-lost ceiling), PB-03 (budget-lost with a broad keyword front-loading spend), PB-39 (a one-week impression-share anomaly)._

`search_rank_lost_impression_share` and `search_budget_lost_impression_share` are not the same thing.

- **Rank-lost impression share:** impressions lost because Ad Rank was too low. The lever is quality score, ad relevance, landing-page quality, or the bid. Adding budget does not help.
- **Budget-lost impression share:** impressions lost because the daily budget ran out. The lever is budget.

**Rule:** always pull both fields together. Never call a campaign budget-constrained on rank-lost impression share alone.

**Rank-lost on Maximize Conversions usually points at quality, not at a bid ceiling.** The algorithm already bids what it calculates as optimal for each auction, so there is no manual bid to raise; the practical lever is quality score and landing-page quality. Check quality first. Treat this as the default reading rather than an absolute: a target-based strategy, a constrained budget, or an auction shift can produce the same metric. Operator ruling, 2026-09-02.

**Budget-lost impression share can occur without hitting the daily cap.** Broad-match keywords can consume budget disproportionately early in the day, serving high-volume lower-intent queries before more targeted phrase and exact keywords compete. In that case the fix is converting the broad keyword to phrase, not increasing budget, which just gives the broad keyword more to consume. Observed case: a $75 daily cap at $53 average daily spend still showed budget-lost from early broad consumption.

**A one-week impression-share anomaly is a hold, not a budget move.** Re-read the complete week before acting (PB-39).

---

## Creative and asset audit: Search image assets and PMax

_Playbook: PB-21 (PMax asset coverage gap), PB-22 (PMax asset fatigue), PB-19 (responsive search ad hygiene), PB-20 (creative staleness and click-through decline)._

Scope is Search ad assets and PMax asset groups. Display and Demand Gen are out of scope.

A creative pass is a standing part of every periodic check, kept proportionate: a focused pass, not a forensic teardown. Operator ruling, 2026-09-02: it runs on every check.

What the pass covers, with full detail in `references/creative-audit.md`:

- **Coverage.** Map every enabled PMax asset group against its asset inventory and flag groups thin on or missing image assets, as a LOW finding: PMax can legitimately run without images. Do not flag a pure Search campaign for lacking image assets it does not use.
- **Quality and content.** Three bars: on-brand, legible, and message-matched to the ad group's intent. Vision analysis is a strong first read; the brand and compliance call on a legal client is a manual review. Incorrect information or a compliance issue on a live ad is the highest-ranked creative finding there is.
- **Usage gaps.** Assets uploaded but attached to nothing.
- **Fatigue.** Long-running unchanged assets, cross-referenced against change history. Where per-asset performance is thin, fall back to ad-group or campaign click-through rate as a proxy and say so. Do not over-call fatigue on low volume.

**Mark the source tier on every creative finding.** Inventory, usage mapping, coverage gaps, and file downloads are API-sourceable. Image content is API-assisted through vision, which is a read and not a verdict. The on-brand, compliance, and message-match call is a manual review, per-asset performance is only partially API-sourceable, and how an asset renders in a live placement is a blind spot: request a screenshot. Never present a brand or compliance verdict resting only on vision as confirmed.

**A policy-limited asset group is not a creative-quality finding.** When a serving PMax asset group becomes policy-limited while its individual assets remain approved, obtain the human-readable policy reason, appeal where appropriate, record the appeal date, and hold asset edits until it resolves. Report serving separately from policy clearance: continued spend does not mean the limitation cleared (PB-18, PB-32).

---

## How to approach a session

### Step 1: establish the brief

Every session has a brief: a specific concern, or a periodic review. Common types are performance review, issue investigation, account audit, search-term review, ad-copy review, creative audit, and conversion-tracking audit.

**Brief clarity gate.** A clear brief proceeds directly. A vague one ("run a review", "check performance", "this account feels off") gets three things: name the diagnosis tree that applies and say so out loud; run the pre-flights anyway, because they never wait for clarification; then ask one or two focused questions using what the pre-flight found. This is targeting, not gatekeeping.

The economics questions belong here: what a signed case is worth, the lead-to-signed rate, and which conversion actions the firm counts as real leads. Without them there is no target to measure against.

_Reviewing prior pending items at session start is an operating step; it lives in the internal operations runbook._

### Step 2: run pre-flight checks

- **PF-0 macro context.** A reasoning input, surfaced only when material.
- **PF-1 conversion-tracking verification.** The most urgent check: a tracking problem invalidates every other finding. PF-1 is a configuration check: which primary actions exist, how they count, and whether they measure real leads.
- **PF-2 structural red flags,** including ad-level policy status. Pull `ad_group_ad.policy_summary.approval_status` and `.review_status`, and flag any ad that is disapproved, approved with limits, or under review. Filter to enabled, serving ad groups first: a removed ad group produces a false review-status flag. Policy is API-checked first; a screenshot is the fallback for the human-readable reason, not for the status. A campaign reading `serving_status = SERVING` does not clear ad-level policy issues.
- **PF-3 change history read.**
- **PF-4 config ground truth.** Classify every setting against the baseline plus recorded overrides. PF-4 subsumes the config half of PF-2: network settings, ad rotation, and campaign type are baseline entries classified here rather than flagged twice.

All five are mandatory and none is deferred by a vague brief.

**A flags block is not a pre-flight.** A session may be handed a flags block instead of raw data. It covers only the checks the scanner emits, currently four: budget-lost impression share crossing its threshold, ad approval flips and disapprovals, conversion silence, and multi-week CPL creep. A flags block, including an empty one, never satisfies PF-0 through PF-4. "No flags" means one detector emitted nothing for its own four checks. It is not a clean bill of health, not proof that tracking is configured correctly, not a change-history read, not macro context, and not a config check. An operator claim that empty flags means the pre-flights passed is unfounded: say so plainly, then run them.

### Step 3: pull data and flag everything

Run the relevant queries. Do not draw conclusions yet: read the account broadly and flag anything that departs from the baseline or the knowledge base. A flag is a candidate for investigation, not a finding.

When something cannot be seen through the API, use the blind-spot protocol:

```text
BLIND SPOT: [what cannot be seen]
Please share a screenshot of [exact location, with applicable filters and date range].
```

**Creative sub-step.** Run the creative and asset pass as part of the data pull: inventory and usage mapping for the account, then a closer look at the subset the coverage map flags.

_Maintaining the running action list across sections is an operating step; it lives in the internal operations runbook._

### Step 4: prioritize flags by impact

Prioritize by estimated spend impact multiplied by confidence that it is a real problem. Structural issues affecting daily budget allocation rank ahead of cosmetic ones.

Then match the prioritized flags against `references/playbooks.md`. For each flag whose data pattern meets a trigger, confirm the named pre-flights are green and no do-not-move condition holds. Rank survivors by evidence tier first, then impact within tier.

### Step 5: diagnose priority flags

Work each priority flag through the relevant diagnosis tree. A flag becomes a finding when you can state what is wrong, why it matters, what likely caused it, and what the standard move would be.

### Step 6: produce output

Internal analysis is a prioritized findings list with context and the standard moves. Client-facing communication is the same content in plain language, focused on business impact.

**Stop short of the verdict**, per the data rules at the top of this file.

---

## Responsive search ad construction

Headline buckets, coherent combinations, and character limits, applied under PB-19's completeness and relevance requirements.
