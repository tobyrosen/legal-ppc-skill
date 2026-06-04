# Legal PPC Skill — Google Ads Analysis for Law Firms

![Version](https://img.shields.io/badge/version-v3.6-blue)
![Evals](https://img.shields.io/badge/eval%20delta-%2B86pp-brightgreen)
![Status](https://img.shields.io/badge/production-active-success)

> A Claude Code skill that turns Google Ads analysis from a manual, error-prone process into a structured, expert-level diagnostic session — every time.

---

## The Problem

Legal PPC is one of the most expensive ad environments on the planet. Family law clicks run $10–30. Elder law, $15–40. Personal injury, $20–80+. One misread metric, one wrong bid decision, one unconverted BROAD keyword left running — and you've burned real money with nothing to show for it.

Most AI-assisted PPC analysis fails in exactly the same ways: it reads the wrong keywords (negatives mixed with positives), trusts bad data (paused ad group history blending into search term reports), and makes the wrong bidding call (lowering tCPA when it's already above target, restricting the campaign right when it needs room to convert).

This skill fixes that.

---

## What It Does

Plug it into Claude Code with a Google Ads MCP and you get structured, expert-level account analysis without step-by-step direction. Give it a brief — or just say "something feels off" — and it runs the right diagnostic, in the right order, with the right safeguards.

**Session flow:**

1. Read account notes (prior session history, pending actions)
2. Run three mandatory pre-flights: conversion tracking, structural issues, change history
3. Pull live data via GAQL and flag candidates
4. Diagnose priority issues through structured decision trees
5. Produce a prioritized action list — and write a session log for the next session

**What it gets right that a general model doesn't:**

| Failure mode                      | What a general model does                 | What this skill does                                                                       |
| --------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------ |
| Negative keywords in GAQL results | Flags them as active optimization targets | Filters `negative = FALSE` — required in every keyword query                               |
| Paused ad group search terms      | Treats them as active waste               | Requires `ad_group.status = ENABLED` filter; `status = NONE` terms are explicitly excluded |
| Cheap CPC on a legal term         | Explains it as "low-intent traffic"       | Routes to data contamination first — paused ad group history bleeding in                   |
| 58% rank-lost IS                  | Recommends raising budget                 | Correctly identifies as QS/bid quality problem; budget won't help                          |
| tCPA above target                 | Recommends lowering tCPA to "tighten up"  | Applies direction rule: lowering when above target restricts volume, not cost              |
| CPA from 4 conversions            | Treats it as a reliable signal            | Flags the 15-20 conversion threshold; below that, CPA is noise                             |
| Search term waste estimates       | Reports face-value numbers                | Discloses the ~50% API coverage ceiling and scales estimates accordingly                   |

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
3. Add `account-notes/[account].md` files for accounts you manage regularly (see the internal version note below)
4. Load the skill in Claude Code and run `list_accounts()` to confirm API access

---

## File Structure

```text
legal-ppc-skill/
├── SKILL.md                           # Main skill file — load this
├── account-audit-checklist.md         # Structured first-review checklist (Sections A–I)
├── references/
│   ├── google-ads-knowledge-base.md   # Core philosophy — read before any analysis
│   ├── diagnosis-trees.md             # Decision trees for common problems
│   ├── gaql-query-library.md          # Pre-built GAQL queries by diagnostic task
│   └── negative-keyword-library.md    # Master negative lists by practice area
└── evals/
    └── evals_v2.json                  # Adversarial test suite
```

---

## Practice Areas

Negative keyword libraries, search intent guidance, and diagnostic priors for:

- Family law (divorce, child custody, child support)
- Probate / estate disputes
- Elder law (Medicaid planning, conservatorship)
- Personal injury
- Criminal defense
- Real estate / landlord-tenant

---

## Public vs. Internal Version

This is the **public version**. The internal version used in production at Rosen Advertising adds:

- `account-notes/[account].md` — per-account session history, pending actions, market-specific priors
- `session-logs/` — structured logs written at session end (what ran, what changed, what's next). Directory is created automatically on first use.
- `references/learnings.md` — validated patterns extracted from live session history across multiple accounts

The public version is the full skill minus the client-specific data. It works standalone.

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
