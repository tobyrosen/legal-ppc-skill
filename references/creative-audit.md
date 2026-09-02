# Creative and asset audit: Search assets and Performance Max

The creative pass that runs as part of every periodic account check. Scope is Search ad assets and PMax asset groups. Display and Demand Gen are out of scope.

A creative pass runs on every periodic check (operator ruling, 2026-09-02); keep it proportionate. This file covers what to pull, what to look for, and how to report, including which parts are API-sourceable and which need a manual review.

---

## Tooling: Image Assets Live Only in the Sidecar

The image-asset tools are NOT in the official Google Ads MCP. They exist **only in the incumbent `googleAdsServer` sidecar**, which is precisely why the sidecar is retained alongside the official MCP. Four tools, and only these four, drive the creative pass:

| Tool                   | What it does                                      | Use for                                                              |
| ---------------------- | ------------------------------------------------- | -------------------------------------------------------------------- |
| `get_image_assets`     | Lists image assets in the account                 | Asset inventory, what creative exists at all                         |
| `get_asset_usage`      | Maps which campaigns / ad groups use which assets | Coverage mapping, which campaigns have image coverage, which don't   |
| `download_image_asset` | Fetches the actual image file                     | Pulling a file for visual inspection or vision analysis              |
| `analyze_image_assets` | Vision analysis of image content / quality        | On-brand / legible / message-match assessment without manual eyeball |

If the sidecar tool names change, update this table only. The workflow below remains valid. Do not substitute or invent other tool names; these four are the complete surface for image-asset work.

**Why GAQL doesn't cover this:** the GAQL library (`references/gaql-query-library.md`) handles RSA/text creative (section 7) and asset metrics where exposed, but it does not provide image-asset listing, usage mapping, file download, or vision analysis. The creative pass is the sidecar's job.

---

## What to Pull

Run these in order; later steps depend on the inventory from the first.

1. **Asset inventory**: `get_image_assets` for the account. This is the universe of image creative that exists, regardless of whether it's in use. Note asset IDs, names, dimensions/type where returned.
2. **Usage mapping**: `get_asset_usage` to map assets → campaigns / ad groups. This is the join that answers "which campaigns have image coverage and which don't." Cross-reference against the live campaign list (pull campaigns via GAQL `FROM campaign WHERE campaign.status = 'ENABLED'`) so you know the full set of campaigns that _should_ have coverage, not just the ones that already do.
3. **Performance where available**: pull asset-level or ad-level metrics where the API exposes them. Asset-level performance for images is thin in the Google Ads API; treat it as **partially API-sourceable** (see the API-sourceability table below). Where per-asset performance is unavailable, fall back to ad-group / campaign-level CTR and impression trends (GAQL section 7) as a proxy and say so explicitly.
4. **Visual content**: for assets that warrant a closer look (new, high-spend, or coverage-critical), run `analyze_image_assets` for a vision read, and `download_image_asset` when you need the file itself for manual review or to attach to a finding.

**Scope discipline:** this is a focused pass, not a forensic teardown of every asset. Default to inventory + usage mapping for the whole account (cheap, high-signal), then vision-analyze the subset that the coverage/usage map flags as worth inspecting. Don't `analyze_image_assets` every image in a large account by reflex.

---

## What to Look For

Four checks.

### (a) Asset coverage per PMax asset group: the thin or missing gap

Map every ENABLED PMax asset group against its asset usage. Flag groups that are thin on or missing image assets: an asset group that cannot fill its inventory is constrained on serving, not just on aesthetics.

- **Missing:** an ENABLED PMax asset group with zero image assets attached. This is a LOW finding: Performance Max can legitimately run without images. Operator ruling, 2026-09-02.
- **Thin:** coverage well below what the inventory needs, for example a single image where the format expects several aspect ratios. (`PROPOSED` threshold.)
- **Cross-reference the campaign type.** A Search campaign with no image assets is expected, not a gap. Search image extensions are checked as a Search asset item and never as a PMax coverage gap.

### (b) Image quality + content via vision: on-brand, legible, message-matched

Use `analyze_image_assets` (and `download_image_asset` for manual confirmation) to assess each in-use asset against three bars:

The three bars below are `PROPOSED` as stated standards.

- **On-brand:** colors, logo presence and treatment, and overall look match the firm's brand. A wrong palette or a stretched logo reads as low-trust.
- **Legible:** text on the image is readable at the size it serves, not clipped by safe-area cropping, not low-contrast. PMax crops to many aspect ratios, so text near the edge fails.
- **Message-matched to the asset group's intent:** the image matches the practice area it serves. A probate asset group running a generic stock image of a young couple is a mismatch that depresses relevance and trust. Match the visual to the family, immigration, or elder intent the group targets.

Vision analysis is a strong first read, but **content/brand judgment on a legal client is a human-review call**. See the API-sourceability table. Surface the vision read, then flag anything brand- or compliance-adjacent for manual confirmation rather than asserting it as final.

### (c) Usage gaps: uploaded-but-unused and uncovered campaigns

Two directions of the same map:

- **Uploaded but unused:** assets in the inventory that usage mapping shows attached to nothing live. Treated as wasted creative to deploy or remove. (`PROPOSED`)
- **Campaigns with no image coverage:** the inverse, covered in (a), but call it out here too when the gap is a usage gap rather than a missing-upload gap (the asset exists in the account but simply isn't attached to the campaign that needs it). The fix differs: attach an existing asset vs. produce/upload a new one.

### (d) Fatigue candidates: long-running assets / declining signals

Image assets fatigue like any creative. Flag candidates for refresh:

- **Long-running:** an asset live and unchanged for a long stretch, cross-referenced against change history. It is a refresh candidate only where performance is also declining. Assets that are old and still performing are not candidates: on the one refresh we measured, old Search images were still performing and age alone did not make them candidates.
- **Declining signals:** where per-asset performance exists, falling click-through rate or rising cost per result on an asset that previously performed. Where it does not, fall back to ad-group or campaign click-through decline on stable creative and label it a proxy, not a per-asset measurement. (`PROPOSED` as a proxy)
- **Do not over-call fatigue on low volume.** A click-through wobble on an asset with trivial impressions is noise. Flag fatigue only on meaningful volume.
- **A policy-limited asset group is not a fatigue finding.** Where a serving asset group is policy-limited while its assets remain approved, hold every asset edit until the appeal resolves (PB-18, PB-32).

---

## How to Report

Fold creative findings into the session's running action list using the same format as every other finding, and lead with the campaign and ad group path so the operator can navigate to the asset in the UI:

```text
- [ACTION] [campaign → ad group → asset]: [one-line rationale] | [scope: account/campaign/ad-group]
```

**Prioritization.** Same lens as the main flag prioritization: spend impact multiplied by confidence the pattern is real. The order below is an operator ruling, 2026-09-02.

1. **Incorrect information or a compliance issue on a live ad or in-use asset:** this ranks first, always. It is a trust and a bar-advertising risk on a legal client.
2. **Brand or message mismatch on an in-use asset.**
3. **Thin coverage** on a PMax asset group.
4. **Fatigue candidates** on meaningful volume: a refresh, not an emergency.
5. **Missing coverage on a PMax asset group** with zero image assets: a LOW finding, because Performance Max can run without images.
6. **Uploaded-but-unused assets:** cleanup or deploy, rarely urgent.

### API-sourceable vs. manual/visual review: be explicit

Mark what is and is not API-sourceable, per the blind-spot protocol in `references/diagnosis-trees.md`. State this on every creative finding so the operator knows the source tier:

| Item                                          | Source tier                                                                                    |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Asset inventory (what exists)                 | **API-sourceable**: `get_image_assets`                                                         |
| Asset → campaign/ad-group usage mapping       | **API-sourceable**: `get_asset_usage`                                                          |
| Coverage gaps (missing / thin / unused)       | **API-sourceable**: derived from the two tools above + the GAQL campaign list                  |
| Image file itself                             | **API-sourceable**: `download_image_asset`                                                     |
| Image content / quality first read            | **API-assisted (vision)**: `analyze_image_assets`; treat as a strong read, not a final call    |
| On-brand / compliance / message-match verdict | **Manual / visual review**: vision informs it; the final legal-brand call is a human review    |
| Per-asset performance                         | **Partially API-sourceable**: thin in the API; fall back to ad-group/campaign proxy and say so |
| How the asset renders in a live placement     | **NOT API-sourceable**: blind spot; request a screenshot per the protocol below                |

For anything in the bottom three rows, do not present it as auto-pulled. Use the blind-spot protocol when the rendered placement is what's in question:

```text
BLIND SPOT: how this image renders in a live PMax placement is not visible via the API.
Please share a screenshot of the asset as served (Ad Preview, or the Assets report with the image shown), so brand/legibility/crop can be confirmed in placement.
```

**Tracking-QA parallel:** a confident brand or compliance verdict on a legal client that rests only on a vision model is worse than flagging it for human review. When in doubt on a brand or bar-advertising-adjacent call, surface it as a manual-review item, not a finished verdict.
