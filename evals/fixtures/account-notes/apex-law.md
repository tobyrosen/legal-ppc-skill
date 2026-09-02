# Account Notes — Apex Law

_Synthetic eval fixture. Apex Law (ID 1111111111, MCC login 0000000000) is a fictional family-law firm used by the legal-ppc eval suite. Figures are representative, not real client data._

## Firm Profile

- Practice: family law — divorce, child custody, custody modification, child support.
- Market: large competitive metro. Legal CPCs run high ($15–60+).
- Consideration window: LONG. Divorce and custody decisions unfold over weeks to months, so informational queries ("how long does divorce take", "how is custody decided") are real prospects at an earlier funnel stage. Do NOT blanket-negate them in this market (see the negative-keyword-library Section 4 caveat).
- Conversion path: phone calls (CallRail) plus a website intake form. Primary conversion actions measure real consultation requests.

## Firm Economics and Targets (external — operator-provided)

These targets come from the firm's own economics, not from back-solving the account's current CPA. Use them as the reference for whether CPL is acceptable. Never derive a target by averaging what the account currently spends.

- Average signed-case value: ~$12,000 (retainer plus fees, blended across divorce and custody).
- Lead to signed-case rate: ~30%.
- Target cost per signed case: ~$1,800 (15% of case value).
- Implied target CPL (cost per qualified lead): ~$540.
- If the operator's economics differ, they override the numbers here. The skill must not silently substitute account-derived figures.

## Account Structure (representative)

- Campaign: Divorce — metro geo, exact and phrase match, Maximize Conversions (adequate volume).
- Campaign: Child Custody — metro geo, exact and phrase match.
- Campaign: Brand — isolated brand terms, separate from non-brand.
- One shared negative-keyword list applied to all non-brand campaigns.

## Config overrides

Deliberate departures from `references/agency-defaults.md`. A config check classifies a setting
listed here as an override match and reports it only in the summary count, never as a flag. Every
other setting is classified against the baseline directly.

- `campaign.network_settings.target_partner_search_network`: account `true` (baseline `false`), scope: Brand, approved by the operator on 2026-05-04, entry `apex-law-20260504-02`
  Search Partners left on for the Brand campaign only. Partner traffic on branded queries is cheap defensive coverage against competitors bidding on the firm name. Non-brand campaigns keep partners off. Ends if brand CPA moves materially on a network-segmented read.
- `conversion_action.counting_type`: account `ONE_PER_CLICK` (baseline `MANY_PER_CLICK`), scope: the four website form actions, approved by the operator on 2026-04-19, entry `apex-law-20260419-01`
  The site's form plugin double-submits on slow connections, so repeat submissions from one click are noise, not leads. Applies to the form actions only; call and upload actions stay `MANY_PER_CLICK` per the house standard.

Not overrides, for the avoidance of doubt: `positive_geo_target_type = PRESENCE_OR_INTEREST` and
`ad_serving_optimization_status = ROTATE_INDEFINITELY` are the agency baseline on this account, so
they are plain matches and never appear in output.

## Pending Actions (check before any new analysis)

- [P1] Divorce — landing-page post_click_quality_score flagged BELOW_AVERAGE last review. The landing page is the binding constraint; bid and keyword tweaks have limited leverage until it is fixed. UNRESOLVED.
- [P2] Brand — CPA review pending: confirm the ~$284 brand CPA reflects real lead cost versus a tracking artifact before considering any pause.
- [P3] Child Custody — "best child custody lawyer near me" is a confirmed converting term. Do not negate it.
