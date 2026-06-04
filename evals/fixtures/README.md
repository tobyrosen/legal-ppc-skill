# Eval Fixtures

Committed test fixtures for the legal-ppc eval suite. These exist so evals that
assert "reads `account-notes/<account>.md`" are actually testable in a clean
checkout — the real `account-notes/` directory is Toby-version-only and
git-ignored, so without these the notes-read step is untestable and shows up as
a false failure.

## account-notes/

Synthetic per-account notes for the suite's fixed fictional accounts:

- `apex-law.md` — Apex Law (ID 1111111111), family law, competitive metro.
- `greenfield-legal.md` — Greenfield Legal (ID 2222222222), elder law, small market.

Each fixture carries: firm profile, **external firm economics/targets**
(case value, cost-per-signed-case, target CPL — operator-provided, never
back-solved from the account), representative account structure, durable
market context, and a Pending Actions list.

They provide realistic context without leaking eval answers — e.g. Greenfield
documents that a tracking cleanup happened but leaves the
inflation-vs-broken-tag question open, and states the low-volume facts without
prescribing the bid strategy.

## How the runner uses these

When an eval prompt names an account that has a fixture here, the runner must
make the matching `account-notes/<account>.md` content available to the agent
(the account slug maps to the filename). A run that does not surface the fixture
cannot fairly grade a "reads account notes" assertion.

Mapping: account name -> slug -> `account-notes/<slug>.md`
(e.g. "Greenfield Legal" -> `greenfield-legal`).
