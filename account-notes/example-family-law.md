# Account Notes — example-family-law (SYNTHETIC EXAMPLE)

This file is a fully synthetic template example for the Accounts table in SKILL.md. No real firm, account ID, or performance data appears here. Copy this structure for each real account.

## Config overrides

Deliberate departures from `references/agency-defaults.md`. A config check reports a setting listed
here as an override match, never as a flag. One line per overridden setting: the field path, the
account's value, the baseline value it departs from, the scope, who approved it and when, and the
journal entry id. Rendered from `rule` entries carrying the `config-override` tag; never hand-written.
See `NOTATION.md` §8 for the mechanism and `journal/templates.md` for the entry shape.

- `campaign.geo_target_type_setting.positive_geo_target_type`: account `PRESENCE` (baseline `PRESENCE_OR_INTEREST`), scope: Search - Family Law, approved by operator (ref-0001) on YYYY-MM-DD, entry `example-family-law-YYYYMMDD-NN`
  Presence-only on this one campaign. Interest traffic was measured across a full quarter and produced clicks with no intake contact. Ends if the firm opens a second office or the campaign geography widens.
- `campaign_budget.explicitly_shared`: account `true` (baseline `false`), scope: the two custody campaigns, approved by operator (ref-0002) on YYYY-MM-DD, entry `example-family-law-YYYYMMDD-NN`
  The two custody campaigns are deliberately run as one line item against a single pooled budget. Per-campaign budget-lost impression share is therefore expected and is not read as a campaign-level constraint.

_None recorded means every setting is expected to match the baseline, and any departure is a
deviation._

## Pending Actions

- [WATCH from YYYY-MM-DD] One line per open item: what was observed, what decision or verification is due, and when the next read is.
- [DECIDED YYYY-MM-DD] Record operator decisions with their trigger (message/date), what changed, and what the next check should verify.

## Resolved

- [YYYY-MM-DD] Closed items move here with the closing evidence, so the pending list stays short.

## Context

- Firm economics (source for targets — see "Target Setting" in SKILL.md): average signed-case value, lead-to-signed rate, acceptable cost per signed case.
- Tracking setup notes: which conversion actions are primary, any lead-quality filtering between the CRM/call tracking and Google Ads.
- Market priors: practice area, geography, consideration-window notes.
