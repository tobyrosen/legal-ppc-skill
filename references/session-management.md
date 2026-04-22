# Session Management *(Toby version only)*

This file is for the internal Toby version of the skill. Public version users do not need this file.

---

## Session Log Template

Copy this template and fill it out at the end of every session. Save to `session-logs/YYYY-MM-DD-[account-name].md`.

```markdown
# Session Log — [YYYY-MM-DD] — [Account Name]

## Brief
[One or two sentences: what triggered this session, what the stated objective was]

## Entry Point
[Which diagnostic tree was the primary starting point]
- [ ] Conversions low
- [ ] CPA too high
- [ ] Budget not spending
- [ ] Performance dropped
- [ ] Inherited account / first review
- [ ] Search term review
- [ ] Other: ___

## Diagnostic Path
[Ordered account of what was checked and why — not a polished narrative, just what actually happened]
1. [What was pulled] → [What it showed] → [What that led to]
2. ...

## Flags Raised
[Everything that looked wrong before prioritization]
- [Flag] | [Why flagged] | [Severity: High / Medium / Low]

## Confirmed Findings
[Flags that became actual findings after investigation]
- [Finding] | [Root cause if identified] | [Recommended action]

## Actions Taken This Session
[What was actually changed, not just recommended. "None" is a valid answer.]

## Blind Spots Hit
[What couldn't be diagnosed via API and whether a screenshot was obtained]
- [What] | [Screenshot obtained? Y/N] | [Outcome / what it showed]

## Open Questions
[What couldn't be resolved and why — for follow-up in next session]

## Session Observations
[The most important field. Anything surprising. Anything the current skill doesn't account for. New diagnostic patterns. Client context that matters for future sessions. If nothing is surprising, say so explicitly.]
```

---

## Skill Development Loop

Session logs accumulate in `session-logs/`. After approximately 4–8 sessions with substantive findings, run a synthesis session:

1. Read all session logs, focusing on `Session Observations` and `Diagnostic Path` fields
2. Identify patterns that appear in 2+ sessions and aren't already in the diagnosis trees
3. Propose additions or revisions to the relevant skill files
4. Review and approve before any file is updated
5. Add validated patterns to `references/learnings.md` with the date and source session log(s)

This is the mechanism by which the skill improves. The model doesn't learn — the files learn.
