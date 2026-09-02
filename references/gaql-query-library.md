# GAQL Query Library: Google Ads for Law Firms

Queries are organized by diagnostic task. All queries are pure GAQL. Execute via `run_gaql(customer_id, query, format)` or any equivalent GAQL execution tool.

**Notes on values:**

- `cost_micros` is in millionths of the **account's** currency. Divide by 1,000,000 to get the value in that currency, which is not necessarily dollars. Never label a converted figure a dollar value without confirming the account's currency.
- **Pull the currency before reporting any cost figure:** `SELECT customer.currency_code FROM customer`. Report each account in its native currency (symbol or ISO code). Cross-currency totals, averages, or rankings require an operator-approved FX source, with the rate and effective date stated in the output. Never sum, average, or rank raw numbers across currencies.
- `metrics.average_cpc` is already in the account currency (not micros).
- `cpc_bid_micros` on keywords/ad groups is in micros.
- **Valid `DURING` date literals only:** `LAST_7_DAYS`, `LAST_14_DAYS`, `LAST_30_DAYS`, `THIS_MONTH`, `LAST_MONTH`, `THIS_WEEK_MON_TODAY`, `LAST_WEEK_MON_SUN`. **There is no `LAST_60_DAYS` or `LAST_90_DAYS`**. They error with `INVALID_VALUE_WITH_DURING_OPERATOR`. For a 90-day (or any custom) window, use `segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'` with explicit dates (end = today, start = today − N days).
- GAQL does not support subqueries or calculated fields. Do division (cost_micros/1e6) after retrieval.

---

## 1. Account Structure

### 1.1 All Campaigns: Status, Budget, Bid Strategy

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

### 1.2 Ad Groups: Structure and Status

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

**Use:** Review campaign names manually for brand isolation. There is no API flag for "brand campaign". Identification is by name convention. Flag any campaign where the name suggests both branded and non-branded traffic could coexist.

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

- Multiple actions with `include_in_conversions_metric = TRUE`. Are these all intentional primary actions?
- `counting_type = ONE_PER_CLICK` on phone call or form lead actions with no recorded override: a deviation from the house standard (agency-defaults.md Sec 3.4: `MANY_PER_CLICK` is standard on lead actions, situational rather than universally correct for legal PPC, since an agency may choose `ONE_PER_CLICK` where repeat events are noise, recorded as an override)
- Mismatched attribution models across actions
- `type` field: `WEBPAGE` actions should have verifiable tag sources; `AD_CALL` actions are auto-tracked; `UPLOAD_CLICKS` suggests offline import
- Any action with a suspicious name (e.g., "All Web Site Visits" set as primary)

---

### 2.2 Recent Conversion Volume by Action

```gaql
SELECT
  segments.conversion_action_name,
  segments.conversion_action_category,
  metrics.all_conversions,
  metrics.conversions
FROM customer
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.conversions DESC
```

**Why this segments off `customer`, not `conversion_action`:** `metrics.conversions` is PROHIBITED on the `conversion_action` resource (`PROHIBITED_METRIC_IN_SELECT_OR_WHERE_CLAUSE`, only `metrics.all_conversions` is allowed there). To get true `conversions` volume per action you must segment a metrics-bearing resource: `FROM customer` for account-wide per-action totals, or `FROM campaign` (add `campaign.name`) to also see which campaign drove each action. Cross-reference `segments.conversion_action_name` against the config from 2.1 (status, `include_in_conversions_metric`). Those config fields are not available alongside segmented metrics.
**What to look for:** Actions with high `all_conversions` but low/zero `conversions` (e.g. an `ENGAGEMENT`-category action) are secondary/soft actions, not real leads. They should not be primary. An action that is `include_in_conversions_metric = TRUE` (per 2.1) but shows zero `conversions` over 30 days is either broken or misconfigured.

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

**Use:** Evaluate whether campaigns have enough conversion volume to support their current bid strategy. Smart bidding (tCPA, Maximize Conversions) is unreliable below the account's reliability floor, which is volume-dependent judgment rather than a fixed count. For a longer (90-day) view, switch the date filter to `segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'` (start = today minus 90). `LAST_90_DAYS` is not a valid GAQL literal.

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
  AND ad_group_criterion.negative = FALSE
  AND ad_group_criterion.status = 'ENABLED'
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
ORDER BY campaign.name, ad_group.name
```

**What to look for:** the quality-score trend on the spending keywords rather than any cutoff. A falling quality score with impressions collapsing while ad rank and bid hold is the throttling shape and is a finding. Where the score is falling, check which QS component is below average (`BELOW_AVERAGE`): `search_predicted_ctr` = ad copy problem; `creative_quality_score` = ad relevance problem; `post_click_quality_score` = landing page problem.

**Required filter:** `ad_group_criterion.negative = FALSE` is mandatory. `ad_group_criterion` returns both positive and negative keywords. Omitting this filter causes ad-group-level negatives to appear as positive keywords, producing false BROAD match flags and misidentified waste (P6).

**Output-format note (verified live 2026-06-05):** `quality_info.*` are nested message fields. A plain table formatter can silently DROP them. The keyword shows but `quality_score` is absent, making QS look unavailable when it actually sources fine. Pull this query with `format='json'` (or read the nested `qualityInfo` object) to get `qualityScore` plus the three component labels (`creativeQualityScore`, `postClickQualityScore`, `searchPredictedCtr`). Confirmed live: brand keywords returned QS 7–10 with `ABOVE_AVERAGE`/`AVERAGE` labels.

---

### 3.2 Match Type Distribution

```text
-- ILLUSTRATIVE ONLY, not runnable: GAQL does not support COUNT().
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

**Note:** GAQL does not support `COUNT()`. Retrieve all rows and aggregate after retrieval. This query structure is a guide; pull without the COUNT and count by match type from results.

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
  AND ad_group_criterion.negative = FALSE
  AND ad_group_criterion.status != 'REMOVED'
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
ORDER BY campaign.name, ad_group_criterion.keyword.match_type
```

**What to look for:** Any `BROAD` match type keywords outside of a deliberate SKAG test structure. Broad match in legal is almost always a mistake.

**Required filter:** `ad_group_criterion.negative = FALSE` is mandatory here for the same reason as 3.1. Negatives have match types too, and without this filter ad-group-level negative BROAD keywords appear as positive BROADs.

---

### 3.3 Keyword Performance: Long-Term Bleed Detection (90-day)

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
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
  AND ad_group_criterion.negative = FALSE
  AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC
```

**What to look for:** Keywords with significant cost and zero conversions over 90 days. This is the long-term bleed pattern: keywords that survive short-term reviews because individually they don't look catastrophic, but collectively represent consistent waste. Evaluate against the account's actual cost-per-lead target before pausing. Context matters.

---

### 3.4 Keyword Performance: 30-day for Current Period

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
  AND ad_group_criterion.negative = FALSE
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
LIMIT 150
```

**What to look for:** Search terms that are irrelevant to the firm's practice areas. Cross-reference against the negative keyword library.

**Status meaning (mandatory, matches SKILL.md "Search term queries"):** `search_term_view.status = 'NONE'` means the term matched **historically** and is not currently served by any keyword. `NONE` is **never** an active finding: not current waste, not a current structure problem. Do not flag it, and do not treat it as a review candidate. Only terms whose status describes their present state are eligible for active review: `ADDED` (a keyword currently matches it, review its performance) and `EXCLUDED` (already blocked, no action needed). `ADDED_EXCLUDED` counts as excluded.

**Required filter:** `ad_group.status = 'ENABLED'` is mandatory. Without it, results include historical terms from paused/removed ad groups, producing false findings (P8).

---

### 4.2 Search Terms: 90-day, All Traffic (for negative mining)

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
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
ORDER BY metrics.impressions DESC
LIMIT 150
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

### 6.1 Campaign Performance: 30-day

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

### 6.2 Campaign Performance: 90-day (for trend comparison)

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
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
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
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
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

**What to look for:** Ads with very low CTR relative to campaign average. `ad_strength` values (`POOR`, `AVERAGE`, `GOOD`, `EXCELLENT`) reflect Google's preference for creative flexibility. Treat as a signal only, not as a performance proxy. Low impression share on a specific ad within an ad group suggests the rotation settings may be set to "optimize" despite account-level settings.

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

### 7.3 Ad Policy / Approval Status

```gaql
SELECT
  campaign.id,
  campaign.name,
  ad_group.id,
  ad_group.name,
  ad_group_ad.ad.id,
  ad_group_ad.status,
  ad_group_ad.policy_summary.approval_status,
  ad_group_ad.policy_summary.review_status
FROM ad_group_ad
WHERE ad_group_ad.status != 'REMOVED'
ORDER BY campaign.name, ad_group.name
```

**What to look for:** Ad approval and review status are API-accessible. Pull them here first, do not default to a screenshot. Flag any ad where `ad_group_ad.policy_summary.approval_status` is `DISAPPROVED` (ad is not serving) or `APPROVED_LIMITED` (serving with restrictions, limited reach, geography, or audience), OR where `ad_group_ad.policy_summary.review_status` is `UNDER_REVIEW` or `REVIEW_IN_PROGRESS` (approval pending, the ad may not be fully serving yet; the live API commonly returns `REVIEW_IN_PROGRESS` for ads still under review). `DISAPPROVED` is the most urgent: a disapproved ad in an otherwise-serving campaign silently starves that ad group of eligible creative. `APPROVED_LIMITED` is the common trap on a campaign whose `serving_status` reads `SERVING` at the campaign level while individual ads are throttled by policy. Cross-reference flagged ads against the campaign's `serving_status` (query 1.1). A normal campaign serving_status does NOT clear ad-level policy issues. A screenshot of the Policy Manager is the fallback only for the human-readable disapproval reason, which the API summary does not fully expand.

---

## 8. Change History

### 8.1 Recent Changes: Last 30 Days

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
WHERE change_event.change_date_time >= 'YYYY-MM-DD 00:00:00'
  AND change_event.change_date_time <= 'YYYY-MM-DD 23:59:59'
ORDER BY change_event.change_date_time DESC
LIMIT 500
```

**`change_event` has three hard constraints, all required, or the query errors:**

1. **Bounded date range.** Filter `change_event.change_date_time` with BOTH a `>=` start and a `<=` end (or `BETWEEN`). A bare `>=` errors with `CHANGE_DATE_RANGE_INFINITE`. Do NOT use `DURING LAST_30_DAYS`. Its start resolves to exactly 30 days ago and trips `START_DATE_TOO_OLD` (the window must be _strictly inside_ 30 days). Set start = today − 29 days, end = today.
2. **A `LIMIT` is mandatory** (≤ 10000), or the query errors with `LIMIT_NOT_SPECIFIED`.
3. **30-day ceiling.** Change history older than 30 days is unavailable: `LAST_60_DAYS` / `LAST_90_DAYS` do not exist and would error regardless.
   **What to look for:**

- `client_type = 'GOOGLE_ADS_AUTOMATED_RULE'` or `'GOOGLE_ADS_RECOMMENDATIONS'`: auto-applied changes from Google. Each one is worth reviewing.
- Gaps of weeks with no changes: neglected account.
- Bursts of many changes in a short window: potential algorithm instability from repeated adjustments.
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
WHERE change_event.change_date_time >= 'YYYY-MM-DD 00:00:00'
  AND change_event.change_date_time <= 'YYYY-MM-DD 23:59:59'
  AND change_event.client_type IN ('GOOGLE_ADS_AUTOMATED_RULE', 'GOOGLE_ADS_RECOMMENDATIONS')
ORDER BY change_event.change_date_time DESC
LIMIT 500
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
  campaign.status,
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
  campaign.status,
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

**Required SELECT field:** `geographic_view` and `user_location_view` reject a `campaign.status` filter unless `campaign.status` is also in the SELECT clause (`EXPECTED_REFERENCED_FIELD_IN_SELECT_CLAUSE`). Both queries above include it for this reason. Don't remove it.

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

**What to look for:** Disproportionate spend on mobile with significantly lower conversion rates than desktop. Legal clients frequently research on mobile but convert (call or fill a form) on desktop or by phone. Device bid adjustments may be warranted.

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

**Use:** Identifies whether spend is concentrated during hours when the firm can actually answer calls. Call extensions should be scheduled to office hours. This query helps verify alignment and identify off-hours waste.

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

**What to look for:** Shared bidding strategies that pool multiple campaigns together. In legal, campaigns often have different economics (branded vs. non-branded, different practice areas). Pooling them into a shared strategy can degrade performance by mixing signals.

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

**Use:** Verify that ads are pointing to the correct URLs. Spot ads going to the homepage when they should go to a practice-area-specific landing page. Flag any `/404` or redirect chains by checking URLs manually. GAQL cannot verify landing page status.

---

## 13. Search Term Spend Pulls

Two pulls that sit under any search-term analysis: what the campaign actually spent, and what its
search terms spent. Report what the data returns. Nothing here is estimated, extrapolated, or scaled
to stand for spend the pull did not return.

### 13.1 Actual Campaign Spend

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

Sum `cost_micros / 1e6` across all campaigns for total spend. Note per-campaign spend: it is needed
for the per-campaign search-term pulls in 13.2.

---

### 13.2 Search Term Spend (Per Campaign)

Run once per active campaign, not as an all-campaigns query: a single all-campaigns pull returns a
coarse, truncated result. Use the date range from 13.1.

```gaql
SELECT
  campaign.id,
  campaign.name,
  metrics.cost_micros
FROM search_term_view
WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
  AND campaign.id = CAMPAIGN_ID_HERE
```

Sum `cost_micros / 1e6` across the per-campaign results.

---

### 13.3 Reporting

Report the measured figures next to the campaign's actual CPL. A waste figure is the spend the pull
shows in the categories named, and it is presented as exactly that. Never multiply it up, never
present a derived total as a measurement, and never attribute a gap to an API row cap.

---

## 14. Config Baseline Pull

The queries that read every setting in `references/agency-defaults.md`. Run this set in pre-flight
(PF-4), then classify each setting as MATCH, OVERRIDE-MATCH, or DEVIATION against the baseline.
Structure queries: no date segmentation, no metrics.

**Field names verified against Google Ads API v23.** Three v23 changes bite here:

1. **`change_event` requires a `LIMIT`.** A `change_event` query without one fails with
   `changeEventError.LIMIT_NOT_SPECIFIED`. The limit must be 10,000 or less.
2. **`campaign_asset` has no `policy_summary`.** `campaign_asset.policy_summary.approval_status`
   and `.review_status` return `queryError.UNRECOGNIZED_FIELD`. Campaign-level asset approval is
   readable only via `campaign_asset.primary_status` and `.primary_status_reasons`.
   `asset_group_asset.policy_summary.*` does still exist, so PMax asset-group approval is fully
   readable; only the campaign-level assets are limited.
3. **`campaign.url_expansion_opt_out` is gone.** Final URL expansion is read from
   `campaign.asset_automation_settings`.

Two more API behaviours to expect in the results:

- **Boolean fields are omitted, not returned as `false`.** `campaign_conversion_goal.biddable` and
  `customer_conversion_goal.biddable` are absent when not true. Absence is the negative case, not
  missing data.
- **`campaign_asset` queries require `campaign.id` in the SELECT**, or the query fails on a
  required-field error.

---

### 14.1 Campaign Settings Baseline

Covers agency-defaults §1 (networks, ad rotation, geo target type, dates, tracking template,
serving state, AI Max, EU political) and the PMax guideline fields in §5.

```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign.serving_status,
  campaign.primary_status,
  campaign.primary_status_reasons,
  campaign.advertising_channel_type,
  campaign.advertising_channel_sub_type,
  campaign.experiment_type,
  campaign.network_settings.target_google_search,
  campaign.network_settings.target_search_network,
  campaign.network_settings.target_content_network,
  campaign.network_settings.target_partner_search_network,
  campaign.ad_serving_optimization_status,
  campaign.geo_target_type_setting.positive_geo_target_type,
  campaign.geo_target_type_setting.negative_geo_target_type,
  campaign.start_date_time,
  campaign.end_date_time,
  campaign.tracking_url_template,
  campaign.final_url_suffix,
  campaign.ai_max_setting.enable_ai_max,
  campaign.contains_eu_political_advertising,
  campaign.selective_optimization.conversion_actions,
  campaign.brand_guidelines_enabled,
  campaign.brand_guidelines.main_color,
  campaign.brand_guidelines.accent_color,
  campaign.brand_guidelines.predefined_font_family,
  campaign.asset_automation_settings,
  campaign.text_guidelines.term_exclusions,
  campaign.text_guidelines.messaging_restrictions,
  campaign.dynamic_search_ads_setting.domain_name,
  campaign.dynamic_search_ads_setting.use_supplied_urls_only
FROM campaign
WHERE campaign.status != 'REMOVED'
ORDER BY campaign.name
```

**What to check:** §1.1 through §1.12, plus §5.2 to §5.5 on any `PERFORMANCE_MAX` row.
`campaign.asset_automation_settings` returns a list of type/status pairs; the standard is every
type `OPTED_OUT`, including the final-URL-expansion type. Brand guideline and text guideline fields
are populated only on PMax campaigns; their absence on a Search campaign is not a finding.

---

### 14.2 Budget and Bidding Baseline

Covers agency-defaults §2.

```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign.bidding_strategy_type,
  campaign.bidding_strategy,
  campaign.bidding_strategy_system_status,
  campaign.maximize_conversions.target_cpa_micros,
  campaign.target_cpa.target_cpa_micros,
  campaign.target_cpa.cpc_bid_ceiling_micros,
  campaign.target_cpa.cpc_bid_floor_micros,
  campaign.target_spend.cpc_bid_ceiling_micros,
  campaign.maximize_conversion_value.target_roas,
  campaign.target_roas.target_roas,
  campaign_budget.id,
  campaign_budget.name,
  campaign_budget.amount_micros,
  campaign_budget.total_amount_micros,
  campaign_budget.period,
  campaign_budget.delivery_method,
  campaign_budget.explicitly_shared,
  campaign_budget.status
FROM campaign
WHERE campaign.status != 'REMOVED'
ORDER BY campaign.name
```

**What to check:** §2.1 to §2.4. A target CPA field omitted from the response means no target is
set, which is the standard below the volume floor. Read the strategy against the campaign's own
30-day conversion count, not the account's.

Portfolio strategies attached via `campaign.bidding_strategy` need the shared-strategy query
(§11.2) to read their targets.

---

### 14.3 Geo, Language, Device, and Proximity Criteria

Covers agency-defaults §1.7, §5.6, §6.6, §6.7.

```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign_criterion.criterion_id,
  campaign_criterion.type,
  campaign_criterion.status,
  campaign_criterion.negative,
  campaign_criterion.bid_modifier,
  campaign_criterion.location.geo_target_constant,
  campaign_criterion.proximity.radius,
  campaign_criterion.proximity.radius_units,
  campaign_criterion.proximity.address.city_name,
  campaign_criterion.proximity.address.province_name,
  campaign_criterion.language.language_constant,
  campaign_criterion.device.type,
  campaign_criterion.ad_schedule.day_of_week,
  campaign_criterion.ad_schedule.start_hour,
  campaign_criterion.ad_schedule.end_hour,
  campaign_criterion.content_label.type
FROM campaign_criterion
WHERE campaign.status = 'ENABLED'
  AND campaign_criterion.status != 'REMOVED'
  AND campaign_criterion.type IN ('LOCATION', 'PROXIMITY', 'LANGUAGE', 'DEVICE', 'AD_SCHEDULE', 'CONTENT_LABEL')
ORDER BY campaign.name, campaign_criterion.type
```

**What to check:** language set (§1.7), any `AD_SCHEDULE` row (§6.6), any `DEVICE` row carrying a
`bid_modifier` (§6.7), negative location coverage. Location rows return a geo target constant
resource name, not a place name; resolve it via `geo_target_constant` if the name is needed.

Note: the geo _target type_ setting lives on `campaign` (§14.1), not on the criteria. The criteria
say _where_; the setting says _who counts as being there_.

---

### 14.4 Campaign-Level Negative Keywords and Webpage Exclusions

Covers agency-defaults §4.4, §4.5, §5.3, §5.7.

```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign_criterion.criterion_id,
  campaign_criterion.type,
  campaign_criterion.negative,
  campaign_criterion.status,
  campaign_criterion.keyword.text,
  campaign_criterion.keyword.match_type,
  campaign_criterion.webpage.criterion_name
FROM campaign_criterion
WHERE campaign.status = 'ENABLED'
  AND campaign_criterion.negative = TRUE
  AND campaign_criterion.status != 'REMOVED'
  AND campaign_criterion.type IN ('KEYWORD', 'WEBPAGE')
ORDER BY campaign.name, campaign_criterion.type
```

**What to check:** brand-term exclusions on a non-brand PMax test (§5.7), and whether any negative
blocks a term with conversion history (§4.5, cross-reference the search terms report).

---

### 14.5 Shared Negative Lists and Their Attachment

Covers agency-defaults §4.1 to §4.3. Two queries: what exists, and what is attached.

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
  AND shared_set.status != 'REMOVED'
ORDER BY shared_set.name
```

```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign_shared_set.shared_set,
  campaign_shared_set.status,
  shared_set.id,
  shared_set.name,
  shared_set.member_count
FROM campaign_shared_set
WHERE campaign.status = 'ENABLED'
  AND campaign_shared_set.status != 'REMOVED'
ORDER BY campaign.name
```

**What to check:** a list existing at all (§4.1, red flag if none), and every serving campaign
appearing in the second result set (§4.2). A serving campaign absent from the second query
references no shared list. `shared_set.reference_count` gives the same information in aggregate but
does not say _which_ campaigns are missing.

---

### 14.6 Conversion Action Configuration

Covers agency-defaults §3.3 to §3.9. This is the configuration half of PF-1.

```gaql
SELECT
  conversion_action.id,
  conversion_action.name,
  conversion_action.status,
  conversion_action.type,
  conversion_action.category,
  conversion_action.origin,
  conversion_action.counting_type,
  conversion_action.include_in_conversions_metric,
  conversion_action.primary_for_goal,
  conversion_action.phone_call_duration_seconds,
  conversion_action.click_through_lookback_window_days,
  conversion_action.view_through_lookback_window_days,
  conversion_action.attribution_model_settings.attribution_model,
  conversion_action.attribution_model_settings.data_driven_model_status,
  conversion_action.google_analytics_4_settings.event_name,
  conversion_action.google_analytics_4_settings.property_name,
  conversion_action.owner_customer,
  conversion_action.value_settings.default_value,
  conversion_action.value_settings.always_use_default_value
FROM conversion_action
WHERE conversion_action.status != 'REMOVED'
ORDER BY conversion_action.category, conversion_action.name
```

**What to check:** every §3 entry. PRIMARY is `status = ENABLED` **and**
`include_in_conversions_metric = true`; `primary_for_goal` is a separate field and does not mean
the same thing, so do not read one for the other. Count primaries by category before reading any
CPL figure.

Conversion silence (§3.9) needs the metric, which requires a date range:

```gaql
SELECT
  conversion_action.id,
  conversion_action.name,
  conversion_action.status,
  conversion_action.include_in_conversions_metric,
  metrics.all_conversions,
  metrics.conversion_last_conversion_date
FROM conversion_action
WHERE conversion_action.status = 'ENABLED'
  AND segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
ORDER BY metrics.all_conversions DESC
```

---

### 14.7 Conversion Goal Wiring

Covers agency-defaults §3.1 and §3.2. Four resources, because the goal set is assembled from four
places and reading any one alone gives the wrong answer.

```gaql
SELECT
  campaign.id,
  campaign.name,
  conversion_goal_campaign_config.goal_config_level,
  conversion_goal_campaign_config.custom_conversion_goal
FROM conversion_goal_campaign_config
WHERE campaign.status = 'ENABLED'
ORDER BY campaign.name
```

```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign_conversion_goal.category,
  campaign_conversion_goal.origin,
  campaign_conversion_goal.biddable
FROM campaign_conversion_goal
WHERE campaign.status = 'ENABLED'
ORDER BY campaign.name, campaign_conversion_goal.category
```

```gaql
SELECT
  customer_conversion_goal.category,
  customer_conversion_goal.origin,
  customer_conversion_goal.biddable
FROM customer_conversion_goal
ORDER BY customer_conversion_goal.category
```

```gaql
SELECT
  custom_conversion_goal.id,
  custom_conversion_goal.name,
  custom_conversion_goal.status,
  custom_conversion_goal.conversion_actions
FROM custom_conversion_goal
```

**How to read the four together:**

1. `conversion_goal_campaign_config.goal_config_level` says whether the campaign uses the account
   default (`CUSTOMER`) or its own set (`CAMPAIGN`).
2. `customer_conversion_goal` is the account default map of category and origin to biddable.
3. `campaign_conversion_goal` is the campaign's effective map. At `CUSTOMER` level it mirrors the
   customer map; at `CAMPAIGN` level it is the campaign's own.
4. `custom_conversion_goal` is the named goal set the UI's campaign-specific goal picker offers.
   An empty result means the picker has nothing in it, which is worth knowing before proposing that
   someone select one.

The biddable map names _categories_, not actions. Translate it into actions by joining the biddable
category and origin pairs against the §14.6 result: the actions the campaign can optimise toward
are the ENABLED, `include_in_conversions_metric = true` actions whose category and origin are
biddable. That join is the check, and it is where a page-view or content-download category
quietly widens the goal set (§3.2).

---

### 14.8 Account-Level Settings

Covers agency-defaults §7.2 to §7.7.

```gaql
SELECT
  customer.id,
  customer.descriptive_name,
  customer.currency_code,
  customer.time_zone,
  customer.status,
  customer.manager,
  customer.test_account,
  customer.auto_tagging_enabled,
  customer.conversion_tracking_setting.conversion_tracking_status,
  customer.conversion_tracking_setting.conversion_tracking_id,
  customer.conversion_tracking_setting.cross_account_conversion_tracking_id,
  customer.conversion_tracking_setting.enhanced_conversions_for_leads_enabled,
  customer.conversion_tracking_setting.accepted_customer_data_terms,
  customer.conversion_tracking_setting.google_ads_conversion_customer,
  customer.call_reporting_setting.call_reporting_enabled,
  customer.call_reporting_setting.call_conversion_reporting_enabled,
  customer.call_reporting_setting.call_conversion_action,
  customer.tracking_url_template,
  customer.final_url_suffix,
  customer.contains_eu_political_advertising,
  customer.optimization_score
FROM customer
```

**What to check:** every §7 entry except auto-apply, which is not exposed here (see §14.12).
`conversion_tracking_id` differing from `google_ads_conversion_customer` means conversions are owned
by another account in the hierarchy, which changes who can edit them.

---

### 14.9 Campaign-Level Assets

Covers agency-defaults §6.5, and the campaign-level assets on a PMax campaign (§5.4).

```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign_asset.asset,
  campaign_asset.field_type,
  campaign_asset.status,
  campaign_asset.source,
  campaign_asset.primary_status,
  campaign_asset.primary_status_reasons,
  asset.id,
  asset.name,
  asset.type,
  asset.sitelink_asset.link_text,
  asset.callout_asset.callout_text,
  asset.structured_snippet_asset.header,
  asset.call_asset.phone_number,
  asset.final_urls
FROM campaign_asset
WHERE campaign.status = 'ENABLED'
  AND campaign_asset.status != 'REMOVED'
ORDER BY campaign.name, campaign_asset.field_type
```

**`campaign.id` is required in the SELECT** or the query errors. Asset approval at this level comes
from `primary_status` and `primary_status_reasons`; there is no `policy_summary` on
`campaign_asset` in v23.

**What to check:** which asset field types are present per campaign (§6.5), and any asset in a
non-serving primary status. `ASSET_UNDER_REVIEW` on a newly created asset is expected; a
disapproved or limited asset that has been in place for a while is not.

---

### 14.10 Performance Max Asset Groups

Covers agency-defaults §5.8 and §5.9.

```gaql
SELECT
  campaign.id,
  campaign.name,
  asset_group.id,
  asset_group.name,
  asset_group.status,
  asset_group.ad_strength,
  asset_group.primary_status,
  asset_group.primary_status_reasons,
  asset_group.final_urls,
  asset_group.final_mobile_urls,
  asset_group.path1,
  asset_group.path2
FROM asset_group
WHERE campaign.status = 'ENABLED'
  AND asset_group.status != 'REMOVED'
ORDER BY campaign.name, asset_group.name
```

```gaql
SELECT
  asset_group.id,
  asset_group.name,
  asset_group_asset.field_type,
  asset_group_asset.status,
  asset_group_asset.primary_status,
  asset_group_asset.primary_status_reasons,
  asset_group_asset.policy_summary.approval_status,
  asset_group_asset.policy_summary.review_status,
  asset_group_asset.policy_summary.policy_topic_entries,
  asset.id,
  asset.type,
  asset.source,
  asset.text_asset.text
FROM asset_group_asset
WHERE asset_group_asset.status != 'REMOVED'
ORDER BY asset_group.name, asset_group_asset.field_type
```

```gaql
SELECT
  asset_group.id,
  asset_group.name,
  asset_group_signal.audience.audience,
  asset_group_signal.search_theme.text
FROM asset_group_signal
```

**What to check:** field-type coverage per asset group (§5.8), ad strength once review has
completed, and at least one signal (§5.9). Unlike `campaign_asset`, `asset_group_asset` **does**
carry `policy_summary`, so asset-group approval is fully readable. `approval_status = UNKNOWN` with
`review_status = REVIEW_IN_PROGRESS` is the normal state for a campaign under review, not a
disapproval, and `policy_topic_entries` is null until review finishes.

---

### 14.11 Ad-Level Policy and Match Types

Covers agency-defaults §6.1 and §6.4. Ad policy has its own query at §7.3; this pairing is here so
the config pull is self-contained.

```gaql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_ad.ad.id,
  ad_group_ad.ad.type,
  ad_group_ad.status,
  ad_group_ad.ad_strength,
  ad_group_ad.policy_summary.approval_status,
  ad_group_ad.policy_summary.review_status
FROM ad_group_ad
WHERE ad_group_ad.status = 'ENABLED'
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name, ad_group.name
```

```gaql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.keyword.text,
  ad_group_criterion.status,
  ad_group_criterion.negative
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'KEYWORD'
  AND ad_group_criterion.negative = FALSE
  AND ad_group_criterion.status = 'ENABLED'
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name, ad_group.name
```

**What to check:** RSA count per ad group (§6.4), any `BROAD` match type outside a named test
structure (§6.1). The keyword query filters `negative = FALSE` deliberately: the API returns
positive and negative keywords in the same result set, and counting them together produces a
confirmed misdiagnosis.

---

### 14.12 Config Drift and Auto-Applied Changes

Covers agency-defaults §7.1 and §2.7. `change_event` is the only way to see who changed a setting
and when, and the only available signal on the auto-apply setting.

```gaql
SELECT
  change_event.change_date_time,
  change_event.user_email,
  change_event.client_type,
  change_event.change_resource_type,
  change_event.resource_change_operation,
  change_event.changed_fields,
  change_event.campaign,
  change_event.old_resource,
  change_event.new_resource
FROM change_event
WHERE change_event.change_date_time >= 'YYYY-MM-DD 00:00:00'
  AND change_event.change_date_time <= 'YYYY-MM-DD 23:59:59'
ORDER BY change_event.change_date_time DESC
LIMIT 200
```

**`LIMIT` is mandatory** and must be 10,000 or less. Without it the query fails with
`changeEventError.LIMIT_NOT_SPECIFIED`. Start at 200 and raise it only if the window truncates.

**What to check:** any row with `client_type` in `('GOOGLE_ADS_AUTOMATED_RULE',
'GOOGLE_ADS_RECOMMENDATIONS')` is an auto-applied change (§7.1, red flag). Bid strategy or budget
changes inside a 14-day learning window (§2.7). Any change by a user email that is not ours, which
is how outside editor access surfaces.

**Coverage limits, and they matter for config verification:**

- `change_event` covers roughly the last 30 days. Older configuration changes are invisible.
- Timestamps are in the **account's** time zone, not UTC and not yours. A window built from local
  dates will miss rows at both ends.
- Not every mutation produces a `change_event` row. Verified on 2026-08-17: an asset group rename
  and a conversion goal level change were both live in the resources while producing no change
  event in the same window. **A config setting is verified by reading the resource, never by the
  absence of a change event.** Change history says what was logged, not what is true.

---

## Query Composition Notes

**Date range options:**

```gaql
DURING LAST_7_DAYS
DURING LAST_14_DAYS
DURING LAST_30_DAYS
DURING THIS_MONTH
DURING LAST_MONTH
BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

There is no `LAST_60_DAYS` or `LAST_90_DAYS` literal. For any window longer than 30 days (or any custom range), use `BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'` with explicit dates.

**Filtering by status:**

- Always add `campaign.status != 'REMOVED'` or `= 'ENABLED'` to exclude historical data clutter
- For keywords: `ad_group_criterion.status = 'ENABLED'` excludes paused and removed keywords
- For ads: `ad_group_ad.status = 'ENABLED'` excludes paused ads

**Result limits:**

- Default API page size is 10,000 rows; large accounts may need pagination
- Add `LIMIT N` to queries when testing or when you only need a sample

**Resources that do NOT support date segmentation:**

- `campaign` (structure queries, section 1): omit date filter for structural queries
- `conversion_action`: omit date filter for the action list; add for metrics queries
- `shared_set` / `shared_criterion`: no date segmentation available
