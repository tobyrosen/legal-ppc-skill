# Legacy account notes: frozen

This directory is retained for migration history only. Do not add or edit account data here.

The system of record is:

- Journal: `$PPC_JOURNAL_ROOT/journal/<slug>.jsonl`
- Rendered account notes: `$PPC_JOURNAL_ROOT/notes/<slug>.md`
- CLI and method: `journal/` in this repo (`journal.py`, `NOTATION.md`)

Append with `journal.py append`; regenerate views with `journal.py render`. Rendered Markdown is never hand-edited.
