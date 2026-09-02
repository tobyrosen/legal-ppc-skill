<!-- markdownlint-disable MD025 -->

# Optimization Playbooks: Legal PPC

The standard move for a recognized data pattern, written down once so a check does not re-derive it.

A playbook is not a verdict. The check presents DATA; the analytical calls belong to the operator. A triggered playbook adds exactly one labelled line to the walk card saying what the standard move for that pattern is. The operator accepts or rejects it. **The agent never executes a playbook move**, before or after acceptance.

---

## The Evidence field

Every entry carries an `Evidence:` line with one of three values. It says where the entry came from, and it decides precedence.

- **`validated in practice (n outcomes)`**: the move has been made on a live account and the result measured, n separate times. The entry's abstract states the conditions, the direction and rough magnitude of what happened, and how long it took to show up. A validated entry may record a move that FAILED: a measured failure is evidence, and it usually lives in the entry's do-not-move block.
- **`partially validated`**: either the pattern's detection is confirmed but the fix has never been executed, or the one measured outcome is confounded by a simultaneous change.
- **`textbook only`**: correct as far as platform mechanics go, never yet tested on an account we run. Not wrong; unproven.
- **`unconfirmed`**: general practice not yet confirmed by the operator; it is presented as a candidate, never as a house tactic. It appears as a `(unconfirmed)` marker on the individual claim or threshold, or as an `**Evidence.** unconfirmed` line where a whole section or gate carries it. A `PROPOSED` threshold is unconfirmed by definition and carries only the one tag.

**Precedence.** When two entries match the same pattern, the validated one outranks the textbook one, and its abstract governs the expected result. The 3-card-line cap per account still holds: within that cap, rank validated entries above textbook ones before ranking by spend at stake.

**Tally after the 2026-09 refresh and the evidence-verdict pass.** 40 playbooks: 13 `validated in practice`, 12 `partially validated`, 15 `textbook only`. Before the refresh: 39 playbooks, 13 validated, 8 partially validated, 18 textbook. Changes in the refresh: PB-15 retired; PB-40 and PB-41 added; PB-06, PB-32 promoted from textbook to partially validated; PB-39 incremented to 3 outcomes; PB-34 extended to eight sequential readings.

The verdict pass on 2026-09-02 changed no tier. It resolved the unconfirmed markers themselves: markers on claims the operator confirmed were removed, claims contradicted by measured outcomes were rewritten or killed, and practice-area CPC bands, the search-term coverage ceiling, and the fixed conversion floor came out everywhere. 11 `unconfirmed` markers remain in this file, all on windows and thresholds nobody has yet run to completion. 35 `PROPOSED` tags remain.

**Reading the abstracts.** Magnitudes are stated as ranges and directions, never as a promise. A range drawn from one or two outcomes is a prior, not a forecast. Where an outcome contradicts the textbook move, the entry says so in a `Contradiction` note and the entry has been rewritten to what actually worked.

---

## Legal PPC realities

Every threshold and every expected result below sits inside these five facts. An entry that reads sensibly for e-commerce can be actively wrong here.

**1. Volume is low, and the reliability floor gates out most playbooks most of the time.** Practice-area campaigns routinely run 0 to 12 conversions a week; whole accounts run 4 to 8 in the harder categories. Weekly CPL swings of +/-150% happen on conversion moves that are pure noise. The working resolution: **read the 30-day window for any CPL verdict, and read the week only for direction, and only when a change landed inside it.** A week is evidence of serving, not of performance.

**2. Consideration windows are long, and informational queries are real prospects.** Some legal markets have a structural waiting period before the matter can even be filed, which creates months of research behavior before any contact. Informational queries can be genuine top-of-funnel in these markets, which the operator's not-waste list confirms for the family and elder terms it names. Do not apply generic informational-intent negatives without checking whether those queries convert in this account first. Competitor-name queries are not a lever in either direction: they are not targeted deliberately and they are not negated, and no instruction to do either belongs in this file.

**3. Call-tracking uploads are the primary phone signal; Google-side call conversions are secondary.** The call-tracking platform is where the qualified-call signal lives, and its own qualification filter sits between the phone ringing and a conversion being counted, so a live campaign can legitimately show zero conversions while the phone rings. Google obscures its own call data, and tuning the Google-side call-length threshold is low-priority work. Report the Google call figure; do not build a diagnosis on it, and never call a low-volume zero week a tracking break without checking the sibling primaries.

**4. Nothing is judged on CPL below the reliability floor, and the floor is a judgment, not a fixed number.** How many conversions a window needs before CPL means anything depends on the account's volume: sometimes 5 is enough, sometimes 20 is not. There is no house number, and one must never be asserted as though there were. Below whatever the floor is for that account, the arithmetic is noise dressed as a metric. Three playbooks deliberately target the sub-floor case (PB-07, PB-08, PB-09) because at low volume the answer is a structural change, not a target tweak. Every other entry stays silent there.

**5. Seasonality is real, per practice area, and is the standard excuse for a slide.** Because a seasonal claim is cheap to make and expensive to act on, it needs a same-period-last-year check before it is stated as fact.

**And the one that outranks all five: intake quality beats raw lead count.** A cheap conversion is not a client. Cost per lead is a proxy for cost per signed case, and the two have been observed diverging by geography inside a single account. Any CPL comparison across markets, campaigns or geographies is provisional until leads have been matched back to the firm's CRM. Say so when presenting one.

---

## Needs operator confirmation (PROPOSED thresholds)

Every threshold below was set by judgment while writing this file, not by an existing rule in `SKILL.md`, the knowledge base, the diagnosis trees, or the audit checklist. Each is marked `PROPOSED` at its point of use. Confirm, change, or drop them.

| #   | Playbook | Proposed threshold or step                                                                                                                                                                                                                        |
| --- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | PB-01    | Trigger at budget-lost IS >= 20% for 2 consecutive complete weeks (`PROPOSED`). Step size is a default, not a rule: 20 to 30% of current daily budget ordinarily, with explicit exceptions up to doubling or tripling where circumstances demand. |
| 2   | PB-02    | Trigger at rank-lost IS >= 40%.                                                                                                                                                                                                                   |
| 3   | PB-03    | "BROAD keyword front-loading spend" = one BROAD keyword taking >= 40% of the campaign's daily spend before 10:00 account time.                                                                                                                    |
| 4   | PB-05    | The 15% acquisition-budget share in the SKILL.md worked example is an illustration only. Treat the percentage as a firm input; confirm whether a house default exists.                                                                            |
| 5   | PB-07/08 | "High avg CPC" = at or above the campaign's own trailing 30-day median CPC and high against the account's other campaigns. There are no practice-area CPC bands.                                                                                  |
| 6   | PB-08    | CPC cap set at or slightly below the campaign's trailing 30-day median CPC.                                                                                                                                                                       |
| 7   | PB-09    | No CPL judgment on a new campaign until it clears the reliability floor for its own volume or 30 days live, whichever is later, except a deliberately budget-capped market test (PB-35).                                                          |
| 8   | PB-12    | "Also a major conversion source" = the keyword supplies >= 25% of the campaign's conversions in the window.                                                                                                                                       |
| 9   | PB-13    | N-gram negative candidate = an n-gram carrying >= 3% of the campaign's search-term spend with zero conversions over >= 60 days.                                                                                                                   |
| 10  | PB-16    | Duplicate = same keyword text with overlapping match type in 2+ ENABLED ad groups of the same campaign, both with impressions in 30d.                                                                                                             |
| 11  | PB-17    | Long-term bleed = 90-day spend >= 2x target CPL with zero conversions.                                                                                                                                                                            |
| 12  | PB-19    | RSA hygiene floor = 8 headlines, 3 descriptions, no more than 2 pinned headlines.                                                                                                                                                                 |
| 13  | PB-20    | Creative staleness = no meaningful ad edit in 6 months (existing checklist item) AND CTR down >= 15% over 3 months (proposed).                                                                                                                    |
| 14  | PB-21    | Thin image coverage = fewer than 3 image assets, or fewer than 2 aspect ratios, on an image-serving campaign.                                                                                                                                     |
| 15  | PB-23    | Config drift = a primary that fired weekly goes silent for 14+ days with meaningful clicks. (The checklist's 30-day silence rule stands for never-fired and long-silent actions.)                                                                 |
| 16  | PB-24    | Call anomaly = primary call action down >= 50% vs its trailing 4-week average while form actions hold, or up >= 2x.                                                                                                                               |
| 17  | PB-25    | LP blocker = `post_click_quality_score` BELOW_AVERAGE on keywords carrying >= 25% of campaign spend.                                                                                                                                              |
| 18  | PB-28    | Geo leakage = out-of-area terms >= 10% of the campaign's search-term spend.                                                                                                                                                                       |
| 19  | PB-29    | CPL creep = 30d CPL up >= 20% vs prior 30d with conversions inside +/-10%, holding for 2 consecutive checks.                                                                                                                                      |
| 20  | PB-30    | "Material spend" in a zero-conversion streak = at least 1x target CPL spent in the window.                                                                                                                                                        |
| 21  | PB-31    | Seasonality confirmed = the same period last year is within +/-15% of the current period.                                                                                                                                                         |
| 22  | PB-32    | PMax post-launch cadence: the day-14 full configuration and goals read. The day-3 verify-poll is no longer a proposal; it is validated on two launches.                                                                                           |

### Thresholds that are NOT proposals

The windows in the six validated entries added in the 2026-08-18 revision (PB-34 to PB-39) came from measured outcomes, not from judgment, and are marked `MEASURED` where they appear. They are still small samples, usually one or two outcomes, so they are priors rather than settled numbers: the four-to-six-week ramp absorption window in PB-34, the three-day and seven-day read points in PB-35, the three-day auto-pause check in PB-36, the two-to-four-week starvation read in PB-38, and the one-week-is-not-a-pattern rule in PB-39. Treat them as the best evidence we have and update them as more outcomes land, rather than confirming them once and freezing them.

---

## How a playbook flows

1. **Detect.** The pattern is present in the pulled data, at or beyond its stated threshold, over its stated minimum window and volume.
2. **Gate.** The named pre-flights are green, and no do-not-move condition holds. A failed hard gate kills the card line: the playbook does not fire, and the pre-flight finding is reported instead. A pre-flight marked **caveat-and-fire** does not kill the line: the line fires with the stated caveat, and the standard move starts with the missing pull.
3. **Rank and cap.** At most 3 playbook lines per account per card. Rank by evidence first, then by impact: a `validated in practice` entry outranks a `partially validated` one, which outranks a `textbook only` one; within the same evidence tier, rank by spend at stake times confidence the pattern is real. Untriggered and gated playbooks are silent. Triggered playbooks that miss the cap are not silent: they are named on the surplus line. If two entries match the same pattern and disagree, the validated one governs and the other does not fire at all.
4. **Present.** The `PLAYBOOKS:` group on the walk card, after the `RED FLAGS:` block. One `playbook PB-nn:` line per carded entry. Never phrased as a judgment on the account. Empty form and surplus wording: Card-line grammar below.
5. **Operator decides.** Accept or reject. Execution is the operator's, in the UI.
6. **Journal.** Accept becomes a `decision` entry with `expect.statement` and `expect.review_by` set to the playbook's verification window. Reject becomes a `decision` entry recording the rejection, so the same line does not resurface next check.

### Card-line grammar

The group sits immediately after the `RED FLAGS:` block. Header text is literal: `PLAYBOOKS:`

```text
PLAYBOOKS:
playbook PB-nn (<scope>): standard move for <the pattern in the data> is <the move>. accept/reject
```

Empty form, when none fire (this is the entire PLAYBOOKS block, analogous to `RED FLAGS: none`):

```text
playbooks: none fired
```

A card line is a pattern paired with a standard move, ending `accept/reject`. Naming a PB id without a move (the surplus line, a gated-candidate mention) is not a card line.

`<scope>` is the campaign name. Use `account` when the pattern is account-wide.

The line names a pattern and the standard move for that pattern. It never characterises the account. Banned in a card line: "should", "needs", "recommend", "underperforming", "the problem is", any go/no-go. If a line cannot be written without one of those, the playbook does not fire. Restate the observed value from the data, not the trigger threshold.

**Surplus (N triggered, 3 carded, rest journaled).** When more than 3 trigger, card 3 and acknowledge the rest. Worked example:

```text
PLAYBOOKS: 4 triggered, 3 carded
playbook PB-02 (Northbridge - Estate Litigation): standard move for rank-lost IS 58% on a converting campaign with page ownership confirmed is a landing-page relevance pass before any bid change. accept/reject
playbook PB-24 (account): standard move for call conversions down 61% vs the trailing 4-week average is a call-tracking route check before any bidding read. accept/reject
playbook PB-11 (Northbridge - Trust Disputes): standard move for a BROAD keyword carrying 44% of spend at zero conversions over 30 days is pausing it and adding the phrase-match equivalent. accept/reject
surplus journaled: PB-21
```

`surplus journaled: PB-nn` (comma-separated when more than one) is the exact surplus line. It is not a move line and does not end `accept/reject`.

### Universal do-not-move conditions

These override every entry below. When any of these holds, no playbook fires on the affected scope.

The gates are enforced as written. Where a window or a number below is still a proposal, that is marked at the point of use, and it does not make the gate optional: an unconfirmed gate still blocks the playbook.

- **Learning period.** Any bid-strategy, budget, or targeting change inside the last 14 days on the campaign. Each change resets the clock. (unconfirmed window)
- **Below the reliability floor.** Too few conversions in the window being read for the figure to mean anything, unless the playbook explicitly targets low volume (PB-07, PB-08, PB-09). The floor is volume-dependent judgment for that account, not a fixed count.
- **Tracking not verified.** PF-1 not run, a primary silent, or a suspected duplicate. Every downstream figure is unreliable.
- **Immature window.** The window is still inside the ~72-hour conversion lag. Provisional conversions and CPL cannot trigger a move. (unconfirmed lag figure)
- **Standing rule or open decision covers it.** An open operator rule, or a decision whose review date has not arrived, holds the item. Do not re-raise what the operator already closed.
- **Currency or comparison invalid.** Partial-vs-full windows, cross-currency aggregates, zero-conversion CPL percentages.

---

## Index

Ordered by evidence within each theme: validated entries first, then partially validated, then textbook. `V` = validated in practice, `P` = partially validated, `T` = textbook only. This index carries the reading order. In the body each entry sits in its theme section and keeps its own number, so cross-references stay stable and new entries append rather than renumber (which is why PB-38 and PB-39 sit inside the keyword and budget sections rather than at the end).

**Budget and impression share:** PB-01 `V`, PB-39 `V`, PB-02 `V`, PB-40 `P`, PB-03 `T`
**Bidding:** PB-08 `V`, PB-09 `V`, PB-04 `T`, PB-05 `T`, PB-06 `T`, PB-07 `T`, PB-10 `T`
**Keywords and search terms:** PB-14 `V`, PB-38 `V`, PB-11 `P`, PB-13 `P`, PB-12 `T`, PB-16 `T`, PB-17 `T`
**Ads and creative:** PB-20 `V`, PB-18 `P`, PB-19 `T`, PB-21 `T`, PB-22 `T`
**Tracking and measurement:** PB-24 `V`, PB-25 `P`, PB-23 `P`
**Network and geography:** PB-27 `P`, PB-26 `T`, PB-28 `T`
**Account-level patterns:** PB-34 `V`, PB-35 `V`, PB-36 `V`, PB-37 `V`, PB-30 `P`, PB-29 `P`, PB-32 `P`, PB-41 `P`, PB-31 `T`, PB-33 `T`

The four account-level validated entries (PB-34 ramp, PB-35 small-cap geo test, PB-36 reactivation, PB-37 external change) are the ones most likely to change a decision, and PB-37 should be read before any performance data on any account.

PB-15 retired 2026-09. Ids are never renumbered: PB-15 is not reused.

---

# Budget and impression share

## PB-01: Budget-lost IS on a converting campaign

**Evidence.** `validated in practice (3 outcomes)`

_What happened when we did it._ Raising a daily budget into real budget-lost headroom, on a campaign already converting below the account's blended CPL, bought volume. Across two campaigns a doubled cap moved spend +88% and conversions +67% over the following fortnight, at a CPL premium of roughly 15%. Serving and impression share moved inside 7 days, conversions inside 14. Two corrections to the textbook version: one step does NOT clear budget-lost, it roughly halved per step from a 55-70% base and needed two steps plus time; and CPL does not hold flat, because buying deeper into the same auction costs more per lead. The same move made into campaigns with ZERO conversions in the prior fortnight bought pure auction price and nothing else, which is now a do-not-move condition below.

**Trigger.** `search_budget_lost_impression_share` >= 20% (`PROPOSED`) on a campaign whose CPL for the same window is at or below the firm's target CPL, sustained across 2 consecutive complete weeks (`PROPOSED`), with >= 15 conversions in the trailing 30 days. Pull both IS fields together via GAQL 5.1: a rank-lost figure never triggers this playbook.

**Pre-flight green.** PF-1 (tracking verified, primaries firing), PF-3 (no budget or bid-strategy change in the last 14 days). Target CPL must exist as a firm input (PB-05); without it there is no "converting at target" test and this playbook does not fire.

**Standard move.** Raise the campaign's daily budget in one step, then hold every other setting for 14 days. Budget only: no simultaneous tCPA change, no keyword or targeting edit in the same window, because two changes at once make the read unattributable. That isolation rule is evidenced. The one-step-per-14-days cadence is separate and stays `PROPOSED`. State the step size on the card line.

Step-size rule. There is no hard rule here. The step is a default with explicit exceptions, never a ceiling.

- Default: 20 to 30% of current daily budget. This is what an ordinary step looks like on an established budget.
- Exception: where the circumstances demand it, a much larger step is legitimate, up to doubling or tripling the daily budget. The measured case doubled a small test-sized cap and it worked.
- The usual reason to exceed the default is a low, test-sized daily cap with high budget-lost, where a 20% step is not a meaningful test at all. Size the step to the cap instead.
- Whatever the step, state it on the card line with the reason, so the operator is deciding on a number and not on a rule.

**Do not move when.** Rank-lost IS is the larger of the two components (go to PB-02). The campaign's CPL is above target (buying more of an unprofitable auction). **The campaign has zero conversions in the trailing fortnight, whatever its budget-lost figure says.** This is the measured failure case: the same raise made into two zero-conversion campaigns moved spend up 44 to 74% while clicks stayed flat or fell and avg CPC rose 68 to 74%, and in one of them impression share actually FELL. With no conversion signal, extra budget is spent on auction price, not on volume. Route to PB-30 or PB-08 instead. One BROAD keyword is front-loading the daily spend (go to PB-03). The campaign is inside a learning period or a post-tracking-fix lockdown (PB-06). Conversions in the window are provisional. Budget-lost has been over threshold for only one week: on low-volume campaigns the figure oscillates by 20 points week to week and has been observed halving on its own with no change made. The account's total budget is fixed and the raise would have to come out of a better-performing campaign, which is an allocation decision, not a playbook.

**Verification window.** Serving and impression-share change: readable at 7 days. Conversion effect: readable at 14 days. Conversions in the first week are provisional. Re-read: GAQL 5.1 for both IS components, GAQL 6.1 for spend, conversions, and CPL over the 14 days after the change against the 14 days before.

**Expected result.** Budget-lost IS falls and impressions rise; conversions follow inside 14 days. Expect a CPL premium rather than a flat CPL: in the validated case, conversions rose about two thirds while CPL rose about 15%, because the added spend buys deeper into the same auction. Expect the budget-lost figure to roughly halve per step from a high base rather than clear: getting from the 50-70% range down to single digits took two steps plus several weeks.

If conversions do not move at all while spend and avg CPC both rise, the raise has failed. Step the budget back and route to PB-30: this is the failure signature from the measured case, and it shows up inside one week.

**Card line.**

```text
playbook PB-01 (Westhollow - Divorce): standard move for budget-lost IS 25%+ on a campaign converting at target is a single 20 to 30% daily budget step, then hold 14 days. accept/reject
```

**Related.** SKILL.md "Impression share: two separate metrics"; diagnosis trees Sub-tree A; audit checklist Section 6; knowledge base "Bidding". Cross-refs PB-02, PB-03, PB-05.

---

## PB-02: Rank-lost IS ceiling

**Evidence.** `validated in practice (2 outcomes)`

_What happened when we did it._ A rank-lost ceiling held at 52-67% for over ten weeks on an account whose budget-lost sat at 0-8% throughout. A daily budget raise made into it changed nothing, exactly as the metric predicts, while 30-day CPL climbed by roughly half. The quality lever was correctly identified and then proved unexecutable: the landing page belonged to a third party and access has been an open client ask for about three months. Second outcome, on a different account: where every enabled ad in a sensitive category sits permanently limited by policy, rank-lost in the 50%+ range is partly a policy reach ceiling and Quality Score work will not move it. Time to signal on the failed money lever: nothing at 30 days, nothing at 60.

**Trigger.** `search_rank_lost_impression_share` >= 40% (`PROPOSED`) and dominant over budget-lost IS on an ENABLED campaign with meaningful spend over 30 days.

**Pre-flight green.** PF-2 (no ad-level policy issue suppressing reach: a DISAPPROVED or APPROVED_LIMITED set produces a reach ceiling that looks like rank loss, and that is PB-18, not this). PF-1.

**Standard move.** Route to quality work, not spend. In order: pull QS components (GAQL 3.1) for the campaign's spending keywords, fix the weakest component first (landing page, then ad relevance, then expected CTR), and hold budget and bid strategy unchanged while it lands. On a Maximize Conversions campaign there is no bid ceiling to raise, so the move is quality work only. On tCPA with budget-lost IS near zero, raising the target is the one bid-side lever that is legitimate here, in 10 to 15% steps (unconfirmed).

**First, establish who owns the landing page.** If the page belongs to a third party the firm does not control, this stops being an in-account move. It is a client-relationship escalation with a multi-month clock, and it should be stated once, as an access ask with an owner and a date, then carried as a standing condition. Re-presenting it as an available move at every check is the failure mode we actually committed: on one account the same rank ceiling was re-raised across roughly three months while the only real lever sat behind someone else's code access. If the page IS ours, the move is real and PB-25 sequences it.

**Second, check whether the ad set is policy-limited before attributing anything to Quality Score.** Where every enabled ad in a sensitive practice area sits limited by policy, part of the rank-lost figure is a reach ceiling that quality work cannot move (PB-18).

**Third, do not skip the cheap lever.** Before concluding the ceiling is structural, note that an ad refresh alone has been measured closing a CPA gap that had been attributed to a landing page for months (PB-20). Ad relevance is the component you can move this week without anyone else's permission.

**Do not move when.** The campaign is on Maximize Conversions and someone proposes a bid or budget change: there is nothing to raise. Rank loss is rising alongside CPC with stable QS, which is competitive pressure, not an account defect (go to PB-31 or accept the new auction price). Ads are limited by policy.

**Expected result and verification.** QS components move off BELOW_AVERAGE within 30 to 60 days; rank-lost IS falls after that, not before (unconfirmed). Verify at 30 and 60 days: GAQL 3.1 for components, GAQL 5.1 for rank-lost IS. Nothing here verifies inside one check cycle, so do not re-fire the playbook at the next check.

**Card line.**

```text
playbook PB-02 (Westhollow - Custody): standard move for rank-lost IS 40%+ is QS and landing-page work, budget held flat, no bid change. accept/reject
```

**Related.** SKILL.md "Impression share: two separate metrics" (on Maximize Conversions, rank-lost usually points at quality, check quality first); diagnosis trees Sub-tree A and Sub-tree B; audit checklist Section 7. Cross-refs PB-01, PB-18, PB-25.

---

## PB-03: Budget-lost IS with a BROAD keyword front-loading spend

**Evidence.** `textbook only`

**Trigger.** Budget-lost IS present on a campaign that is not hitting its daily cap late in the day, plus one BROAD-match positive keyword consuming >= 40% (`PROPOSED`) of the campaign's daily spend before 10:00 account time.

**Pre-flight green.** PF-1. Keyword query filtered `ad_group_criterion.negative = FALSE` and `ad_group.status = 'ENABLED'`: an unfiltered result mixes negatives into the keyword list and this trigger becomes meaningless.

**Standard move.** Convert the BROAD keyword to phrase match. Do not raise the budget: more budget gives the same keyword more to consume early in the day. Add negatives for the irrelevant query categories the term is catching, then re-read budget-lost IS after 14 days.

**Do not move when.** The BROAD keyword is also a major conversion source, in which case the phrase conversion still applies but the sequencing and monitoring of PB-12 governs. The dayparting evidence is absent: without hour-of-day spend, this is an unproven hypothesis and the honest output is PB-01 or a blind-spot note, not this.

**Expected result and verification.** Spend spreads across the day, budget-lost IS falls without a budget increase, CPL holds or improves. Verify at 14 days: GAQL 5.1, GAQL 10.4 (daypart), and search terms for the converted keyword.

**Card line.**

```text
playbook PB-03 (Westhollow - Divorce): standard move for budget-lost IS with one BROAD keyword taking most of the early-day spend is broad to phrase, budget unchanged. accept/reject
```

**Related.** SKILL.md "Impression share" (budget-lost without hitting the daily cap) and "BROAD Match Keyword Remediation"; diagnosis trees Tree 6. Cross-refs PB-01, PB-11, PB-12.

---

## PB-39: Single-week impression-share flip on a low-volume campaign

**Evidence.** `validated in practice (3 outcomes)`

_Refresh 2026-09._ Increment from 2 to 3. The final recorded outcome showed budget-lost impression share reverting from the mid-30% range to about 1% after the accepted hold, while rank remained the actual ceiling.

_What happened when we did it._ An account with a months-long stable pattern (rank-lost high, budget-lost at zero) inverted in a single week: budget-lost went 0% to 37%, total impression share fell by roughly a third, while weekly spend FELL. Held with no action. Three to four days later the flip had gone and the original pattern was back, unchanged, with nothing touched. Second outcome, on a different account: a campaign's budget-lost figure fell from 55% to 33% on its own inside four days with conversions holding, while it was being deliberately held. Time to signal on both: 3 to 4 days.

**Trigger.** A campaign's impression-share components move sharply against their established multi-week pattern in a single week, and at least one of the following is true: the campaign is below the conversion reliability floor; weekly spend moved in the opposite direction to what the flip implies (budget-lost rising while spend falls is internally contradictory); no change event landed in the window.

**Pre-flight green.** PF-3 (change history pulled for the window: a flip WITH a change behind it is not this playbook, it is the change's own verification). Both IS components pulled together via GAQL 5.1, with spend for the same window alongside.

**Standard move.** Hold, and say why on the card: name the contradiction in the data, state that one week is not a pattern on this campaign, and set the re-read for the next check rather than proposing anything. Carry it as a watch item with an explicit expiry: if the flip is still present at the second consecutive check, it becomes a real trigger and routes to PB-01 or PB-02 on its own merits.

**Do not move when.** This playbook is itself a do-not-move, so the question is when it does not apply: a flip with a change event behind it, a flip on a campaign well above the reliability floor with consistent spend, or a flip sustained across two consecutive complete weeks. Any of those and the ordinary entries govern.

**Expected result and verification.** The most likely outcome is that the figure returns to its established band on its own within one check cycle, which is what happened both times we measured. Verify at the next check: GAQL 5.1 for both components plus spend for the same window. If it has reverted, record the reversion so the same flip does not get re-raised the next time it appears.

**Card line.**

```text
playbook PB-39 (Westhollow - Probate): standard move for a one-week impression-share flip against a stable multi-week pattern, on a sub-floor campaign, is hold and re-read at the next check. accept/reject
```

**Related.** Universal do-not-move conditions ("Below the reliability floor"); Legal PPC realities item 1. Cross-refs PB-01, PB-02, PB-30.

---

## PB-40: Top-spend campaign concentrating spend without a budget constraint

**Evidence.** `partially validated`

_Refresh 2026-09._ The pattern has been detected on a live account and the hold was applied, but no cap or reallocation outcome has been measured.

**Trigger.** The account's top-spend Search campaign spends at least 50% above its trailing four-week weekly mean while conversions run at least 50% below that mean, budget-lost impression share is below 10%, and conversion volume is below the reliability floor. Thresholds are `PROPOSED`.

**Pre-flight green.** PF-1 (tracking verified: a conversion collapse is a tracking hypothesis first). PF-3 (no budget or bid-strategy change in the last 14 days that would explain the spend move). Windows complete and mature.

**Standard move.** Hold further budget increases on the campaign. Read the complete week, the trailing 30 days, the campaign's share of portfolio spend, and intake quality together rather than separately. If the pattern persists across two complete weeks, cap the campaign to its pre-spike spend band and leave the reallocation decision to the operator.

**Do not move when.** It is a single sub-floor week. Signed-case quality justifies the premium: cost per signed case, not cost per lead, is the test where the matchback exists. The campaign is a deliberately bounded test still inside its cap (PB-32). Budget-lost impression share is high, which makes this a budget question and not a concentration question (PB-01).

**Expected result and verification.** Incremental auction spend stops concentrating in a campaign with no proven volume, and portfolio spend share returns toward its prior band. Verify at 7 and 30 days: GAQL 6.1 for spend, conversions and CPL by campaign, GAQL 5.1 for both impression-share components.

**Card line.**

```text
playbook PB-40 (campaign): standard move for a top-spend campaign absorbing materially more spend while conversions fall and budget-lost stays near zero is hold further increases and re-read the complete week plus 30-day contribution. accept/reject
```

**Related.** SKILL.md "Account macro context" and "Impression share". Cross-refs PB-01, PB-29, PB-34, PB-41.

---

# Bidding

## PB-04: tCPA direction

**Evidence.** `textbook only`. No tCPA step, up or down, has been made and measured on an account we run.

**Trigger.** A proposal or question about moving a tCPA target on a live campaign.

**Pre-flight green.** PF-1, PF-3. The campaign is at or above the reliability floor for its own volume in the window used for the cost/conv reading.

**Standard move.** Direction follows headroom, not instinct.

- cost/conv comfortably below target: lowering is available, in 10 to 15% steps, one step per 14 days.
- cost/conv near target: hold. There is no headroom.
- cost/conv above target: do not lower. Fix the drivers first (QS, ad relevance, landing page, negatives).
- cost/conv well above target with high rank-lost IS and budget-lost IS near zero: the legitimate move is raising the target to let the algorithm compete, not lowering it.

**Do not move when.** Inside 14 days of any prior bid, budget, or targeting change. Inside a post-tracking-fix lockdown (PB-06). Below the conversion floor, where the reported cost/conv is noise. When the change would be more than one step: staircase moves inside a learning window are the churn pattern in PB-10.

**Expected result and verification.** After a downward step: conversion volume holds while CPA drifts toward the new target. After an upward step: impression share and conversion volume rise. Verify at 14 days minimum, 28 days preferred: GAQL 6.1 for CPA and volume, GAQL 5.1 for IS. A volume drop after a downward step is the signal to step back up.

**Card line.**

```text
playbook PB-04 (Westhollow - Custody): standard move when cost/conv sits well under target is a single 10 to 15% tCPA step down, then hold 14 days. accept/reject
```

**Related.** SKILL.md "tCPA direction rule" (consolidated here in full); diagnosis trees Tree 2 Step 3 and Sub-tree D Question 3; knowledge base "Bidding". Cross-refs PB-05, PB-06, PB-10.

---

## PB-05: Setting a target from firm economics

**Evidence.** `textbook only`. No target has ever been derived from firm economics on an account we run. Every CPL judgment to date has been made against the account's own trailing baseline instead. Treat that as the gap it is, and say so when presenting a CPL comparison.

**Trigger.** A target CPL, tCPA, or cost-per-signed-case is needed and none is recorded, or the recorded one is being questioned.

**Pre-flight green.** None required: this is an input step, not a data reading.

**Standard move.** Take the target from the firm, in this order: recorded firm economics in the account's rendered notes (average signed-case value, lead-to-signed rate, acceptable cost per signed case), then an explicit operator override, then ask. Compute: case value x acquisition share = target cost per signed case; target cost per signed case x lead-to-signed rate = target CPL. Worked illustration with fictional numbers: $12,000 case value x 15% (`PROPOSED` as an illustration only, not a house default) = $1,800 per signed case; at a 30% lead-to-signed rate that is a $540 target CPL. Where the live target is far from the economics target, step the live tCPA toward it per PB-04 rather than jumping.

**Do not move when.** The only available basis is the account's own current CPA. Back-solving a target from current performance ratifies the status quo and can never improve the account. That is the one forbidden move in target setting. If the economics are missing, the output is the ask, not a number.

**Expected result and verification.** The target exists as a recorded journal `context` or `rule` entry with its inputs, and every subsequent CPL reading is measured against it. Verify by re-reading the rendered notes at the next check.

**Card line.**

```text
playbook PB-05 (account): standard move when no target CPL is on record is to take it from firm economics, case value x acquisition share x lead-to-signed rate. accept/reject
```

**Related.** SKILL.md "Target Setting: Targets Come From Firm Economics, Not Account Data" (consolidated here in full); NOTATION.md `context` and `rule` entry types. Cross-refs PB-04, PB-29, PB-30.

---

## PB-06: Post-tracking-fix bidding lockdown

**Evidence.** `partially validated`

_Refresh 2026-09._ One interim post-counting-change hold was completed, but the full 14-day and 28-day verification was not. Rebuild both comparison windows by conversion action after any non-retroactive counting change.

**Trigger.** Conversion tracking contamination has just been fixed (duplicate action removed, tag repaired, counting method corrected) on a campaign running tCPA, Maximize Conversions, or tROAS.

**Pre-flight green.** PF-1 re-run after the fix and confirmed clean.

**Standard move.** Hold the current target, whatever it is. Announce a 2 to 4 week lockdown: no target change, no bid-strategy change, no budget change. Expect apparent CPA to rise and conversion volume to fall, both of which are the contamination leaving the numbers. Re-evaluate the target only after 2 to 4 weeks of clean data.

**Basis break, every spanning comparison (fold, 2026-09).** A counting or conversion-action change is not retroactive, so the two sides of any comparison crossing its effective date are counted on different definitions and can manufacture a false collapse. Record the effective date, and reconstruct both sides of every spanning week-over-week and 30-day comparison from action-level data before reading it. Rebuild both the 14-day and the 28-day windows by conversion action, not from headline totals. See PB-23.

**Do not move when.** Always: there is no version of this pattern where an immediate target change is right. Setting a "corrected" target before relearning completes replaces one wrong number with another. If clean volume falls below the reliability floor during relearning, the exception is a strategy change to Maximize Conversions (PB-07), or Max Clicks with a CPC cap if avg CPC is also high (PB-08), not a target tweak.

**Expected result and verification.** 14-day rolling CPA rises then stabilises; impression share may dip as the algorithm recalibrates; learning status clears. Verify at 14 and 28 days: GAQL 6.3 (weekly), GAQL 2.2 (conversion volume by action, confirming the clean count), GAQL 5.1.

**Card line.**

```text
playbook PB-06 (Westhollow - Divorce): standard move after a tracking fix on a smart-bidding campaign is a 2 to 4 week freeze at the current target, apparent CPA rise expected. accept/reject
```

**Related.** SKILL.md "Smart bidding: post-tracking-fix protocol" (consolidated here in full); diagnosis trees Tree 7 Step 5. Cross-refs PB-07, PB-08, PB-23.

---

## PB-07: tCPA below the conversion floor

**Evidence.** `textbook only`

**Trigger.** A campaign on tCPA running below the reliability floor for its own volume over 30 days, sustained over 60 days, with erratic week-to-week CPA and impression share.

**Pre-flight green.** PF-1 (the low count is real, not a tracking break: a silent primary produces the same shape, and that is PB-23). PF-3 (the erratic performance is not just a fresh learning period).

**Standard move.** Remove the target: switch to Maximize Conversions. Maximize Conversions optimises direction rather than a specific number, and is more forgiving at low volume. Hold everything else for 28 days.

**Do not move when.** Avg CPC is also high against the campaign's own trailing 30-day median and the account's other campaigns, where Maximize Conversions is not the safe harbour and PB-08 applies instead. The campaign has been on tCPA for under 30 days. Conversion volume is low because the account is seasonally quiet (PB-31).

**Expected result and verification.** Week-to-week swings narrow; conversion volume holds or rises; CPA becomes readable over 30 days rather than 7. Verify at 28 days: GAQL 2.3 and GAQL 6.3.

**Card line.**

```text
playbook PB-07 (Westhollow - Probate): standard move for tCPA running under the reliability floor is dropping the target to Maximize Conversions, then 28 days untouched. accept/reject
```

**Related.** SKILL.md "Smart bidding" low-volume flag and "Handling Comparative and Premise-Based Questions" (conversion volume threshold); diagnosis trees Sub-tree D Question 2; knowledge base "Bidding". Cross-refs PB-06, PB-08, PB-10.

---

## PB-08: Sub-floor volume plus high CPC

**Evidence.** `validated in practice (1 outcome, five monthly readings)`

_What happened when we did it._ On the heaviest-spend campaign of a high-CPC practice area sitting far below the conversion floor, switching Maximize Conversions to Maximize Clicks with a CPC cap halved the auction price and bought back reach: avg CPC down about 54% over two months, clicks up about 25% at peak, impression share up 13 to 33 points, budget-lost from over 40% to zero, monthly spend down about 44%. Time to signal about 30 days on cost and reach. Read this as a cost-control and signal-rebuilding move, never as a conversion move, and set the revisit window on that basis.

**Not a promise.** CPL moved in the measured case (down 28 to 76%) because cost moved; conversions were flat at the same low monthly count for two months, then went to zero across the following half-month. That arithmetic must not be presented as a conversion outcome. Never carry "CPL fell" onto a card as what the move achieved.

**Trigger.** A campaign already on Maximize Conversions (or tCPA), converting but below the reliability floor for its volume, carrying an avg CPC at or above its own trailing 30-day median and high against the account's other campaigns (`PROPOSED` as a trigger reading), with budget-lost IS present.

**Pre-flight green.** PF-1. The CPC reading is from live campaign data, not a search-term sample, and the currency is the account's own.

**Standard move.** Switch to Maximize Clicks with a CPC cap (`PROPOSED`: cap at or slightly below the campaign's trailing 30-day median CPC). The cap stops a single auction eating the daily budget; Max Clicks buys the volume needed to rebuild a conversion signal. Set an explicit 3 to 4 week revisit and watch CVR, because Max Clicks optimises for clicks, not conversions.

**Do not move when.** Conversions are zero rather than thin: a zero-conversion campaign at high CPC with adequate impression share points at the landing page or tracking (PB-25, PB-23), not at the bidding model. The high CPC is normal for a high-value practice area and the CPA is acceptable: an expensive click that acquires a large case is not a defect. Tracking is unverified.

**Observed failure mode.** In the measured case, conversions were flat at the same low monthly count for two months after the switch, then dropped to zero across the following half-month. That drop is not itself grounds to abandon the move early, but it must be watched for.

**Expected result.** Click volume rises, avg CPC falls to near the cap, impression share recovers, budget-lost falls. Do not expect conversion count or CPL to improve. Verify at 3 to 4 weeks: GAQL 6.1 for clicks, CPC, impression share, budget-lost, and explicitly CVR. If clicks recover but CVR craters, the volume has done its job and the move back to a conversion-based strategy is the next step.

**Card line.**

```text
playbook PB-08 (Westhollow - Elder Abuse): standard move for sub-floor conversions at a CPC above the campaign's own trailing median is Maximize Clicks with a CPC cap, revisit in 3 to 4 weeks on CVR. accept/reject
```

**Related.** SKILL.md "Smart bidding" low-volume flag and "Campaign-Level CPC Anomaly" third condition; diagnosis trees Sub-tree D. Cross-refs PB-07, PB-25, PB-33.

---

## PB-09: New campaign in its learning period

**Evidence.** `validated in practice (1 outcome)`

_What happened when we did it._ Two campaigns launched into a new geography at a deliberately small daily cap read TRUE at day three, converting at roughly half the account's blended 30-day CPL, and were stable enough at week one to make the budget decision on. Week two was near-identical, which is what a hard budget cap looks like. Applied literally, the original form of this entry would have forbidden the correct call for a month. See the Contradiction note.

**Trigger.** A campaign, ad group, or bid strategy less than 14 days old, or a campaign that has not yet cleared the reliability floor for its own volume (`PROPOSED`: no CPL judgment until the floor is cleared or 30 days live, whichever is later, except a deliberately budget-capped market test, which is a rationed sample readable against the account blend from about day 3, see PB-35).

**Pre-flight green.** PF-2 and PF-3 only. This playbook exists to stop premature moves, so it fires on the absence of data rather than on a threshold.

**Standard move.** Hold on the CPL verdict, and separate it from the two questions that ARE readable early.

1. **Is it serving as intended?** Readable from day 1. The verify-poll checks exactly this and stops: status and serving state, budget and pacing, bid strategy, conversion goals, asset review state, disapprovals, spend. No performance judgment, no structural edit, no target change.
2. **Is it converting at all, and roughly in what band relative to the account?** Readable from about day 3 on a budget-capped campaign, firmly by week 1. This is a coarse, order-of-magnitude question: is it landing near the account's blended CPL, at a fraction of it, or nowhere near it. State it as a band with the conversion count attached, never as a CPL figure.
3. **What is its CPL?** NOT readable until the campaign clears the reliability floor for its own volume or 30 days live, whichever is later. This is the gate the entry protects.

Report the poll, give the band from question 2 once there is any conversion volume, name the date the campaign becomes readable for question 3, and set that date as the `review_by`.

**Contradiction with the original entry.** The original form forbade any CPL judgment before the floor or 30 days. Applied literally it would have blocked the correct budget decision for a month on the one launch we measured, where the direction was clear at day 3 and stable at week 1. The distinction the original missed: **a budget-capped campaign is a rationed sample, not a noisy one.** A hard daily cap makes weeks 1 and 2 near-identical by construction, which is exactly why the early read held. On an UNCAPPED new campaign, where spend and mix are still moving, the original gate stands in full.

**Do not move when.** A structural error is found in the poll (wrong goals, wrong geo constant, disapproved ads, zero serving): those are corrections, not optimisations, and they run immediately under their own playbooks (PB-18, PB-23, PB-27). The distinction is: fix what is broken, judge nothing that is merely young. Do not use the early band to make an in-campaign optimisation: it is good enough to decide whether to feed the campaign or stop it, and not good enough to decide anything inside it.

**Expected result and verification.** The campaign reaches its readable date with no clock resets in change history. On a capped launch, expect week 2 to look like week 1 in spend and impression share; that is the cap binding, not a plateau. Verify at the readable date: GAQL 8.1 (confirm no interim changes), then the normal read.

**Card line.**

```text
playbook PB-09 (Westhollow - Mediation, day 6): standard move inside the learning period is hold and verify-poll only, first performance read at day 30. accept/reject
```

**Related.** SKILL.md pre-flight PF-3; diagnosis trees Sub-tree D Question 1; knowledge base "Bidding" (14-day learning phase). Cross-refs PB-10, PB-18, PB-32.

---

## PB-10: Chronic learning-phase churn

**Evidence.** `textbook only`. Never observed on an account we run. Our accounts change too rarely to generate churn, which is itself worth knowing before diagnosing it.

**Trigger.** Change history shows repeated bid-strategy or target changes at intervals under 14 days, over 2 or more cycles, with performance never stabilising.

**Pre-flight green.** PF-3 read in full, with dates and sequence recorded.

**Standard move.** One freeze, two valid forms:

1. Hold the current target, whatever it is, for a minimum of 4 full weeks (28 days). Not 21 days.
2. If the target has been staircased so far from any achievable baseline that no current value reflects real data, drop the target entirely and run Maximize Conversions for the same 28 days.

Either way: **do not set a "better" number at the start of the freeze.** Changing the target to begin the freeze resets the clock the freeze exists to protect. The freeze starts from the live value.

**Do not move when.** Nothing overrides the freeze once started. A poor week inside the window is expected and is not grounds to intervene. The one exception is a genuine break (tracking silence, disapproval, outage), which is handled under its own playbook without touching the bid strategy.

**Expected result and verification.** Week-to-week variance narrows by the end of the 28 days; the strategy shows a readable baseline for the first time. Verify at 28 days: GAQL 8.1 to confirm no interim changes, GAQL 6.3 for the weekly trend.

**Card line.**

```text
playbook PB-10 (Westhollow - Divorce): standard move for repeated sub-14-day bid changes is a 28-day freeze at the current live target, no adjustment to start it. accept/reject
```

**Related.** Diagnosis trees Sub-tree D Question 4 (consolidated here); SKILL.md pre-flight PF-3; knowledge base "Bidding" (the mismanaged-account cycle). Cross-refs PB-04, PB-06, PB-07.

---

# Keywords and search terms

## PB-11: BROAD match remediation

**Evidence.** `partially validated`

_What happened when we did it._ A large broad-to-phrase conversion (about 70 keywords converted, about 150 legacy broads paused) shipped in the same session as a geo launch, and the campaigns involved went on to run the cheapest CPLs in the account. The outcome is confounded: two changes, one window, no isolated read. What it does support is that phrase conversion at scale did not suppress volume. The pruned campaigns kept serving and kept converting.

**Trigger.** A BROAD-match positive keyword flagged for cleanup: high CPA, search-term waste, or match-type tightening.

**Pre-flight green.** Keyword query filtered `ad_group_criterion.negative = FALSE`, `ad_group.status = 'ENABLED'`, `campaign.status` selected. An unfiltered query returns negatives alongside positives and has produced confirmed misdiagnosis.

**Standard move.** Convert BROAD to phrase match. Not exact, not delete, not pause. Phrase preserves near-intent variants and filters the loosest queries, and it is the lower-risk path. Do not assume it carries the criterion's conversion history intact: verify performance after the change. Sequence: convert to phrase, monitor search terms for 2 to 4 weeks (unconfirmed), and only then evaluate tightening to exact or adding specific negatives if CPA is still above target.

**Do not move when.** The keyword is irrelevant rather than merely broad (wrong practice area or wrong geography): those are hard deletes, not conversions. The keyword is also a major conversion source, where PB-12 governs the sequencing. The "BROAD keyword" turns out to be a negative keyword, which is the most common false trigger here.

**Expected result and verification.** Irrelevant search terms fall away, conversion volume from the keyword survives, CPA improves or holds. Verify at 2 to 4 weeks: GAQL 4.1 for the campaign's search terms, GAQL 3.4 for the keyword's own performance.

**Card line.**

```text
playbook PB-11 (Westhollow - Divorce, ag Uncontested): standard move for a wasteful BROAD keyword is convert to phrase, monitor search terms 2 to 4 weeks. accept/reject
```

**Related.** SKILL.md "Broad-match keyword remediation: default path" (consolidated here in full) and "GAQL Query Integrity"; knowledge base "Match Type Philosophy"; diagnosis trees Tree 6 Step 4. Cross-refs PB-03, PB-12, PB-13.

---

## PB-12: Wasteful broad keyword that is also a major conversion source

**Evidence.** `textbook only`

**Trigger.** A BROAD positive keyword showing real waste (a material block of clearly irrelevant search-term spend) that also supplies >= 25% (`PROPOSED`) of the campaign's conversions in the window, especially on a smart-bidding campaign where those conversions feed the model.

**Pre-flight green.** Same keyword-query filters as PB-11. Conversion attribution for the keyword read from keyword-level data, not inferred from search terms.

**Standard move.** Convert broad to phrase, add specific negatives for the irrelevant categories, set a monitoring window, and keep the keyword running. Pause only if, after the phrase conversion and negatives, the converting traffic does not survive. Pausing or deleting first throws away the conversion volume and starves smart bidding of signal.

**Do not move when.** The conversions attributed to the keyword are provisional. The campaign is inside a learning period, where even the phrase conversion resets the clock: sequence it after the window closes.

**Expected result and verification.** Conversion share from the keyword holds within its prior band while irrelevant spend falls. Verify at 2 to 4 weeks and again at 6 weeks: GAQL 3.4 for keyword conversions, GAQL 4.1 for the search-term mix. The 6-week read is what licenses any further tightening.

**Card line.**

```text
playbook PB-12 (Westhollow - Custody): standard move for a wasteful BROAD keyword that also drives a quarter of conversions is phrase plus targeted negatives, not a pause. accept/reject
```

**Related.** SKILL.md "Search-term data" (wasteful-broad-that-converts paragraph, consolidated here). Cross-refs PB-11, PB-13, PB-17.

---

## PB-13: Search-term waste and n-gram negatives

**Evidence.** `partially validated`

_What happened when we did it._ The waste MEASUREMENT is validated and repeatable: per-campaign search-term pulls on a fresh launch put roughly a quarter of the campaign's search-term spend in obvious junk categories. The negatives half has never been executed. A prepared negatives file was rejected outright by the operator for carrying too many broad practice-vocabulary strings, and the untreated campaigns then produced the cheapest CPLs in the account while its 30-day CPL improved. See the Contradiction note.

**Trigger.** A recurring n-gram across the campaign's search terms carrying >= 3% of the campaign's search-term spend (`PROPOSED`) with zero conversions over >= 60 days (`PROPOSED`), where the n-gram is irrelevant to what the firm actually handles.

**Pre-flight green.** `search_term_view.status` selected in the query, `ad_group.status = 'ENABLED'` in the WHERE clause. Terms with `status = NONE` excluded. Existing negatives (GAQL 9.1 to 9.4): caveat-and-fire, not a hard gate. If the pull is unavailable, the line still fires with the explicit caveat `existing negatives not checked`, and the standard move starts with that pull. If the pull is available, confirm the n-gram is not already blocked before carding the negative.

**Standard move.** Every negative proposed here comes from this account's own search terms, checked against the not-waste list and the term's own conversion record. A category from the negative-keyword library is never applied to a live account wholesale; that library seeds new campaigns. First, pull existing negatives (GAQL 9.1 to 9.4) if that pull was not already done. Then add the n-gram as a negative at the narrowest sufficient level: account-level shared list if irrelevant to everything the firm does, campaign level if irrelevant to that practice area or geography, ad group level if narrowly irrelevant. Phrase match is the default; exact where the word has legitimate uses to preserve. Where an account has accumulated many reactive exact strings sharing one 2 or 3 word root, one phrase-match categorical replaces the lot and catches future variants. Check the replacement against the not-waste list before it ships: a broader categorical is a broader blocking risk.

**Contradiction: a waste percentage is not a performance diagnosis.** On the one launch where we measured both, roughly a quarter of the campaign's search-term spend sat in obvious junk categories AND those same untreated campaigns went on to run the cheapest CPLs in the account, several times better than the mature campaigns that had years of negative-list maintenance behind them. Over the same window the account's 30-day CPL improved. We never applied the negatives, so this is not evidence that negatives do not work: it is evidence that **waste share did not predict campaign CPL, and is not on its own a reason to move.** Present waste as a measured figure next to the campaign's actual CPL. Never present it as the explanation for a CPL problem unless the CPL problem exists.

Second, practical: a negatives plan the operator has REJECTED is closed, not overdue. Ours was re-surfaced as an outstanding item for two weeks after it had been declined, which is exactly the "do not re-raise what the operator already closed" failure in the universal do-not-move block.

**Do not move when.** The term has converted. A converting term is a customer, not waste, however much it looks like a referral, nonprofit, or category mismatch. The term is informational or procedural intent in a market with a long consideration window, where research queries are real prospects at an earlier stage. The term names a practice area you have not confirmed the firm declines. The proposed list is broad enough to catch the practice vocabulary itself: a negatives file heavy in the firm's own category words (the practice-area nouns, the profession nouns) will suppress real traffic, and one was rejected for exactly that. The finding rests on a handed export whose filters cannot be confirmed. The campaign is converting below the account's blended CPL: it is not the place to spend a change window.

**Expected result and verification.** Irrelevant spend in that category falls to zero without a drop in campaign conversions. Verify at 30 days: GAQL 4.1 for the term category, GAQL 6.1 for campaign conversions over the 30 days after against the 30 before. Note honestly that we have never run this verification, because the move has never been executed on an account we run.

**Card line.** State both thresholds as `PROPOSED` on the card. If existing negatives were not pulled, put `existing negatives not checked` on the line; the move then starts with that pull.

```text
playbook PB-13 (Westhollow - Divorce): standard move for a zero-conversion n-gram at 3%+ of the campaign's search-term spend (PROPOSED) over >= 60 days (PROPOSED) is a phrase negative at campaign level. existing negatives not checked; start with that pull. accept/reject
```

**Related.** SKILL.md "Search-term data" and its negative-precision rules; negative keyword library Sections 1 to 5, as seed categories for a new campaign only; diagnosis trees Tree 6. Cross-refs PB-12, PB-14, PB-28.

---

## PB-14: Geo-mismatched query containing the core service term

**Evidence.** `validated in practice (1 outcome)`

_What happened when we did it._ On a geo-mismatched query that also carried the firm's core service term, negating the geo token alone kept the service term serving everywhere else. The alternative on the table at the time, a phrase negative on the whole query, would have suppressed the firm's primary intent in every other geography. No adverse effect observed afterwards.

**Trigger.** A search term combining the firm's core service term with a location the firm does not serve.

**Pre-flight green.** Same search-term integrity checks as PB-13. Confirm the location is genuinely out of scope against the account's targeting and notes, not merely unfamiliar.

**Standard move.** Decompose the query, negate the geo token only, keep the service term serving. A phrase-level negative on the whole query, or any negative touching the service words, removes good traffic in every other geography to solve a location problem.

**Do not move when.** The out-of-area query has converted: out-of-area searchers can be real prospects who understand which jurisdiction their matter falls under. The geo token is ambiguous (a city name that is also a common word or a firm name element). The pattern is broad enough to be a targeting question rather than a keyword one, in which case PB-28 governs.

**Expected result and verification.** Queries containing that geography stop appearing; queries containing the service term in target geographies are unaffected. Verify at 30 days: GAQL 4.1 filtered for both the geo token and the service term.

**Card line.**

```text
playbook PB-14 (Westhollow - Divorce): standard move for a geo-mismatched query carrying the core service term is negating the city token only. accept/reject
```

**Related.** SKILL.md "Search-term data" negative-precision rules; negative keyword library Section 6. Cross-refs PB-13, PB-28.

---

## PB-16: Duplicate keywords and cross-ad-group cannibalisation

**Evidence.** `textbook only`. No duplicate-keyword case has been found or acted on across the accounts we run.

**Trigger.** The same keyword text with overlapping match type appears in 2 or more ENABLED ad groups of the same campaign, both with impressions in the last 30 days (`PROPOSED`).

**Pre-flight green.** Keyword query filtered for `negative = FALSE` and `ad_group.status = 'ENABLED'`. Duplicates across an ENABLED and a PAUSED ad group are not duplicates.

**Standard move.** Keep the instance that CONVERTS and pause the other. Conversion is the deciding consideration: if one instance converts and the other does not, the converter is kept, whatever the ad copy or landing page suggests about intent match. Intent breaks ties only, when neither instance has a conversion record or both convert at comparable rates: then keep the instance in the ad group whose ad copy and landing page match the keyword's intent most tightly. Where both ad groups are legitimate but serve different intents, the fix is tighter negatives between them (each ad group negatives the other's distinguishing token), not a pause.

**Do not move when.** The duplication is deliberate structure (a SKAG isolation test, a brand and non-brand split). The two instances sit in different campaigns with different budgets or geographies, which is segmentation, not cannibalisation. Neither instance has enough data to say which converts: read longer rather than choosing on intent alone. Never pause the instance carrying the conversions in order to keep the one with the tighter intent match.

**Expected result and verification.** Impressions consolidate into the kept ad group and campaign conversions hold. Conversion volume is the metric that decides whether the consolidation worked; CTR and quality score on the kept instance are supporting detail. Verify at 30 days: GAQL 3.4 for both instances, GAQL 6.1 for campaign totals.

**Card line.**

```text
playbook PB-16 (Westhollow - Divorce): standard move for the same keyword serving in two ad groups is keeping the instance that converts, pausing the other. accept/reject
```

**Related.** Audit checklist Section 2 (no duplicate keywords across ad groups); knowledge base "Campaign Structure"; diagnosis trees Tree 5 Step 4. Cross-refs PB-11, PB-19.

---

## PB-17: Long-term bleed keyword

**Evidence.** `textbook only`

**Trigger.** A keyword with 90-day spend >= 2x the target CPL (`PROPOSED`) and zero conversions over the same 90 days, in an ENABLED ad group on an ENABLED campaign.

**Pre-flight green.** PF-1 (a tracking gap produces the same signature account-wide, in which case this is not a keyword finding). Target CPL on record (PB-05). Keyword query filters as above. Both 30-day and 90-day windows read, not one.

**Standard move.** Pause the keyword. Where the keyword is relevant but simply too loose, tighten the match type first per PB-11 and re-read at 30 days before pausing.

**Do not move when.** The keyword converts in bursts with long cold stretches, which is conversion clustering, not bleed, and reflects seasonality or market rhythm. The 90-day window includes a tracking outage or a site outage. The keyword is new: youth is not bleed (PB-09). The account-wide conversion count is at or near zero, which makes this a tracking or landing-page finding, not a keyword one.

**Expected result and verification.** Spend reallocates to converting keywords in the same ad group; campaign conversions hold. Verify at 30 days: GAQL 3.3 for the ad group's keyword set, GAQL 6.1 for campaign conversions.

**Card line.**

```text
playbook PB-17 (Westhollow - Probate, ag Estate Admin): standard move for a keyword at 90 days of spend and zero conversions is a pause, or a match-type tighten first if the term is on-practice. accept/reject
```

**Related.** Knowledge base "Long-Term Keyword Management"; audit checklist Section 2; diagnosis trees Tree 5 Step 4. Cross-refs PB-05, PB-11, PB-13.

---

## PB-38: Hyper-granular ad groups in a low-volume practice area

**Evidence.** `validated in practice (1 outcome, six test groups against one control)`

_What happened when we did it._ Six narrow ad groups were built inside working campaigns: four sub-type splits of a single practice area, one adjacent-service group, and one high-intent qualifier group. After roughly four weeks live, each sub-type group had accumulated 1 to 3 impressions per fortnight, the adjacent-service group had 18 impressions and zero spend, and the qualifier group had 7 impressions. Over the same fortnight the general group covering the whole practice area produced 7 conversions. The granular build did not underperform: it did not run at all, while the general group carried the practice area unchanged. Time to signal: four weeks of near-zero impressions is conclusive, and two weeks is already suggestive.

**Trigger.** New or existing ad groups built as narrow sub-type, qualifier, or intent splits of a practice area, in an account or geography whose whole-campaign volume runs in the low tens of conversions per month, showing near-zero impressions after 2 or more weeks live while a broader sibling group in the same campaign serves normally.

**Pre-flight green.** PF-2 (the groups' ads are approved and the groups are ENABLED: a policy block or a paused group is a different finding). Impressions pulled at ad-group level over an aligned window, with the broader sibling group in the same pull for comparison.

**Standard move.** Consolidate up, do not tune down. Fold the narrow groups' keywords into the broader group that is already serving, keep the ad copy that matches the practice area rather than the sub-type, and let match types rather than ad-group structure carry the intent distinction. Do not try to rescue a starved group with bids or budget: it has no impressions to bid on, and the query volume for that split does not exist in this market at this geography.

**Do not move when.** The account or geography actually has the volume to support the split, which is the whole question: pull the broader group's impression volume first and ask whether dividing it by the number of splits leaves anything workable. The groups are less than 2 weeks live (PB-09). The near-zero impressions have a policy or serving cause rather than a demand cause (PB-18). The split exists for a reporting reason the firm has asked for, in which case it is a deliberate cost, not a defect. A narrow group IS accumulating impressions, however slowly, and its conversions are marginal additions rather than cannibalised from the sibling (PB-13's marginal-contribution logic applies, and volume-driving groups are judged on marginal contribution).

**Expected result and verification.** After consolidation the broader group absorbs the impression volume without a conversion drop, and the account carries fewer near-dead objects. Verify at 30 days: ad-group impressions, clicks and conversions for the consolidated group against the sum of its parts before.

**Card line.**

```text
playbook PB-38 (Westhollow - Custody): standard move for sub-type ad groups at near-zero impressions after 4 weeks, beside a serving general group, is folding them up into the general group. accept/reject
```

**Related.** Legal PPC realities item 1 (low volume); the marginal-contribution rule for volume-driving ad groups; audit checklist account-structure section. Cross-refs PB-09, PB-13, PB-16, PB-35.

---

# Ads and creative

## PB-18: Disapprovals and limited ads on serving campaigns

**Evidence.** `partially validated`

_Refresh 2026-09._ A removed ad group caused a false review-status flag, while two serving PMax asset groups became policy-limited. Filter to enabled serving groups and hold asset edits while an appeal is pending.

_What happened when we did it._ The disapproval half is untested. The limited-ads half is contradicted by sustained observation: on an account in a sensitive practice area, every enabled ad has sat limited for months, 27 rising to 31 of 31, with new ads inheriting the same status on review and not one instance ever clearing. Zero disapprovals throughout. See the Contradiction note.

**Trigger.** GAQL 7.3 returns any ad with `approval_status` in {`DISAPPROVED`, `APPROVED_LIMITED`} or `review_status` in {`UNDER_REVIEW`, `REVIEW_IN_PROGRESS`} on an ENABLED ad group in an ENABLED campaign, or a serving PMax asset group reads policy-limited. Filter to enabled, serving ad groups first: a removed ad group produces a false review-status flag.

**Pre-flight green.** This is PF-2 itself. A campaign reading `serving_status = SERVING` does not clear ad-level policy: check the ad-level policy summary, do not default to a screenshot.

**Standard move.** Split by status.

- `DISAPPROVED`: the ad is not serving. Get the human-readable reason (Policy Manager screenshot is the only route, the API does not expand it), edit the offending element, resubmit. Confirm at least one approved ad remains live in the ad group in the meantime.
- `UNDER_REVIEW` / `REVIEW_IN_PROGRESS` on a new ad: wait. This is not a finding, it is a state.
- `APPROVED_LIMITED`: the ad serves with restricted reach. Where the limitation is a chronic policy sensitivity attached to the practice area rather than to the copy, the standard move is to record it as a known reach ceiling and stop re-flagging it. Rewriting copy against a category-level sensitivity churns creative for nothing.
- **PMax asset group policy-limited while its assets stay approved (fold, 2026-09).** This is a group-level limitation, not an asset-quality finding. Obtain the human-readable policy reason, appeal where appropriate, record the appeal date, and hold every asset edit until it resolves. Report serving separately from policy clearance: continued spend does not mean the limitation cleared. See PB-32.

**Do not move when.** The limited status is already carried as a standing rule or known issue: report it as carried, do not re-raise it as new. The ads sit in a PAUSED or REMOVED campaign or ad group. An asset-group appeal is pending: no asset edits until it resolves. The disapproval is on a variant that is not the ad group's only ad and a fix is already in review.

**Contradiction: in sensitive practice areas, limited is the steady state, not a defect.** The entry reads as though a limited ad is a fixable problem. On one account in a sensitive category, the count went 27 to 30 to 31 of 31 enabled ads limited, across months, with every newly built ad inheriting the same status on review and not one instance ever clearing. Zero disapprovals throughout. Two consequences the check must respect: (1) a new limited ad on such an account is not news, and re-flagging it weekly produced months of noise and no action; (2) part of that account's rank-lost impression share is a policy reach ceiling, so do not attribute rank-lost movement there to Quality Score work (PB-02).

The corollary is a real finding when it happens: on such an account, a DISAPPROVED ad, or a sudden jump in the limited count on copy that used to serve fine, is a genuine signal precisely because the chronic baseline is so stable.

**Expected result and verification.** Disapproved ads return to APPROVED and resume serving; the ad group has at least one serving ad throughout. Verify at the next check: GAQL 7.3, plus impressions on the repaired ad. Chronic category-level limited ads have never been observed returning to APPROVED, so no verification is scheduled for them.

**Card line.**

```text
playbook PB-18 (Westhollow - Custody): standard move for a DISAPPROVED ad on a serving ad group is pulling the policy reason, editing, resubmitting, with an approved ad kept live meanwhile. accept/reject
```

**Related.** SKILL.md PF-2; diagnosis trees PF-2 and Tree 3 Step 1; audit checklist PF-2. Cross-refs PB-02, PB-09, PB-32.

---

## PB-19: RSA hygiene

**Evidence.** `textbook only`. The low-RSA-hygiene pattern has been detected and repeatedly held, but no rewrite has been made and measured.

_Refresh 2026-09._ A later weekly improvement without a rewrite does not validate the rewrite.

**Trigger.** An ENABLED ad group with no active RSA, or an RSA below the hygiene floor (`PROPOSED`: fewer than 8 headlines, fewer than 3 descriptions, or more than 2 pinned headlines), or an ad group whose only ads are paused or removed. An ad group running exactly one RSA at or above the hygiene floor is a config item under agency-defaults.md Sec 6.4 (standard is 2 to 3 RSAs per ad group), not a playbook trigger on its own.

**Pre-flight green.** PF-2. GAQL 7.1 pulled for the campaign.

**Standard move.** Bring the ad group to the floor: 2 to 3 active RSAs (agency-defaults.md Sec 6.4), each carrying 8 or more headlines and 3 or more descriptions, at most 2 pinned headlines, unpinned by default, referencing the specific practice area and geography rather than generic copy. Where headlines are pinned to satisfy a client requirement, keep the pin and record it as a requirement, not a defect.

**Do not move when.** Ad strength alone is the trigger. Ad strength reflects Google's preference for creative flexibility, not performance, and a POOR rating is addressed after landing page and structure issues, never ahead of them. The ad group is inside a learning period. The pins are a bar-compliance or client requirement on record.

**Expected result and verification.** Impression volume and CTR hold or improve as the asset pool widens. Verify at 30 days: GAQL 7.1 for CTR and impressions against the prior 30 days. Do not read individual asset performance at low volume.

**Card line.**

```text
playbook PB-19 (Westhollow - Custody, ag Physical Custody): standard move for an ad group under the RSA floor is building to 2 to 3 RSAs, each at 8+ headlines and 3+ descriptions, unpinned. accept/reject
```

**Related.** Knowledge base "Ad Copy" (RSAs, ad strength, extensions); audit checklist Section 4; SKILL.md "Responsive search ad construction"; diagnosis trees Sub-tree B. Cross-refs PB-20, PB-25.

---

## PB-20: Creative staleness and CTR decline

**Evidence.** `validated in practice (1 outcome)`

_What happened when we did it._ A long-standing CPA gap, with a problem ad group running several times its sibling's CPA, had been attributed to a third-party landing page and parked as out of scope for months. An ad refresh ALONE, new headlines on an intent-matched and near-me angle with no landing-page change, closed the gap almost entirely in the following window. Time to signal: visible in the next complete window. The general lesson sits in the do-not-move block: a structural or LP-gated CPA flag is a hypothesis with a shelf life and must be re-pulled before it is re-asserted.

**Trigger.** Gradual CTR decline over 3 or more months on stable impression share, with no meaningful ad edit in the last 6 months (checklist rule) and CTR down >= 15% over that window (`PROPOSED`).

**Pre-flight green.** PF-3 (the decline is not explained by a structural change). Ad rotation checked (GAQL 1.3): check rotation before diagnosing a CTR decline, because OPTIMIZE can suppress variants and depress the aggregate. Treat it as a settings check to rule out, not as a demonstrated cause.

**Standard move.** Creative refresh: new headlines on a different angle, intent-matched and near-me variants where the practice area supports them, contrast language against the generic competitor set. Set rotation to `ROTATE_INDEFINITELY` and let it settle before the refresh window opens, so the new variants accrue data. Never change rotation and creative in the same window: doing so is what made the one measured instance unattributable.

**Do not move when.** The decline is abrupt over 1 to 2 weeks rather than gradual: that is an external change (new entrants, SERP layout) and creative refresh is not the first answer. Impression share is falling alongside CTR, which is a reach problem (PB-01, PB-02). Volume is too thin for a CTR read.

**Expected result and verification.** CTR recovers toward its prior band within 30 to 60 days (unconfirmed); `search_predicted_ctr` moves off BELOW_AVERAGE if it had slipped. Verify at 30 and 60 days: GAQL 7.1, GAQL 6.3, GAQL 3.1.

Note the corollary: a CPA gap long attributed to a structural or landing-page ceiling can close on creative alone. Re-pull before re-asserting a standing structural flag, and retire it when the data shows it no longer binds.

**Card line.**

```text
playbook PB-20 (Westhollow - Divorce): standard move for a 3-month CTR slide on 6-month-old creative is a headline refresh with rotation set to rotate indefinitely. accept/reject
```

**Related.** Diagnosis trees Sub-tree C (consolidated here); knowledge base "Ad Copy" and "Diagnosing Performance" (staleness); audit checklist Section 4. Cross-refs PB-19, PB-25, PB-31.

---

## PB-21: Image-asset coverage gap

**Evidence.** `textbook only`. No account we run currently serves image assets on the Google side, so this has zero outcomes.

**Trigger.** An ENABLED Performance Max asset group with zero image assets attached, or thin coverage (`PROPOSED`: fewer than 3 assets or fewer than 2 aspect ratios), derived from the account's image-asset inventory plus asset usage, cross-referenced against the ENABLED PMax campaign list. Scope is PMax. Search image extensions are in scope as a Search asset check but do not trigger this playbook.

**Pre-flight green.** Campaign type confirmed as Performance Max. A Search campaign without image assets is expected and never flagged.

**Standard move.** Two different fixes depending on which gap it is. If suitable assets already exist in the account but are attached to nothing, attach them: that is a usage gap. If no suitable asset exists, the move is a production request, with the required aspect ratios named. Missing images on a PMax asset group is a LOW creative finding: PMax can legitimately run without images. Incorrect information or a compliance issue on a live ad outranks it every time.

**Do not move when.** The campaign is a Search campaign. The campaign is paused or in a deliberate hold. The asset group is policy-limited and an appeal is pending: hold asset edits until it resolves (PB-18). The asset that would be attached fails the brand, legibility, or message-match bar: attaching a wrong-brand image to a legal client is worse than leaving the gap, and the brand call is a human review, not a vision verdict.

**Expected result and verification.** Impressions appear on image inventory for the campaign within 14 days. Verify at 14 days: `get_asset_usage` for attachment, campaign impressions by network for serving.

**Card line.**

```text
playbook PB-21 (Westhollow - PMax Mediation): standard move for a PMax asset group with no image assets attached, a low finding, is attaching existing on-brand assets, or a production request if none fit. accept/reject
```

**Related.** SKILL.md "Creative and asset audit" and Step 4b; `references/creative-audit.md` sections (a) and (c) and the source-tier table. Cross-refs PB-22, PB-32.

---

## PB-22: Image-asset fatigue

**Evidence.** `textbook only`. Same gap as PB-21. Zero image outcomes across every account.

**Trigger.** An in-use Performance Max image asset live and unchanged for a long stretch (cross-referenced against change history) with declining signals on meaningful volume: falling CTR or rising cost per result where per-asset metrics exist, otherwise ad-group or campaign CTR decline on stable creative, explicitly labelled a proxy.

**Pre-flight green.** Volume is meaningful. Change history (GAQL 8.1) confirms when creative last changed.

**Standard move.** Refresh the asset: a new execution on the same message, matched to the ad group's practice-area intent, at the aspect ratios the inventory needs. Retire or replace, do not simply add, where the fatigued asset is absorbing the impressions.

**Do not move when.** The volume is trivial, where a CTR wobble is noise, not fatigue. Per-asset performance is unavailable and the campaign-level proxy is itself explained by something else (budget change, seasonality, disapprovals). The asset is new.

**Expected result and verification.** CTR on the ad group recovers toward its prior band within 30 days of the new asset accruing impressions. Verify at 30 days: campaign or ad-group CTR, plus per-asset metrics where exposed. Say which tier the reading came from.

**Card line.**

```text
playbook PB-22 (Westhollow - PMax Probate): standard move for a long-running PMax image asset with declining CTR on real volume is a same-message refresh at the needed ratios. accept/reject
```

**Related.** `references/creative-audit.md` section (d) and the prioritisation list; SKILL.md "Creative and asset audit"; audit checklist Section 4. Cross-refs PB-20, PB-21.

---

# Tracking and measurement

## PB-23: Conversion-action config drift

**Evidence.** `partially validated`

_Refresh 2026-09._ Per-lead matching proved that a thank-you-page import and a CRM import counted the same submission. The noisier action was demoted, but the final volume and bidding impact remain pending. A secondary action continuing in `all_conversions` is not a tracking failure.

_What happened when we did it._ Detection is validated across two accounts and the real-world state is worse than this entry implies: one account carries 44 enabled primary actions with 38 silent over 30 days, junk page-view actions counted in the Conversions column and firing, a legacy phone-vendor action still primary at zero volume, and five of six live campaigns bidding Maximize Conversions on the account-default goal set, so any junk that fires steers the bidding. Remediation has never been applied, so the FIX has zero outcomes. Separately validated as a gate: a primary that goes silent by vendor design is not drift. See the do-not-move block.

**Trigger.** Any of: a primary action that previously fired weekly goes silent for 14+ days with meaningful clicks (`PROPOSED`); a primary action that has never fired; two primaries proven by event-level matching to fire on the same lead; a lead action left at `ONE_PER_CLICK` with no recorded override, against the house standard `MANY_PER_CLICK` (agency-defaults.md Sec 3.4; situational, not universally correct for legal PPC: an agency may choose `ONE_PER_CLICK` where repeat events are noise, recorded as an override): info severity, not a red flag.

**Pre-flight green.** This is PF-1 itself, and PF-1 is a configuration check: a scanner reporting conversion volume or conversion silence has verified none of it.

**Standard move.** Match the fix to the drift.

- Silent primary that used to fire: treat as a break, diagnose by action type (page URL change for WEBPAGE, forwarding config for AD_CALL, lead rule and GCLID capture for UPLOAD_CLICKS), repair, then apply PB-06.
- Never-fired primary: a standing configuration error, not an acute event. Report it separately from any current drop.
- **Ebook and guide downloads are PRIMARY.** They are never demotion candidates, in any account or campaign, whatever their volume or category looks like. A recommendation to demote, exclude, or discount an ebook conversion is wrong on its face. The same holds for the CRM-native and tag-manager or analytics versions of the same event.
- Duplicate pair: demotion requires per-lead matching, and nothing else will do. Match the two actions lead by lead across systems and show that the same submission produced both. Only then demote, and demote the noisier duplicate, not the canonical one. Matching totals, similar ratios, and matching non-integer conversion tails are at most a prompt to go and look. They are never evidence, and on the one account where duplication was later proven per lead the decimal fingerprint came back negative.
- **Canonical action and basis break (fold, 2026-09).** Once event-level matching proves two primaries fire on the same lead, keep the once-per-real-lead action canonical, demote the noisier duplicate, record the effective date, start PB-06, and reconstruct both sides of every comparison spanning that date from action-level data. A non-retroactive change means the two sides of a week-over-week or 30-day read use different definitions, which manufactures a false collapse. Do not fold on aggregate totals or decimal tails at all: per-lead matching is the only proof.
- A secondary action still accumulating in `all_conversions` is not a tracking failure. It is a secondary action doing what secondary actions do.
- `ONE_PER_CLICK` on a lead action with no recorded override: set `MANY_PER_CLICK`, the house standard. Info-level card line only, not a red flag. If an override is on file for that action (repeat events recorded as known noise), this is OVERRIDE-MATCH, not a finding.

**Do not move when.** The action is an ebook or guide download: it is primary by standing ruling and no demotion branch applies to it. The only duplicate evidence is aggregate totals or similar decimal tails, with no per-lead matching: go and look, do not demote. The zero is low-volume noise on a genuinely low-volume action while the account's other primaries are still firing: verify against the other primaries before calling a break. This is the measured case, twice: a scanner-flagged zero week on an action that runs one to three a week, with the sibling qualified-lead and lead-form primaries both still firing in the same week. **The silence is by vendor design.** Where a call-tracking platform pushes only qualified or quotable leads into Google Ads, or where tracking numbers have been deliberately retired at the vendor, the affected primary going quiet is the configuration working, not drift. Check the vendor's push rules and the account's standing rules before calling any silence a break: on one account this exact shape was raised as a tracking gap and resolved as working-as-designed, then recurred by design a month later. The window is immature. A scanner flag is the only evidence and the configuration itself has not been read. A lead action running `MANY_PER_CLICK` is the house standard, not a deviation: every touch is signal under data-driven attribution with automated bidding, so it is never a finding on its own. A lead action left at `ONE_PER_CLICK` under a recorded override (repeat events known to be noise for that specific action) is also not a finding, it is OVERRIDE-MATCH. Only an unrecorded `ONE_PER_CLICK` against the house standard is.

**Expected result and verification.** The action resumes firing at its prior weekly rate, or the primaries set matches what the firm counts as a lead. Verify at 7 and 28 days (unconfirmed windows): GAQL 2.1 for configuration, GAQL 2.2 for volume by action, weekly not just 30-day.

**Card line.**

```text
playbook PB-23 (account): standard move for a primary conversion action silent 14+ days on live click volume is diagnose by action type, repair, then a 2 to 4 week bidding freeze. accept/reject
```

**Related.** SKILL.md PF-1 and the `ppc_flags` input contract; diagnosis trees PF-1 and Tree 7 Steps 2 to 4; audit checklist PF-1. Cross-refs PB-06, PB-24, PB-30.

---

## PB-24: Call-tracking anomaly

**Evidence.** `validated in practice (2 outcomes)`

_What happened when we did it._ Both measured instances were FALSE positives, correctly held. First: an automated scanner flagged a call primary reading zero for a week against a four-and-four baseline, while the sibling primaries, a qualified-lead call action and a lead form, were both still firing that same week. The zero was low-volume noise on an action that runs one to three a week. Second: a campaign reading zero conversions resolved as the call-tracking vendor pushing qualified leads only into Google Ads, by configuration, account-wide. Time to signal both times: same session, from one sibling-primary pull. In low-volume legal accounts a weekly zero on a minor primary is the base rate, not the exception.

**Trigger.** A primary call action down >= 50% versus its trailing 4-week average while form actions hold, or up >= 2x (`PROPOSED` both directions), over a complete week.

**Pre-flight green.** PF-1. The comparison uses aligned complete weeks. The window is outside the conversion lag.

**Standard move.** Split by direction and integration type.

- Drop, Google-native `AD_CALL`: query `call_view` over the window. Records present rules out a Google-side capture failure. It does not rule out a capture problem generally and it does not establish real demand: reconcile the sibling primaries and the call vendor's qualification filter before calling the drop real demand. Both measured instances were resolved at the sibling check. Zero records over a normal-volume window means the forwarding or tracking configuration is the fault.
- Drop, third-party (`UPLOAD_CLICKS`): check the two silent failure modes, a missing or changed lead rule in the platform's Google Ads integration, and GCLID capture on the landing page, with Enhanced Conversions as the phone-match fallback.
- Spike: check for a new tracker, a duplicated number, or a second integration uploading the same calls before treating the volume as real. A spike that is really double counting degrades smart bidding exactly as a duplicate action does (PB-23).

**Do not move when.** The action is low-volume by nature (a handful of calls per week), where zero in one week is noise and the other primaries confirm tracking is intact. A tracker change is already on record for that window. The account is in a known site-outage window, which explains a call drop without any tracking fault.

**Expected result and verification.** Call volume returns to its trailing band, or the spike resolves as an identified duplicate. Verify at 7 and 14 days: GAQL 2.2 weekly by action, plus `call_view` for native calls.

**Card line.**

```text
playbook PB-24 (account): standard move for a primary call action halving while forms hold is a call_view and lead-rule check before treating the drop as demand. accept/reject
```

**Related.** Diagnosis trees Tree 7 Step 4 (consolidated here); audit checklist PF-1 (third-party lead rule); SKILL.md "Conversion lag". Cross-refs PB-23, PB-30.

---

## PB-25: Landing-page and post-click quality blocker

**Evidence.** `partially validated`

_Refresh 2026-09._ No remediation outcome. The delta quantified a landing-page blocker across a large share of scored keywords, but third-party access still prevents execution.

_What happened when we did it._ The DIAGNOSIS is validated over roughly three months on one account: rank-lost held at 52-67% with budget-lost near zero, ad strength POOR across the scored set, and the landing page confirmed as the binding constraint. The FIX has never been executable, because a third party owns the page and code access has been an open client ask throughout. That is the practical finding: when the page is not ours, this is not an in-account move, it is a client-relationship escalation with a multi-month clock, and re-presenting it as a move every week wastes checks. Separately validated as a detection gap: page AVAILABILITY, not only page quality. A monitored client site showed 18 of 21 nights down in a recurring late-night window, and nothing inside Google Ads reports a landing page that times out.

**Trigger.** `post_click_quality_score` BELOW_AVERAGE on keywords carrying >= 25% of campaign spend (`PROPOSED`), or CVR that has never been strong across the life of the campaign on meaningful click volume, or high CPC with zero conversions over 14+ days while impression share is adequate (> 30%) (unconfirmed).

**Pre-flight green.** PF-1 first: zero conversions with meaningful clicks is a tracking hypothesis before it is a landing-page one. Then PF-2 and PF-3.

**Standard move.** Treat the landing page as the binding constraint and sequence around it: landing page first, then ad relevance, then ad copy. Do not optimise copy or bids on a page that does not convert. Because page quality is not API-assessable, the move includes the blind-spot request, phrased exactly:

```text
BLIND SPOT: Landing page quality cannot be assessed via API.
→ Please share a screenshot of the landing page receiving this campaign's traffic (clear CTA, message match to the ad, phone number above the fold, mobile behaviour).
```

**Do not move when.** The landing page is controlled by a third party and the constraint is already recorded as a standing item. Even then, note that the flag is a hypothesis with a shelf life: re-pull before re-asserting it, because a creative refresh can close a gap long blamed on the page (PB-20). Retire the flag when the data shows it no longer binds.

**Expected result and verification.** CVR and `post_click_quality_score` improve within 30 to 60 days of a page change (unconfirmed). Verify at 30 and 60 days: GAQL 3.1 for the component, GAQL 6.1 for CVR. Nothing verifies faster than 30 days here.

**Card line.**

```text
playbook PB-25 (Westhollow - Divorce): standard move for post-click quality below average across a quarter of campaign spend is landing-page work before any bid or copy change. accept/reject
```

**Related.** Diagnosis trees Tree 1 Step 4 and Sub-tree B (consolidated here); SKILL.md "Prior state versus live data" (standing flags have a shelf life) and "Campaign-Level CPC Anomaly" high-CPC branch; knowledge base "Diagnosing Performance". Cross-refs PB-02, PB-20.

---

# Network and geography

## PB-26: Search Partners CPA distortion

**Evidence.** `textbook only`. A network was switched off without a pre-decision split, and no isolated network outcome has been recorded.

_Refresh 2026-09._ The delta confirms that the required segmentation was skipped, not that exclusion worked.

**Trigger.** A campaign is running on both Search and Search Partners with no note on the account or the campaign explaining it. Search Partners being enabled is itself the trigger: it is atypical for these accounts and it is not wanted. It is flagged, not automatically switched off, and a recorded note on the account or campaign clears the flag.

**Pre-flight green.** PF-2 (network settings read).

**Standard move.** Report the blended CPA as the account's CPA, and flag Search Partners separately as an atypical, unwanted network setting with no reason on record. The blended figure is the most accurate statement of what the account actually paid per conversion: it is never withheld pending a split, never replaced by the Search-only number, and never described as invalid. Then pull performance by `segments.network`, clicks, conversions, cost and CPA per network, and report the split underneath the blended figure as supporting detail. The split informs an exclusion decision; it does not substitute for the reported CPA. Then:

- Partners CPA above target and Partners conversion volume small relative to Search: exclusion is the reasonable move, signal loss minimal.
- Partners CPA above target but Partners contributing significant conversion volume: exclusion carries real signal risk. Check whether blended CPA stays on target without it before deciding.
- Search CPA already on target: the issue is contained to Partners and exclusion is the likely fix, after confirming volume contribution.

**Do not move when.** The campaign is near the reliability floor for its volume, where removing Partners can push it under and destabilise smart bidding. The network split has not actually been pulled: no exclusion decision on an unsegmented number. Note that this gates the exclusion decision only. It never gates reporting the blended CPA, which ships either way. The conversions in the window are provisional.

**Expected result and verification.** If Partners is excluded, the blended CPA (still the reported number) moves toward the former Search-only figure, and total conversion volume falls by no more than the Partners contribution. Verify at 28 days: GAQL 6.1 with `segments.network`, and conversion volume against the reliability floor.

**Card line.**

```text
playbook PB-26 (Westhollow - Custody): standard move for Search Partners enabled on a Search campaign is flagging the setting and pulling the network split beneath the reported blended CPA, exclusion only after the volume contribution is known. accept/reject
```

**Related.** SKILL.md "Search Partners and the blended CPA" (consolidated here in full); knowledge base "Campaign Structure" (network settings); audit checklist PF-2. Cross-refs PB-07, PB-27.

---

## PB-27: Search Partners or Display enabled on a Search campaign by mistake

**Evidence.** `partially validated`

_Refresh 2026-09._ No attributable outcome. Search Partners and rotation changed together, with the actor and exact change date unresolved.

_What happened when we did it._ Applied once, on a campaign pair whose weekly CPL had risen over 150% on falling conversions and which carried the account's only Search-Partners-on configuration. The outcome had not been read when this file was last revised. The move was made together with an ad-rotation change in the same session, which will make attribution impossible: a live illustration of this entry's own one-change-at-a-time rule.

**Trigger.** `network_settings.target_partner_search_network = TRUE` or `network_settings.target_content_network = TRUE` on a Search campaign with no documented justification on record.

**Pre-flight green.** PF-2. Account notes and standing rules checked for a documented deliberate reason.

**Standard move.** Turn the network off, one at a time, not both in the same week, and note the date so the change is attributable in the next read. Search network only is the default and Search Partners being enabled is flagged as atypical. That partners and display deliver inferior traffic for legal at the same cost is a general expectation, not a measured result on these accounts.

**Do not move when.** A documented reason is on record. The campaign is inside a learning period, where a network change resets the clock: sequence it after the window. The network is carrying a material share of conversions, where PB-26's volume test governs the Partners case. Both networks are on and someone proposes flipping both at once, which makes the result unattributable.

**Expected result and verification.** Impressions and clicks fall on that network to zero, CPA on the remaining Search traffic holds or improves. Verify at 28 days: GAQL 6.1 segmented by network, and total conversion volume against the reliability floor.

**Card line.**

```text
playbook PB-27 (Westhollow - Divorce): standard move for display network on a Search campaign with no reason on record is switching it off alone, dated, then reading 28 days. accept/reject
```

**Related.** Diagnosis trees PF-2; audit checklist PF-2; knowledge base "Campaign Structure" (network settings) and "What Bad Looks Like". Cross-refs PB-26, PB-09.

---

## PB-28: Geo leakage in search terms

**Evidence.** `textbook only`

**Trigger.** Out-of-area location terms carrying >= 10% of the campaign's search-term spend (`PROPOSED`), or user-location data (GAQL 10.2) showing material spend on physical locations outside the target market.

**Pre-flight green.** Search-term integrity checks. Targeting settings read.

**Standard move.** Handle it with negatives and geo exclusions, not by changing the location setting. `PRESENCE_OR_INTEREST` is the house standard and is never a finding: do not compare a campaign against a presence-only ideal, and do not propose flipping the setting. The moves available are: negate the specific out-of-area geo tokens at campaign level (per PB-14, geo token only), and add explicit location exclusions for the out-of-area regions. The only location-setting item worth raising is a campaign explicitly set to presence-only against the house standard, or a wrong geo constant.

**Do not move when.** The out-of-area terms have converted: out-of-area searchers frequently understand which jurisdiction their matter falls under and are real prospects. The leakage is a handful of low-spend terms below the threshold. The campaign deliberately targets a wider region on record.

**Expected result and verification.** Out-of-area spend share falls, in-area impressions and conversions unaffected. Verify at 30 days: GAQL 10.2 for user location, GAQL 4.1 for the geo tokens, campaign conversions before and after.

**Card line.**

```text
playbook PB-28 (Westhollow - Divorce): standard move for out-of-area terms at 10%+ of the campaign's search-term spend is geo-token negatives plus location exclusions, targeting setting unchanged. accept/reject
```

**Related.** The presence-or-interest standing rule; knowledge base "Geography and Topic as Strategy"; audit checklist Section 5; negative keyword library Section 6. Cross-refs PB-13, PB-14.

---

# Account-level patterns

## PB-29: CPL creep with flat conversions

**Evidence.** `partially validated`

_Refresh 2026-09._ Held CPL gaps cooled, but one comparison crossed a counting-basis change and another omitted the required 30-day read. Weekly improvement cannot close a 30-day playbook.

_What happened when we did it._ This pattern fires readily and was WRONG in the largest instance we have measured. During a deliberate spend ramp, an account's 30-day CPL read worse for about five weeks running, peaking near +68% on flat conversions, a textbook trigger for this entry, before crossing to flat and then about 9% better as the added spend matured into conversions. Firing at week three would have decomposed a defect that did not exist and argued for cutting a ramp that was working. See the Contradiction note; PB-34 now owns the ramp case.

**Trigger.** 30-day CPL up >= 20% versus prior 30 days (`PROPOSED`) with conversions inside +/-10% (`PROPOSED`), holding across 2 consecutive checks (`PROPOSED`), on aligned complete windows, at or above the reliability floor. A CPL move over ~30% is a red-flag item and leads the card regardless of what this playbook does (unconfirmed threshold).

**Pre-flight green.** PF-1, PF-3. Windows aligned complete-to-complete. Conversions mature (outside the ~72-hour lag). Currency native, no cross-account comparison. **Plus the ramp gate: spend across the two windows is inside +/-15% (unconfirmed).** If spend rose materially, this playbook does not fire and PB-34 owns it. Pull spend direction before CPL direction, every time.

**Contradiction: the biggest instance we measured was not a defect.** During a deliberate spend ramp, an account's 30-day CPL read worse for roughly five consecutive weekly checks, peaking near +68% on flat conversions, which is a clean trigger for this entry twice over. Nothing was wrong. The added spend had simply not matured into conversions yet: by week six the same 30-day window read flat, and shortly after about 9% better on spend up more than half. Decomposing CPC versus CVR at week three would have produced a confident, well-evidenced, wrong answer, and the natural recommendation from it (stop buying) would have killed a working ramp. CPL creep is only a defect when nothing structural changed, which is what the ramp gate above now enforces.

**Standard move.** Decompose before acting: CPL = CPC divided by CVR. Pull which side moved.

- CPC rose while CVR held: check rank-lost IS. Rising rank loss alongside CPC is competitive pressure, and the move is to decide whether the account's CPA is still acceptable at the new auction price, not to reflexively bid up.
- CVR fell while CPC held: route to the conversion-rate side, landing page and search-term mix (PB-25, PB-13).
- Both moved: sequence CVR first, then CPC. Do not optimise cost per click on a broken funnel.

**Do not move when.** The prior window contained an anomaly (an outage, a tracking gap, a one-off spike) that makes it a bad baseline. The conversion count is below the reliability floor, where a single conversion can swing CPL far beyond 30 to 50%. Seasonality explains it (PB-31). The move is inside a learning window.

**Expected result and verification.** The identified driver is named with data before any change; after the change, CPL returns toward its prior band. Verify at 30 days: GAQL 6.1 for CPC, CVR and CPL, GAQL 5.1 for IS.

**Card line.**

```text
playbook PB-29 (account): standard move for a 20%+ 30-day CPL rise on flat conversions is decomposing to CPC versus CVR before any bid or budget change. accept/reject
```

**Related.** SKILL.md "Output Format" direction rules and "RED FLAGS FIRST"; diagnosis trees Tree 2 and Tree 4 Step 2; audit checklist PF-0. Cross-refs PB-02, PB-13, PB-25, PB-31.

---

## PB-30: Zero-conversion spend streak

**Evidence.** `partially validated`

_Refresh 2026-09._ A three-week zero-conversion streak ended on one conversion, but the structural branch and keep-or-kill decision were never completed. A streak break is positive direction, not clearance.

_What happened when we did it._ Zero-conversion streaks are common at legal volumes and have been observed repeatedly across accounts. Exactly one move has ever been made against one, a budget raise, and it made matters worse: spend up 44 to 74%, clicks flat or down, avg CPC up 68 to 74%, and the streak unbroken. That outcome is now a do-not-move condition on PB-01 and is the strongest evidence in this file for routing a zero-conversion streak to structure rather than to money.

**Trigger.** 2 or more consecutive complete weeks with zero conversions and material spend on an ENABLED campaign (`PROPOSED`: material = at least 1x target CPL spent in the window). This is a red-flag item and leads the card.

**Pre-flight green.** PF-1 before anything: an account-wide zero is a tracking hypothesis first. PF-2 (ads serving, not disapproved). Windows complete and mature.

**Standard move.** Route by scope and by what else is true.

- Zero across the whole account: tracking, until PF-1 proves otherwise (PB-23, PB-24).
- Zero on one campaign while others convert, with adequate impression share and high CPC: the landing page or the audience (PB-25).
- Zero on one campaign with thin history and a high CPC: the bidding model has nothing to work with (PB-08).
- Zero with an anomalously low CPC against the campaign's own trailing median: data integrity first (PB-33).

Whatever the route, the streak itself is not the fix: the move is to name the branch with data and pull the branch's query set.

**A streak break ends the run, not the diagnosis (fold, 2026-09).** When a multi-week zero-conversion streak breaks on one provisional or sub-floor conversion, reset the streak count and record the positive direction, but keep the 30-day spend and CPL read and the structural branch open until reliable volume or an intake-quality review closes the decision. One conversion is not clearance. Equally, do not keep describing the streak as active once it has broken.

**Do not move when.** The campaign is genuinely low volume and the zero weeks alternate with converting weeks, which is lumpiness at low volume, not a streak. The window is provisional. A site outage covers the window. The campaign is new (PB-09). One conversion is being used either to declare the campaign fixed or to keep the old streak alive.

**Expected result and verification.** The branch is identified within the same check; after the branch's fix, conversions resume within its own verification window. Verify weekly until the streak breaks: GAQL 6.3.

**Card line.**

```text
playbook PB-30 (Westhollow - Probate): standard move for 2+ weeks of material spend at zero conversions is PF-1 first, then routing on impression share and CPC. accept/reject
```

**Related.** SKILL.md "Campaign-level CPC anomaly"; diagnosis trees Tree 1 and Tree 7. Cross-refs PB-08, PB-23, PB-25, PB-33.

---

## PB-31: Seasonality dip

**Evidence.** `textbook only`. A seasonal read has been asserted once on an account we run without the same-period-last-year check this entry requires. Until that check is run, an unverified seasonal claim is an open question, not a finding, and it is the cheapest available excuse for a slide.

**Trigger.** A volume or conversion decline that coincides with a known practice-area seasonal pattern, where the same period last year is within +/-15% of the current period (`PROPOSED`) and change history shows no structural change.

**Pre-flight green.** PF-3 (nothing changed). Year-over-year data exists and spans a comparable period. Windows aligned.

**Standard move.** Do nothing, and say so with the data. The standard move for a confirmed seasonal dip is to hold budgets, targets, and structure, record the pattern as account context so the next check does not re-diagnose it, and set the review for when the season is expected to turn. Volume in legal moves over weeks, not days: a drop is evaluated over weeks.

**Do not move when.** There is no year-over-year data, in which case seasonality is a hypothesis, not a finding, and it does not get presented as an explanation. The decline exceeds the seasonal band. Structural changes exist in the window. The account is being asked to hit a volume target regardless of season, which is a budget decision for the operator, not a playbook.

**Expected result and verification.** Volume recovers on the historical schedule. Verify at the expected turn: GAQL 6.3 weekly against the same weeks last year.

**Card line.**

```text
playbook PB-31 (account): standard move for a decline matching last year's same-period pattern with no account changes is hold and record, review at the expected turn. accept/reject
```

**Related.** Diagnosis trees Tree 4 Step 3 (seasonal blind spot); knowledge base "Diagnosing Performance" (volume drops in legal); SKILL.md PF-0 macro context. Cross-refs PB-29, PB-30.

---

## PB-32: PMax post-launch, first 14 days

**Evidence.** `partially validated`

_Refresh 2026-09._ Locked ruling applied. Two PMax launches reached day-3 serving reads and one reached a second weekly read, but the complete day-14 configuration and goals read is missing. Brand and final-URL overrides require measurement at the final test judgment.

**Trigger.** A Performance Max campaign inside its first 14 days. The knowledge base position stands: PMax is avoided for law firms by default. This playbook governs one that is live by operator decision.

**Pre-flight green.** PF-2 and PF-3. The campaign's presence is on record as deliberate: an undocumented PMax campaign is a PF-2 structural flag first, and this playbook does not apply to it.

**Standard move.** Two polls, then hold. The day-3 verify-poll is validated on two launches. The day-14 full configuration and goals read is still `PROPOSED` and has never been completed.

- **Day 3 poll, serving and policy only:** status and serving state, budget pacing, bid strategy, conversion goals at campaign level, asset group review state, disapprovals, spend, plus the cap block below. Nothing else. No performance judgment.
- **Day 14 read:** the same, plus first spend and conversions, plus what the campaign is actually optimising on (which goals are reachable), plus the override block below.

**Cap tracking, both polls (fold, 2026-09).** A PMax campaign launched with a fixed daily budget and a hard total-spend cap carries four extra fields at every poll: cumulative spend to date, recent pace, the estimated cap date derived from that pace, and the named cap-or-kill owner. A bounded test that reaches its cap without a decision on record becomes an unbounded park, which is the observed failure mode. Do not use short-term performance as the reason to move while the campaign is still inside its cap.

**Overrides require measurement at judgment (fold, 2026-09).** Brand exclusion and final-URL expansion are the two structural corrections available in this window: exclusions so the campaign does not harvest branded queries as its easiest conversions, and expansion off so it does not invent landing pages. Where either is deliberately overridden for a bounded test, brand-query share and landing-page distribution are required inputs at the final test judgment. Without them the campaign cannot be credited with new-client conversions. An override is a recorded decision, not an unconditional exclusion rule.

**A policy-limited asset group is handled, not rebuilt (fold, 2026-09).** When a serving asset group becomes policy-limited while its individual assets remain approved, obtain the human-readable policy reason, appeal where appropriate, record the appeal date, and hold asset edits until it resolves. Report serving separately from policy clearance: continued spend does not mean the limitation cleared. See PB-18.

Goals are corrected if a soft action is primary, subject to the standing ruling that ebook and guide downloads are primary and are never the soft action in question. Everything else waits.

**Do not move when.** Performance is the reason. A 14-day PMax read is not a performance verdict, and custom goals or target changes before performance data exist have nothing to calibrate against. The campaign is still inside its approved test cap. An asset-group appeal is pending: no asset edits until it resolves. Geographic overlap with an existing campaign is not automatically a defect: it may be accepted deliberately. The location setting is `PRESENCE_OR_INTEREST`, which is the house standard and never a flag.

**Expected result and verification.** Assets clear review and serve; goals match what the firm counts as a lead; branded queries are excluded or the override is on record with its measurement attached; cumulative spend is tracked against the cap with a cap date and an owner. Verify at day 3 and day 14 against the poll list, then fold the campaign into the normal cadence.

**Card line.**

```text
playbook PB-32 (Westhollow - PMax Mediation, day 3): standard move inside the first 14 days is the serving-and-policy poll plus brand exclusions, no performance read. accept/reject
```

**Related.** SKILL.md PF-2 and "Account macro context"; knowledge base "Bidding" (Performance Max). Cross-refs PB-09, PB-18, PB-21, PB-23, PB-41.

---

## PB-33: Anomalously low campaign avg CPC

**Evidence.** `textbook only`. Never observed on an account we run.

**Trigger.** Campaign-level avg CPC well below the campaign's own trailing 30-day median and well below the account's other campaigns, read from campaign performance rather than search terms. There are no practice-area CPC bands: every campaign is judged against its own trailing median CPC. A gap against that median is a prompt to look, never a threshold to act on.

**Pre-flight green.** Currency confirmed as the account's own: a low number in a different currency is not a low CPC. PF-1.

**Standard move.** Data integrity first, keyword targeting second. In order: check tracking integrity, then pull campaign history (PF-3) to establish the CPC trajectory. A CPC that was historically normal and recently dropped means something changed: tracking, keyword structure, or a bid-strategy reset. Only after contamination is ruled out does the keyword and match-type frame apply, and only if search-term data confirms the clicks are genuinely low-intent queries at low cost.

**Do not move when.** The instinct is to explain cheap clicks as wrong match type or low-intent keywords straight away. That frame is secondary here and routing to it first has produced misdiagnosis. The data is handed rather than pulled, where legal terms under ~$2 per click signal paused-ad-group history in the export, and the move is to confirm the source, not to act. The campaign is brand, where low CPC is expected.

**Expected result and verification.** Either the contamination is identified and the figure is restated, or the trajectory confirms the CPC is real and the keyword frame opens. Verify within the same check: GAQL 6.2 and 6.3 for the CPC trajectory, GAQL 4.1 for the query mix.

**Card line.**

```text
playbook PB-33 (Westhollow - Divorce): standard move for a campaign avg CPC far under its own trailing median is a tracking and history check before any keyword read. accept/reject
```

**Related.** SKILL.md "Campaign-level CPC anomaly: routing protocol" (consolidated here in full) and "Auditing search term data you are handed". Cross-refs PB-08, PB-23, PB-30.

---

## PB-34: Spend ramp in progress, CPL reading worse

**Evidence.** `validated in practice (1 outcome, eight sequential 30-day readings)`

_Refresh 2026-09._ The same ramp produced one additional clean-basis 30-day reading, about 25% better on substantially higher spend and conversion volume. This extends the sequence without incrementing the outcome count.

_What happened when we did it._ An account ramped spend hard over about six weeks through expansion and new campaigns. Its 30-day CPL read WORSE at every check for roughly five weeks, peaking near +68% against the prior 30 days on conversions that were flat to slightly down. Then it crossed: 30-day CPL flat at week five, about 5% better at week six, about 9% better at week seven, on spend up 58 to 80% and conversions up 73 to 88%. The weekly CPL turned about two weeks before the 30-day did. Nothing was fixed in between; the added spend simply matured. Time to signal: expect the 30-day window to look wrong for four to six weeks after a material ramp starts.

**Trigger.** Account or campaign 30-day CPL up materially against the prior 30 days, WITH spend up materially over the same windows (the two moving together is the signature), during or within about six weeks of a deliberate expansion: new campaigns, new geographies, a keyword expansion, a budget programme, or any combination.

**Pre-flight green.** PF-3 change history pulled, so the ramp is established as a fact with dates rather than inferred. Windows aligned complete-to-complete. Conversions mature. Weekly series pulled alongside the 30-day, because the week turns first and is the early read.

**Standard move.** Hold the CPL verdict and report the arithmetic instead. State three numbers together every check: spend direction, conversion direction, CPL direction, in that order. A ramp where conversions are rising faster than spend is working even while CPL reads worse than the pre-ramp baseline, because the baseline is a smaller, older account. Name the date the 30-day window will have fully absorbed the ramp and make that the review point. Do not reallocate, do not cut, and do not decompose CPC versus CVR while this is live.

**The one thing to watch instead of CPL.** Conversion direction. A ramp with rising conversions and rising CPL is buying volume at a premium, which is a business decision and belongs to the operator. A ramp with FLAT OR FALLING conversions on materially higher spend, sustained past about four weeks, is not maturing and routes to PB-30 or PB-29 with the ramp gate now satisfied.

**Do not move when.** This entry is a hold, so the question is when it stops applying: the ramp is more than about six weeks old and conversions have not moved; the spend rise was not deliberate (an unintended budget or bidding change is a defect, not a ramp); or the conversion count is below the reliability floor for that account, in which case none of these percentages mean anything and the honest output is the raw counts.

**Expected result and verification.** The 30-day CPL crosses back toward, and often below, the pre-ramp baseline four to six weeks after the ramp begins, driven by conversion growth rather than by spend falling. Verify weekly on the same aligned windows: GAQL 6.1 for spend, conversions and CPL at both 7 and 30 days, and hold the same window definition across checks so the series is comparable.

**Card line.**

```text
playbook PB-34 (account): standard move for a 30-day CPL rise that sits alongside a deliberate spend ramp is holding the CPL verdict and reading conversion direction until the window absorbs the ramp. accept/reject
```

**Related.** Legal PPC realities item 1; SKILL.md direction rules. Cross-refs PB-01, PB-29, PB-30, PB-35.

---

## PB-35: New market test at a deliberately small daily cap

**Evidence.** `validated in practice (1 outcome)`

_What happened when we did it._ Two campaigns were launched into a new county at a small fixed daily cap each, built on existing shells with proven copy. They converted from day three at roughly half the account's blended 30-day CPL, held that through weeks one and two, and were then raised in one step to double the cap, after which they produced the account's cheapest CPLs for the following month. The cap did the work: it bought a stable, cheap, decision-grade read for a small, bounded amount of money, and it made weeks one and two comparable to each other by construction. Time to signal: 3 days for direction, 7 for a decision.

**Trigger.** A question about entering a new geography, or a new practice-area segment, where the account already has proven copy and structure to clone and where the firm serves the market.

**Pre-flight green.** PF-2 on the cloned assets BEFORE launch: this is where a clone bites. Old firm-name text, stale descriptions, or ad copy inherited from a long-paused campaign will serve the moment the campaign is enabled. Run the rename and copy sweep on any reactivated or cloned shell first, and verify at the ad level, not the campaign level. Confirm the geo constant, and confirm the firm actually serves the market.

**Standard move.** Launch small and capped rather than modelled. Set a deliberately small fixed daily budget, clone the structure and copy that already convert, and let the cap ration the spend while the market answers. Read at day 3 for direction and at week 1 for the go or no-go band (PB-09 governs what may and may not be concluded from that read). Then, if the band is good and budget-lost is high, step the cap up under PB-01, which is where the measured budget-raise evidence lives.

Expect budget-lost impression share in the 50 to 80% range while capped. That is the measured range across two accounts, and it is the cap working as designed, not a finding, and it is the reason the read is stable rather than noisy.

**Do not move when.** There is no proven copy or structure to clone, in which case this is a build, not a test, and the launch risk is different. The account cannot spare the cap without taking it from a campaign that is already converting, which makes it an allocation decision for the operator. The firm does not serve the market, which is a question to ask before building anything, not after. A prior test in the same market has been run and closed: check the account's standing rules before proposing it again.

**Expected result and verification.** A directional read at day 3, a decision-grade band at day 7, and a stable week 2 that looks like week 1. Verify: daily spend, clicks and conversions for the first 3 days; then aligned weekly reads with both impression-share components. Pull per-campaign search terms at the first weekly read, so the waste picture is on record even if no negatives follow (PB-13).

**The measurement that is still missing.** A cheap CPL in a new market is not a proven market. Whether those leads become signed cases has never been checked in any account we run, and the same account showed one geography converting at a fraction of another's cost with no matched-back evidence about quality. Say this whenever a market test is presented as a success.

**Card line.**

```text
playbook PB-35 (new geo): standard move for testing a new market with proven copy available is a small fixed daily cap, cloned structure, direction read at day 3 and band read at day 7. accept/reject
```

**Related.** Legal PPC realities (intake quality over lead count); the pre-reactivation copy sweep rule. Cross-refs PB-01, PB-09, PB-13, PB-36, PB-38.

---

## PB-36: Reactivating a dormant campaign

**Evidence.** `validated in practice (1 outcome, verified in change history)`

_What happened when we did it._ Two campaigns dormant for many months were re-enabled after a pre-check confirmed their ads approved and no policy blocks. Three things then happened that the pre-check had not looked for. First, Google's low-activity system bulk change fired on reactivation day and auto-paused a large share of each campaign's keywords: dozens in one, a smaller batch in the other. Second, ad re-review produced a run of newly limited ads. Third, one campaign was effectively not serving at all at day three, with near-zero impressions and no clicks, which read as a launch failure but was the auto-pause. Reactivating the full paused keyword inventory restored serving, verified in change history with no re-pauses since, and impression share recovered into the 60 to 84% range. Conversions did not follow: both campaigns ran roughly one conversion each across the following six weeks on meaningful weekly spend. Verdict: mechanically met, commercially not.

**Trigger.** Any proposal to re-enable a campaign, ad group, or keyword set that has been paused for months, or the first check after such a reactivation.

**Pre-flight green.** Before enabling: ad-level copy sweep on the dormant inventory (PB-35's pre-flight, and the sharpest trap here, since paused inventory carries whatever was true when it was paused). Ad policy status pulled at ad level. Keyword statuses counted before the reactivation, so the after-count means something.

**Standard move.** Treat reactivation as a launch with an extra failure mode, and check the platform's own edits first.

1. **Before enabling:** run the copy and naming sweep on every ad in the dormant inventory. Record the count of ENABLED versus PAUSED keywords.
2. **Within 3 days of enabling:** pull `change_event` filtered for INTERNAL_TOOL entries and re-count keyword statuses. Google's low-activity auto-pause fires on exactly this inventory, and it fired on reactivation day in the case we measured.
3. **If keywords were auto-paused:** the decision to reactivate them is the operator's. Reactivating the full inventory rather than only the platform's batch is what was done and it worked mechanically, with no re-pauses observed since.
4. **Re-pull ad policy status at 3 and 14 days:** dormant ads get re-reviewed on reactivation and can come back limited even when they were clean before.
5. **Then treat it as PB-09:** the campaign is new again for judgment purposes, whatever its history says.

**The platform rule, from Google's own documentation, verified against a live reactivation.** The low-activity auto-pause has no off switch and has been platform-wide since 2024. It targets keywords 13+ months old with zero impressions in 13 months, and it re-pauses after 3 months of zero impressions following a reactivation. Do not promise the operator it can be prevented; schedule the re-check instead.

**Do not move when.** The campaign was paused for a reason that still holds: check the account's standing rules and journal before proposing reactivation, because dormant inventory is often dormant on purpose. The copy sweep has not been run. There is no budget for it that does not come out of a converting campaign.

**Expected result and verification.** Serving resumes within about a week and impression share climbs into a normal band. Conversion recovery is a separate and much slower question, and in the one case measured it did not arrive within six weeks: budget the reactivation as an experiment with a cost, not as a restoration. Verify at 3 days (serving, INTERNAL_TOOL change events, keyword status counts, ad policy), 14 days (serving stability, policy again), and 6 weeks (conversions, against the spend it consumed).

**Card line.**

```text
playbook PB-36 (Westhollow - Probate, dormant 9 months): standard move on reactivation is a copy sweep before enabling, then an INTERNAL_TOOL change-event and keyword-status check within 3 days. accept/reject
```

**Related.** The pre-reactivation copy sweep rule and the low-activity auto-pause; SKILL.md change-history section. Cross-refs PB-09, PB-18, PB-35, PB-37.

---

## PB-37: An unexpected change in the account, made by someone else

**Evidence.** `validated in practice (2 outcomes, one with measured cost)`

_Refresh 2026-09._ No increment. Another unexplained settings change was detected, but it lacks attribution and an isolated performance outcome.

_What happened when we did it._ An outside party with account access paused every running campaign. It was caught about 36 hours later during unrelated verification, not by a performance signal. The measured cost of those 36 hours: the affected week ran roughly 3 conversions against a four-week average near 17, and its CPL came in about four times the prior week's, on roughly half the spend. Read without the change log, that week is a catastrophic performance collapse demanding a diagnosis. Read with it, it is 36 hours of darkness and needs no diagnosis at all. The same external party recurred three weeks later with a different edit, which is why the watch became standing rather than closed.

**Trigger.** Any change event in the window that was not made by us or by the operator: an external user, an agency or vendor account, an automation, or the platform itself. Also fires on the reverse shape: a week whose numbers moved far more than any in-account explanation supports.

**Pre-flight green.** This IS a pre-flight. It runs before the performance read, not after it.

**Standard move.** Read the change log before the performance data, every check, on every account. When an unexpected change is found:

1. **Attribute it.** Who, what resource, what fields, what time. An external editor and an automated platform edit call for different responses.
2. **Quantify the dark window** if anything was paused or disabled: dates, hours, and the spend and conversions of the affected period against the trailing average. Do this before anyone tries to explain the period's performance.
3. **Report it verbatim and immediately.** An unexpected change on a live client account is a surface-now item, not a card line to rank against others.
4. **Make it standing, not closed.** External-editor access is a condition, not an incident. One occurrence means the access exists and will be used again, which it was.
5. **Quarantine the affected window** from every trend comparison that follows, and say in the card that you have done so.

**Do not move when.** The change is ours or the operator's and is already recorded (that is a verification, not a finding). The change is a known and accepted vendor behaviour already carried as a standing rule, for example tracking-template tagging by an integration partner. The platform's own routine edits are documented as such: separate genuine platform intervention, like a low-activity auto-pause (PB-36), from ordinary system churn like ad-review status updates, which are noise.

**Card placement: exempt from the 3-line cap.** PB-37 is a flag-class line, not an ordinary optimization playbook: report it in the `RED FLAGS:` block or immediately after it, not in the `PLAYBOOKS:` group, and it does not count against the 3-per-account playbook cap (SKILL.md "Optimization Playbooks"). An unexpected external change is a surface-now item per the standard move above, not something to rank against spend-at-stake for a card slot.

**Expected result and verification.** The account's edit surface is known and every unexplained performance move has a change-log answer or an explicit "no change behind this" statement. Verify every check: `change_event` for the full window since the last check, with the actor field selected, before any metric is read.

**Card line.**

```text
playbook PB-37 (account): standard move for an unexpected external change event is attributing it, quantifying any dark window, and quarantining that window from trend comparisons. accept/reject
```

**Related.** SKILL.md PF-3 and change-history verification; audit checklist change-history section. Cross-refs PB-09, PB-29, PB-34, PB-36.

---

## PB-41: A PMax launch contaminates blended account metrics

**Evidence.** `partially validated`

_Refresh 2026-09._ Detection is confirmed on a live account where a new PMax campaign supplied most of the account's clicks at a much lower CPC than Search. No decision has yet been made and measured on the split.

**Trigger.** A new Performance Max campaign supplies a material share of account clicks or conversions at a CPC or conversion mix unlike Search, and a blended CPC, CPL, or conversion rate is about to drive an account-level decision.

**Pre-flight green.** PF-2 (campaign types read, PMax presence on record as deliberate). Currency confirmed. Windows aligned and complete.

**Standard move.** Present blended, Search-only, and PMax-only results side by side. The blended figure remains the reported account number; the two splits sit underneath it. Treat the direction as robust only if it survives the Search-only split, or if the operator explicitly accepts the inventory-mix change as the thing being measured.

**Do not move when.** PMax is inside day 14 and the proposed action is performance-driven: segmentation explains the number, it does not accelerate PB-32. The PMax campaign's share of clicks and conversions is immaterial. The conversions in the window are provisional.

**Expected result and verification.** The account verdict is not an artefact of a cheap-click traffic class, and any recovery or decline is attributed to the campaign type that actually produced it. Verify within the same check: GAQL 6.1 segmented by campaign and campaign type, over the same window on both sides.

**Card line.**

```text
playbook PB-41 (account): standard move when a new PMax campaign materially changes the traffic mix is splitting Search-only and PMax results before any blended account verdict. accept/reject
```

**Related.** SKILL.md "Campaign-level CPC anomaly" and "Account macro context". Cross-refs PB-26, PB-32, PB-33, PB-34, PB-40.

---

## Not playbooks

These are method rules, not moves, and stay where they are:

- **GAQL query integrity** (`SKILL.md`). Query hygiene that must hold before any keyword or search-term playbook can trigger.
- **Premise verification and the pressure rule** (`SKILL.md`). Governs how a question is answered, not what is done to an account.
- **Rendered notes versus live data** (`SKILL.md`). Governs where a number may come from.
- **Output format, direction, currency, conversion lag** (`SKILL.md`). Governs the card, and constrains every playbook's trigger windows.
