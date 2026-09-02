# Negative keyword library: legal PPC

Candidate negative-keyword patterns for family, immigration, and elder law Google Ads accounts, organized by category and scope.

**Nothing in this file is a blanket list.** Every section below is `unconfirmed`: it is general practice, not a house tactic confirmed by the operator. Two rules override every category here, in every account:

1. **The operator's not-waste list wins.** The terms named in SKILL.md "Search terms that are NOT waste" are never negated, whatever category in this file would catch them. That list includes free-consultation variants, cheap divorce, uncontested divorce online, child support calculator, divorce mediator, how long does a divorce take, how to file for divorce without a lawyer, family law attorney jobs, divorce therapist, child support office, pay child support online, medicaid office phone number, and nursing homes near me.
2. **Never negate a term that has converted.** Check the term's own conversion data before excluding it. A converting term is a client, not waste.

**This library seeds new campaigns. It is never applied to a live account.** On a live account, every negative comes from that account's own search terms, checked against the not-waste list above and against the term's own conversion record. Add at the narrowest sufficient scope. Do not paste a section wholesale onto anything.

## How to Use This Library

**Account-level shared list.** Sections 1 to 4 are candidate categories. Whether an account needs a shared list at all, and which categories belong in it, is decided against that account's own search-term data. The absence of a shared list is not a red flag on its own.

**Campaign-level negatives.** Apply the practice-area cross-exclusions in section 5 at the campaign level, and only for practice areas the firm demonstrably does not handle. Never cross-exclude family, immigration, or elder work from one another without confirming the firm does not take those matters: a firm running all three would be blocking its own clients.

**Ad group-level negatives:** Narrow exclusions specific to one ad group's keyword theme. Not covered here — these are account-specific and determined through search term review.

**Match type guidance:** Phrase match `"term"` is the default for most negatives — it catches the term as part of a longer query without being overly restrictive. Exact match `[term]` is used when a word has legitimate uses you want to preserve (e.g., blocking [free] exactly but not "free consultation attorney"). Broad match (no quotes/brackets) should be used sparingly for negatives — it blocks any query containing the word in any form, which can be too aggressive for ambiguous terms.

---

## Section 1 — Price & Affordability Signals

Price and affordability signals split two ways, and the split is ruled, not inferred.

**Confirmed waste:** free divorce lawyer, pro bono divorce lawyer, legal aid divorce, free divorce papers, divorce lawyer salary, free elder law attorney, free will template, elder law attorney salary.

**Money terms, never negated:** free consultation variants, cheap divorce, uncontested divorce online, child support calculator, divorce mediator, how long does a divorce take.

That price and affordability searchers rarely convert to paying clients is a general claim, not a measured result on these accounts. Check every candidate against the ruling above and against the term's own conversion data before negating it.

### Broad Match (use cautiously — review for collateral blocking)

```text
quick
legal aid
pro bono
assistance
easy
fast
diy
aid
loan
low cost
```

`free`, `cheap`, `cost`, `fees` and `afford` are deliberately absent: as broad negatives they catch
free consultation and cheap divorce, which are ruled money terms.

### Phrase Match

```text
"aid"
"assistance"
"diy"
"easy"
"fast"
"legal aid"
"loan"
"low cost"
"pro bono"
"quick"
```

Same reason: `"afford"`, `"cheap"`, `"cost"`, `"fees"` and `"free"` are not on the phrase list.
The named confirmed-waste strings above are negated as written, not as bare words.

### Exact Match

```text
[afford]
[aid]
[assistance]
[cheap]
[cost]
[diy]
[easy]
[fast]
[fees]
[free]
[legal aid]
[loan]
[low cost]
[pro bono]
[quick]
```

**Note on "assistance" and "aid":** These are broad words with legitimate adjacent uses. Monitor for over-blocking after adding. "Legal aid" and "pro bono" are safer to block aggressively; standalone "assistance" may need to remain phrase/exact only.

---

## Section 2 — Employment & Career Signals

Candidates for blocking job seekers, law students, and people researching legal careers. Not wholesale: the operator has ruled `family law attorney jobs` explicitly NOT waste, so an attorney-jobs query is not automatically a job seeker. `attorney jobs` and `lawyer jobs` are therefore absent from both lists below. Retain only the job-seeker patterns proven in the account's own search-term data.

### Phrase Match

```text
"legal jobs"
"paralegal jobs"
"law clerk"
"law school"
"law degree"
"bar exam"
"become a lawyer"
"become an attorney"
"how to become"
"legal internship"
"law internship"
"attorney salary"
"lawyer salary"
"legal career"
"hiring attorney"
"attorney opening"
"law firm jobs"
"associate attorney"
"legal assistant jobs"
"legal secretary"
```

### Exact Match

```text
[law school]
[bar exam]
[paralegal]
[law clerk]
[law degree]
```

---

## Section 3 — Self-Help & DIY Legal Resources

Candidates for blocking people seeking forms or self-representation. Procedural family, immigration, and elder queries are frequently real prospects in these practice areas.

Four strings are deliberately absent from the list below. `how to file` and `without a lawyer` both block `how to file for divorce without a lawyer`, which is a ruled not-waste term. `free consultation` and `free case review` are money terms and belong as keywords, not negatives. Do not apply this section wholesale.

### Phrase Match

```text
"how to represent"
"self represent"
"pro se"
"court forms"
"legal forms"
"fill out forms"
"download forms"
"free forms"
"legal documents"
"do it yourself"
"represent myself"
"without an attorney"
"without hiring"
"legal advice"
"legal help online"
"online legal"
"legal aid society"
"free legal"
"free attorney"
"free lawyer"
```

---

## Section 4 — Research & Informational Intent

Candidates only. Blanket informational negatives conflict with the long-consideration reality of these practice areas: informational queries can be genuine top-of-funnel here and have been observed converting. `how long does` is absent from the list below because it blocks `how long does a divorce take`, a ruled money term. Check whether every remaining pattern converts in this account before negating it. Use phrase match; exact is too narrow and broad risks catching too much.

### Phrase Match

```text
"definition"
"what is"
"what does"
"what are"
"how does"
"how much does"
"what happens"
"can i"
"should i"
"do i need"
"do i have to"
"statistics"
"average"
"typical"
"examples"
"explained"
"guide"
"overview"
"introduction to"
"basics of"
"understanding"
"vs"
"difference between"
"wiki"
"wikipedia"
```

**Important caveat:** Many of these queries ("how much does a divorce cost," "do I need a lawyer for custody") represent early-stage prospects who may convert later. Blocking them reduces top-of-funnel reach. Consider whether your account has the budget and landing page depth to nurture this traffic. If budget is constrained, block these and focus on high-intent traffic. If budget allows, run them in a separate campaign with lower bids and educational landing pages.

---

## Section 5: practice-area cross-exclusions

Apply at campaign level, never account level, and only for practice areas the firm demonstrably does not handle. Confirm the firm's actual practice list before applying any of it. The default is no cross-exclusion unless the firm has declined the work, and that default is operator-confirmed.

**Family, immigration, and elder work are never cross-excluded from one another by default.** All three are in scope for this skill, and a firm may run any combination of them. Excluding immigration terms from a family campaign, or estate and probate terms from an elder campaign, blocks the firm's own clients unless the firm has confirmed it does not take that work. Estate planning, wills, trusts, and probate overlap elder law and stay in scope.

### For a family law campaign, where the firm does not handle these areas

```text
"estate planning"
"will"
"trust"
"probate"
```

Apply only where the firm has confirmed it does not take estate or probate matters. If it runs an elder practice, these belong as keywords in that campaign, not as negatives here.

### For an elder law campaign, where the firm does not handle these areas

```text
"divorce"
"custody"
"child support"
"alimony"
```

Same condition: apply only where the firm has confirmed it does not take family matters.

### For an immigration campaign

No cross-exclusion set is recorded. Immigration has no vertical-specific tactics encoded yet, so build this from the account's own search-term data rather than from a template.

**Rule.** A cross-exclusion list is derived from what the firm declines, not from a template. Verify the firm declines a category before negating it, and never negate a term the account has converted on.

---

## Section 6: geography exclusions

Managed at the campaign targeting level first. Where out-of-area queries persist in search terms, add the geo token as a campaign negative.

**Negate the geo token only, never the service term.** Decompose the query first: for a city-mismatched query shaped `[core service term] [wrong city]`, negate the wrong city, so the campaign keeps serving the service term in its real geography. Negating whole city-plus-service phrases blocks the core service phrase and is the failure mode this rule exists to prevent.

```text
"[wrong city]"
"[out-of-state locality]"
```

These are account-specific and cannot be standardized here. Identify them from the geographic performance report and search-term analysis.

---

## Maintenance

- **Review search terms monthly** (or at each optimization session) and add new negatives discovered in search term reports. The library above is a starting point, not a complete list.
- **Date-stamp significant additions.** When adding a batch of negatives after a search term review, note the date in account records so future managers know when the list was last reviewed.
- **Don't set and forget.** A negative keyword added two years ago may be blocking a term that's now relevant — especially after a firm expands its practice areas.
- **Shared lists vs. campaign-level:** Items added to the shared account-level list affect every campaign. Be conservative about what goes there. When in doubt, add at campaign level first and promote to shared list after confirming no collateral damage.
