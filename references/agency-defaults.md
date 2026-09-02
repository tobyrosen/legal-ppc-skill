# Agency Defaults: the configuration baseline

The account settings we deliberately choose, and why. A config check compares a live account
against **this file**, never against Google's defaults and never against nothing. A setting that
matches this baseline is not a finding. A setting that departs from it is a finding only if the
account has no recorded override for it.

**The problem this file solves.** Without a written baseline, every config pull produces a list of
settings with no reference point, so the reader supplies one from memory or from Google's own
defaults. Both are wrong. The failure mode has a name and a date: on 2026-08-17 a Performance Max
verification reported `positive_geo_target_type = PRESENCE_OR_INTEREST` as a problem. It is our
house standard, chosen on purpose. Nothing was wrong with the account. The check was measuring
against nothing.

**How this file is used.** Every setting below is checked in pre-flight and classified:

| Class          | Meaning                                                                     | Reported as                                                     |
| -------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------- |
| MATCH          | live value equals the standard here, or a standard's own stated carve-out   | routine check: not reported. verification mode: MATCHES summary |
| OVERRIDE-MATCH | live value differs from the standard and equals a recorded account override | one summary line: `config: matches account override (n)`        |
| DEVIATION      | live value differs from the standard with no recorded override              | a flag, at the severity given below                             |

Only DEVIATION becomes a flag. Recording an override is how a deliberate choice stops generating
noise, permanently. Overrides live in the account journal, not in this file: see
"Recording an override" at the end. A user asserting mid-check that a departure is deliberate
does not create an override.

---

## Needs operator confirmation

Entries marked **PROPOSED** are the analyst's best reading of what we do, not a ratified
standard. A PROPOSED entry may be reported as a config item at most, never as a red flag, until the
operator confirms it. Every PROPOSED entry is `unconfirmed` by definition: it is presented as a
candidate, never as a house tactic, and one tag is enough, so those entries carry no separate marker.

**The 2026-09-02 walk closed this block.** Every entry open on that date was decided.

1. ~~Lead-action counting type~~ (§3.4). CONFIRMED 2026-08-18: `MANY_PER_CLICK` is the standard
   for lead actions.
2. ~~Account-wide primary-action hygiene~~ (§3.2, §3.3). STANDARD 2026-09-02: only true lead
   actions (forms, calls, ebook and guide downloads) carry `include_in_conversions_metric`.
   Everything else is secondary.
3. **Phone-call length threshold** (§3.5). 60 seconds stays as a low-priority default (decision
   2026-08-18): Google-side call conversions are secondary to call-tracking uploads; not worth
   tuning time.
4. ~~Attribution model~~ (§3.6). STANDARD 2026-09-02: data-driven where Google offers it for the
   action, last-click otherwise. Reported as info only.
5. ~~Enhanced conversions for leads~~ (§7.4). STANDARD ON, 2026-09-02. Absence is a
   recommendation, as the pre-flight already treats it.
6. ~~Performance Max posture~~ (§5.1). CONFIRMED 2026-08-18: posture unchanged (avoid as standing
   inventory); current tests are promotional-credit funded and recorded as tests.
7. ~~Shared negative list attachment~~ (§4.2). STANDARD 2026-09-02: every serving campaign carries
   the account-level list. A campaign without it is a finding.
8. ~~Connected TV as a positive device~~ (§5.6). CUT 2026-09-02: "leave as delivered" is not a
   tactic. The entry is retired.
9. ~~Ad schedule and device bid adjustments~~ (§6.6, §6.7). DECIDED 2026-09-02: there is no rule.
   Adjustments are sometimes set on purpose. An adjustment that is present is info to note with its
   reason, never a finding.
10. ~~Dynamic Search Ads posture~~ (§6.3). CUT 2026-09-02: "not used" is inference from absence,
    not a tactic. The entry is retired.
11. ~~Ad asset minimums~~ (§6.5). STANDARD 2026-09-02, without counts: every serving Search
    campaign carries sitelinks, callouts, structured snippets and a call asset. The proposed
    numbers are gone.
12. ~~RSA count per ad group~~ (§6.4). STANDARD 2026-09-02: at least two responsive search ads per
    ad group, ideally three, potentially more. Fewer than two is a finding.
13. ~~Shared negative list naming~~ (§4.1). MOVED to internal 2026-09-02: a naming convention is
    housekeeping, not a tactic that improves a campaign.
14. ~~Linked properties~~ (§7.6). STANDARD 2026-09-02: GA4, Business Profile and Search Console all
    linked. A missing link is info.
15. ~~Campaign tracking template and final URL suffix~~ (§1.9). STANDARD 2026-09-02: empty at
    campaign level unless a recorded override. Populated without a record is a config finding.

---

## How to read an entry

```text
**`field.path`**, standard `VALUE`, severity if it deviates
Rationale, one or two lines.
Override: the case where a different value is legitimate.
```

**Severity**

- **red flag**: corrupts the data or spends money wrongly today. Leads the walk card.
- **config item**: real, decide it at the next check. Reported below the red-flag block.
- **info**: recorded, surfaced only on request or during a full audit.

**Status**: entries are STANDARD unless labeled PROPOSED. A PROPOSED entry may be reported as a
config item at most, never as a red flag, until the operator confirms it.

**Readability**: every entry names the GAQL field where the setting is readable. Where a setting
is not exposed by the API, the entry says so and names the indirect signal or the blind spot.
The queries that read these fields are in `references/gaql-query-library.md` §14.

---

## 1. Campaign settings

### 1.1 Google Search network

**`campaign.network_settings.target_google_search`**, standard `true`, red flag if `false`
Search is the channel. A Search campaign with Google Search off is not serving where we think.
Override: none.

### 1.2 Search Partners

**`campaign.network_settings.target_partner_search_network`**, standard `false`, red flag if `true`
Partner traffic converts worse at the same cost in legal, and it blends into the campaign's CPA, so
the damage is invisible unless the report is segmented by network. Every CPA figure from a
partner-enabled campaign is a blended average across two different traffic qualities.
Override: a deliberate partner test with a recorded decision and a network-segmented read. Note
that removing partners also removes its conversions from the smart-bidding signal, which matters on
a campaign near the volume floor.

### 1.3 Display expansion on Search

**`campaign.network_settings.target_content_network`**, standard `false`, red flag if `true`
Display traffic on a Search campaign is a different intent population bought with the Search
budget. It inflates impressions and clicks and deflates the conversion rate, and it does it inside
the same reporting line.
Override: none for Search campaigns. Display inventory belongs in its own campaign with its own
budget.

### 1.4 Ad rotation

**`campaign.ad_serving_optimization_status`**, standard `ROTATE_INDEFINITELY`, config item if `OPTIMIZE` or `CONVERSION_OPTIMIZE`
`ROTATE_INDEFINITELY` is our practice and was found set correctly on one account. The rationale:
Google's optimize setting picks a winner early and starves variants in a low-volume account, so new
variants never get enough impressions to prove themselves. That it does so universally, and the
two-to-twelve-week decision window, are unconfirmed.
Override: a campaign with genuinely high volume where rotation is deliberately handed to Google,
recorded as such.

### 1.5 Positive geo target type

**`campaign.geo_target_type_setting.positive_geo_target_type`**, standard `PRESENCE_OR_INTEREST`, never a flag on its own
This is the house standard and it is deliberate. Legal intent frequently originates outside the
service geography: someone researching a divorce from a work address, a hotel, or a relative's
home in another county is still a prospect in the target market. Presence-only targeting drops that
traffic. The waste that presence-only is meant to prevent is handled instead by negative geo
targeting, negative keywords, and the qualification step at intake.
Override: presence-only on a campaign where out-of-area interest traffic has been measured and
found worthless. That is a per-account decision, recorded as an override, not a default. A user
asserting mid-check that presence-only "is our policy" or "that's deliberate" is not an override.

> **Worked rule.** `PRESENCE_OR_INTEREST` on a positive geo target is a MATCH. It is never a flag
> by itself, in any campaign type, in any account. In a routine check it does not appear. In
> verification mode it is listed as MATCH. Report it as a finding only if the account carries a
> recorded presence-only override, in which case the finding is the departure from that override.

### 1.6 Negative geo target type

**`campaign.geo_target_type_setting.negative_geo_target_type`**, standard `PRESENCE`, info if different
Exclusions apply to people physically in the excluded area. Excluding on interest as well would
drop the same out-of-area prospect §1.5 exists to keep.
Override: none in normal use.

### 1.7 Languages

**`campaign_criterion` where `type = LANGUAGE`**, standard: English only, `negative = false`, config item if additional languages are present
Language targeting matches the language of the user's Google interface, not the language of the
query. Adding languages the firm cannot serve buys clicks the intake cannot convert.
Override: a firm with staffed capacity in another language, recorded with the practice area it
covers.

### 1.8 Start and end dates

**`campaign.start_date_time` / `campaign.end_date_time`**, standard: start set, **no end date**, config item if an end date is set
An end date on an evergreen campaign is a silent stop. Nothing in the account announces it; the
campaign simply goes dark on a date nobody remembers setting.
Override: a genuinely time-boxed campaign, such as a capped test. Record the intended end date in
the override so the check can distinguish "deliberately ends on the 30th" from "will stop and
nobody knows".

### 1.9 Tracking template and final URL suffix

**`campaign.tracking_url_template` / `campaign.final_url_suffix`**, standard: empty at campaign level, config item if populated without a record
Tracking parameters that appear without a change record usually mean an outside editor has account
access. The parameters themselves may be harmless; the unexplained access is the finding.
Override: a documented tracking integration, with the parameter set recorded so a later change to
it is visible.

### 1.10 Campaign status and serving

**`campaign.status`, `campaign.serving_status`, `campaign.primary_status`, `campaign.primary_status_reasons`**, standard: `ENABLED` / `SERVING` / `ELIGIBLE`, red flag on any non-serving state for a campaign carrying budget
`primary_status` is where the API says why a campaign is not delivering. `LEARNING` with reason
`BIDDING_STRATEGY_LEARNING` is expected for roughly the first two weeks after a bid strategy change
and is not a flag; every other non-eligible reason is.
Override: a paused campaign held deliberately, recorded with the condition for reactivation.

### 1.11 AI Max for Search

**`campaign.ai_max_setting.enable_ai_max`**, standard `false`, config item if `true`
AI Max hands query matching and asset generation to Google on a Search campaign, which reverses the
match-type control §6.1 exists to hold. It is the same trade as broad match plus automated creative,
turned on at the campaign level.
Override: an explicit AI Max test on one campaign with a recorded decision and a review date.

### 1.12 EU political advertising

**`campaign.contains_eu_political_advertising` / `customer.contains_eu_political_advertising`**, standard: not declared, info
Not applicable to US law-firm accounts. The field is checked so that a declaration appearing on its
own is visible, since it changes what Google will serve.
Override: none expected.

---

## 2. Budget and bidding

### 2.1 Budget period and delivery

**`campaign_budget.period`**, standard `DAILY`; **`campaign_budget.delivery_method`**, standard `STANDARD`, config item if `ACCELERATED`
Accelerated delivery spends the day's budget as fast as the auctions allow, which front-loads the
morning and leaves the evening dark. Legal intent runs late: the hours when someone finally
searches for a divorce lawyer are not the hours accelerated delivery buys.
Override: none in normal use.

### 2.2 Shared budgets

**`campaign_budget.explicitly_shared`**, standard `false`, config item if `true`
A shared budget removes per-campaign spend control, which is the control the whole campaign
structure exists to give us. When one campaign takes the shared pool, another goes quiet, and the
budget-lost impression share reads as a campaign problem rather than an allocation problem.
Override: a deliberately pooled set of campaigns treated as one line item, recorded as such.

### 2.3 Bidding strategy by maturity

**`campaign.bidding_strategy_type`**, standard depends on conversion volume, config item if the strategy does not match the tier

The tiers below are `unconfirmed`: they turn on the reliability floor, which is volume-dependent
judgment for the account rather than a fixed number. The one measured rung is the Maximize Clicks
plus CPC cap case at the bottom.

- Below the account's reliability floor: `MAXIMIZE_CONVERSIONS` with **no** target CPA. The
  algorithm needs conversion volume before a target means anything; a target set on thin data
  restricts the auction entries that would produce the data.
- At or above that floor with an economics-derived target available: `TARGET_CPA`.
- Already on `MAXIMIZE_CONVERSIONS`, below the floor, **and** carrying a high average CPC against
  the campaign's own trailing median: `MAXIMIZE_CLICKS` with a CPC cap, to buy volume and rebuild
  signal while capping runaway auctions. Watch conversion rate, since Maximize Clicks optimizes for
  clicks.
- `TARGET_ROAS` only where case values differ enough between campaigns to justify it. (unconfirmed)
- `MANUAL_CPC` only in a genuine crisis. (unconfirmed)

Override: any of the above held deliberately through a transition, recorded with the review date.

### 2.4 Target CPA presence

**`campaign.maximize_conversions.target_cpa_micros` / `campaign.target_cpa.target_cpa_micros`**, standard: absent below the volume floor, config item if a target is set on a sub-floor campaign
A target on a campaign that cannot clear its own reliability floor is a constraint applied to
noise.
Override: a target carried through a temporary volume dip, recorded with the expected recovery.

### 2.5 Target CPA direction

Not a field, a rule, enforced whenever a target changes. Lower a target only when actual cost per
conversion is already comfortably below it. Lowering a target while CPA sits at or above it tells
the algorithm to enter fewer auctions, which produces fewer conversions rather than cheaper ones.
Where CPA is well above target with low impression share, the constraint is Ad Rank, not budget.
Full statement: SKILL.md, "tCPA Direction Rule".

### 2.6 Where targets come from

A bidding target is an external input derived from the firm's economics: case value, lead-to-signed
rate, acceptable cost per signed case. It is never back-solved from the account's own CPA. The
account's CPA says how performance compares to the target; it is not the source of the target.
Severity if a target appears with no economics behind it: config item, and the target is treated as
unset for diagnostic purposes.

### 2.7 Bid strategy churn

**`change_event` on bidding fields**, standard: no bid strategy change inside a 14-day learning
window, config item if the window was interrupted
Repeated strategy changes inside the learning period restart the clock. That this is the most
common reason a smart-bidding account never stabilises is unconfirmed: churn has not been observed
on the accounts in scope (PB-10), and the 14-day window is itself unconfirmed.
Override: none. A change forced by a tracking fix is recorded as a decision with its own review
date, following the post-tracking-fix protocol in SKILL.md.

---

## 3. Conversion goal set

### 3.1 Goal configuration level

**`conversion_goal_campaign_config.goal_config_level`**

MATCH:

- Search campaign: live value is `CUSTOMER`.
- Performance Max test: live value is `CAMPAIGN`.

DEVIATION, config item:

- A PMax campaign, including a PMax test, at `CUSTOMER`: it is inheriting the account default. That is not a MATCH. Pinning to campaign-level goals is the standard for PMax; `CUSTOMER` on PMax is the finding.
- A Search campaign at `CAMPAIGN` with no recorded override.

Search campaigns share the account's goal set. A PMax test does not: it optimizes toward whatever
is biddable, and the account default is usually wider than the lead set. Pinning the test to
campaign-level goals is what keeps it aimed at leads.
Override: a Search campaign with a deliberate campaign-level goal set, recorded with the reason.

### 3.2 Which goal categories are biddable

**`campaign_conversion_goal.biddable` / `customer_conversion_goal.biddable`**, standard: lead
categories only, config item if a non-lead category is biddable on a live campaign

**Ebook and guide downloads are a LEAD category here, by standing operator ruling.** They are
biddable, they are primary, and they are never a demotion candidate. The ads sell the ebooks and the
nurture funnel behind them produces clients. Any recommendation to make a download category
non-biddable is wrong on its face, whatever its volume or its Google-side category label. This
applies equally to the CRM-native and the tag-manager or analytics versions of the same event.

Biddable: the website default lead category, contact, phone call lead from call-from-ads, lead form
submission, and ebook or guide download. Not biddable by default: generic page view, directions,
store or hosted engagement, and video engagement or follow-on views. (unconfirmed as a category
list; only the ebook ruling is operator-confirmed.)

A generic page-view category left biddable trains the bid algorithm on browsing rather than on
intake. That is a real risk, and it is a different thing from an ebook download, which the firm
treats as a lead.

Override: a category deliberately included for a specific test, recorded with the review date.

**Note:** the API omits `biddable` entirely when it is not true, rather than returning `false`.
Absence is the negative case; do not read an omitted field as missing data.

### 3.3 Primary versus secondary actions

**`conversion_action.include_in_conversions_metric`**, standard: `true` on true lead actions only
(forms, calls, ebook and guide downloads), config item where a generic engagement action is primary.
Operator ruling, 2026-09-02.

**Ebook and guide downloads are PRIMARY, by standing operator ruling.** They count in the headline
conversions number and they train the bid model, deliberately. They are never demoted to secondary,
never excluded, and never discounted. The operator ranks them above phone calls.

The residual risk this entry covers is a generic engagement or page-view action left primary: a
scroll depth, a navigation event, a directions click. Those inflate the count without representing
intake, and they are secondary.

Demotion of a duplicate lead action requires per-lead matching showing that two primaries fire on
the same lead. Matching totals or similar decimal tails are at most a prompt to go and look, never
evidence and never grounds to demote (PB-23).

Override: an account whose intake genuinely treats a specific engagement event as a lead, recorded
with the reasoning, or a legacy set scheduled for cleanup with a date.

### 3.4 Counting type (STANDARD, confirmed 2026-08-18)

**`conversion_action.counting_type`**, house standard `MANY_PER_CLICK` on lead actions; situational,
not universally correct for legal PPC: an agency may choose `ONE_PER_CLICK` for actions where repeat
events are noise, recorded as an override. Info if `ONE_PER_CLICK` with no recorded override.
Every touch counts. Under data-driven attribution with automated bidding, each conversion event
is signal the optimizer uses; collapsing repeat calls or submissions to one per click removes signal.
Reporting de-duplicates leads downstream (call-tracking uploads and CRM), not at the counting layer.
Override: an action where repeat events are known noise (a form that double-submits), recorded.

### 3.5 Call conversions (PROPOSED threshold, low priority)

**`conversion_action.phone_call_duration_seconds`**, proposed standard 60 seconds, info if lower or unset on a call action
A call that lasts under a minute is rarely an intake conversation. Low priority by decision
(2026-08-18): Google-side call conversions are secondary evidence; call-tracking uploads carry the
qualified-call signal and Google obscures most call data. Report the value, do not spend time
tuning it.
Override: a firm whose intake genuinely qualifies faster, recorded with the number.

Call-from-ads and click-to-call actions are expected to exist and to be primary; website lead form
and website contact actions likewise. A live account with no call conversion action is a red flag,
since phone is the dominant intake path in legal.

### 3.6 Attribution

**`conversion_action.attribution_model_settings.attribution_model`**, standard: data-driven where Google offers it for the action, last-click otherwise, info only
Position-based attribution is unusual for legal and worth a question. The model matters less than
its consistency: a mixed set of models across actions makes campaign comparison meaningless.
Override: any model with a stated reason.

### 3.7 Analytics-imported actions

**`conversion_action.origin` / `.type` = `GOOGLE_ANALYTICS_4_CUSTOM`**, standard: an imported
analytics action is secondary only where a native action is the canonical lead record, config item
where imported events are primary in bulk with a native canonical action already in place
Origin is not a defect signal. An imported event that is the firm's lead record is primary,
including the GA4 or tag-manager version of the ebook event. What this entry catches is a wholesale
imported set sitting primary alongside the native action that already records the lead.
Override: an account where the analytics event is the canonical lead record, recorded as such.

### 3.8 Duplicate lead actions

**`conversion_action`, compared by name, type, and category**, standard: one primary action per real
intake event, red flag on duplicates that are both primary
Two actions measuring the same form double the conversion count and halve the reported CPL. This is
the single most common way an account appears to be performing well.
Override: a deliberate parallel measurement during a tracker migration, recorded with an end date.

### 3.9 Conversion silence

**`metrics.conversion_last_conversion_date` per action**, standard: every primary action has fired
inside a plausible window, red flag on a primary action that has stopped
A primary action that has gone quiet is either a broken tag or a dead intake path, and both
invalidate the CPL the account is being judged on.
Override: an action known to be dormant, recorded so it stops being re-flagged. Note that a quiet
action is not automatically a break: where a call tracker forwards only qualified leads, silence on
low volume is the designed behavior, and that belongs in the account's rules.

---

## 4. Negative keyword lists

### 4.1 Account-level shared list

**`shared_set` where `type = NEGATIVE_KEYWORDS`**, standard: an account-level shared negative list
where the account's own search-term data supports one, config item if none exists

The absence of a shared list is a config item at most, never a red flag. Treating it as a red flag
conflicts with two standing positions: the operator's not-waste list, which several of the usual
blanket categories would catch, and the outcome in which proposed blanket negatives were rejected.
Category-level waste that recurs across every campaign does belong at account scope, but the
categories are derived from the account's own search-term data, never from a template, and every
candidate is checked against the not-waste list before it ships.
Override: none.

### 4.2 Attachment

**`campaign_shared_set`**, standard: every serving campaign references the account-level
list, config item where a serving campaign references none
A list that exists but is attached to nothing blocks nothing. This is worth checking on every newly
built campaign, which is where the gap normally appears.
Override: a campaign deliberately excluded from the shared list, recorded with the reason.

### 4.3 Auto-generated lists

**`shared_set.name` suggesting automatic generation**, standard: present is acceptable, but it does
not substitute for the maintained list, info
Google-generated negative sets are not curated against the firm's practice areas.
Override: none.

### 4.4 Scope hierarchy

Exclusions sit at the narrowest scope that is correct: irrelevant to the whole account goes to the
shared list, irrelevant to one campaign goes to campaign level, irrelevant to one ad group goes to
ad group level. A campaign-level negative that should be account-level is an info item, not a flag,
but a pattern of them means the shared list is not being maintained.

### 4.5 Negatives that block converting traffic

**`campaign_criterion` / `ad_group_criterion` where `negative = true`**, standard: no negative
blocks a term with conversion history, red flag if one does
Legal has a long consideration window, so informational queries convert at a lower rate but a real
one. A negative added on a waste review can silently remove a converting term.
Override: a term deliberately excluded despite conversions, recorded with the reason.

---

## 5. Performance Max

### 5.1 Presence (STANDARD, confirmed 2026-08-18)

**`campaign.advertising_channel_type = PERFORMANCE_MAX`**, standard: not part of the standing
build; runs only as a recorded, budget-capped test (typically promotional-credit funded), config
item if a PMax campaign runs without a recorded decision. Posture is unchanged from the knowledge
base (avoid); a test that teaches something may change the posture later, a test by itself does not.
PMax controls placements, creative, and bidding at once, and without heavy conversion history it
finds the cheapest conversions available, which in a law firm account means branded queries and
remarketing rather than new clients. Run as a test with a cap and a review date, it answers a
question; run as standing inventory, it quietly absorbs budget from campaigns that can be steered.
Override: exactly what this entry expects, a recorded test decision naming the cap and the review
date.

### 5.2 Asset automation

**`campaign.asset_automation_settings`**, standard: every automation type `OPTED_OUT`, config item on any `OPTED_IN`
Automatically generated text, image extraction, image enhancement, and enhanced video put creative
we did not write in front of legal prospects, under bar-association advertising rules that make
"Google generated it" an unhelpful defense. The relevant types include text asset automation, image
extraction, image enhancement, enhanced YouTube video, and final URL expansion.
Override: an explicit creative-automation test, recorded, on an account whose firm has approved it.

### 5.3 Final URL expansion

**`campaign.asset_automation_settings`, final URL expansion type**, standard `OPTED_OUT`, config item if opted in
URL expansion lets Google send traffic to any page on the site it thinks converts, which in a law
firm site means blog posts and practice areas the campaign is not about. The campaign's own landing
page is the one that was chosen.
Override: an expansion test with recorded exclusions.

> **v23 note:** `campaign.url_expansion_opt_out` no longer exists. Read expansion from
> `campaign.asset_automation_settings`.

### 5.4 Brand guidelines

**`campaign.brand_guidelines_enabled`**, standard `true`, with main color, accent color, and font
family set, config item if disabled or unset
With brand guidelines off, generated layouts pick their own colors and type. A law firm's ads are
part of its brand and, in several states, part of its regulated advertising.
Override: none expected.

### 5.5 Text guidelines

**`campaign.text_guidelines.term_exclusions` / `.messaging_restrictions`**, standard: both populated, config item if empty
Term exclusions block the words that read as discount retail in a legal ad, and the words that
imply free service when the firm does not offer it. Messaging restrictions carry the bar-rule
constraints: no competitor names, no superlatives, no services the ad does not name. The specific
list is per-account, since state bar rules differ; the requirement that it is not empty is not.
Override: none. An empty guideline set on a live PMax campaign is always worth a line.

### 5.6 Devices

Retired 2026-09. "Leave as delivered" is not a tactic, so there is no baseline entry here. Section
numbers are not reused.

### 5.7 Campaign-level brand exclusions

**`campaign_criterion` where `type = KEYWORD` and `negative = true`, plus brand exclusion asset
sets**

MATCH on a non-brand PMax test: at least one campaign-level brand-term negative, or a brand-exclusion
asset set, is present.

DEVIATION, config item: a non-brand PMax test with no campaign-level KEYWORD negatives and no
brand-exclusion asset set. Absence is the finding. Do not file this as MATCH because other PMax
settings matched, and do not treat "no keyword negatives listed" as N/A on PMax.

Without a brand exclusion, a PMax test spends its budget on the firm's own name and reports the
resulting conversions as its own. The test then reads as a success and proves nothing about new
client acquisition, which is the only question it was built to answer.
Override: a PMax campaign deliberately including brand, recorded, with the brand share reported
separately in every read.

### 5.8 Asset group coverage

**`asset_group`, `asset_group_asset`**, standard: every field type populated to at least Google's
minimum, and `asset_group.ad_strength` not `POOR` at the point the campaign is judged, config item
`POOR` ad strength on a brand new asset group under review is expected and not a finding. `POOR`
persisting after review completes is a finding, since it limits the combinations the campaign can
serve.
Override: none.

### 5.9 Asset group signals

**`asset_group_signal`**, standard: at least one audience or search theme signal, info if none
Signals are a starting hint, not targeting. Their absence is worth a line on a new test because it
lengthens the learning period.
Override: a deliberately unsignalled test.

---

## 6. Search campaigns

### 6.1 Match types

**`ad_group_criterion.keyword.match_type`**, standard: `PHRASE` and `EXACT`, config item on any
`BROAD` outside a named test structure
The argument for broad match is that it captures intent beyond the literal keyword. In legal the
cost of the miss is high and adjacent-looking queries routinely carry entirely different intent.
Phrase and exact are the defaults. Broad is not banned: it is tested deliberately in an isolated
structure, with the PB-11 remediation path ready.
Override: broad match isolated in single-keyword ad groups for a recorded test, monitored.

**Remediation note:** a broad keyword that is both wasteful and a major conversion source converts
to phrase match, it does not get paused. Pausing throws away the conversion history the bid model
is running on. Convert, add the specific negatives, set a monitoring window, and only then consider
pausing.

### 6.2 Brand isolation

**Campaign naming, no API field**: standard: brand terms in their own campaign, config item if a
campaign name suggests mixed brand and non-brand
Brand and non-brand have different economics and different conversion paths. Mixed together, brand
flatters the non-brand CPL and hides what is actually happening. There is no API flag for this; the
signal is the naming convention, which is why the convention matters.
Override: none.

**Related:** pausing a brand campaign does not simply save its spend. Competitors bidding on the
firm's name fill the gap, and non-brand CPL usually rises. Reduce brand spend rather than
eliminating it, and check conversion volume reliability before either.

### 6.3 Dynamic Search Ads

Retired 2026-09. "Not used" was inference from absence rather than a tactic, so there is no baseline
entry here. Section numbers are not reused.

### 6.4 Responsive search ads

**`ad_group_ad`, `ad_group_ad.ad_strength`**, standard: at least two responsive search ads per ad
group, ideally three, potentially more; config item where an ad group carries fewer than two
One RSA gives nothing to compare. Operator ruling, 2026-09-02.
Ad strength itself is a Google heuristic, not a performance measure. `POOR` is a config item worth
a line, never a red flag on its own.
Override: a single-ad group during a deliberate creative reset.

### 6.5 Ad assets

**`campaign_asset`, `ad_group_asset`**, standard: sitelinks, callouts, structured snippets, and a
call asset present on every serving Search campaign, config item where a type is missing. No
minimum count is set for any type.
Assets raise the ad's space on the results page and its Ad Rank inputs at no additional cost per click, and the
call asset is the direct path for the intake channel that matters most in legal.
Override: a campaign where an asset type is deliberately withheld, recorded.

**v23 note:** `campaign_asset` has no `policy_summary`. Asset approval at campaign level is read
from `campaign_asset.primary_status` and `.primary_status_reasons` only.

### 6.6 Ad schedule

**`campaign_criterion` where `type = AD_SCHEDULE`**, no standard, info only
There is no rule here. A schedule is sometimes set on purpose. Smart bidding already models time of
day, and a hand-built schedule on top of it can remove hours the algorithm would have bought
profitably, so a schedule that is present gets noted with its reason. It is never a finding.
Operator ruling, 2026-09-02.
Override: not applicable; there is nothing to deviate from.

### 6.7 Device bid adjustments

**`campaign_criterion` where `type = DEVICE`, bid modifier**, no standard, info only
There is no rule here. A modifier is sometimes set on purpose. Note any modifier that is present
with its reason; it is never a finding. Mobile is where most legal calls originate, so a negative
mobile modifier is worth a question wherever it appears. Operator ruling, 2026-09-02.
Override: not applicable; there is nothing to deviate from.

### 6.8 Quality Score components

**`ad_group_criterion.quality_info`**, standard: no keyword sitting at all-`BELOW_AVERAGE` while
carrying spend, config item
All three components below average with near-zero impressions is throttling, not a bid problem.
The lever is landing page and ad relevance.
Override: none.

---

## 7. Account level

### 7.1 Auto-apply recommendations

**Not readable directly.** Detect via `change_event.client_type` in
`('GOOGLE_ADS_AUTOMATED_RULE', 'GOOGLE_ADS_RECOMMENDATIONS')`, standard: OFF, therefore zero
auto-applied changes in the window, red flag on any auto-applied change to keywords, match types,
budgets, bidding, or targeting
Auto-apply lets Google make the changes Google's incentives favor, most often broad match
expansion and budget increases, without review. An auto-applied change is generally a red flag and
every one of them is checked, individually, against the account. A long auto-applied list is a
finding regardless of whether the individual changes look harmless, because it means the account is
not being managed. Operator ruling, 2026-09-02.
Override: a specific recommendation type deliberately left on, recorded by name.

> **Blind spot.** The auto-apply _setting_ is not exposed by the API. Zero auto-applied changes in
> the window is evidence, not proof. Confirm the setting in the UI on a first-review audit.

### 7.2 Conversion tracking status

**`customer.conversion_tracking_setting.conversion_tracking_status`**, standard: conversion
tracking enabled and owned by the expected account, red flag otherwise
Every other number in the account depends on this one.
Override: none.

### 7.3 Call reporting

**`customer.call_reporting_setting.call_reporting_enabled` and `.call_conversion_reporting_enabled`**, standard `true`, red flag if `false`
With call reporting off, calls from ads are not measured at all, and in legal that is usually the
majority of the intake.
Override: an account where a third-party call tracker owns call measurement end to end, recorded,
with the tracker named.

### 7.4 Enhanced conversions for leads

**`customer.conversion_tracking_setting.enhanced_conversions_for_leads_enabled`**, standard
`true`, config item if `false`
Enhanced conversions for leads hashes first-party contact data from form submissions and matches it
back, which recovers attribution that cookie loss otherwise destroys.
Override: a firm that has declined data-terms acceptance, recorded.

### 7.5 Auto-tagging

**`customer.auto_tagging_enabled`**, standard `true`, red flag if `false`
Without auto-tagging, the click identifier never reaches the analytics property or the CRM, and
imported conversions cannot be attributed back to the campaign that produced them.
Override: none.

### 7.6 Linked properties

Standard: GA4, Business Profile and Search Console all linked, with conversion imports arriving
from GA4 where the intake is measured there. A missing link is info.
Not directly readable as a link list in a single GAQL query; the practical signal is the presence of
conversion actions whose type is a GA4 custom event, and location assets whose source is the
Business Profile.
Severity: config item where an expected link is absent. Override: recorded per account.

### 7.7 Account currency and time zone

**`customer.currency_code`, `customer.time_zone`**, standard: whatever the account is set to,
pulled every session and never assumed, red flag if a report was produced without pulling it
Not a setting we choose, a setting we must read. Every cost figure is denominated in the account's
own currency, and every date boundary is in the account's own time zone. Two accounts both reading
"200" in different currencies are not tied, and a week that ends on Sunday in one account does not
end on Sunday in another.
Override: none.

---

## Recording an override

An override is a journal entry, not an edit to this file. This file holds what the agency does; the
journal holds what a given account does differently and why.

**How an override is established.** An override exists only when it is a recorded journal entry
(operator version: a recorded rule carrying the `config-override` tag) or, in the public version, an
entry in the example overrides file. A user asserting mid-check
"that's deliberate" does not create an override. The check reports the DEVIATION and notes
"operator states deliberate; record an override to clear".

The entry is a `rule` carrying the `config-override` tag and a `config_override` object naming the
setting path, the account's value, and the agency default it departs from. The body carries the
reason. The approver and the date come from the entry's own `source` and `ts`. Format and a worked
example: `NOTATION.md` §8 and `journal/templates.md`.

Rendered account notes surface these under **Config overrides**, so the operator reading an account
before a check sees the deliberate deviations in one block rather than rediscovering them as flags.

**Canonical OVERRIDE-MATCH output.** The body carries only the summary line:

```text
config: matches account override (n)
```

Never itemise the matched overrides in the body. The per-setting counterfactual (what the standard
is, and why the override exists) goes only in a trailing `basis` block, and only if the operator
asks.

**An override is not a permanent excuse.** It records that a deviation was decided, by whom, and
why. Where the deviation is a legacy state we intend to clean up rather than a choice we stand
behind, record it as a `decision` with a `review_by` date instead, so it comes back through the due
queue rather than going quiet.

**Public version note:** overrides for real accounts live in the operator's private journal. The
public version of this skill ships the example override in
`account-notes/example-family-law.md` and nothing else.
