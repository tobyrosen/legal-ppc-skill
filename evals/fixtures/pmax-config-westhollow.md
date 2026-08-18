# PMax config verification: Westhollow (fixture)

Account: Apex Law (1111111111)
Currency: USD
Account TZ: America/Chicago
Pull: 2026-05-18T02:11:04Z (GAQL v23, read-only)
Capture first: `capture_account_state.py apex-law` -> config CHANGED, 9 new changes, 640 stat-rows, 6 campaigns
Identified PMax: advertising_channel_type = PERFORMANCE_MAX, 1 non-REMOVED row

DATA only. No verdicts.

QUERY NOTES

- change_event first call failed: `changeEventError.LIMIT_NOT_SPECIFIED` ("Change event requests must specify a LIMIT in query and LIMIT should be less than or equal to 10k."). Retried with LIMIT 200. OK, 9 rows.
- campaign_asset sitelink first call failed: campaign.id required in SELECT. Retried with campaign.id. OK, 1 row.
- campaign_asset.policy_summary.approval_status / .review_status: UNRECOGNIZED_FIELD in v23. Campaign-level asset approval reported via campaign_asset.primary_status only.
- campaign.url_expansion_opt_out: not a v23 field (removed). URL expansion read from campaign.asset_automation_settings.

---

## CAMPAIGN

name: PMax - Westhollow Custody Test
id: 24000000001
advertising_channel_type: PERFORMANCE_MAX
advertising_channel_sub_type: (omitted)
experiment_type: BASE
status: ENABLED
serving_status: SERVING
primary_status: LEARNING
primary_status_reasons: BIDDING_STRATEGY_LEARNING
start_date_time: 2026-05-18 02:03:41 America/Chicago
end_date_time: (omitted -- no end date)
start vs pull: created ~7 minutes before this GAQL pull
eligible/serving: serving_status=SERVING AND primary_status=LEARNING; asset group primary_status=PENDING (ASSET_GROUP_UNDER_REVIEW)
tracking_url_template: (omitted)
final_url_suffix: (omitted)
brand_guidelines_enabled: true
brand_guidelines.main_color: #1f3d5c
brand_guidelines.accent_color: #cddcec
brand_guidelines.predefined_font_family: Source Serif 4
business name (campaign_asset BUSINESS_NAME): Apex Law, PLLC
text_guidelines.term_exclusions: cheap, free, quick, pro bono, aid
text_guidelines.messaging_restrictions: "Don't mention competitor names" (RESTRICTION_BASED_EXCLUSION)
text_guidelines.messaging_restrictions: "Don't mention any superlatives" (RESTRICTION_BASED_EXCLUSION)

asset_automation_settings:

- GENERATE_IMAGE_EXTRACTION: OPTED_OUT
- TEXT_ASSET_AUTOMATION: OPTED_OUT
- GENERATE_IMAGE_ENHANCEMENT: OPTED_OUT
- GENERATE_ENHANCED_YOUTUBE_VIDEOS: OPTED_OUT
- FINAL_URL_EXPANSION: OPTED_OUT

---

## BUDGET+BIDDING

campaign_budget.id: 15700001234
campaign_budget.name: PMax - Westhollow Custody Test
campaign_budget.amount_micros: 20000000 -> $20.00 / day
campaign_budget.period: DAILY
campaign_budget.delivery_method: STANDARD
campaign_budget.explicitly_shared: false
campaign_budget.status: ENABLED
campaign_budget.total_amount_micros: (omitted)
bidding_strategy_type: MAXIMIZE_CONVERSIONS
bidding_strategy_system_status: ENABLED
maximize_conversions.target_cpa_micros: (omitted -- no tCPA)
target_cpa.target_cpa_micros: (omitted)

---

## GEO+LANGUAGE

geo_target_type_setting.positive_geo_target_type: PRESENCE_OR_INTEREST
geo_target_type_setting.negative_geo_target_type: PRESENCE

positive LOCATION (1):

- geoTargetConstants/9900001 = Westhollow, Longmoor, United States (City, US, ENABLED)

positive PROXIMITY (1):

- address streetAddress: "Westhollow, Longmoor"
- radius: 5
- radius_units: MILES
- geo_point: lat 41.881832 / lon -93.097702

negative LOCATION: none
negative PROXIMITY: none
LANGUAGE: English (languageConstants/1000, code=en, negative=false, ENABLED)

other campaign_criterion (all ENABLED, negative=false):

- DEVICE DESKTOP
- DEVICE MOBILE
- DEVICE TABLET
- DEVICE CONNECTED_TV

campaign-level KEYWORD negatives: none
CONTENT_LABEL exclusions: none
WEBPAGE (URL-expansion exclusions): none

asset_group_signal (1):

- audience id 300100200 name="Pmax - Custody Test1" status=ENABLED
- search_theme: none

---

## NETWORKS

network_settings.target_google_search: true
network_settings.target_search_network: true
network_settings.target_content_network: true
network_settings.target_partner_search_network: false

---

## ASSET GROUP

asset_group count: 1
id: 67000000001
name: Westhollow 1 - Child Custody
status: ENABLED
ad_strength: POOR
primary_status: PENDING
primary_status_reasons: ASSET_GROUP_UNDER_REVIEW
final_urls: <https://apexlawfirm-example.test/child-custody/>
final_mobile_urls: (omitted)
path1 / path2: (omitted)

asset_group_asset count (status != REMOVED): 21
all 21: status=ENABLED, source=ADVERTISER, primary_status=PENDING, primary_status_reasons=[ASSET_UNDER_REVIEW]
all 21: policy_summary.approval_status=UNKNOWN
all 21: policy_summary.review_status=REVIEW_IN_PROGRESS

counts by field_type:

- HEADLINE: 6
- LONG_HEADLINE: 4
- DESCRIPTION: 4
- MARKETING_IMAGE: 2
- SQUARE_MARKETING_IMAGE: 2
- PORTRAIT_MARKETING_IMAGE: 2
- CALL_TO_ACTION_SELECTION: 1 (CONTACT_US)
- YOUTUBE_VIDEO / VIDEO: 0

campaign-level assets (brand guidelines + sitelink), all ENABLED / PENDING / ASSET_UNDER_REVIEW:

- LOGO asset 500100010 name="Suggested logo #1" type=IMAGE
- BUSINESS_NAME asset 500100011 text="Apex Law, PLLC"
- SITELINK asset 500100012 linkText="Client Resources" final_urls=<https://apexlawfirm-example.test/resources/>

---

## CONVERSION GOALS

conversion_goal_campaign_config.goal_config_level: CUSTOMER
custom_conversion_goal on this campaign: none
campaign_conversion_goal rows: 12 (identical biddable map to customer_conversion_goal)

biddable=true (campaign inherits account default):

- DEFAULT / WEBSITE
- PHONE_CALL_LEAD / CALL_FROM_ADS
- SUBMIT_LEAD_FORM / WEBSITE
- CONTACT / WEBSITE

biddable field omitted (not true) on campaign_conversion_goal:

- PAGE_VIEW / WEBSITE
- PAGE_VIEW / GOOGLE_HOSTED
- CONTACT / CALL_FROM_ADS
- CONTACT / GOOGLE_HOSTED
- CONVERTED_LEAD / WEBSITE
- ENGAGEMENT / GOOGLE_HOSTED
- ENGAGEMENT / YOUTUBE_HOSTED
- YOUTUBE_FOLLOW_ON_VIEWS / YOUTUBE_HOSTED

account conversion_action (status != REMOVED): 18
ENABLED: 15
ENABLED + include_in_conversions_metric=true (PRIMARY): 8
ENABLED + include_in_conversions_metric=false (SECONDARY): 7

PRIMARY actions this campaign can optimize toward (goal_config_level=CUSTOMER, so account primaries in biddable categories):

DEFAULT / WEBSITE (4 PRIMARY):

- Contact form submission (WEBPAGE, ONE_PER_CLICK)
- Consultation request form (WEBPAGE, ONE_PER_CLICK)
- CallRail tracked call (WEBSITE_CALL, MANY_PER_CLICK)
- Phone Call (UPLOAD_CLICKS, MANY_PER_CLICK)

SUBMIT_LEAD_FORM / WEBSITE (2 PRIMARY):

- Intake form submit (WEBPAGE, ONE_PER_CLICK)
- Callback request form (WEBPAGE, ONE_PER_CLICK)

CONTACT / WEBSITE (1 PRIMARY):

- Google Ads Leads (UPLOAD_CLICKS, MANY_PER_CLICK)

PHONE_CALL_LEAD / CALL_FROM_ADS (1 PRIMARY):

- Calls from ads (AD_CALL, MANY_PER_CLICK)

ENABLED SECONDARY (include_in_conversions_metric=false):

- Newsletter signup | ENGAGEMENT / GOOGLE_HOSTED | primary_for_goal=false
- Resource guide download | PAGE_VIEW / WEBSITE | primary_for_goal=false
- Blog page view - custody | PAGE_VIEW / WEBSITE | primary_for_goal=false
- Click to call (unverified) | CONTACT / GOOGLE_HOSTED | primary_for_goal=false
- YouTube channel subscriptions | ENGAGEMENT / YOUTUBE_HOSTED | primary_for_goal=false
- YouTube follow-on views | YOUTUBE_FOLLOW_ON_VIEWS / YOUTUBE_HOSTED | primary_for_goal=false
- Directions requested | GET_DIRECTIONS / GOOGLE_HOSTED | primary_for_goal=false

---

## NEGATIVES/SHARED SETS

campaign_shared_set attached to this campaign: 0
account shared negative lists (exist, not attached here):

- "Apex Law shared negatives" id 1500002000, 84 members, reference_count 3

---

## CHANGE EVENTS

query: FROM change_event WHERE change_date_time >= '2026-05-17 02:00:00' AND change_date_time <= '2026-05-19 02:00:00' ORDER BY change_date_time DESC LIMIT 200
returned: 9 rows, resource types CAMPAIGN, CAMPAIGN_ASSET, CAMPAIGN_BUDGET, CAMPAIGN_CRITERION, ASSET

CAMPAIGN CREATE campaigns/24000000001 -- user <operator@example.com> -- 2026-05-18 02:03:41 -- client_type GOOGLE_ADS_WEB_CLIENT -- fields include name, status, brandGuidelines, assetAutomationSettings, geoTargetTypeSetting, networkSettings, textGuidelines, campaignBudget, advertisingChannelType

CAMPAIGN_ASSET CREATE campaigns/24000000001~500100012~SITELINK -- user <operator@example.com> -- 2026-05-18 02:03:41 -- client_type GOOGLE_ADS_WEB_CLIENT

CAMPAIGN_ASSET CREATE campaigns/24000000001~500100010~LOGO -- user <operator@example.com> -- 2026-05-18 02:03:41 -- client_type GOOGLE_ADS_WEB_CLIENT

CAMPAIGN_CRITERION CREATE campaigns/24000000001~1000 -- user <operator@example.com> -- 2026-05-18 02:03:41 -- client_type GOOGLE_ADS_WEB_CLIENT

CAMPAIGN_CRITERION CREATE campaigns/24000000001~9900001 -- user <operator@example.com> -- 2026-05-18 02:03:41 -- client_type GOOGLE_ADS_WEB_CLIENT

CAMPAIGN_CRITERION CREATE campaigns/24000000001~24000000002 -- user <operator@example.com> -- 2026-05-18 02:03:41 -- client_type GOOGLE_ADS_WEB_CLIENT -- fields include proximity.address.streetAddress, proximity.radius, proximity.radiusUnits

CAMPAIGN_BUDGET UPDATE campaign_budgets/15700001234 -- user (system) -- 2026-05-16 09:14:02 -- client_type GOOGLE_ADS_RECOMMENDATIONS -- field amount_micros: 15000000 -> 20000000 ($15.00/day -> $20.00/day)

ASSET CREATE assets/500100010 -- user <operator@example.com> -- 2026-05-17 21:55:10 -- client_type GOOGLE_ADS_WEB_CLIENT

ASSET CREATE assets/500100011 -- user <operator@example.com> -- 2026-05-17 21:55:44 -- client_type GOOGLE_ADS_WEB_CLIENT

auto-applied rows in window (client_type in GOOGLE_ADS_AUTOMATED_RULE, GOOGLE_ADS_RECOMMENDATIONS): 1 (the CAMPAIGN_BUDGET UPDATE above)

---

## QUERY NOTES

- Pull is read-only; no changes made by this check.
- campaign.geo_target_type_setting and campaign.network_settings both read cleanly on PMax in v23; no blind spot on this account.
- account has no other PMax rows (0 REMOVED or paused PMax campaigns found in the same pull).
