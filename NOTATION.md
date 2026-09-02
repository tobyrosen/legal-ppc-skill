# Google Ads Notes & Notation Standard (v1.0, 2026-08-10)

The managed-account memory system for RA client ad accounts. Trading-journal model:
every meaningful event is one small machine-readable entry; every decision carries an
expectation and a review date; outcomes are scored against expectations later. Human-readable
notes are RENDERED from the journal, never hand-written.

Notation standard for the journal. Owned by the methodology maintainer; written during each
recurring check.

---

## 1. The one rule that matters

**The journal is the only write surface.** `$PPC_JOURNAL_ROOT/journal/<slug>.jsonl`:
append-only JSONL, one entry per line. Account-notes and session-log markdown files are
generated views. Nobody hand-edits a rendered file; a hand edit is drift and will be
overwritten by the next render.

## 2. Files

| Path                                                                | What                                                                                  | Written by                          |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------- |
| `$PPC_JOURNAL_ROOT/journal/<slug>.jsonl`                            | The journal (system of record)                                                        | `journal.py append` during checks   |
| `$PPC_JOURNAL_ROOT/journal/vocab.json`                              | Controlled tag vocabulary                                                             | methodology maintainer (deliberate) |
| `$PPC_JOURNAL_ROOT/notes/<slug>.md`                                 | Rendered account notes (open rules, pending by review date, recent outcomes, context) | `journal.py render`                 |
| `$PPC_JOURNAL_ROOT/session-logs/<date>-<slug>.md`                   | Rendered per-check log                                                                | `journal.py render`                 |
| skill `journal/` dir (schema.json, vocab schema, journal.py, tests) | Method + tooling                                                                      | methodology maintainer              |

Account slugs match the operator's existing capture set: one lower-case, hyphenated firm slug per
account, for example `example-family-law`. The roster itself is private and lives outside this repo.

**Former clients are structurally excluded: no journal, no backfill, never**, regardless of
retained historical data. Which accounts those are is part of the private roster, not this file.

## 3. Entry schema (normative; enforced by `schema.json` + validator)

One JSON object per line. Required: `id`, `ts`, `account`, `platform`, `type`, `status`, `source`, `session`.

- `id`: `<slug>-<YYYYMMDD>-<NN>` (per-account, per-day sequence). Unique per file.
- `ts`: ISO 8601 with offset (`2026-08-10T09:15:00+07:00`).
- `account`: account slug.
- `platform`: `google | call-tracking | analytics | crm | site | admin | other`. Journals written
  under schema v1 carry `meta`, `callrail`, `ga4` or `hubspot`; `journal.py migrate` moves them
  forward. See §3a.
- `type`: the event kind:
  - `obs`: data point / observation, no action implied
  - `flag`: anomaly raised for a decision
  - `decision`: a call made (incl. "let it run"); **requires `expect`**
  - `change`: a change actually applied in an account; **requires `expect`**
  - `outcome`: scoring of an earlier decision/change; **requires `re` + `verdict`**
  - `rule`: standing constraint ("do not re-flag this as a tracking break", "do not re-mention outages"); also carries **config overrides**, see §8
  - `context`: background prose (vendor situations, tracker backstories)
- `status`: `open | closed | superseded`. `rule` stays `open` until superseded. `obs`/`context` default `closed`. A `decision`/`change` stays `open` until its `outcome` entry closes it.
- `scope`: optional `{level, ids[], names[]}`; `level` ∈ `account | campaign | ad_group | keyword | ad | budget | tracking | conversion | landing_page | audience`.
- `tags`: array, each MUST exist in `vocab.json` (validator-enforced). Growing the vocabulary = edit vocab.json deliberately, not inline.
- `body`: free text. One-liner for obs; as long as needed for context. Prose is welcome HERE, not in new fields.
- `metrics`: optional `{window: {from, to}, provisional: bool, kv: {spend, conv, cpl, is_budget_lost, is_rank_lost, ...}}`. Native account currency, numbers only.
- `expect`: on decision/change: `{statement, review_by}` (date). "Let it sit" still gets a review_by (the next check).
- `re`: array of entry ids this entry refers to (outcome → its decision; superseding entry → superseded).
- `verdict`: on outcome: `met | not_met | mixed | unclear`.
- `config_override`: on a `rule` only: `{setting, account_value, agency_default, applies_to?}`. Records a deliberate departure from `references/agency-defaults.md`. See §8.
- `source`: `{actor, ref}`. `actor` is the party the entry came from, recorded as a free-form non-empty
  string rather than a fixed list. Recommended values, offered as examples and not as an enum:
  `operator`, `agent`, `automation`. `ref` is an optional external reference id, or null. A ref is a
  generic identifier: letters, digits, dot, colon, underscore and hyphen, starting with a letter or
  digit. Decisions belong to the operator unless recorded otherwise.
- `session`: check id, `YYYY-MM-DD-<slug>` (matches the rendered session-log filename).
- `migrated`: `true` only on backfilled entries parsed from the legacy md ledgers.

## 3a. Schema version and migration

`schema.json` is **v2**. The v1 `platform` values (`meta`, `callrail`, `ga4`, `hubspot`) are no
longer accepted, and they are never coming back to the enum.

`journal.py migrate <slug>` (or `--all`) carries an old journal forward in place, and it moves
only the four known v1 values: `meta` to `other`, `callrail` to `call-tracking`, `ga4` to
`analytics`, `hubspot` to `crm`. Any other value outside the enum is left exactly as it is. An
unrecognized platform is a mistake to look at, not something to rewrite silently, so validate
keeps reporting it as an ordinary enum error. Migrate copies the journal to `<slug>.jsonl.bak`
before writing, and it does nothing at all to a journal that has no legacy values.

Because append, render and validate all read the whole file, one v1 record would otherwise block
every operation on that account. So `journal.py validate` does not fail with a bare enum error on
the four known values: it reports `legacy platform values found: run journal.py migrate` with a
count per value, and the fix is one command. That hint is never offered for a value migrate
cannot handle, which fails on the enum like any other bad field.

## 4. The outcome loop (why this beats prose notes)

Every `decision`/`change` names what we expect and when to look. `journal.py due <slug>`
lists open entries with `review_by <= today`, a mandatory step at the top of every PPC
check. The check then appends `outcome` entries with honest verdicts. Over time
`journal.py` can answer: budget raises at budget-lost >50%, how often did CPL hold?
That is the tuning database this standard exists to build.

## 5. Check workflow (operator, every check)

1. `journal.py due <slug>`: reviews due today; carry into the check agenda.
2. Run the check per SKILL.md (unchanged).
3. Append entries as events happen (`obs`/`flag`/`decision`/`change`/`outcome`).
4. `journal.py render <slug>`: regenerate notes + session log. `journal.py validate` must pass.
5. Off-runbook surprises still escalate to the operator.

## 6. Source of truth / copy sync (closes the two-copy problem)

- **Data lives in exactly one place:** `$PPC_JOURNAL_ROOT/` (journal + rendered views). Skill copies carry NO account data.
- **Canonical method copy:** one physical copy of this skill, with the runtime skill directory a symlink to it. If the symlink is ever replaced by a real copy, restore the symlink rather than maintaining two files.
- `vocab.json` exists in two places by design: the runtime copy at `$PPC_JOURNAL_ROOT/journal/vocab.json` is what `journal.py` validates against (bundled skill copy is the fallback). When editing the vocabulary, edit the bundled canonical copy and sync to the runtime copy. Keep them byte-identical.
- Legacy `account-notes/` + `session-logs/` under the skill copies are frozen after backfill: contents migrated into the journals, each dir left with a `POINTER.md` naming the new locations. Legacy files are kept (history), never updated again.

## 7. Tag vocabulary (v1 seed, grows via vocab.json)

`watch`, `monitor`, `carried`, `known-issue`, `budget`, `negatives`, `impression-share`,
`cpl-direction`, `tracking`, `conversion-config`, `lead-quality`, `outage`, `vendor`,
`launch`, `expansion`, `remarketing`, `pre-reactivation`, `client-comms`, `billing`,
`config-override`.
Each vocab.json entry: `{tag, meaning, when_to_use}`.

---

## 8. Config overrides (per-account departures from the agency baseline)

`references/agency-defaults.md` is the agency-wide configuration baseline: what every account is
expected to be set to, and why. A config check compares the live account against that file and only
a **deviation from it** may become a flag. Accounts that legitimately differ record the difference
here, once, so the check reports it as an override match forever after instead of re-raising it
every session.

This closes the false-flag hole: on 2026-08-17 a config verification reported a positive geo target
type of `PRESENCE_OR_INTEREST` as a problem when it is the house standard. The check had no
baseline to compare against and no place to look up an account's deliberate settings.

**The entry.** A `rule` carrying the `config-override` tag and the `config_override` object:

| Field                            | Holds                                                                      | Source                 |
| -------------------------------- | -------------------------------------------------------------------------- | ---------------------- |
| `config_override.setting`        | the GAQL field path, exactly as it appears in agency-defaults              | required               |
| `config_override.account_value`  | what this account is set to                                                | required               |
| `config_override.agency_default` | the baseline value it departs from                                         | required               |
| `config_override.applies_to`     | campaign or campaign type the override is scoped to; omit for account-wide | optional               |
| `body`                           | why, and what would end the override                                       | required in practice   |
| `source.actor` / `source.ref`    | who approved it and the message reference                                  | required by the schema |
| `ts`                             | when it was approved                                                       | assigned on append     |

`status` is `open` while the override stands, `superseded` once retired. The schema rejects a
`config_override` on any type other than `rule`, and rejects `status: closed`. Copy-paste shape and
a worked example: `journal/templates.md`.

**Reading them.** `journal.py render` groups every open config override into a **Config overrides**
section in the rendered account notes, above Standing Rules, one line per setting. That section is
what a check reads before classifying live config, and it is the only place an account's deliberate
deviations are listed.

**Retiring one.** Append a superseding entry naming the old id in `re`. The render treats a
referenced entry as resolved and drops it. Never edit or delete the original line.

**Not for legacy states.** An override records a decision we stand behind. A deviation we intend to
clean up is a `decision` with a `review_by` date, so it returns through the due queue instead of
going quiet under an override that was never really a choice.

**Public version.** Real accounts' overrides live in the private journal. The public skill ships one
fictional example, in `account-notes/example-family-law.md`.
