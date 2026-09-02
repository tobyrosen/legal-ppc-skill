# Legal PPC skill: Google Ads Search and Performance Max for law firms

![Version](https://img.shields.io/badge/version-v4.1-blue)
![Status](https://img.shields.io/badge/production-active-success)

An encoded set of tactics for improving Google Ads Search and Performance Max campaigns at family law, immigration law, and elder law firms. The skill pulls live account data, runs mandatory pre-flights, and presents what the data shows plus the standard move for a recognized pattern. It does not issue verdicts. Pause, scale, and go/no-go calls stay with the operator.

---

## What it does

Load it in Claude Code alongside a Google Ads MCP. Give it a brief, or say the account feels off. It runs the diagnostic in order, with the safeguards a general model skips.

**Session flow:**

1. Establish the brief, including the firm's economics, and name the diagnosis tree that applies.
2. Run five mandatory pre-flights: macro context (PF-0), conversion tracking (PF-1), structural red flags (PF-2), change history (PF-3), config ground truth (PF-4).
3. Pull live data through the GAQL library and flag candidates.
4. Match recognized patterns against the playbook library.
5. Produce a prioritized findings list as data and standard moves, never as verdicts.

**The two structural pieces:**

- **Config ground truth.** A configuration finding is a departure from a stated baseline (`references/agency-defaults.md`), not from Google's defaults and not from nothing. Matching settings are silent. Recorded overrides are one summary line. Only an unrecorded departure becomes a flag.
- **Optimization playbooks.** 40 pattern-to-standard-move entries in `references/playbooks.md`. Each carries a trigger, the standard move, the do-not-move conditions, the verification window, and an evidence tier. The agent never executes a move.

**Evidence tiers.** Every playbook carries one of `validated in practice`, `partially validated`, `textbook only`, or `unconfirmed`. Unconfirmed means general practice not yet confirmed by the operator: a candidate, never a house tactic. As of the 2026-09 refresh and the evidence-verdict pass that followed it: 40 playbooks, 13 validated, 12 partially validated, 15 textbook only. 14 `unconfirmed` markers remain across the reference files, 11 of them in the playbook library, all on windows and thresholds nobody has yet run to completion.

**What it gets right that a general model does not:**

| Failure mode                       | What a general model does                 | What this skill does                                                                      |
| ---------------------------------- | ----------------------------------------- | ----------------------------------------------------------------------------------------- |
| Negative keywords in GAQL results  | Flags them as active optimization targets | Filters `negative = FALSE`, required in every keyword query                               |
| Paused ad group search terms       | Treats them as active waste               | Requires `ad_group.status = ENABLED`; `status = NONE` terms are explicitly excluded       |
| Cheap CPC on a legal term          | Explains it as low-intent traffic         | Routes to data contamination first, then to a Search versus PMax split                    |
| High rank-lost impression share    | Recommends raising budget                 | Separates rank-lost from budget-lost; budget does not fix a rank problem                  |
| tCPA above target                  | Recommends lowering tCPA to tighten up    | Applies the direction rule: lowering when above target restricts volume, not cost         |
| CPA from a handful of conversions  | Treats it as a reliable signal            | Flags the reliability floor; below it, CPA is noise                                       |
| Search term waste estimates        | Reports face-value numbers                | Reports the measured figure and never extrapolates or scales it                           |
| Config that matches house standard | Flags it against Google's defaults        | Classifies against the baseline; a MATCH is silent                                        |
| Ebook and guide downloads          | Demotes them as soft conversions          | Treats them as PRIMARY conversions by standing operator ruling, never demotion candidates |

---

## Public and operator modes

The public skill ships the methodology, query library, config baseline, and playbooks, with fictional example notes only. The operator version additionally reads the per-account journal and rendered notes; per-account config overrides live in that journal, not in this repo.

Operator mode configuration: set `PPC_JOURNAL_ROOT` to the directory holding the journal and rendered views, and `PPC_JOURNAL_TZ` to your IANA timezone. With no `PPC_JOURNAL_ROOT` set, the data root is this repo and journals are written to `./journal`. Anyone holding real account data should point `PPC_JOURNAL_ROOT` at a private directory outside this repo. Entry ids and "today" are computed in that zone.

---

## Adapting the config baseline

`references/agency-defaults.md` is one agency's baseline. To use this skill elsewhere, replace each STANDARD value with yours and keep the MATCH / OVERRIDE-MATCH / DEVIATION classification. Entries marked PROPOSED stay at config-item severity until you confirm them. Per-account exceptions belong in your own notes or journal as overrides, not in the baseline file.

---

## Evals

The skill ships an adversarial eval suite. Each case runs the same prompt with and without the skill loaded, then scores against specific behavioral assertions.

**Most recent round (2026-08-18, round 2):** Sonnet scored 36 of 37 assertions with the skill loaded; Opus scored 5 of 5. Earlier suites are retained for regression coverage but their headline delta figure has been withdrawn pending a re-run on the v4.1 content.

**How to run them.** Suites are JSON assertion files under `evals/`: `evals.json`, `evals_v2.json`, `evals_v3.json`, `evals_v4.json`, `evals_v5.json`, and `trigger_evals.json`. Each case is a prompt plus an `assertions` array. Run the prompt with and without the skill, then score against the assertions.

- `evals_v4.json` covers config ground truth and the optimization playbooks.
- `evals_v5.json` is the 2026-09 refresh suite: the retired PB-15 cases are gone, Display cases are re-scoped to PMax or cut, and it adds cases for PB-40, PB-41, the PB-16 conversion-over-intent ruling, the PB-26 blended-CPA ruling, and PB-32 cap tracking.
- `trigger_evals.json` tests skill-activation reliability, separate from output quality.

Fixtures for the fictional accounts live in `evals/fixtures/`. There is no in-repo eval runner.

---

## Requirements

- [Claude Code](https://claude.ai/code) with skill support
- A Google Ads MCP server exposing `run_gaql` or `execute_gaql_query`
- The `Agent` tool for multi-campaign parallel search term reviews. Without it the skill runs sequentially.

### Recommended MCP

Tested with **[cohnen/mcp-google-ads](https://github.com/cohnen/mcp-google-ads)**. Any GAQL-capable MCP works; update the execution note in `SKILL.md` for a different implementation.

---

## Installation

```bash
git clone https://github.com/tobyrosen/legal-ppc-skill
```

1. Set up your Google Ads MCP.
2. Confirm your account roster outside this skill. The skill will not run a multi-account pull without one.
3. Public mode: `account-notes/example-family-law.md` shows the notes and override shape. Do not add real account files to this repo. Operator mode: the journal and rendered notes live outside this skill.
4. Load the skill in Claude Code and confirm API access.

---

## File structure

```text
legal-ppc-skill/
├── SKILL.md                           # Main skill file, load this
├── NOTATION.md                        # Journal notation standard (operator mode)
├── pyrightconfig.json                 # Type-check path for journal tests
├── account-notes/
│   └── example-family-law.md          # Fictional example notes and override shape
├── references/
│   ├── google-ads-knowledge-base.md   # The legal-PPC lens
│   ├── agency-defaults.md             # Configuration baseline for PF-4
│   ├── playbooks.md                   # The optimization playbook library
│   ├── diagnosis-trees.md             # Symptom-to-action routing
│   ├── gaql-query-library.md          # Pre-built GAQL queries by diagnostic task
│   ├── negative-keyword-library.md    # Candidate negative patterns by category
│   ├── creative-audit.md              # Search asset and PMax asset audit procedure
│   └── session-management.md          # Session record template (operator mode)
├── journal/                           # Journal CLI, schema, and tests (operator mode)
└── evals/
    ├── evals.json                     # Eval suite v1
    ├── evals_v2.json                  # Eval suite v2
    ├── evals_v3.json                  # Eval suite v3
    ├── evals_v4.json                  # Config ground truth and playbooks
    ├── evals_v5.json                  # 2026-09 refresh suite
    ├── trigger_evals.json             # Skill-activation trigger evals
    └── fixtures/                      # Fictional account notes and config pulls
```

---

## Practice areas

Search intent guidance, negative-keyword candidates, and diagnostic priors for:

- Family law (divorce, child custody, child support)
- Elder law (estate planning, probate, estate and trust disputes, elder abuse)
- Immigration law

Immigration is in scope but carries no vertical-specific tactics yet: no encoded doctrine for case-type segmentation, multilingual intent, status-specific queries, or immigration-specific negatives. Immigration accounts run on the general Search and PMax tactics until that gap is closed.

No other practice area is in scope, and no other advertising platform is.

---

## Known limitations

**Search-term negative precision.** The skill reports what the search-term pull returns and never estimates, extrapolates, or scales a figure to stand for spend it did not see. Negatives come from the account's own search terms, checked against the operator's not-waste list and each term's conversion record, and a term category is never blocked on search-term data alone.

**Conversion tracking configuration is read-only through GAQL.** There is no structured API object for conversion action settings. The skill reconstructs them from `conversion_action` queries. For complex setups, UI verification is faster.

**Asset-level creative performance is thin.** Per-asset image performance is only partially exposed by the API, and responsive search ad headline and description scores are not pulled. The skill falls back to an ad-group or campaign proxy and labels it as one.

**Immigration doctrine is absent.** See the practice areas note above.

**Some windows and thresholds are unconfirmed.** After the 2026-09-02 verdict pass, the claims that survive unmarked are either operator rulings or measured outcomes. What still carries an `(unconfirmed)` marker or a `PROPOSED` tag is a window or a threshold nobody has run to completion. Treat those as candidates and confirm them against your own outcomes.

---

## License

MIT
