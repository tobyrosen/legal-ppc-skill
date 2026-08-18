# Google Ads journal entry templates

`journal.py append <slug>` supplies `account`, `id`, and `ts`. During a check, fill the remaining fields and pipe one JSON object to stdin. Use only tags defined in `vocab.json`.

Blocks below are pretty-printed for reading and pipe as-is; the appended journal line is written compact regardless of how the input was formatted.

## Observation

```json
{
  "platform": "google",
  "type": "obs",
  "status": "closed",
  "scope": { "level": "account", "ids": [], "names": [] },
  "tags": ["cpl-direction"],
  "body": "<one factual data point>",
  "source": { "actor": "ra-clients", "ref": null },
  "session": "YYYY-MM-DD-<slug>"
}
```

## Flag

```json
{
  "platform": "google",
  "type": "flag",
  "status": "open",
  "scope": {
    "level": "campaign",
    "ids": ["<campaign-id>"],
    "names": ["<campaign-name>"]
  },
  "tags": ["watch"],
  "body": "<anomaly, consequence, and what needs a decision>",
  "source": { "actor": "ra-clients", "ref": null },
  "session": "YYYY-MM-DD-<slug>"
}
```

## Decision

```json
{
  "platform": "google",
  "type": "decision",
  "status": "open",
  "scope": { "level": "account", "ids": [], "names": [] },
  "tags": ["budget"],
  "body": "<the call made, including let-it-run decisions>",
  "expect": {
    "statement": "<observable result expected>",
    "review_by": "YYYY-MM-DD"
  },
  "source": { "actor": "toby", "ref": "tg-NNNN" },
  "session": "YYYY-MM-DD-<slug>"
}
```

## Change

```json
{
  "platform": "google",
  "type": "change",
  "status": "open",
  "scope": {
    "level": "budget",
    "ids": ["<campaign-id>"],
    "names": ["<campaign-name>"]
  },
  "tags": ["budget"],
  "body": "<exact change applied>",
  "expect": {
    "statement": "<observable result expected>",
    "review_by": "YYYY-MM-DD"
  },
  "source": { "actor": "toby", "ref": "tg-NNNN" },
  "session": "YYYY-MM-DD-<slug>"
}
```

## Outcome

```json
{
  "platform": "google",
  "type": "outcome",
  "status": "closed",
  "tags": ["budget"],
  "body": "<what happened versus the expectation>",
  "re": ["<decision-or-change-id>"],
  "verdict": "met",
  "source": { "actor": "ra-clients", "ref": null },
  "session": "YYYY-MM-DD-<slug>"
}
```

## Rule

```json
{
  "platform": "admin",
  "type": "rule",
  "status": "open",
  "scope": { "level": "account", "ids": [], "names": [] },
  "tags": ["known-issue"],
  "body": "<standing constraint in direct language>",
  "source": { "actor": "toby", "ref": "tg-NNNN" },
  "session": "YYYY-MM-DD-<slug>"
}
```

## Config override

A `rule` carrying the `config-override` tag and the `config_override` object. Records that an
account deliberately departs from `references/agency-defaults.md`, so the config check reports the
setting as an override match instead of flagging it. `source.actor` is who approved it and `ts` is
when, so neither is repeated in the body.

`setting` is the GAQL field path from agency-defaults. `applies_to` is optional and scopes the
override to one campaign type or campaign; omit it and the override applies account-wide.

```json
{
  "platform": "google",
  "type": "rule",
  "status": "open",
  "scope": { "level": "campaign", "ids": [], "names": ["<campaign-name>"] },
  "tags": ["config-override"],
  "config_override": {
    "setting": "campaign.network_settings.target_partner_search_network",
    "account_value": "true",
    "agency_default": "false",
    "applies_to": "<campaign-name>"
  },
  "body": "<why this account runs the non-standard value, and what would end the override>",
  "source": { "actor": "toby", "ref": "tg-NNNN" },
  "session": "YYYY-MM-DD-<slug>"
}
```

Worked example, fully fictional:

```json
{
  "platform": "google",
  "type": "rule",
  "status": "open",
  "scope": { "level": "campaign", "ids": [], "names": ["Search - Family Law"] },
  "tags": ["config-override", "conversion-config"],
  "config_override": {
    "setting": "campaign.geo_target_type_setting.positive_geo_target_type",
    "account_value": "PRESENCE",
    "agency_default": "PRESENCE_OR_INTEREST",
    "applies_to": "Search - Family Law"
  },
  "body": "Presence-only on this campaign only. Interest traffic was measured across a full quarter and produced clicks with no intake contact. Ends if the firm opens a second office or the campaign geo widens.",
  "source": { "actor": "toby", "ref": "tg-1234" },
  "session": "2026-07-01-example-family-law"
}
```

Retiring an override: append a superseding entry that names the old id in `re`. The render treats a
referenced entry as resolved and drops it from the standing set automatically. Never edit or delete
the original line.

## Context

```json
{
  "platform": "other",
  "type": "context",
  "status": "open",
  "scope": { "level": "account", "ids": [], "names": [] },
  "tags": [],
  "body": "<durable backstory needed to interpret future checks>",
  "source": { "actor": "ra-clients", "ref": null },
  "session": "YYYY-MM-DD-<slug>"
}
```
