#!/usr/bin/env python3
"""ci-generic-leak-check.py: public-safe, generic pre-publish PII check.

Runs in CI on every push/PR to this public repo. It knows nothing about
any specific client, firm, or account, it only looks for SHAPES that
real account data tends to take:

  1. 10-digit numbers shaped like a Google Ads customer ID
  2. phone-number-shaped strings (xxx-xxx-xxxx / (xxx) xxx-xxxx / xxx.xxx.xxxx)
  3. email addresses that are not obviously placeholder addresses

A small ALLOWLIST below covers this repo's own documented placeholders
(see SKILL.md's ID table and evals/fixtures/). Nothing in this file or
its allowlist is client-specific, that pairing lives outside this repo
in a private denylist run separately before any release
(public-repo-leak-gate.py; see the internal wiki's Shared Capabilities
page). This script is a coarse net, not the release gate.

stdlib only. Exit 1 on any un-allowlisted hit.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Files/dirs this check does not need to look at (build artifacts, vendored
# lockfiles, and this checker's own source, which necessarily contains the
# patterns as regex literals rather than as real data).
SKIP_PATH_PARTS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
SKIP_FILES = {"ci-generic-leak-check.py", "package-lock.json", "uv.lock", "poetry.lock"}

PHONE_RE = re.compile(r"\b\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b")
TEN_DIGIT_RE = re.compile(r"\b\d{10}\b")
EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")

# Documented, generic placeholders, see SKILL.md's account-ID table and
# evals/fixtures/README.md. All-repeated-digit IDs (1111111111 ... ) are
# the house convention for synthetic fixture IDs.
ALLOWLISTED_10DIGIT = {str(d) * 10 for d in range(10)} | {"1234567890"}
ALLOWLISTED_EMAIL_SUFFIXES = ("@example.com", ".example.com")


def looks_like_date_or_timestamp(digits: str) -> bool:
    n = int(digits)
    if 1_000_000_000 <= n <= 2_000_000_000:  # unix epoch, ~2001-2033
        return True
    year, month, day = digits[0:4], digits[4:6], digits[6:8]
    if 1990 <= int(year) <= 2035 and 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
        return True
    return False


def tracked_files() -> list[Path]:
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "-z", "-co", "--exclude-standard"],
        capture_output=True,
        check=True,
    ).stdout.decode(errors="replace")
    return [REPO_ROOT / p for p in out.split("\0") if p]


def main() -> int:
    findings: list[str] = []

    for fp in tracked_files():
        rel = fp.relative_to(REPO_ROOT)
        if any(part in SKIP_PATH_PARTS for part in rel.parts):
            continue
        if fp.name in SKIP_FILES:
            continue
        try:
            data = fp.read_bytes()
        except OSError:
            continue
        if b"\0" in data[:8192]:
            continue  # binary
        text = data.decode("utf-8", errors="replace")

        for idx, line in enumerate(text.splitlines(), start=1):
            for m in PHONE_RE.finditer(line):
                findings.append(f"{rel}:{idx}: phone-shaped: {m.group(0)}")
            for m in TEN_DIGIT_RE.finditer(line):
                digits = m.group(0)
                if digits in ALLOWLISTED_10DIGIT:
                    continue
                if looks_like_date_or_timestamp(digits):
                    continue
                findings.append(f"{rel}:{idx}: 10-digit customer-ID-shaped: {digits}")
            for m in EMAIL_RE.finditer(line):
                email = m.group(0)
                if email.lower().endswith(ALLOWLISTED_EMAIL_SUFFIXES):
                    continue
                findings.append(f"{rel}:{idx}: email address: {email}")

    if not findings:
        print("ci-generic-leak-check: CLEAN")
        return 0

    print(f"ci-generic-leak-check: {len(findings)} finding(s)\n")
    for f in findings:
        print(f"  {f}")
    print(
        "\nIf this is a documented placeholder, add it to the allowlist in "
        "scripts/ci-generic-leak-check.py with a comment explaining why. "
        "If this is real account data, remove it before merging, do not "
        "widen the allowlist to make it pass."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
