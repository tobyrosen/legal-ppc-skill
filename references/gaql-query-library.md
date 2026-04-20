# GAQL Query Library — Google Ads for Law Firms

Queries are organized by diagnostic task. All queries are pure GAQL — execute via `run_gaql(customer_id, query, format)` or any equivalent GAQL execution tool.

**Notes on values:**
- `cost_micros` is in millionths of the account currency. Divide by 1,000,000 for dollar value.
- `metrics.average_cpc` is already in the account currency (not micros).
- `cpc_bid_micros` on keywords/ad groups is in micros.
- Date placeholders: replace `LAST_30_DAYS`, `LAST_90_DAYS`, `LAST_7_DAYS` with `BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'` for custom ranges.
- GAQL does not support subqueries or calculated fields — do division (cost_micros/1e6) after retrieval.

---

## 1. Account Structure

### 1.1 All Campaigns — Status, Budget, Bid Strategy
```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign.advertising_channel_type,
  campaign.bidding_strategy_type,
  campaign_budget.amount_micros,
  campaign_budget.delivery_method,
  campaign.network_settings.target_search_network,
  campaign.network_settings.target_content_network,
  campaign.network_settings.target_partner_search_network,
  campaign.serving_status
FROM campaign
ORDER BY campaign.name
```
**What to look for:** PMax campaigns (`PERFORMANCE_MAX`), display/content network enabled, delivery method (`STANDARD` vs `ACCELERATED`), bid strategy types that don't match account conversion volume.

---

### 1.2 Ad Groups — Structure and Status
```gaql
SELECT
  campaign.name,
  campaign.status,
  ad_group.id,
  ad_group.name,
  ad_group.status,
  ad_group.type,
  ad_group.cpc_bid_micros
FROM ad_group
WHERE campaign.status = 'ENABLED'
ORDER BY campaign.name, ad_group.name
```

---

### 1.3 Ad Rotation Settings
```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign.ad_serving_optimization_status
FROM campaign
WHERE campaign.status = 'ENABLED'
ORDER BY campaign.name
```
**What to look for:** `OPTIMIZE` or `CONVERSION_OPTIMIZE` means Google is controlling rotation. Correct value is `ROTATE_INDEFINITELY` ("Do Not Optimize").

---

### 1.4 Brand vs. Non-Brand Campaign Check
```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign.bidding_strategy_type,
  campaign_budget.amount_micros
FROM campaign
WHERE campaign.status != 'REMOVED'
ORDER BY campaign.name
```
**Use:** Review campaign names manually for brand isolation. There is no API flag for "brand campaign" — identification is by name convention. Flag any campaign where the name suggests both branded and non-branded traffic could coexist.

---

## 2. Conversion Tracking Audit

### 2.1 All Conversion Actions
```gaql
SELECT
  conversion_action.id,
  conversion_action.name,
  conversion_action.status,
  conversion_action.type,
  conversion_action.category,
  conversion_action.counting_type,
  conversion_action.attribution_model_settings.attribution_model,
  conversion_action.view_through_lookback_window_days,
  conversion_action.click_through_lookback_window_days,
  conversion_action.include_in_conversions_metric,
  conversion_action.value_settings.default_value,
  conversion_action.value_settings.always_use_default_value
FROM conversion_action
WHERE conversion_action.status != 'REMOVED'
ORDER BY conversion_action.name
```
**What to look for:**
- Multiple actions with `include_in_conversions_metric = TRUE` — are these all intentional primary actions?
- `counting_type = MANY_PER_CLICK` on phone call or form actions — usually wrong for legal (one lead = one conversion)
- Mismatched attribution models across actions
- `type` field: `WEBPAGE` actions should have verifiable tag sources; `AD_CALL` actions are auto-tracked; `UPLOAD_CLICKS` suggests offline import
- Any action with a suspicious name (e.g., "All Web Site Visits" set as primary)

---

### 2.2 Recent Conversion Volume by Action
```gaql
SELECT
  conversion_action.name,
  conversion_action.status,
  conversion_action.include_in_conversions_metric,
  metrics.all_conversions,
  metrics.conversions
FROM conversion_action
WHERE segments.date DURING LAST_30_DAYS
  AND conversion_action.status = 'ENABLED'
ORDER BY metrics.all_conversions DESC
```
**What to look for:** Actions with `include_in_conversions_metric = TRUE` but zero `metrics.conversions` in 30 days — either the tag is broken or the action is misconfigured. Actions with very high `all_conversions` but low `conversions` suggest a primary/secondary classification issue.

---

### 2.3 Conversion Volume by Campaign (30/90 day)
```gaql
SELECT
  campaign.name,
  campaign.status,
  campaign.bidding_strategy_type,
  metrics.conversions,
  metrics.all_conversions,
  metrics.cost_micros,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```
**Use:** Evaluate whether campaigns have enough conversion volume to support their current bid strategy. Smart bidding (tCPA, Maximize Conversions) is unreliable below ~15–20 conversions/month per campaign. Adjust date range to `LAST_90_DAYS` for a longer view.

---

## 3. Keyword Analysis

### 3.1 All Active Keywords with Quality Score
```gaql
SELECT
  campaign.name,
  campaign.status,
  ad_group.name,
  ad_group.status,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.negative,
  ad_group_criterion.status,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.post_click_quality_score,
  ad_group_criterion.cpc_bid_micros,
  ad_group_criterion.effective_cpc_bid_micros
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'KEYWORD'
  AND ad_group_criterion.status = 'ENABLED'
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
ORDER BY campaign.name, ad_group.name
```
**What to look for:** Quality scores below 5 on important keywords — check which QS component is below average (`BELOW_AVERAGE`): `search_predicted_ctr` = ad copy problem; `creative_quality_score` = ad relevance problem; `post_click_quality_score` = landing page problem.

---

### 3.2 Match Type Distribution
```gaql
SELECT
  campaign.name,
  ad_group_criterion.keyword.match_type,
  COUNT(ad_group_criterion.keyword.text) AS keyword_count
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'KEYWORD'
  AND ad_group_criterion.status != 'REMOVED'
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name, ad_group_criterion.keyword.match_type
```
**Note:** GAQL does not support `COUNT()` — retrieve all rows and aggregate after retrieval. This query structure is a guide; pull without the COUNT and count by match type from results.

**Actual query:**
```gaql
SELECT
  campaign.name,
  campaign.status,
  ad_group.name,
  ad_group.status,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.negative,
  ad_group_criterion.status
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'KEYWORD'
  AND ad_group_criterion.status != 'REMOVED'
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
ORDER BY campaign.name, ad_group_criterion.keyword.match_type
```
**What to look for:** Any `BROAD` match type keywords outside of a deliberate SKAG test structure. Broad match in legal is almost always a mistake.

---

### 3.3 Keyword Performance — Long-Term Bleed Detection (90-day)
```gaql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM keyword_view
WHERE segments.date DURING LAST_90_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
  AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC
```
**What to look for:** Keywords with significant cost and zero conversions over 90 days. This is the long-term bleed pattern — keywords that survive short-term reviews because individually they don't look catastrophic, but collectively represent consistent waste. Evaluate against the account's actual cost-per-lead target before pausing — context matters.

---

### 3.4 Keyword Performance — 30-day for Current Period
```gaql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

## 4. Search Term Analysis

### 4.1 Search Terms Report (30-day, high cost)
```gaql
SELECT
  campaign.name,
  ad_group.name,
  search_term_view.search_term,
  search_term_view.status,
  segments.keyword.info.text,
  segments.keyword.info.match_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND metrics.impressions > 0
ORDER BY metrics.cost_micros DESC
```
**What to look for:** Search terms that are irrelevant to the firm's practice areas. Cross-reference against the negative keyword library. `search_term_view.status = 'NONE'` means the term is not yet added as a keyword or excluded — these are candidates for review. `EXCLUDED` means it's already blocked.

**Required filter:** `ad_group.status = 'ENABLED'` is mandatory. Without it, results include historical terms from paused/removed ad groups, producing false findings (P8).

---

### 4.2 Search Terms — 90-day, All Traffic (for negative mining)
```gaql
SELECT
  campaign.name,
  search_term_view.search_term,
  search_term_view.status,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_90_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
ORDER BY metrics.impressions DESC
```
**Use:** Broader view for negative keyword mining. Sort by impressions to find irrelevant terms eating impression share without necessarily spending a lot.

---

## 5. Impression Share & Competitive Position

### 5.1 Campaign-Level Impression Share Breakdown
```gaql
SELECT
  campaign.name,
  campaign.status,
  metrics.search_impression_share,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.search_top_impression_share,
  metrics.search_absolute_top_impression_share,
  metrics.cost_micros,
  metrics.impressions,
  metrics.clicks
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND campaign.advertising_channel_type = 'SEARCH'
ORDER BY metrics.cost_micros DESC
```
**What to look for:**
- High `search_budget_lost_impression_share` → budget-constrained; more spend = more traffic
- High `search_rank_lost_impression_share` → quality/bid problem; throwing money at it won't help, fix QS or bids
- The ratio between the two matters: if rank loss >> budget loss on an already-high-budget campaign, that's a QS/relevance problem, not a budget problem

---

### 5.2 Auction Insights (via available campaigns)
**Note:** Auction insights are not available via GAQL. Use the Google Ads UI Auction Insights report for competitor overlap analysis. When flagging competitor pressure as a diagnosis factor, note this limitation and direct to the UI.

---

## 6. Performance Over Time

### 6.1 Campaign Performance — 30-day
```gaql
SELECT
  campaign.name,
  campaign.status,
  campaign.bidding_strategy_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_from_interactions_rate,
  metrics.cost_per_conversion,
  metrics.search_impression_share
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

---

### 6.2 Campaign Performance — 90-day (for trend comparison)
```gaql
SELECT
  campaign.name,
  campaign.status,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_90_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```
**Use:** Run both 30-day and 90-day queries together to identify whether recent performance is deviating from trend. When comparing periods, segment by `segments.month` or `segments.week` for time-series visibility.

---

### 6.3 Weekly Segmented Performance (last 13 weeks)
```gaql
SELECT
  campaign.name,
  segments.week,
  metrics.impressions,
  metrics.clicks,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_90_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY campaign.name, segments.week
```
**Use:** Trend analysis. Identifies whether a performance change is gradual (creative staleness, creeping competition) or abrupt (structural change, algorithm shift, bidding instability).

---

## 7. Ad Creative Performance

### 7.1 RSA Performance by Campaign
```gaql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_ad.ad.id,
  ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad.responsive_search_ad.descriptions,
  ad_group_ad.ad_strength,
  ad_group_ad.status,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM ad_group_ad
WHERE segments.date DURING LAST_30_DAYS
  AND ad_group_ad.status = 'ENABLED'
  AND campaign.status = 'ENABLED'
ORDER BY metrics.impressions DESC
```
**What to look for:** Ads with very low CTR relative to campaign average. `ad_strength` values (`POOR`, `AVERAGE`, `GOOD`, `EXCELLENT`) reflect Google's preference for creative flexibility — treat as a signal only, not as a performance proxy. Low impression share on a specific ad within an ad group suggests the rotation settings may be set to "optimize" despite account-level settings.

---

### 7.2 Ad Copy Freshness Check
```gaql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_ad.ad.id,
  ad_group_ad.status,
  ad_group_ad.ad.final_urls,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros
FROM ad_group_ad
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group_ad.status = 'ENABLED'
ORDER BY campaign.name, ad_group.name
```
**Use:** Combined with change history query (section 8) to assess when ads were last meaningfully updated. CTR decline on stable or high-QS keywords with unchanged ads is a strong freshness signal.

---

## 8. Change History

### 8.1 Recent Changes — Last 30 Days
```gaql
SELECT
  change_event.change_date_time,
  change_event.user_email,
  change_event.client_type,
  change_event.change_resource_type,
  change_event.resource_name,
  change_event.resource_change_operation,
  change_event.changed_fields
FROM change_event
WHERE change_event.change_date_time DURING LAST_30_DAYS
ORDER BY change_event.change_date_time DESC
LIMIT 500
```
**Note:** change_event API limit is 30 days — LAST_60_DAYS and LAST_90_DAYS will error.
**What to look for:**
- `client_type = 'GOOGLE_ADS_AUTOMATED_RULE'` or `'GOOGLE_ADS_RECOMMENDATIONS'` — auto-applied changes from Google. Each one is worth reviewing.
- Gaps of weeks with no changes — neglected account.
- Bursts of many changes in a short window — potential algorithm instability from repeated adjustments.
- Changes to bid strategy, budgets, or targeting during what should be a smart bidding learning phase.

---

### 8.2 Auto-Applied Recommendations Check
```gaql
SELECT
  change_event.change_date_time,
  change_event.user_email,
  change_event.client_type,
  change_event.change_resource_type,
  change_event.resource_change_operation,
  change_event.changed_fields
FROM change_event
WHERE change_event.change_date_time DURING LAST_30_DAYS
  AND change_event.client_type IN ('GOOGLE_ADS_AUTOMATED_RULE', 'GOOGLE_ADS_RECOMMENDATIONS')
ORDER BY change_event.change_date_time DESC
```
**Use:** Isolates Google-initiated changes specifically. In a well-managed account, this list should be short or empty for most change types. A long list of auto-applied changes is a red flag regardless of whether individual changes look benign.

---

## 9. Negative Keyword Structure

### 9.1 Account-Level Shared Negative Keyword Lists
```gaql
SELECT
  shared_set.id,
  shared_set.name,
  shared_set.type,
  shared_set.status,
  shared_set.member_count,
  shared_set.reference_count
FROM shared_set
WHERE shared_set.type = 'NEGATIVE_KEYWORDS'
  AND shared_set.status = 'ENABLED'
ORDER BY shared_set.name
```
**What to look for:** Whether any shared negative lists exist at all. No shared negative lists = one of the clearest signs of an unmanaged account.

---

### 9.2 Contents of a Specific Shared Negative List
```gaql
SELECT
  shared_criterion.keyword.text,
  shared_criterion.keyword.match_type,
  shared_criterion.type
FROM shared_criterion
WHERE shared_set.id = 'SHARED_SET_ID_HERE'
ORDER BY shared_criterion.keyword.text
```
**Replace `SHARED_SET_ID_HERE`** with the ID from query 9.1.

---

### 9.3 Campaign-Level Negative Keywords
```gaql
SELECT
  campaign.name,
  campaign_criterion.keyword.text,
  campaign_criterion.keyword.match_type,
  campaign_criterion.negative
FROM campaign_criterion
WHERE campaign_criterion.type = 'KEYWORD'
  AND campaign_criterion.negative = TRUE
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name, campaign_criterion.keyword.text
```

---

### 9.4 Ad Group-Level Negative Keywords
```gaql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.negative
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'KEYWORD'
  AND ad_group_criterion.negative = TRUE
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name, ad_group.name
```

---

## 10. Geographic & Device Performance

### 10.1 Geographic Performance by Campaign
```gaql
SELECT
  campaign.name,
  geographic_view.country_criterion_id,
  geographic_view.location_type,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM geographic_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```
**Note:** For city/region-level data, use `user_location_view` instead of `geographic_view`. `geographic_view` reflects targeting settings; `user_location_view` reflects where users actually were.

### 10.2 User Location View (Actual Physical Location)
```gaql
SELECT
  campaign.name,
  user_location_view.targeting_location,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions
FROM user_location_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

### 10.3 Device Performance by Campaign
```gaql
SELECT
  campaign.name,
  segments.device,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name, segments.device
```
**What to look for:** Disproportionate spend on mobile with significantly lower conversion rates than desktop. Legal clients frequently research on mobile but convert (call or fill a form) on desktop or by phone — device bid adjustments may be warranted.

---

### 10.4 Daypart Performance
```gaql
SELECT
  campaign.name,
  segments.hour,
  segments.day_of_week,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name, segments.day_of_week, segments.hour
```
**Use:** Identifies whether spend is concentrated during hours when the firm can actually answer calls. Call extensions should be scheduled to office hours — this query helps verify alignment and identify off-hours waste.

---

## 11. Bidding & Budget

### 11.1 Budget Utilization by Campaign
```gaql
SELECT
  campaign.name,
  campaign.status,
  campaign_budget.amount_micros,
  campaign_budget.delivery_method,
  metrics.cost_micros,
  metrics.impressions,
  metrics.search_budget_lost_impression_share
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```
**Use:** Compare `cost_micros / 1e6 / days_in_period` against `campaign_budget.amount_micros / 1e6` to see if campaigns are hitting their daily budget ceiling. Combined with `search_budget_lost_impression_share` this tells you whether budget constraint is actively limiting performance.

---

### 11.2 Shared Bidding Strategies
```gaql
SELECT
  bidding_strategy.id,
  bidding_strategy.name,
  bidding_strategy.type,
  bidding_strategy.status,
  bidding_strategy.campaign_count,
  bidding_strategy.target_cpa.target_cpa_micros,
  bidding_strategy.target_roas.target_roas
FROM bidding_strategy
ORDER BY bidding_strategy.name
```
**What to look for:** Shared bidding strategies that pool multiple campaigns together. In legal, campaigns often have different economics (branded vs. non-branded, different practice areas) — pooling them into a shared strategy can degrade performance by mixing signals.

---

## 12. Landing Page & Final URL Audit

### 12.1 Final URLs by Campaign
```gaql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_ad.ad.final_urls,
  ad_group_ad.status,
  metrics.impressions,
  metrics.clicks
FROM ad_group_ad
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group_ad.status = 'ENABLED'
ORDER BY campaign.name
```
**Use:** Verify that ads are pointing to the correct URLs. Spot ads going to the homepage when they should go to a practice-area-specific landing page. Flag any `/404` or redirect chains by checking URLs manually — GAQL cannot verify landing page status.

---

## 13. Search Term Coverage Verification

**Run this before any search term analysis.** Establishes the coverage ratio (visible STV spend ÷ actual campaign spend) that must be stated before presenting any search term findings.

The Google Ads API has a hard row cap on `search_term_view` — typically returning ~50% of actual spend regardless of query granularity. This is not a privacy threshold; it cannot be bypassed with query splitting or pagination (GAQL has no OFFSET). Always disclose the ratio and scale waste estimates accordingly.

### 13.1 Step 1 — Actual Campaign Spend

Run first. This is the denominator.

```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  metrics.cost_micros
FROM campaign
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND campaign.status != 'REMOVED'
  AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC
```

Sum `cost_micros / 1e6` across all campaigns for total actual spend. Note per-campaign spend — needed for per-campaign STV pulls in Step 2.

---

### 13.2 Step 2 — Visible Search Term Spend (Per Campaign)

Run once per active campaign — NOT as an all-campaigns query (all-campaigns hits the 500-row cap immediately, giving far worse coverage). Use the date range from Step 1.

```gaql
SELECT
  campaign.id,
  campaign.name,
  metrics.cost_micros
FROM search_term_view
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND campaign.id = CAMPAIGN_ID_HERE
```

Sum `cost_micros / 1e6` across all per-campaign results for total visible spend.

---

### 13.3 Compute and Report Coverage

```
Coverage = (sum of visible STV cost) / (sum of actual campaign cost) × 100
```

**Mandatory reporting format before presenting any findings:**

> Search term data covers **$[visible]** of **$[actual]** actual spend (**[Z]%** coverage). This is the Google Ads API ceiling — the hidden portion (~[100-Z]%) is randomly distributed, not systematically different.

**Scale all waste estimates:**

> Visible waste in identified categories: **$[waste_visible]**
> Estimated total waste (scaled): **~$[waste_visible / coverage_pct]**

Do not present findings, waste estimates, or negative keyword recommendations without this disclosure on the table.

---

*Note: Per-ad-group query splitting beyond per-campaign will yield marginal additional coverage (a few percentage points at most) once the per-campaign ceiling is reached. The ~50% ceiling is a hard API limit, not improvable through query structure.*

---

## Query Composition Notes

**Date range options:**
```
DURING LAST_7_DAYS
DURING LAST_14_DAYS
DURING LAST_30_DAYS
DURING LAST_90_DAYS
DURING THIS_MONTH
DURING LAST_MONTH
BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

**Filtering by status:**
- Always add `campaign.status != 'REMOVED'` or `= 'ENABLED'` to exclude historical data clutter
- For keywords: `ad_group_criterion.status = 'ENABLED'` excludes paused and removed keywords
- For ads: `ad_group_ad.status = 'ENABLED'` excludes paused ads

**Result limits:**
- Default API page size is 10,000 rows; large accounts may need pagination
- Add `LIMIT N` to queries when testing or when you only need a sample

**Resources that do NOT support date segmentation:**
- `campaign` (structure queries, section 1) — omit date filter for structural queries
- `conversion_action` — omit date filter for the action list; add for metrics queries
- `shared_set` / `shared_criterion` — no date segmentation available
