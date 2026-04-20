# Account Audit Checklist

Use for: first-contact account reviews and periodic structural audits.
Maps to: Tree 5 (Inherited Account / First Review) in `references/diagnosis-trees.md`.

**How to use:**
Work through each section in order. Mark each item ✓ (pass), ✗ (flag), or — (not applicable). Every ✗ becomes an item in the session's running action list. Do not skip sections because you assume something is fine — the checklist exists to catch assumptions.

---

## Pre-Flight Checks

These run before anything else. Pre-flight findings take priority over every other finding.

### PF-1: Conversion Tracking
*GAQL: 2.1 (all conversion actions), 2.2 (recent conversion volume)*

- [ ] At least one conversion action is enabled and active
- [ ] Primary conversion actions (`include_in_conversions_metric = TRUE`) measure real leads — not page views, sessions, or soft engagements
- [ ] Every enabled primary action has recorded at least one conversion in the last 30 days — flag any that have never fired or have been silent for 30+ days despite meaningful click volume
- [ ] Conversion volume is plausible given click volume (not zero with >100 clicks/month)
- [ ] No duplicate primary actions tracking the same event (check for DDA decimal fingerprint: identical fractional conversion tails across two actions)
- [ ] No deprecated tracking sources present (e.g., PhoneWagon — acquired, unreliable)
- [ ] GA4 and HubSpot (or other platforms) are not double-counting the same form submissions
- [ ] `counting_type = ONE_PER_CLICK` for lead-type conversions (not MANY_PER_CLICK)
- [ ] Attribution model is appropriate (DDA or Last Click acceptable; flag unusual models)
- [ ] If a third-party call tracking platform is in use (CallRail, CTM, etc.): confirm a Lead Rule or equivalent qualifying filter is configured — without it the integration is a silent no-op

**Blind spot:** Tag firing cannot be confirmed via API. If conversions are zero despite meaningful clicks, request GTM or GA4 debug view screenshot.

---

### PF-2: Structural Red Flags
*GAQL: 1.1 (all campaigns), 1.3 (ad rotation)*

- [ ] No Performance Max campaigns (PMax is almost always wrong for law firms)
- [ ] Display/content network disabled on all search campaigns (`target_content_network = FALSE`)
- [ ] Search Partners disabled on all campaigns (`target_partner_search_network = FALSE`) — or documented reason it's enabled
- [ ] Ad rotation set to `ROTATE_INDEFINITELY` on all campaigns (not OPTIMIZE or CONVERSION_OPTIMIZE)
- [ ] Brand campaign is isolated in its own campaign — no brand keywords mixed with non-brand
- [ ] No broad match keywords in active campaigns (except deliberately named test campaigns)
- [ ] No active Performance Max or Display campaigns without explicit brief

---

### PF-3: Change History Read
*GAQL: 8.1 (60-day changes), 8.2 (auto-applied changes 90-day)*

- [ ] No auto-applied changes from Google (`client_type = GOOGLE_ADS_AUTOMATED_RULE` or `GOOGLE_ADS_RECOMMENDATIONS`) in the last 90 days — or each one reviewed and confirmed intentional
- [ ] No learning phase disruption pattern: repeated bid strategy changes at <14-day intervals
- [ ] Account shows signs of active management (changes present within last 3 weeks on active campaigns)
- [ ] No budget, bid strategy, or targeting changes within the last 14 days that would explain current performance issues as learning phase noise

---

## Section 1: Account Structure

*GAQL: 1.1 (campaigns), 1.2 (ad groups)*

- [ ] Geographic segmentation present — campaigns organized by target market/city
- [ ] Practice area segmentation present — separate campaigns per practice area (divorce, custody, etc.)
- [ ] No single catch-all campaign containing all practice areas and geographies
- [ ] Campaigns covering overlapping territory or practice areas have clear strategic distinction
- [ ] Ad group structure aligns with keyword themes — not one large ad group per campaign
- [ ] Budget allocation reflects account priorities (highest-value practice areas receive appropriate share)
- [ ] Paused campaigns reviewed: are they paused for a known reason, or abandoned?
- [ ] Local Services Ads (LSA) campaign status noted if present

**Structural observations:** Note anything surprising about the architecture that doesn't fit the above pattern. Some accounts have deliberate exceptions — document the reason, not just the exception.

---

## Section 2: Keyword Health

*GAQL: 3.1 (keywords + QS), 3.2 (match type distribution), 3.3 (90-day keyword performance)*

- [ ] No broad match keywords in active campaigns
- [ ] Core keywords have Quality Score ≥ 6 (flag keywords with high spend and QS < 5)
- [ ] No QS component consistently BELOW_AVERAGE across multiple keywords (pattern = structural fix needed)
- [ ] No keywords with 90-day spend and zero conversions that exceed the account's target CPA (long-term bleed)
- [ ] No duplicate keywords appearing in multiple ad groups with identical or overlapping match types
- [ ] Keyword themes are tight within each ad group — no "kitchen sink" ad groups

**QS component mapping:**
- `search_predicted_ctr` BELOW_AVERAGE → ad copy problem
- `creative_quality_score` BELOW_AVERAGE → keyword/ad mismatch problem
- `post_click_quality_score` BELOW_AVERAGE → landing page problem

---

## Section 3: Negative Keyword Infrastructure

*GAQL: 9.1 (shared lists), 9.2 (shared list contents), 9.3 (campaign negatives), 9.4 (ad group negatives)*

- [ ] At least one shared negative keyword list exists and is applied to all active campaigns
- [ ] Shared list contains phrase-match categoricals (not only exact-match reactive strings)
- [ ] Section 1 coverage (price/affordability): `"legal aid"`, `"pro bono"` present as phrase match
- [ ] Section 2 coverage (career/jobs): `"attorney jobs"`, `"law school"`, `"bar exam"` etc. present
- [ ] Section 3 coverage (self-help/DIY): evaluate per account — see library Section 4 caveat below
- [ ] Section 5 coverage (practice area cross-exclusions): campaigns exclude irrelevant practice areas
- [ ] Geographic exclusions: out-of-market city names blocked at campaign level where relevant
- [ ] No obvious irrelevant term categories entirely absent from negative structure

**Market-specific caveat (Section 4 — Informational Intent):** In markets with a long consideration window (e.g., NC family law with mandatory 1-year separation), informational queries ("how long does divorce take in NC") represent real prospects at an earlier funnel stage. Do NOT block these wholesale in those markets. Review account notes before applying Section 4 negatives.

---

## Section 4: Ad Creative

*GAQL: 7.1 (RSA performance), 7.2 (ad freshness), 8.1 (change history for ad update dates)*

- [ ] At least one active RSA per ad group
- [ ] No ad groups with paused or removed ads only
- [ ] Ad strength ratings: note any POOR-rated ads (address only after landing page and structure issues are resolved)
- [ ] Ads reference the specific practice area and geography — not generic "need a lawyer?" copy
- [ ] Creative last meaningfully updated within the last 6 months (flag stale creative)
- [ ] CTR is not in consistent decline over the last 3+ months without a creative change (creative staleness signal)

**Blind spot:** Ad rendering in the SERP is not visible via API. Screenshot of ad preview or manual SERP check needed to see how ads actually appear.

---

## Section 5: Geographic & Device Performance

*GAQL: 10.1 (geographic — targeting view), 10.2 (user location — actual physical location), 10.3 (device performance)*

- [ ] Spend is concentrated in the target geographic area — not leaking to out-of-market locations
- [ ] User location data (10.2) aligns with geographic targeting intent — check for "interested in" serving reaching out-of-market users
- [ ] Mobile vs. desktop performance reviewed — if mobile CVR is significantly lower than desktop, bid adjustments may be warranted
- [ ] Device with highest spend has acceptable CPA (flag if highest-spend device has lowest conversion rate)

---

## Section 6: Bidding & Budget

*GAQL: 11.1 (budget utilization), 11.2 (shared bidding strategies), 2.3 (conversion volume by campaign)*

- [ ] Campaigns with smart bidding (tCPA, Maximize Conversions) have at least 15–20 conversions/month — if not, flag bid strategy mismatch
- [ ] tCPA targets are realistic — not set significantly below the account's historical CPA (causes oscillation)
- [ ] No shared bidding strategies pooling campaigns with different economics (brand + non-brand, different practice areas)
- [ ] Budget-constrained campaigns (`search_budget_lost_impression_share` high) reviewed — determine whether more budget is warranted given CPA
- [ ] Delivery method is `STANDARD` on all campaigns (not `ACCELERATED`)

---

## Section 7: Impression Share & Competitive Position

*GAQL: 5.1 (IS breakdown)*

- [ ] Overall search IS reviewed — note whether budget loss or rank loss is the dominant constraint
- [ ] Top IS and absolute top IS noted for core campaigns (indicates whether brand is dominating for brand terms)
- [ ] If rank loss IS is elevated: flag for Quality Score diagnosis before recommending bid increases

**Blind spot:** Auction Insights competitor breakdown is not available via GAQL. Request screenshot of Auction Insights from the UI for campaigns where competitive pressure is suspected.

---

## Synthesis Output

After completing all sections:

1. **Priority 1 (structural blockers):** Pre-flight items that corrupt the meaning of all other data. Fix these first.
2. **Priority 2 (spend impact):** Items with the largest estimated daily waste or conversion loss.
3. **Priority 3 (structural improvement):** Items that won't show immediate impact but compound over time.
4. **Not actionable yet (needs screenshot or more data):** Blind spots that need external input before a recommendation is possible.

Format each item for the running action list:
```
- [ACTION] [target] — [one-line rationale] | [scope: account/campaign/ad-group]
```

---

## Account Notes Update

After the audit, update `account-notes/[account].md` with:
- Account structure summary (campaigns, ad groups, active/paused state)
- Any permanent market-specific context discovered (e.g., practice area nuances, seasonality, client brief preferences)
- All Priority 1–3 items in the `## Pending Actions` section

---

*This checklist is v1 — battle-test it against at least 2 accounts and update based on what it misses or over-specifies.*
