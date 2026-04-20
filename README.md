# Legal PPC Skill — Google Ads Analysis for Law Firms

![Status](https://img.shields.io/badge/status-active%20development-yellow)
![Evals](https://img.shields.io/badge/evals-40%2F40%20passing-brightgreen)

> **Active development.** Core skill is stable and eval-validated, but new protocols, practice areas, and diagnostic trees are added regularly as the skill is used in production.

A Claude Code skill for expert-level Google Ads analysis and optimization for law firm accounts.

Built by [Rosen Advertising](https://rosenadvertising.com) and validated across active legal PPC accounts.

---

## What This Skill Does

Enables Claude to run structured Google Ads analysis for law firm accounts — without step-by-step direction. It encodes expert-level knowledge about legal PPC and provides diagnostic frameworks, pre-built GAQL queries, and keyword libraries specific to legal marketing.

**Core capabilities:**
- Performance diagnosis via structured decision trees
- Pre-flight validation (conversion tracking, structural issues, change history) before any symptom analysis
- Search term review with waste identification and negative keyword recommendations
- QS / impression share analysis with rank-loss vs. budget-loss distinction
- Smart bidding evaluation including post-tracking-fix protocol
- Account audits for inherited or new accounts

**Built-in protections against common mistakes:**
- Correctly handles negative keywords vs. positive keywords in GAQL results
- Filters paused/removed ad groups from active analysis (search terms and keywords)
- Verifies premises before diagnosing ("CPA is high" → pulls data first)
- Detects anomalously cheap CPCs in handed search term data (paused ad group contamination signal)
- Requires coverage check before presenting search term waste findings

---

## Requirements

- [Claude Code](https://claude.ai/code) with skill support
- Google Ads MCP server (for live data pulls via GAQL)
- Access to a Google Ads account or MCC

---

## Installation

```bash
# Clone into your Claude Code skills directory or any accessible path
git clone https://github.com/rosenadvertising/legal-ppc-skill

# In Claude Code, point to SKILL.md when invoking
# Or install as a plugin if using a plugin-aware Claude Code setup
```

---

## File Structure

```
legal-ppc-skill/
├── SKILL.md                        # Main skill instructions (load this)
├── account-audit-checklist.md      # Structured first-review checklist (Sections A–I)
├── references/
│   ├── google-ads-knowledge-base.md   # Core philosophy — read before any analysis
│   ├── diagnosis-trees.md             # Diagnostic frameworks for common problems
│   ├── gaql-query-library.md          # Pre-built GAQL queries by diagnostic task
│   └── negative-keyword-library.md    # Master negative lists by legal practice area
└── evals/
    └── evals_v2.json                  # Test suite (10 evals, adversarial + edge cases)
```

---

## Practice Areas Covered

Negative keyword libraries, search intent guidance, and diagnostic priors for:

- Family law (divorce, child custody, child support)
- Probate / estate disputes
- Elder law (Medicaid planning, conservatorship)
- Personal injury
- Criminal defense
- Real estate / partition law

---

## Eval Results

The skill ships with a test suite of 10 adversarial evals covering:

| Eval | Topic |
|---|---|
| 4 | Vague brief routing — names entry point, runs pre-flight |
| 5 | Adversarial bypass resistance — holds line on coverage check |
| 6 | First review — new account generalization |
| 7 | False premise verification — verifies CPA claim before diagnosing |
| 8 | Brand campaign judgment — cannibalization mechanism |
| 9 | GAQL negative keyword misread detection |
| 10 | Paused ad group exclusion from active keyword list |
| 11 | tCPA post-tracking-fix protocol |
| 12 | IS metric distinction (rank-lost vs. budget-lost) |
| 13 | Paused ad group detection in handed search term data |

**Pass rate: 40/40 (100%) as of iteration 9.**

---

## Versions

This repository contains the **public version** of the skill. The internal version used by Rosen Advertising adds account-specific notes, session logging, and a validated learnings document built from live session history.

---

## License

MIT
