# Diagnosis Trees — Google Ads for Law Firms

## How to Use This Document

These are diagnostic frameworks, not flowcharts. They guide judgment — they don't replace it. Work through the guiding questions in order, but be prepared to branch based on what you find. The trees cross-reference each other because real problems rarely have single causes.

**GAQL references** point to sections in `gaql-query-library.md` (e.g., "GAQL 2.1" = Section 2, Query 1).

**Blind spot callouts** appear wherever the API cannot provide what's needed. The screenshot protocol is:
> ⚠️ **BLIND SPOT — [what cannot be seen]**
> → Please share a screenshot of [exact location, with applicable filters/date range].

**Version note:** This skill has two operational modes:
- **Toby version** — reads `learnings.md` and the relevant `account-notes/[account].md` at session start. Has historical context. Generates a session log at session end.
- **Public version** — reads skill reference files only. No historical context. No session logging.

Sections marked *[Toby version]* describe behaviors that only apply in the internal version.

---

## Pre-Flight Checks

**Run before any diagnostic tree. These take priority over everything else.**

Pre-flight findings are not symptoms to diagnose — they are foundational problems that corrupt the meaning of everything else. A high CPA finding means nothing if conversion tracking is counting page views as leads. Fix the foundation first.

### PF-1: Conversion Tracking Verification

Pull: GAQL 2.1 (all conversion actions), GAQL 2.2 (recent conversion volume by action)

Work through these questions in order:

**Are there any enabled conversion actions?**
If no conversion actions are configured at all: the account has never had tracking. Flag as critical. No further diagnosis is meaningful until tracking is established.

**What is each enabled conversion action actually measuring?**
Evaluate the `type` and `name` fields together. The types that represent real leads in legal:
- `WEBPAGE` actions with names suggesting form completion, contact submission, or appointment booking
- `AD_CALL` or `PHONE_CALL` actions (auto-tracked call extensions)
- `UPLOAD_CLICKS` (offline import — only meaningful if the firm is actually importing intake data)

Flag immediately if the primary conversion action (`include_in_conversions_metric = TRUE`) is:
- A session or page view (name suggests "All Visits," "Sessions," "Time on Site")
- A soft engagement action (scroll depth, video play)
- A duplicate of another primary action with identical settings

**Is conversion volume plausible given clicks?**
If there are 500 clicks in 30 days but 0 conversions, the tracking is almost certainly broken — even low-converting legal accounts convert at some rate with that much traffic.

> ⚠️ **BLIND SPOT — Tag firing cannot be verified via API**
> The API shows conversion action configuration. It cannot confirm whether the tag is actually firing on the correct page events.
> → If conversions are zero despite meaningful click volume, please share a screenshot of the Google Tag Manager container (or GA4 debug view) showing whether the conversion tag fires on a form submission or call event.

**Are there duplicate conversion actions?**
Look for multiple actions of the same type with similar names and `include_in_conversions_metric = TRUE`. Duplicates inflate conversion counts and deflate CPA — the account appears to perform better than it does.

**What attribution model is being used?**
Data-driven attribution is fine for accounts with volume. Last-click is acceptable. Time-decay is acceptable. Position-based is unusual for legal. Flag any attribution model that seems inconsistent with how the firm's intake process actually works.

---

### PF-2: Structural Red Flags

Pull: GAQL 1.1 (all campaigns), GAQL 1.3 (ad rotation settings)

Evaluate against the good-account checklist from the knowledge base. These are binary flags — either present or not:

- **Performance Max campaign present?** Flag. PMax is almost universally wrong for law firms without overwhelming conversion history. Note which campaigns are PMax type.
- **Display/content network enabled on any search campaign?** Check `network_settings.target_content_network`. Flag if `TRUE` without a deliberate reason on record.
- **Search partners enabled?** Check `network_settings.target_partner_search_network`. Flag if `TRUE` — usually degrades lead quality in legal.
- **Ad rotation set to OPTIMIZE?** Check `ad_serving_optimization_status`. Flag if `OPTIMIZE` or `CONVERSION_OPTIMIZE`. Correct setting is `ROTATE_INDEFINITELY`.
- **Brand campaign isolated?** Review campaign names for evidence of brand/non-brand separation. There is no API flag for this — use naming convention as the signal. Flag if any campaign name suggests it may contain both.
- **Broad match keywords present?** Pull GAQL 3.2 (match type distribution). Flag any `BROAD` type keywords outside of explicitly named test campaigns.

*[Toby version]: Cross-reference structural flags against `account-notes/[account].md`. Some known accounts have deliberate exceptions to standard structure — don't re-flag things that have already been investigated and resolved.*

---

### PF-3: Change History Read

Pull: GAQL 8.1 (recent changes, 60 days), GAQL 8.2 (auto-applied changes, 90 days)

This is a narrative read, not a metric check. You are asking: what kind of account is this, and what kind of management has it received?

**Signs of neglect:** No changes logged in 3+ weeks on an active account. Budget running, no optimization, no negative keyword additions, no creative updates.

**Signs of Google mismanagement:** Long list of `client_type = GOOGLE_ADS_AUTOMATED_RULE` or `GOOGLE_ADS_RECOMMENDATIONS` changes. Auto-applied broad match expansions, auto-applied audience targeting, auto-applied budget changes. Each of these should be reviewed against knowledge base principles.

**Signs of learning phase disruption:** Multiple bid strategy changes within 14-day windows. This pattern — change, bad performance, change again, bad performance, change again — is the most common cause of smart bidding accounts that never stabilize. Note the dates and the sequence.

**Signs of recent structural changes that may explain current symptoms:** Budget increases/decreases, campaign pauses/enables, targeting changes. If these occurred within the last 30 days and the brief is about performance decline, they're the first hypothesis.

---

## Tier 1: Symptom Trees

---

### Tree 1: Conversions Are Low

**Entry:** Conversion volume is lower than expected, has dropped from prior period, or is zero.

**Pre-flight status check:** If PF-1 found tracking problems, fix those before continuing. Low conversions with broken tracking is not a campaign problem.

---

**Step 1: Is traffic the problem or conversion rate the problem?**

Pull: GAQL 6.1 (30-day campaign performance)

Look at clicks. If clicks are also low relative to impression share expectations, the problem may be upstream of conversion rate entirely.

- **Clicks are low / impressions are low** → Traffic volume is the issue, not conversion rate. Move to Sub-tree A (Impression Share Diagnosis).
- **Clicks are present in reasonable volume** → Conversion rate is the issue. Continue below.

What is "reasonable volume"? There is no universal threshold — evaluate relative to the account's own history (pull GAQL 6.2 for 90-day baseline and compare periods).

---

**Step 2: Is this a new problem or has CVR always been low?**

Compare current CVR (conversions ÷ clicks) against 90-day baseline (GAQL 6.2).

- **CVR has dropped from prior period** → Something changed. When? Cross-reference with change history (PF-3). Continue to Step 3.
- **CVR has never been good** → This is a structural or offer problem, not a recent change problem. The account may be driving traffic to an ineffective landing page. Continue to Step 4.

---

**Step 3: Did the drop correlate with an account change?**

Pull: GAQL 6.3 (weekly segmented performance) to pinpoint when the drop happened.

Cross-reference the timing with change history (PF-3).

- **Drop coincides with a structural account change** (bid strategy, targeting, budget, new keywords): that change is the primary hypothesis. Evaluate whether the change was sound per knowledge base principles. If the change was an auto-applied recommendation, it is the prime suspect.
- **Drop coincides with a smart bidding strategy change or budget change within 14 days**: likely a learning phase disruption. See Sub-tree D (Smart Bidding Instability).
- **Drop is gradual over 2–4 months with no structural changes**: creative staleness is the most likely cause. Check when ads were last updated (GAQL 8.1 change history + GAQL 7.2 ad performance). CTR decline preceding conversion rate decline is the pattern.

> ⚠️ **BLIND SPOT — Landing page changes cannot be detected via API**
> A common cause of sudden conversion rate drops is a website or landing page update that changed the form, CTA, or page structure.
> → Please share a screenshot of the current landing page for the affected campaigns, and confirm whether any website changes were made around the time of the drop.

> ⚠️ **BLIND SPOT — Competitor ad changes are not visible via API**
> New competitors entering the market or existing competitors improving their copy and offers can depress CVR without any change in your account.
> → Please share a screenshot of the Auction Insights tab for the affected campaigns (last 30 days), and optionally a manual search for your top keywords to see what competitor ads currently look like.

---

**Step 4: Is this a landing page / offer problem?**

If CVR has never been strong, the account is driving traffic to something that doesn't convert. This is not an ads problem — it's a conversion infrastructure problem.

Indicators: high click volume, meaningful spend, consistent zero or near-zero conversions over the life of the account. QS `post_click_quality_score` BELOW_AVERAGE (GAQL 3.1) supports this hypothesis.

> ⚠️ **BLIND SPOT — Landing page quality cannot be assessed via API**
> → Please share a screenshot of the landing page(s) receiving ad traffic. Assess: Is there a clear, prominent CTA? Is the messaging aligned with what the ads promise? Is there a phone number visible above the fold? Is the mobile experience functional?

*[Toby version]: Check `account-notes/[account].md` for prior landing page findings. If this has been flagged before and hasn't been addressed, note the recurrence in the session log.*

---

### Tree 2: CPA Is Too High

**Entry:** Cost per conversion is above target, has risen vs. prior period, or is clearly unsustainable.

**Pre-flight status check:** High CPA can be a tracking artifact. If conversion tracking is under-counting real conversions (e.g., only one conversion action is firing when two channels are converting), CPA will appear artificially high. Confirm PF-1 before treating CPA as a real signal.

---

**Step 1: Is this account-wide or campaign-specific?**

Pull: GAQL 6.1 (30-day, by campaign), sorted by cost

If one campaign is driving high CPA while others are acceptable, drill into that campaign specifically. If CPA is elevated across the board, the problem is systemic.

---

**Step 2: What is driving the high CPA — high CPC, low CVR, or both?**

CPA = cost per click ÷ conversion rate. These require different fixes.

Pull: GAQL 3.3 or 3.4 (keyword performance) for the affected campaigns. Look at average CPC and conversion rate at the keyword level.

- **CPC is disproportionately high for the market**: Is impression share rank loss elevated? Pull GAQL 5.1. High rank loss IS means the account is losing auctions on quality/bid grounds — throwing more money at bids may not fix this.
  - Move to Sub-tree B (Quality Score Diagnosis) before adjusting bids.
  
> ⚠️ **BLIND SPOT — Competitor CPC dynamics are not visible via API**
> Rising CPCs without account changes usually indicate increased auction competition. The API cannot show you who is bidding more aggressively or what their bids are.
> → Please share a screenshot of Auction Insights for the campaigns with elevated CPC (last 30 days vs. prior 30 days if available). This will show whether new competitors have entered or existing ones have increased their presence.

- **CVR is the dominant driver**: the cost per click may be reasonable but the traffic isn't converting. Move to Tree 1 (Conversions Low), Step 3 and 4.

- **Both CPC and CVR are problems**: address in order — fix conversion tracking and landing page issues first (higher leverage), then address CPC through QS improvements.

---

**Step 3: Is the bid strategy contributing to inflated CPA?**

Pull: GAQL 1.1 (bid strategy by campaign), GAQL 2.3 (conversion volume by campaign)

- **tCPA campaigns with fewer than ~15–20 conversions/month**: the algorithm lacks sufficient data. It will oscillate, overspend in learning phases, and produce inconsistent CPA. See Sub-tree D.
- **tCPA target set below the account's historical CPA**: this is a common mistake. The target is aspirational rather than achievable, and the algorithm oscillates trying to hit it. Compare tCPA target against actual 90-day CPA from GAQL 6.2.
- **Shared bidding strategy pooling multiple campaigns**: check GAQL 11.2. Shared strategies average signals across campaigns with different economics (branded and non-branded, different practice areas). The shared strategy may be optimizing against a blended target that makes neither campaign's performance meaningful.

---

### Tree 3: Budget Not Spending

**Entry:** Campaigns are ending the day with budget remaining; actual daily spend is consistently below the daily budget limit.

Note: this symptom is counterintuitive. Budget not spending is not a sign that the account is healthy and efficient — it usually means the account can't win auctions at its current quality or bid level.

---

**Step 1: Is the campaign actually eligible to serve?**

Pull: GAQL 1.1. Check `campaign.status` and `campaign.serving_status`.

Expected: `status = ENABLED`, `serving_status = SERVING`.

If serving_status shows anything other than SERVING:

> ⚠️ **BLIND SPOT — Serving status details and policy flags are not fully accessible via API**
> The API returns a serving status code but not the full explanation for why a campaign isn't serving.
> → Please share a screenshot of the campaign status column in the Google Ads UI, and check the Policy Manager for any active disapprovals or account-level issues.

---

**Step 2: What does impression share data say?**

Pull: GAQL 5.1 (impression share breakdown), GAQL 11.1 (budget utilization)

The key insight: if the budget isn't being spent, `search_budget_lost_impression_share` should be near zero — there's no budget constraint if money isn't being used. Focus on total impression share and `search_rank_lost_impression_share`.

- **Total IS is low AND rank lost IS is high**: the account is losing auctions on quality and bid grounds. It doesn't need more budget — it needs better QS or higher bids. Move to Sub-tree B (Quality Score Diagnosis).
- **Total IS is low AND both rank and budget IS are low**: unusual. Suggests the account isn't entering the auction much at all. Check keyword volume (next step).

---

**Step 3: Are keywords getting any impressions?**

Pull: GAQL 3.4 (30-day keyword performance)

Look at how many keywords have `impressions > 0`.

- **Most keywords have zero impressions**: keywords may have extremely low search volume, or match types are so restrictive that no queries are triggering them. Exact match on hyper-specific long-tail terms in small geographic markets can produce genuine zero-traffic situations.

> ⚠️ **BLIND SPOT — Keyword search volume estimates and first-page bid estimates are not in the API**
> → Please share a screenshot of the Keywords tab in the UI with the Status column visible. Google shows "Low search volume" status and bid estimates directly in this view. This will confirm whether the issue is volume-based or bid-based.

- **Keywords have some impressions but far fewer than budget would allow**: bids are below the competitive threshold for these keywords. This is a bid/QS problem, not a budget problem. Increasing the budget does nothing. Move to Sub-tree B (Quality Score Diagnosis) to determine whether QS improvements will help before raising bids.

---

**Step 4: Is the issue specific to time of day or geography?**

Pull: GAQL 10.3 (device performance), GAQL 10.4 (daypart performance)

In some accounts, ad scheduling restrictions are too aggressive — campaigns are only enabled for a narrow window and can't spend their full budget in that time. Check whether ad schedules are set and whether they are appropriate.

> ⚠️ **BLIND SPOT — Ad schedule settings are not easily surfaced via the GAQL API in a readable format**
> → Please share a screenshot of the Ad Schedule settings for the affected campaigns.

---

### Tree 4: Performance Dropped — Something Changed

**Entry:** The brief is "something is wrong" — performance was acceptable and now isn't. The most common brief. The most variable tree.

---

**Step 1: Read change history first**

Pull: GAQL 8.1 (recent changes), GAQL 8.2 (auto-applied changes)

Do not skip this step. The change history often answers the question before any other diagnostic is needed.

- **Auto-applied changes present**: evaluate each one. Auto-applied broad match expansion, audience targeting additions, budget changes, and ad suggestions from Google are all candidates. Check whether the timing correlates with the performance drop.
- **Bid strategy or budget changes within the last 14 days**: strong learning phase disruption hypothesis. See Sub-tree D (Smart Bidding Instability) before anything else.
- **No significant changes**: external factors are likely. Continue to Step 2.

*[Toby version]: Check `account-notes/[account].md` for seasonal patterns or prior incidents that might explain the current drop.*

---

**Step 2: Which metric dropped first, and when?**

Pull: GAQL 6.3 (weekly segmented performance) for the affected campaigns

Run this for both 90-day (to establish the baseline trend) and focus on the period of decline. Identify which metric moved first — this is the diagnostic entry point.

- **Impressions dropped while CTR held steady**: reach problem. The account stopped entering as many auctions. IS data (GAQL 5.1) will tell you whether this is budget or rank. See Sub-tree A.
- **CTR dropped while impressions held**: ad quality or competitive landscape change. See Sub-tree C (CTR Decline).
- **Conversion rate dropped while traffic held**: landing page, offer, or audience quality change. Continue to Step 3.
- **CPC spiked while traffic and CVR held**: competitive pressure or bid strategy instability. Continue to Step 4.
- **Multiple metrics degraded simultaneously**: usually indicates a learning phase disruption from a structural change. See Sub-tree D.

---

**Step 3: Diagnosing conversion rate drop**

When: CVR is down from prior period with stable or normal click volume.

Cross-reference with change history timing (PF-3). Key question: did any change in the account coincide with the drop?

- **A bid strategy change occurred**: the learning phase may have disrupted conversion signals. See Sub-tree D.
- **New keywords were added with broad or phrase match**: check GAQL 4.1 (search terms). Are new irrelevant queries now generating clicks that don't convert?
- **No account changes**: external cause. The two most common are landing page changes and seasonal audience shifts.

> ⚠️ **BLIND SPOT — Landing page changes are not visible via API**
> → Has the website or landing page changed recently? If uncertain, please share a screenshot of the current landing page for the affected campaigns.

> ⚠️ **BLIND SPOT — Seasonal patterns in legal search behavior are not visible within the account data alone**
> → Compare this period to the same period in the prior year if data is available. Family law search volume, for example, typically rises after the holidays and dips in summer — patterns that look like performance drops are sometimes normal seasonality.

---

**Step 4: Diagnosing CPC spike**

When: average CPC has risen significantly vs. prior period without a corresponding bid change.

Pull: GAQL 5.1 (IS breakdown). Is `search_rank_lost_impression_share` increasing alongside the CPC rise?

- **Rank loss IS is increasing with CPC**: competition is intensifying. Other advertisers are bidding more, which raises the auction floor. This is market-driven — the solution is not automatically to raise bids, which compounds cost. Evaluate whether the account's current CPA is still acceptable at the new CPC level before responding.

> ⚠️ **BLIND SPOT — Competitor bid changes are not visible via API**
> → Please share a screenshot of Auction Insights for the affected campaigns. Look specifically for new entrants or a significant increase in impression share for existing competitors.

- **Rank loss IS is stable but CPC is rising**: bid strategy may be bidding more aggressively without a clear reason. Check whether target CPA was recently lowered (making the algorithm bid higher to hit the target) or whether a learning phase caused overspending. See Sub-tree D.

---

### Tree 5: Inherited Account / First Review

**Entry:** New account, no prior analysis context. Goal is to understand the account's state comprehensively before identifying what to do.

This is the structural audit entry point. Don't look for one thing — look for everything and flag it.

---

**Step 1: Run the full pre-flight**

PF-1, PF-2, and PF-3 are all mandatory here, and more thorough than in a targeted analysis. Take notes. Everything that deviates from the good-account checklist (knowledge base, final section) gets flagged.

---

**Step 2: Map the account structure**

Pull: GAQL 1.1 (all campaigns), GAQL 1.2 (ad groups)

Build a mental map: how many campaigns, how are they organized, what are they trying to do? Evaluate against the structural principles from the knowledge base:

- Is there evidence of geographic segmentation? Practice area segmentation? Or is everything in one or two catchall campaigns?
- Is brand isolated? Are there naming conventions that suggest deliberate structure, or does it look like the account grew organically without a plan?
- Are there campaigns that appear to duplicate coverage (same practice area, same geography, no clear strategic distinction)?

---

**Step 3: Establish the performance baseline**

Pull: GAQL 6.2 (90-day campaign performance)

This is your baseline. You need to understand what "normal" looks like for this account before you can identify what's wrong. Note: in an inherited account with a history of mismanagement, the baseline may itself be a problem — you're not trying to restore performance to a broken prior state.

---

**Step 4: Keyword health check**

Pull: GAQL 3.1 (keywords with QS), GAQL 3.2 (match type distribution), GAQL 3.3 (90-day keyword performance)

Flag: broad match keywords, keywords with QS < 5 that are spending significantly, and keywords with 90-day cost and zero conversions (long-term bleed). Don't make keyword decisions yet — flag for further evaluation.

---

**Step 5: Negative keyword infrastructure**

Pull: GAQL 9.1 (shared negative lists), GAQL 9.3 (campaign-level negatives), GAQL 9.4 (ad group negatives)

No shared negative list at all = immediate flag. Compare contents of any existing lists against the negative keyword library. Identify obvious gaps.

---

**Step 6: Ad copy and creative state**

Pull: GAQL 7.1 (RSA performance), GAQL 7.2 (ad freshness)

Cross-reference ad creation/modification dates from change history (GAQL 8.1). How old is the creative? When were ads last meaningfully updated?

> ⚠️ **BLIND SPOT — Ad rendering in the SERP is not visible via API**
> The API returns asset lists (headlines, descriptions) but not which combinations are actually serving or how the ad appears to users.
> → Please share a screenshot of the Ad Preview tool (in the Google Ads UI) for the most important ad groups, or run a manual search for core keywords to see how ads appear in practice.

---

**Step 7: Synthesize findings into a prioritized flag list**

At this point you have a list of flags from every step. Prioritize by: estimated spend impact × confidence that it's a real problem. Structural issues that corrupt budget allocation every day rank ahead of cosmetic issues.

The output of a first-review session is a prioritized findings list, not a to-do list. Some findings require further investigation before becoming actionable. Note which ones do.

*[Toby version]: Write a session log for this session even if no actions were taken. First-review sessions often contain the most valuable `Session Observations` — the things that are surprising about how the account was run.*

---

### Tree 7: Conversion Tracking Failure / Sudden Drop

**Entry:** Conversions dropped suddenly — especially to near-zero or zero — within a defined recent window, without an obvious account change. The brief is typically "tracking looks broken" or "conversions dropped 10 days ago."

This is not the same as "conversions are generally low" (Tree 1) — that is a performance problem. This is a measurement problem. Until it is confirmed or ruled out, no other analysis is meaningful.

---

**Step 1: Read change history for the relevant window**

Pull: GAQL 8.1 (60-day changes), GAQL 8.2 (auto-applied changes)

Establish exactly when the drop started. Cross-reference that date with any account changes.

- **A bid strategy or budget change occurred around the drop date**: don't assume it's a tracking failure — a learning phase disruption can cause a real conversion drop, not just a measurement problem. See Sub-tree D. But also continue this tree, as tracking failure and learning phase disruption can co-occur.
- **No account changes around the drop date**: external cause. Continue.
- **Drop is abrupt (one day to next) rather than gradual**: stronger signal of a tracking change — tag break, integration disconnect, or website change.

---

**Step 2: Break down conversion volume by individual action**

Pull: GAQL 2.2 (recent conversion volume), segmented so each action's volume is visible individually. Compare the 30 days before the drop against the 30 days after.

**All primary actions dropped simultaneously:**
Suggests a shared root cause — an account-level change, a website change affecting all tags, or a change to how Google is attributing conversions. Continue to Step 3.

**One action dropped while others held:**
The broken action is isolated. Skip to Step 4 for that action type directly.

**All actions appear to be working but reported volume is lower:**
Consider whether conversion action settings changed (counting method, attribution window). Also consider Smart Bidding relearning: if tracking was recently fixed or changed, the algorithm may have had a disrupted signal before the fix — the reported "drop" is the period before the fix, not a new failure.

---

**Step 3: Check for never-fired primary actions**

Look at all-time conversion history for each primary action. A primary action with zero all-time conversions has never worked — it is not a new failure, it never functioned. This is distinct from an action that was working and then stopped.

Never-fired primaries are a standing configuration error, not a recent event. Note them separately from the acute drop investigation.

---

**Step 4: Diagnose by action type**

**WEBPAGE (codeless tag or gtag):**
These fire when a user reaches a specific page URL (typically a thank-you or confirmation page).
- Has the website been updated recently? Form submission flows change more often than they appear to.
- Is the thank-you page URL still the same as when the tag was configured?
- Does the current checkout/form flow actually reach the tagged URL on submission?

> ⚠️ **BLIND SPOT — Tag firing cannot be confirmed via API**
> → Request a screenshot of the current thank-you page URL and confirm it matches the conversion action's URL rule. If the URL changed, this is the root cause.

**AD_CALL (Google forwarding number):**
Google-native call tracking. These are the most reliable action type and rarely break without an account-level change. Confirm via GAQL:
```
SELECT call_view.call_tracking_display_name, call_view.duration_seconds, call_view.call_status,
       segments.date
FROM call_view
ORDER BY segments.date DESC
LIMIT 30
```
If call_view returns records, Google forwarding is active and confirmed working. If it returns nothing despite call extensions being live, the call extension itself may be missing a Google forwarding number.

**UPLOAD_CLICKS (third-party call tracking platform — CallRail, CTM, etc.):**
These platforms upload call data to Google Ads via the offline conversions API. Two common silent failure modes:
1. **No Lead Rule configured**: the integration is connected but has no criteria for what constitutes a conversion. It silently uploads nothing. Fix: add a qualifying filter (e.g., call duration > 60 seconds) in the platform's Google Ads integration settings.
2. **GCLID not being captured**: if the landing page doesn't capture and store the GCLID parameter from the ad click, the platform cannot attribute the call back to Google Ads. Enhanced Conversions (matching by phone number) is the fallback — check whether it is enabled in both Google Ads and the call tracking platform.

---

**Step 5: After the fix — Smart Bidding relearning**

If the tracking failure affected a campaign running Maximize Conversions or tCPA:

The algorithm has been operating on incomplete or absent conversion signals. After the tracking fix, the algorithm must relearn. This takes 2–4 weeks. During this window:
- Hold bid strategy and targets constant — do not adjust in response to apparently poor performance
- The apparent CPA may worsen temporarily as the algorithm recalibrates
- A "conversion drop" that coincides with a tracking fix being deployed is the algorithm catching up, not a new failure

> *This is the Smart Bidding Post-Tracking-Fix Protocol from SKILL.md. Do not deviate from it.*

---

### Tree 6: Search Term Waste / Negative Keyword Gaps

**Entry:** The brief is specifically about search term quality — mining for negatives, reviewing match type behavior, or investigating wasted spend on irrelevant queries.

---

**Step 0 (Mandatory): Establish coverage ratio before touching search term data**

Pull: GAQL 13.1 (actual campaign spend), then GAQL 13.2 per active campaign (visible STV spend)

Compute coverage ratio. State it before proceeding:
> "Search term data covers $X of $Y actual spend (Z%). The hidden ~[100-Z]% is the Google Ads API ceiling — not fixable through query splitting."

Do not present any findings, waste estimates, or negative keyword recommendations until this ratio is on the table. Scale all dollar estimates by the coverage ratio.

---

**Step 1: Pull search terms**

Pull: GAQL 4.1 (30-day, sorted by cost), GAQL 4.2 (90-day, sorted by impressions)

Use both windows. The 30-day view surfaces what's spending money now. The 90-day view surfaces high-impression irrelevant terms that may not cost much individually but erode impression share and budget over time.

---

**Step 2: Classify each high-cost or high-impression term**

For each term, the classification is: relevant, irrelevant, or ambiguous.

**Relevant**: query that a prospective client of this firm would plausibly use. Keep or add as keyword.
**Irrelevant**: clearly outside the firm's practice area, geography, or client type. Add as negative at the appropriate level.
**Ambiguous**: could be a prospect but intent is unclear. Flag for review — don't add as negative without further consideration.

Cross-reference against the negative keyword library categories:
- Price/affordability signals (Section 1)
- Employment/career signals (Section 2)
- Self-help/DIY intent (Section 3)
- Research/informational intent (Section 4)
- Practice area cross-contamination (Section 5)

---

**Step 3: Check what's already blocked**

Pull: GAQL 9.1 (shared negative lists), GAQL 9.2 (contents of shared lists), GAQL 9.3 (campaign negatives), GAQL 9.4 (ad group negatives)

Don't recommend negatives that are already in place. Identify structural gaps — categories from the negative keyword library that are entirely absent from the account's existing negative structure.

---

**Step 4: Identify the match type generating waste**

If a significant portion of irrelevant search terms are triggered by phrase or exact match keywords, the problem is keyword selection, not match type. If they're triggered by broad match keywords, that confirms the knowledge base position on broad match in legal.

Pull: GAQL 3.2 (match type distribution). Note which match types are associated with the worst-performing search terms.

---

**Step 5: Organize negative keyword recommendations by scope**

Output should be organized as:
- **Account-level additions** (irrelevant to everything the firm does)
- **Campaign-level additions** (irrelevant to this practice area or geography but not universally)
- **Ad group-level additions** (narrowly irrelevant to this specific keyword cluster)

Produce in the upload format from the negative keyword library (phrase match by default, exact match where appropriate).

---

## Sub-Trees

---

### Sub-tree A: Impression Share / Traffic Volume Diagnosis

**Called from:** Tree 1 (Step 1), Tree 3, Tree 4 (Step 2)

**When:** Total impression share is low or impressions have dropped. The question is whether the constraint is budget or rank.

Pull: GAQL 5.1 (IS breakdown by campaign)

**`search_budget_lost_impression_share` is dominant:**
The campaign is budget-constrained. More budget = more traffic. Whether that's the right answer depends on whether the current CPA is acceptable. If CPA is good, increasing budget is justified. If CPA is poor, fixing conversion rate first is higher priority than buying more traffic.

**`search_rank_lost_impression_share` is dominant:**
Rank is the constraint. Rank = Quality Score × bid. Spending more money on bids before fixing QS is expensive and treats the symptom not the cause. Move to Sub-tree B.

**Both are elevated:**
Fix QS first (free improvement), then evaluate whether budget increase is warranted after rank improves. Addressing budget before rank just throws money at an auction you're losing on merit.

**Neither is elevated, but IS is low:**
This means the campaign is entering auctions but isn't getting many of them — unusual. Check whether geographic or audience targeting is more restrictive than intended, or whether the keyword pool is extremely narrow.

---

### Sub-tree B: Quality Score Diagnosis

**Called from:** Tree 2 (Step 2), Tree 3 (Step 3), Sub-tree A

**When:** IS rank loss is elevated, CPC inflation is present without external explanation, or specific keywords show QS < 6 with meaningful spend.

Pull: GAQL 3.1 (keywords with QS components)

**Which component is BELOW_AVERAGE?**

`search_predicted_ctr` is BELOW_AVERAGE:
Expected CTR is calculated by Google based on historical ad performance for this keyword relative to similar advertisers. Low expected CTR means the ads aren't compelling or relevant enough for the query, by Google's assessment. Action: rewrite headlines for this keyword's specific intent. Ensure the keyword or a close variant appears in at least one headline.

`creative_quality_score` (ad relevance) is BELOW_AVERAGE:
The keyword and the ad don't match well. This is usually a structural problem — the keyword is in an ad group where the ad copy is written for a different theme. Action: tighten the ad group so all keywords share the same intent, or create a new ad group with ad copy that matches this keyword's intent directly.

`post_click_quality_score` (landing page experience) is BELOW_AVERAGE:
Google has assessed that the landing page doesn't deliver what the ad promises, loads slowly, or provides a poor mobile experience.

> ⚠️ **BLIND SPOT — Landing page quality cannot be assessed via API**
> → Please share a screenshot of the landing page receiving traffic from this campaign. Assess: Does the page content match what the ad says? Is there a visible CTA? Does the keyword theme appear in the page headline? Is the page functional on mobile?

**Multiple components are BELOW_AVERAGE:**
Address in order: landing page first (highest impact, foundational), then ad relevance (structural fix), then CTR (copy optimization). Don't optimize ad copy on a broken landing page.

**QS is 7+ but CPC is still inflating:**
QS is not the primary cause. This is competitive pressure — other advertisers are bidding more for these keywords. Refer to Tree 2 Step 4 (CPC spike diagnosis).

---

### Sub-tree C: CTR Decline Diagnosis

**Called from:** Tree 4 (Step 2)

**When:** CTR is falling over time on established campaigns with stable impression share.

Pull: GAQL 6.3 (weekly trend), GAQL 7.1 (RSA performance), GAQL 8.1 (change history for ad updates)

**How long has the decline been happening?**

- **Gradual decline over 3–6+ months**: creative staleness is the most common cause. The same ads have been running long enough that the audience has been repeatedly exposed. CTR decays slowly but consistently. Cross-reference: when were these ads last meaningfully updated? (Change history, GAQL 8.1)
  - Action: creative refresh. New headlines that address a different angle, new emotional hooks, test contrast language.
  
- **Abrupt drop over 1–2 weeks**: external change. New competitors, competitor creative improvement, or SERP layout change.

> ⚠️ **BLIND SPOT — Competitor ad copy and SERP layout changes are not visible via API**
> → Please share a screenshot of the Google SERP for 2–3 of the most important keywords in the affected campaigns. Look at how many ads appear, whether competitor ads have improved, and whether any new high-visibility features (Local Service Ads, featured snippets, etc.) are pushing paid ads down the page.

**Is ad rotation masking the decline?**

Check `ad_serving_optimization_status` (GAQL 1.3). If rotation is set to OPTIMIZE, Google may be preferentially serving one ad and suppressing others. The overall CTR appears to decline because the suppressed ads still count against impression totals in aggregate views.
Action: set rotation to `ROTATE_INDEFINITELY` and measure individual ad CTR.

**Is the QS `search_predicted_ctr` component declining?**

Pull: GAQL 3.1. If `search_predicted_ctr` has moved to BELOW_AVERAGE on previously adequate keywords, Google's model is detecting the CTR decline in a way that now affects ad rank. This creates a reinforcing cycle: lower CTR → lower QS → lower rank → even lower CTR. Break it with creative refresh.

---

### Sub-tree D: Smart Bidding Instability

**Called from:** Tree 2 (Step 3), Tree 4 (Steps 2, 3)

**When:** Campaign performance is erratic — large swings in CPC, impressions, and conversions week to week. Or bid strategy is marked as "learning" for an extended period. Or performance degraded immediately after a bid strategy change and hasn't recovered.

Pull: GAQL 2.3 (30-day conversion volume by campaign), GAQL 8.1 (change history), GAQL 6.3 (weekly trend)

---

**Question 1: How long has the current bid strategy been active?**

Read change history for bid strategy changes. Count the days since the last change.

- **Less than 14 days**: this is the learning phase. Do not make additional changes. Do not evaluate performance as indicative of the strategy's capability. Wait.
- **14–30 days with erratic performance**: the learning phase may still be resolving, or there were additional changes within that window that reset it. Check whether any other changes (budget, targeting, keywords) occurred during the supposed learning window. Each significant change resets the clock.
- **30+ days with still-erratic performance**: the strategy may not have enough conversion data to stabilize. See next question.

---

**Question 2: Does the campaign have enough conversion volume to support the current strategy?**

Look at 30-day conversion count per campaign (GAQL 2.3).

- **tCPA with fewer than ~15–20 conversions/month**: insufficient. The algorithm cannot learn effectively. Recommendation: switch to Maximize Conversions (no tCPA target) until volume builds. Maximize Conversions is more forgiving at low volume because it's optimizing direction rather than a specific target.
- **Maximize Conversions with very low conversions (< 5/month)**: even this strategy struggles. Consider whether eCPC (manual with bid adjustments) is more appropriate until the account builds enough history.

---

**Question 3: Is the tCPA target achievable?**

Compare the current tCPA target against the actual CPA from the prior 90-day period (GAQL 6.2).

A tCPA target set significantly below historical CPA forces the algorithm to oscillate — it bids low (to hit the target), loses auctions, generates no conversions, then bids high in the next period to compensate, overspends, resets. This is the most common pattern in accounts where "smart bidding isn't working."

Action: reset the tCPA target to the historical average (or slightly above it), let the account stabilize for 14+ days, then lower the target incrementally — no more than 10–15% at a time with 14-day stabilization windows between adjustments.

---

**Question 4: Is the learning phase disruption pattern chronic?**

If change history shows repeated bid strategy changes at 1–2 week intervals — often with manual bid adjustments in between — the account has likely never completed a learning phase. This is the most common pattern in inherited accounts with a history of anxious management.

Breaking the cycle requires patience: set the bid strategy, set a realistic target, and commit to no significant changes for 21–30 days. This is often difficult to explain to clients — budget spending erratically during learning phases looks bad in the short term even when the long-term outcome will be better.

*[Toby version]: Note in session log under `Session Observations` if the client has been briefed on the learning phase concept and their reaction. This context is useful for managing expectations in future sessions.*

---

## Session Log Reminder

*[Toby version only]*

At the end of every analysis session, generate a session log using the template in `SKILL.md` and save it to `session-logs/YYYY-MM-DD-[account-name].md`.

The most important fields for future skill development are:
- **Diagnostic Path** — what you actually checked and in what order
- **Blind Spots Hit** — what you couldn't see and whether a screenshot resolved it
- **Session Observations** — anything that surprised you, anything the current trees don't account for

After approximately 4–8 sessions, the session logs should be reviewed collectively to identify patterns worth incorporating into these trees. That synthesis happens in a dedicated session, not incrementally.
