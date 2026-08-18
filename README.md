# Legal PPC Skill — Google Ads Analysis for Law Firms

![Version](https://img.shields.io/badge/version-v3.6-blue)
![Evals](https://img.shields.io/badge/eval%20delta-%2B86pp-brightgreen)
![Status](https://img.shields.io/badge/production-active-success)

Data-first Google Ads analysis for legal PPC. The skill pulls live account data, runs mandatory pre-flights, and presents what the data shows plus the standard move for a recognized pattern. It does not issue verdicts. Pause, scale, and go/no-go calls stay with the operator.

---

## What it does

Load it in Claude Code with a Google Ads MCP. Give it a brief, or say the account feels off. It runs the diagnostic in order, with the safeguards a general model skips.

**Session flow:**

1. Read the agency config baseline, any recorded overrides, and account notes (operator mode)
2. Run five mandatory pre-flights: macro context (PF-0), conversion tracking (PF-1), structural red flags (PF-2), change history (PF-3), config ground truth (PF-4)
3. Pull live data via GAQL and flag candidates
4. Match recognized patterns to the playbook library (at most three `playbook:` lines on the walk card)
5. Produce a prioritized action list as data and standard moves, never as verdicts

**Two capabilities this version adds:**

- **Config ground truth.** A configuration finding is a departure from a stated agency standard (`references/agency-defaults.md`), not from Google's defaults and not from nothing. Matching settings are silent. Recorded overrides are one summary line. Only an unrecorded departure becomes a flag.
- **Optimization playbooks.** 39 pattern-to-standard-move entries in `references/playbooks.md` (PB-01 to PB-39). A triggered playbook adds one labelled `playbook PB-nn:` line to the walk card, after red flags, ending `accept/reject`. The agent never executes the move.

**What it gets right that a general model doesn't:**

| Failure mode                       | What a general model does                 | What this skill does                                                                       |
| ---------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------ |
| Negative keywords in GAQL results  | Flags them as active optimization targets | Filters `negative = FALSE` — required in every keyword query                               |
| Paused ad group search terms       | Treats them as active waste               | Requires `ad_group.status = ENABLED` filter; `status = NONE` terms are explicitly excluded |
| Cheap CPC on a legal term          | Explains it as "low-intent traffic"       | Routes to data contamination first — paused ad group history bleeding in                   |
| 58% rank-lost IS                   | Recommends raising budget                 | Correctly identifies as QS/bid quality problem; budget won't help                          |
| tCPA above target                  | Recommends lowering tCPA to "tighten up"  | Applies direction rule: lowering when above target restricts volume, not cost              |
| CPA from 4 conversions             | Treats it as a reliable signal            | Flags the 15-20 conversion threshold; below that, CPA is noise                             |
| Search term waste estimates        | Reports face-value numbers                | Discloses the ~50% API coverage ceiling and scales estimates accordingly                   |
| Config that matches house standard | Flags it against Google's defaults        | Classifies against `agency-defaults.md`; a MATCH is silent                                 |

---

## Public vs operator mode

The public skill ships the methodology, query library, config baseline, and playbooks, with fictional example notes only. The operator version additionally reads the per-account journal, rendered notes, session logs, and learnings; per-account config overrides live in that journal, not in this repo.

---

## Adapting the config baseline

`references/agency-defaults.md` is Rosen Advertising's baseline. To use this skill at another agency, replace each STANDARD value with yours and keep the MATCH / OVERRIDE-MATCH / DEVIATION classification. Entries marked PROPOSED stay at config-item severity until you confirm them. Per-account exceptions belong in your own notes or journal as overrides, not in the baseline file.

---

## Eval Results

The skill ships with an adversarial eval suite. Each eval runs the same prompt with and without the skill loaded, then scores against specific behavioral assertions. The goal: the skill should catch things a capable general model misses.

**Current delta: +86 percentage points** (with skill: 97.6% — without skill: 11.9%)

Selected discriminating evals:

| Eval                   | Scenario                                                   | With skill | Without skill |
| ---------------------- | ---------------------------------------------------------- | ---------- | ------------- |
| QS throttling          | All-BELOW_AVERAGE + zero impressions                       | 4/4        | 0/4           |
| Coverage check         | Search term analysis before coverage ratio reported        | 4/4        | 0/4           |
| Change history first   | Performance drop — change history before symptom diagnosis | 5/5        | 1/5           |
| BROAD → phrase         | Correct default intervention for BROAD keyword             | 4/4        | 0/4           |
| Budget vs rank IS      | Distinguishes rank-lost from budget-lost IS                | 4/4        | 1/4           |
| CPC anomaly routing    | Low avg CPC → data integrity first, not keyword targeting  | 4/4        | 1/4           |
| Account notes override | Account-specific rule overrides general BROAD guidance     | 4/4        | 1/4           |

**How to run evals.** Suites are JSON assertion files: `evals/evals.json`, `evals/evals_v2.json`, `evals/evals_v3.json`, `evals/evals_v4.json`, `evals/trigger_evals.json`. Each case is a prompt plus a `assertions` array. Run the same prompt with the skill loaded and without it, then score against those assertions. `evals_v4.json` is the config-ground-truth and optimization-playbook suite (17 cases): it verifies config checks classify settings against `references/agency-defaults.md` rather than Google's own defaults, and that triggered playbooks from `references/playbooks.md` appear in the walk card's `PLAYBOOKS:` group with the correct card-line format. `trigger_evals.json` tests skill-activation reliability (should-trigger vs should-not-trigger prompts), separate from output-quality testing. Fixtures for the fictional accounts (Apex Law, Greenfield Legal) live in `evals/fixtures/`. There is no in-repo eval runner; use whatever harness you use for Claude Code skill evals.

---

## Requirements

- [Claude Code](https://claude.ai/code) with skill support
- A Google Ads MCP server that exposes `run_gaql` or `execute_gaql_query`
- The `Agent` tool must be available for multi-campaign parallel search term reviews. If not available, the skill falls back to sequential execution automatically.

### Recommended MCP

Tested with **[cohnen/mcp-google-ads](https://github.com/cohnen/mcp-google-ads)**. Any GAQL-capable MCP works — update the tool note in `SKILL.md` if you're using a different implementation.

---

## Installation

```bash
git clone https://github.com/RosenAdvertising/legal-ppc-skill
```

1. Set up your Google Ads MCP (see cohnen/mcp-google-ads)
2. Update the `## Accounts` table in `SKILL.md` with your account IDs
3. Public mode: `account-notes/example-family-law.md` shows the notes/override shape; do not add real account files to this repo. Operator mode: journal and rendered notes live outside this skill.
4. Load the skill in Claude Code and run `list_accounts()` to confirm API access

---

## File Structure

```text
legal-ppc-skill/
├── SKILL.md                           # Main skill file — load this
├── account-audit-checklist.md         # Structured first-review checklist (Sections A–I)
├── NOTATION.md                        # Journal notation standard (operator mode)
├── pyrightconfig.json                 # Type-check path for journal tests
├── account-notes/
│   └── example-family-law.md          # Fictional example notes / override shape
├── references/
│   ├── google-ads-knowledge-base.md   # Core philosophy — read before any analysis
│   ├── agency-defaults.md             # Configuration baseline for PF-4
│   ├── playbooks.md                   # PB-01 to PB-39 optimization playbooks
│   ├── diagnosis-trees.md             # Decision trees for common problems
│   ├── gaql-query-library.md          # Pre-built GAQL queries by diagnostic task
│   ├── negative-keyword-library.md    # Master negative lists by practice area
│   └── creative-audit.md              # Image-asset audit procedure
├── journal/                           # Journal CLI, schema, and tests (operator mode)
└── evals/
    ├── evals.json                     # Eval suite v1
    ├── evals_v2.json                  # Eval suite v2
    ├── evals_v3.json                  # Eval suite v3
    ├── evals_v4.json                  # Eval suite v4: config ground truth + optimization playbooks (17 cases)
    ├── trigger_evals.json             # Skill-activation trigger reliability evals
    └── fixtures/                      # Fictional account notes and config pulls
```

---

## Practice Areas

Negative keyword libraries, search intent guidance, and diagnostic priors for:

- Family law (divorce, child custody, child support)
- Probate / estate disputes
- Elder law (estate litigation, trust disputes)
- Personal injury
- Criminal defense
- Real estate / landlord-tenant

---

## Known Limitations

**`search_term_view` coverage ceiling (~50%)**
The Google Ads API caps search term rows per query and withholds low-volume terms. Expect ~50% coverage of actual campaign spend in any search term pull. The skill discloses this, scales estimates by coverage ratio, and never recommends blocking a term category based on search term data alone.

**Conversion tracking configuration is read-only via GAQL**
There's no structured API object for conversion action settings (primary vs. secondary, attribution model, counting method). The skill reconstructs this from `conversion_action` queries. For complex setups, UI verification is faster.

**Asset-level creative performance not yet covered**
Responsive search ad headline/description scores are not pulled. Ad copy is reviewed structurally, not at asset level.

---

## License

MIT
