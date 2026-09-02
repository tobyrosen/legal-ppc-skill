# Eval Fixtures

Committed test fixtures for the legal-ppc eval suite. These exist so evals that
assert "reads `account-notes/<account>.md`" are actually testable in a clean
checkout: the real account-notes directory is operator-version only and
git-ignored, so without these the notes-read step is untestable and shows up as
a false failure.

## account-notes/

Synthetic per-account notes for the suite's fixed fictional accounts:

- `apex-law.md`: Apex Law (ID 1111111111), family law, competitive metro.
- `greenfield-legal.md`: Greenfield Legal (ID 2222222222), elder law, small market.

Each fixture carries: firm profile, **external firm economics/targets**
(case value, cost-per-signed-case, target CPL, operator-provided, never
back-solved from the account), representative account structure, durable
market context, and a Pending Actions list.

They provide realistic context without leaking eval answers, e.g. Greenfield
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

## pmax-config-westhollow.md

A fictionalized PMax config-verification pull (Apex Law, account 1111111111,
campaign "PMax - Westhollow Custody Test", fictional geo Westhollow, Longmoor).
Built for `evals/evals_v4.json`'s `config_ground_truth` and `adversarial_user_pressure`
cases, which test the false-flag regression documented in
`references/agency-defaults.md` Sec 1.5: a config check must never flag
`positive_geo_target_type = PRESENCE_OR_INTEREST` as a problem, since it is the
agency's deliberate standard.

**Planted deviation:** an auto-applied Google recommendation
(`client_type = GOOGLE_ADS_RECOMMENDATIONS`) raised the campaign's daily budget
from $14.00 to $20.00, visible in the fixture's CHANGE EVENTS section. This is a
genuine red flag under `agency-defaults.md` Sec 7.1 (auto-apply is standard OFF)
in the base fixture. `evals_v4.json` case 102 supplies an inline override snippet
that reclassifies this same fact as OVERRIDE-MATCH, so the two cases together test
both the flag path and the override path on one planted fact. The fixture file itself
carries no answer key: eval subjects must classify against `agency-defaults.md`, not copy a header.
