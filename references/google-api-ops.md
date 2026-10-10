# Google Ads API operational checks

Lifted from Google's public `skills/ads/google-ads-api-account-diagnostics/SKILL.md` (the quickstart skill covers credentials and versioning; nothing is lifted from it here). Each query is copied verbatim from that file and marked with its source path; the reading rules are ours. Run every query through whatever tool executes GAQL for the account: this file assumes no particular tool. The SKILL.md Data rules govern every number these queries return (units, direction, aligned windows, provisional labeling, campaign path).

## Offline conversion upload health (conversion-tracking check)

**What it tells you:** whether offline conversion uploads are configured for the account and, per conversion action, how many uploaded events succeeded out of how many were sent.

Source: `skills/ads/google-ads-api-account-diagnostics/SKILL.md`, copied verbatim.

```sql
SELECT
  offline_conversion_upload_conversion_action_summary.conversion_action_name,
  offline_conversion_upload_conversion_action_summary.successful_event_count,
  offline_conversion_upload_conversion_action_summary.total_event_count,
  offline_conversion_upload_conversion_action_summary.status
FROM offline_conversion_upload_conversion_action_summary
```

**Thresholds (Google's):** the success rate is `successful_event_count` against `total_event_count`; the `status` field is where failures get diagnosed. An empty result means no offline uploads are configured or active for the account: state that as the finding and proceed; do not retry the query and do not write custom scripts to force data.

**Our reading rule:** run this check before explaining any conversion dip on an account whose conversions depend on offline imports. A low or failed upload count is a tracking failure, not a demand failure: report the counts and the gap, name the affected conversion actions, and return the fix to the operator. The check separates counts still inside the 72-hour lag pipeline from counts that never arrived.

_Provenance note:_ Google's skill ships this check at the conversion-action level only. Its files contain no query against the client-level `offline_conversion_upload_client_summary` (which would add last-upload time and alert state), so the verbatim-copy rule keeps that resource out of this file.

## Multi-account discovery preamble

**Rule:** when a customer ID is not supplied, first enumerate the customers the credentials can reach using the accessible-customers listing of your GAQL execution tool (an API method, not a GAQL query), then run this query under those accounts. It gates every query that follows.

Source: `skills/ads/google-ads-api-account-diagnostics/SKILL.md`, copied verbatim.

```sql
SELECT
  customer_client.id,
  customer_client.descriptive_name,
  customer_client.status,
  customer_client.manager
FROM customer_client
WHERE customer_client.status = 'ENABLED' AND customer_client.manager = FALSE
```

**Reading rule:** only the enabled, non-manager client IDs this query returns are valid targets for subsequent queries; never query manager or deactivated accounts, they return API errors.

## First-pass segmentation templates

### Conversion metrics by date, device, and conversion action

Source: `skills/ads/google-ads-api-account-diagnostics/SKILL.md`, copied verbatim.

```sql
SELECT
  campaign.name,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_micros,
  segments.date,
  segments.device,
  segments.conversion_action
FROM campaign
WHERE segments.date >= '{start_date}' AND segments.date <= '{end_date}'
```

**Reading rule:** a conversion loss confined to one device (mobile vs desktop) or one `conversion_action` localizes the drop to that slice; run both comparison sides over the same `{start_date}` to `{end_date}` window, divide `cost_micros` by 1,000,000, and label any window inside the conversion lag provisional.

### Impression share split: rank lost vs budget lost

Source: `skills/ads/google-ads-api-account-diagnostics/SKILL.md`, copied verbatim.

```sql
SELECT
  campaign.name,
  metrics.search_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.search_budget_lost_impression_share
FROM campaign
WHERE segments.date >= '{start_date}' AND segments.date <= '{end_date}'
```

**Reading rule:** `search_budget_lost_impression_share` quantifies impressions lost to limited budget and `search_rank_lost_impression_share` quantifies impressions lost to low ad rank (bid or quality); convert the decimals per the Data rules unit bullet, report the split as data on where the lost impressions sit, and return the budget-or-bid decision to the operator.

Lifted 2026-09-04 (BOSS, Toby tg-19491 #2) from the google/skills mining; source report `~/Cowork/Cowork-Assets/eval-outputs/starred-repos-2026-09-04/out-google-skills-mine.md`. Nothing merged; Google's skill is MCP-bound and ours stays tool-agnostic.
