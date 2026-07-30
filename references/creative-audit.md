# Creative / Image-Asset Audit — Legal PPC

Reference for the creative pass that runs as a standing part of every periodic account check. As Rosen Advertising accounts shift toward image and (soon) display, image-asset coverage and quality become a first-class account-health dimension — not an afterthought. This file covers what to pull, what to look for, and how to report, including which parts are API-sourceable and which require manual/visual review.

---

## Tooling — Image Assets Live Only in the Sidecar

The image-asset tools are NOT in the official Google Ads MCP. They exist **only in the incumbent `googleAdsServer` sidecar** — which is precisely why the sidecar is retained alongside the official MCP. Four tools, and only these four, drive the creative pass:

| Tool                   | What it does                                      | Use for                                                              |
| ---------------------- | ------------------------------------------------- | -------------------------------------------------------------------- |
| `get_image_assets`     | Lists image assets in the account                 | Asset inventory — what creative exists at all                        |
| `get_asset_usage`      | Maps which campaigns / ad groups use which assets | Coverage mapping — which campaigns have image coverage, which don't  |
| `download_image_asset` | Fetches the actual image file                     | Pulling a file for visual inspection or vision analysis              |
| `analyze_image_assets` | Vision analysis of image content / quality        | On-brand / legible / message-match assessment without manual eyeball |

If the sidecar tool names change, update this table only — the workflow below remains valid. Do not substitute or invent other tool names; these four are the complete surface for image-asset work.

**Why GAQL doesn't cover this:** the GAQL library (`references/gaql-query-library.md`) handles RSA/text creative (section 7) and asset metrics where exposed, but it does not provide image-asset listing, usage mapping, file download, or vision analysis. The creative pass is the sidecar's job.

---

## What to Pull

Run these in order; later steps depend on the inventory from the first.

1. **Asset inventory** — `get_image_assets` for the account. This is the universe of image creative that exists, regardless of whether it's in use. Note asset IDs, names, dimensions/type where returned.
2. **Usage mapping** — `get_asset_usage` to map assets → campaigns / ad groups. This is the join that answers "which campaigns have image coverage and which don't." Cross-reference against the live campaign list (pull campaigns via GAQL `FROM campaign WHERE campaign.status = 'ENABLED'`) so you know the full set of campaigns that _should_ have coverage, not just the ones that already do.
3. **Performance where available** — pull asset-level or ad-level metrics where the API exposes them. Asset-level performance for images is thin in the Google Ads API; treat it as **partially API-sourceable** (see the API-sourceability table below). Where per-asset performance is unavailable, fall back to ad-group / campaign-level CTR and impression trends (GAQL section 7) as a proxy and say so explicitly.
4. **Visual content** — for assets that warrant a closer look (new, high-spend, or coverage-critical), run `analyze_image_assets` for a vision read, and `download_image_asset` when you need the file itself for manual review or to attach to a finding.

**Scope discipline:** this is a focused pass, not a forensic teardown of every asset. Default to inventory + usage mapping for the whole account (cheap, high-signal), then vision-analyze the subset that the coverage/usage map flags as worth inspecting. Don't `analyze_image_assets` every image in a large account by reflex.

---

## What to Look For

Four checks, ordered by how often they matter as accounts move to display.

### (a) Asset coverage per campaign — the thin/missing gap

Map every ENABLED campaign against `get_asset_usage`. Flag campaigns that are **thin or missing image assets**. As accounts move toward display, a campaign with no (or one) image asset cannot serve well across display/PMax inventory — coverage gaps that were cosmetic in a search-only world become a serving constraint.

- **Missing:** an ENABLED campaign (especially Display, PMax, or Demand Gen) with zero image assets attached. This is the highest-priority creative finding — the campaign cannot fill image inventory.
- **Thin:** a campaign with image coverage well below what its inventory needs (e.g., a single image where the format expects multiple aspect ratios). Display and PMax want a spread of sizes/ratios; one square image is thin coverage.
- **Cross-reference the campaign type.** A pure Search campaign with no image assets is expected, not a gap (image assets there are sitelink/extension-level at most). Reserve the "missing coverage" flag for campaigns whose inventory actually serves images — don't flag Search campaigns for lacking display creative.

### (b) Image quality + content via vision — on-brand, legible, message-matched

Use `analyze_image_assets` (and `download_image_asset` for manual confirmation) to assess each in-use asset against three bars:

- **On-brand:** colors, logo presence/treatment, and overall look match the firm's brand. A law firm's display creative carrying the wrong palette or a stretched logo reads as low-trust — high stakes in legal.
- **Legible:** any text on the image is readable at the size it serves, not clipped by safe-area cropping, not low-contrast. Display creative gets cropped to many aspect ratios; text near the edge or tiny text fails.
- **Message-matched to ad-group intent:** the image's message matches the ad group's practice-area intent. A probate ad group serving a generic "car accident" stock image is a mismatch that depresses relevance and trust. Match the visual to the legal intent the ad group targets.

Vision analysis is a strong first read, but **content/brand judgment on a legal client is a human-review call** — see the API-sourceability table. Surface the vision read, then flag anything brand- or compliance-adjacent for manual confirmation rather than asserting it as final.

### (c) Usage gaps — uploaded-but-unused and uncovered campaigns

Two directions of the same map:

- **Uploaded but unused:** assets present in `get_image_assets` that `get_asset_usage` shows attached to no live campaign/ad group. Wasted creative — either it should be deployed or it's dead weight. Flag for the operator to deploy or remove.
- **Campaigns with no image coverage:** the inverse — covered in (a), but call it out here too when the gap is a usage gap rather than a missing-upload gap (the asset exists in the account but simply isn't attached to the campaign that needs it). The fix differs: attach an existing asset vs. produce/upload a new one.

### (d) Fatigue candidates — long-running assets / declining signals

Image assets fatigue like any creative. Flag candidates for refresh:

- **Long-running:** an asset that's been live and unchanged for a long stretch (cross-reference change history, GAQL section 8, for when creative last changed). Legal display creative that's run for many months unchanged is a refresh candidate by default.
- **Declining signals:** where per-asset performance is available, falling CTR / rising cost-per-result on an asset that previously performed. Where it isn't, fall back to ad-group/campaign CTR decline on stable creative (the same freshness logic as GAQL 7.2 for RSAs) and label it a proxy, not a per-asset measurement.
- **Don't over-call fatigue on low volume.** The same conversion-volume reliability discipline applies — a CTR wobble on an asset with trivial impressions is noise, not fatigue. Flag fatigue when the decline is on meaningful volume.

---

## How to Report

Fold creative findings into the session's running action list (SKILL.md Step 5) using the same format as every other finding, and lead with the campaign → ad group path (Step 8) so the operator can navigate to the asset in the UI:

```text
- [ACTION] [campaign → ad group → asset] — [one-line rationale] | [scope: account/campaign/ad-group]
```

**Prioritization** (same lens as Step 6 — spend impact × confidence × the move-to-display direction):

1. **Missing coverage on an image-serving campaign** (Display / PMax / Demand Gen with zero image assets) — highest priority; the campaign literally cannot fill its inventory.
2. **Brand / compliance / message-mismatch on an in-use asset** — high; a wrong-brand or off-message creative on a legal client is a trust and (potentially) bar-advertising risk.
3. **Thin coverage** on an image-serving campaign — medium-high as the account moves to display.
4. **Fatigue candidates** on meaningful volume — medium; a refresh, not an emergency.
5. **Uploaded-but-unused assets** — low-to-medium; cleanup / deploy, rarely urgent.

### API-sourceable vs. manual/visual review — be explicit

Match the skill's standing convention of marking what is and is not API-sourceable (see the audit sections in SKILL.md and the blind-spot protocol in `references/diagnosis-trees.md`). State this on every creative finding so the operator knows the source tier:

| Item                                          | Source tier                                                                                     |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Asset inventory (what exists)                 | **API-sourceable** — `get_image_assets`                                                         |
| Asset → campaign/ad-group usage mapping       | **API-sourceable** — `get_asset_usage`                                                          |
| Coverage gaps (missing / thin / unused)       | **API-sourceable** — derived from the two tools above + the GAQL campaign list                  |
| Image file itself                             | **API-sourceable** — `download_image_asset`                                                     |
| Image content / quality first read            | **API-assisted (vision)** — `analyze_image_assets`; treat as a strong read, not a final call    |
| On-brand / compliance / message-match verdict | **Manual / visual review** — vision informs it; the final legal-brand call is a human review    |
| Per-asset performance                         | **Partially API-sourceable** — thin in the API; fall back to ad-group/campaign proxy and say so |
| How the asset renders in a live placement     | **NOT API-sourceable** — blind spot; request a screenshot per the protocol below                |

For anything in the bottom three rows, do not present it as auto-pulled. Use the blind-spot protocol when the rendered placement is what's in question:

```text
⚠️ BLIND SPOT — How this image renders in a live display/PMax placement is not visible via API.
→ Please share a screenshot of the asset as served (Ad Preview, or the Assets report with the image shown), so brand/legibility/crop can be confirmed in placement.
```

**Bad-tracking parallel:** as with the tracking-QA gate, a confident brand/compliance verdict on a legal client that rests only on a vision model is worse than flagging it for human review. When in doubt on a brand or bar-advertising-adjacent call, surface it as a manual-review item, not a finished verdict.
