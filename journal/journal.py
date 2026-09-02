#!/usr/bin/env python3
"""Append, validate, query, render, and summarize Google Ads journals.

Journals, rendered notes, and session logs live under a data root. Set
PPC_JOURNAL_ROOT to put that root wherever you keep account data, which
for an operator is normally a private directory outside this repo. With
no override the root is the repo itself, so journals land in ./journal.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone, tzinfo
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
# Where journals, rendered notes, and session logs live. PPC_JOURNAL_ROOT
# overrides, and an operator holding real account data should set it to a
# private directory outside this repo. The default root is the repo itself,
# so an unconfigured run writes ./journal/<slug>.jsonl next to this file.


def _data_root() -> Path:
    env = os.environ.get("PPC_JOURNAL_ROOT")
    if env:
        return Path(env).expanduser()
    return REPO_ROOT


DATA_ROOT = _data_root()
SCHEMA_PATH = SCRIPT_DIR / "schema.json"
BUNDLED_VOCAB_PATH = SCRIPT_DIR / "vocab.json"


def _operator_tz() -> tzinfo:
    """Operator timezone: PPC_JOURNAL_TZ (IANA name such as America/New_York),
    else the machine's local zone. Entry ids and 'today' are computed in it."""
    name = os.environ.get("PPC_JOURNAL_TZ")
    if name:
        try:
            return ZoneInfo(name)
        except Exception:  # noqa: BLE001
            pass
    return datetime.now().astimezone().tzinfo or timezone.utc


LOCAL_TZ = _operator_tz()
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
TYPE_ORDER = ("obs", "flag", "decision", "change", "outcome", "rule", "context")
VERDICT_ORDER = ("met", "not_met", "mixed", "unclear")

# Schema v1 platform values. They are not valid under schema v2 and are kept
# here only so `migrate` can carry an old journal forward.
LEGACY_PLATFORMS = {"callrail": "call-tracking", "ga4": "analytics", "hubspot": "crm"}
LEGACY_PLATFORM_FALLBACK = "other"


class JournalError(Exception):
    """A user-fixable journal error."""


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    return True


def _format_error(value: str, fmt: str) -> str | None:
    try:
        if fmt == "date":
            parsed = date.fromisoformat(value)
            if parsed.isoformat() != value:
                return "must be an ISO date (YYYY-MM-DD)"
        elif fmt == "date-time":
            parsed_dt = datetime.fromisoformat(value)
            if parsed_dt.tzinfo is None or parsed_dt.utcoffset() is None:
                return "must be an ISO 8601 date-time with an offset"
    except ValueError:
        return f"must be a valid ISO {fmt}"
    return None


def _schema_errors(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Validate the JSON Schema subset used by schema.json."""
    errors: list[str] = []

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
        return errors
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: must be one of {schema['enum']}")
        return errors

    expected_types = schema.get("type")
    if expected_types is not None:
        if isinstance(expected_types, str):
            expected_types = [expected_types]
        if not any(_json_type_matches(value, item) for item in expected_types):
            errors.append(f"{path}: must have type {' or '.join(expected_types)}")
            return errors

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")

        properties = schema.get("properties", {})
        for key, item in value.items():
            child_path = f"{path}.{key}"
            if key in properties:
                errors.extend(_schema_errors(item, properties[key], child_path))
                continue
            additional = schema.get("additionalProperties", True)
            if additional is False:
                errors.append(f"{path}: unexpected property {key!r}")
            elif isinstance(additional, dict):
                errors.extend(_schema_errors(item, additional, child_path))

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: must contain at least {schema['minItems']} item(s)")
        if schema.get("uniqueItems"):
            seen: set[str] = set()
            for item in value:
                marker = json.dumps(item, sort_keys=True, ensure_ascii=False)
                if marker in seen:
                    errors.append(f"{path}: array items must be unique")
                    break
                seen.add(marker)
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(_schema_errors(item, item_schema, f"{path}[{index}]"))

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(
                f"{path}: must contain at least {schema['minLength']} character(s)"
            )
        pattern = schema.get("pattern")
        if pattern and not re.search(pattern, value):
            errors.append(f"{path}: does not match {pattern!r}")
        fmt = schema.get("format")
        if fmt:
            error = _format_error(value, fmt)
            if error:
                errors.append(f"{path}: {error}")

    for branch in schema.get("allOf", []):
        errors.extend(_schema_errors(value, branch, path))

    conditional = schema.get("if")
    if isinstance(conditional, dict):
        matched = not _schema_errors(value, conditional, path)
        selected = schema.get("then") if matched else schema.get("else")
        if isinstance(selected, dict):
            errors.extend(_schema_errors(value, selected, path))

    return errors


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def platform_values(schema: dict[str, Any] | None = None) -> set[str]:
    """The platform values the current schema accepts."""
    resolved = schema if schema is not None else load_schema()
    return set(resolved["properties"]["platform"]["enum"])


def vocab_path() -> Path:
    data_vocab = DATA_ROOT / "journal" / "vocab.json"
    return data_vocab if data_vocab.exists() else BUNDLED_VOCAB_PATH


def load_vocab() -> set[str]:
    path = vocab_path()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise JournalError(f"cannot load vocabulary {path}: {exc}") from exc
    if not isinstance(data, list):
        raise JournalError(f"{path}: vocabulary root must be an array")
    tags: set[str] = set()
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict) or set(item) != {"tag", "meaning", "when_to_use"}:
            raise JournalError(
                f"{path}: item {index} must contain exactly tag, meaning, when_to_use"
            )
        if not all(isinstance(item[key], str) and item[key] for key in item):
            raise JournalError(f"{path}: item {index} values must be non-empty strings")
        if item["tag"] in tags:
            raise JournalError(f"{path}: duplicate tag {item['tag']!r}")
        tags.add(item["tag"])
    return tags


def journal_path(slug: str) -> Path:
    if not SLUG_RE.fullmatch(slug):
        raise JournalError(f"invalid account slug: {slug!r}")
    return DATA_ROOT / "journal" / f"{slug}.jsonl"


def read_journal(path: Path) -> tuple[list[tuple[dict[str, Any], int]], list[str]]:
    records: list[tuple[dict[str, Any], int]] = []
    errors: list[str] = []
    if not path.exists():
        return records, [f"{path}: journal does not exist"]
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return records, [f"{path}: cannot read journal: {exc}"]
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            errors.append(f"{path}:line {line_number}: blank lines are not valid JSONL")
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(
                f"{path}:line {line_number}: JSON parse error at column {exc.colno}: {exc.msg}"
            )
            continue
        if not isinstance(entry, dict):
            errors.append(f"{path}:line {line_number}: entry must be a JSON object")
            continue
        records.append((entry, line_number))
    return records, errors


def _local_day(ts: object) -> str | None:
    try:
        parsed = datetime.fromisoformat(str(ts)) if isinstance(ts, str) else None
    except (TypeError, ValueError):
        return None
    if parsed is None or parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(LOCAL_TZ).strftime("%Y%m%d")


def validate_records(
    path: Path,
    records: list[tuple[dict[str, Any], int]],
    vocab: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    schema = load_schema()
    platforms = platform_values(schema)
    legacy_platforms: Counter[str] = Counter()
    known_tags = vocab if vocab is not None else load_vocab()
    slug = path.stem
    ids: dict[str, int] = {}

    for entry, line_number in records:
        prefix = f"{path}:line {line_number}"
        entry_platform = entry.get("platform")
        is_legacy_platform = False
        if isinstance(entry_platform, str) and entry_platform not in platforms:
            is_legacy_platform = True
            legacy_platforms[entry_platform] += 1
        for error in _schema_errors(entry, schema):
            if is_legacy_platform and error.startswith("$.platform: must be one of"):
                continue
            errors.append(f"{prefix}: {error}")

        entry_id = entry.get("id")
        if isinstance(entry_id, str):
            if entry_id in ids:
                errors.append(
                    f"{prefix}: duplicate id {entry_id!r}; first seen on line {ids[entry_id]}"
                )
            else:
                ids[entry_id] = line_number

        if entry.get("account") != slug:
            errors.append(f"{prefix}: account must equal journal slug {slug!r}")
        if isinstance(entry_id, str) and not entry_id.startswith(f"{slug}-"):
            errors.append(f"{prefix}: id must start with {slug!r}")

        local_day = _local_day(entry.get("ts"))
        if local_day and isinstance(entry_id, str):
            match = re.search(r"-([0-9]{8})-[0-9]{2}$", entry_id)
            if match and match.group(1) != local_day:
                errors.append(
                    f"{prefix}: id date {match.group(1)} does not match Bangkok ts date {local_day}"
                )

        session = entry.get("session")
        if isinstance(session, str) and len(session) >= 11:
            session_slug = session[11:]
            if session_slug != slug and not session_slug.startswith(f"{slug}-"):
                errors.append(f"{prefix}: session must name account slug {slug!r}")

        tags = entry.get("tags", [])
        for tag in tags:
            if isinstance(tag, str) and tag not in known_tags:
                errors.append(f"{prefix}: unknown vocabulary tag {tag!r}")

        tagged_override = isinstance(tags, list) and "config-override" in tags
        if entry.get("config_override") is not None and not tagged_override:
            errors.append(
                f"{prefix}: config_override requires the 'config-override' tag"
            )
        if tagged_override and entry.get("config_override") is None:
            errors.append(
                f"{prefix}: the 'config-override' tag requires a config_override object"
            )

        if (
            entry.get("type") in {"decision", "change"}
            and entry.get("status") == "open"
        ):
            review_by = entry.get("expect", {}).get("review_by")
            try:
                date.fromisoformat(review_by)
            except (TypeError, ValueError):
                errors.append(
                    f"{prefix}: open {entry.get('type')} requires a parseable expect.review_by"
                )

    known_ids = set(ids)
    for entry, line_number in records:
        prefix = f"{path}:line {line_number}"
        for target in entry.get("re", []):
            if isinstance(target, str) and target not in known_ids:
                errors.append(f"{prefix}: re target does not exist: {target!r}")

    if legacy_platforms:
        detail = ", ".join(
            f"{name}={count}" for name, count in sorted(legacy_platforms.items())
        )
        errors.append(
            f"{path}: legacy platform values found: run journal.py migrate. {detail}"
        )
    return errors


def validate_paths(paths: Iterable[Path]) -> tuple[list[str], int]:
    errors: list[str] = []
    count = 0
    vocab = load_vocab()
    global_ids: dict[str, tuple[Path, int]] = {}
    for path in paths:
        records, parse_errors = read_journal(path)
        errors.extend(parse_errors)
        errors.extend(validate_records(path, records, vocab))
        count += len(records)
        for entry, line_number in records:
            entry_id = entry.get("id")
            if not isinstance(entry_id, str):
                continue
            if entry_id in global_ids and global_ids[entry_id][0] != path:
                first_path, first_line = global_ids[entry_id]
                errors.append(
                    f"{path}:line {line_number}: duplicate global id {entry_id!r}; "
                    f"first seen at {first_path}:line {first_line}"
                )
            else:
                global_ids[entry_id] = (path, line_number)
    return errors, count


def migrate_journal(path: Path) -> Counter[str]:
    """Rewrite schema v1 platform values in place, writing <name>.bak first.

    Returns a count per rewrite, keyed 'old -> new'. A journal with nothing to
    migrate is left untouched and no backup is written.
    """
    records, parse_errors = read_journal(path)
    if parse_errors:
        raise JournalError("\n".join(parse_errors))
    platforms = platform_values()
    changed: Counter[str] = Counter()
    for entry, _ in records:
        platform = entry.get("platform")
        if not isinstance(platform, str) or platform in platforms:
            continue
        replacement = LEGACY_PLATFORMS.get(platform, LEGACY_PLATFORM_FALLBACK)
        entry["platform"] = replacement
        changed[f"{platform} -> {replacement}"] += 1
    if not changed:
        return changed
    path.with_name(path.name + ".bak").write_bytes(path.read_bytes())
    lines = [
        json.dumps(entry, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        for entry, _ in records
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return changed


def list_journals() -> list[Path]:
    directory = DATA_ROOT / "journal"
    return sorted(directory.glob("*.jsonl")) if directory.exists() else []


def _default_status(entry_type: str) -> str:
    return "closed" if entry_type in {"obs", "outcome", "context"} else "open"


def entry_from_flags(args: argparse.Namespace) -> dict[str, Any]:
    if not args.type:
        raise JournalError(
            "flags mode requires --type; otherwise pipe a JSON object to stdin"
        )
    entry: dict[str, Any] = {
        "platform": args.platform,
        "type": args.type,
        "status": args.status or _default_status(args.type),
        "source": {"actor": args.source_actor, "ref": args.source_ref},
        "session": args.session,
    }
    if args.ts:
        entry["ts"] = args.ts
    if args.body is not None:
        entry["body"] = args.body
    if args.tag:
        entry["tags"] = args.tag
    if args.scope_level or args.scope_id or args.scope_name:
        entry["scope"] = {
            "level": args.scope_level or "account",
            "ids": args.scope_id or [],
            "names": args.scope_name or [],
        }
    if args.expect_statement is not None or args.review_by is not None:
        entry["expect"] = {
            "statement": args.expect_statement,
            "review_by": args.review_by,
        }
    if args.re:
        entry["re"] = args.re
    if args.verdict:
        entry["verdict"] = args.verdict
    if args.metrics_json:
        try:
            entry["metrics"] = json.loads(args.metrics_json)
        except json.JSONDecodeError as exc:
            raise JournalError(f"--metrics-json is invalid JSON: {exc}") from exc
    if args.config_override_json:
        try:
            entry["config_override"] = json.loads(args.config_override_json)
        except json.JSONDecodeError as exc:
            raise JournalError(
                f"--config-override-json is invalid JSON: {exc}"
            ) from exc
    if args.migrated:
        entry["migrated"] = True
    return entry


def _next_id(slug: str, ts: str, records: list[tuple[dict[str, Any], int]]) -> str:
    day = _local_day(ts)
    if day is None:
        raise JournalError("ts must be an ISO 8601 date-time with an offset")
    pattern = re.compile(rf"^{re.escape(slug)}-{day}-([0-9]{{2}})$")
    sequences = []
    for entry, _ in records:
        match = pattern.fullmatch(str(entry.get("id", "")))
        if match:
            sequences.append(int(match.group(1)))
    sequence = max(sequences, default=0) + 1
    if sequence > 99:
        raise JournalError(
            f"{slug} {day} has exhausted the two-digit id sequence (99/99 used)"
        )
    return f"{slug}-{day}-{sequence:02d}"


def append_entry(slug: str, entry: dict[str, Any]) -> dict[str, Any]:
    path = journal_path(slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        records, parse_errors = read_journal(path)
        if parse_errors:
            raise JournalError("\n".join(parse_errors))
    else:
        records = []

    candidate = dict(entry)
    candidate.setdefault("account", slug)
    candidate.setdefault("ts", datetime.now(LOCAL_TZ).isoformat(timespec="seconds"))
    candidate.setdefault("id", _next_id(slug, candidate["ts"], records))

    combined = records + [(candidate, len(records) + 1)]
    errors = validate_records(path, combined)
    if errors:
        raise JournalError("\n".join(errors))

    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(
            json.dumps(
                candidate, sort_keys=True, ensure_ascii=False, separators=(",", ":")
            )
        )
        handle.write("\n")
    return candidate


def _loaded_valid_entries(slug: str) -> list[dict[str, Any]]:
    path = journal_path(slug)
    records, parse_errors = read_journal(path)
    errors = parse_errors + validate_records(path, records)
    if errors:
        raise JournalError("\n".join(errors))
    return [entry for entry, _ in records]


def _resolved_targets(entries: list[dict[str, Any]]) -> set[str]:
    targets: set[str] = set()
    for entry in entries:
        if entry.get("type") == "outcome":
            targets.update(entry.get("re", []))
    return targets


def due_entries(slug: str, as_of: date) -> list[dict[str, Any]]:
    entries = _loaded_valid_entries(slug)
    resolved = _resolved_targets(entries)
    due: list[dict[str, Any]] = []
    for entry in entries:
        if entry.get("type") not in {"decision", "change"}:
            continue
        if entry.get("status") != "open" or entry.get("id") in resolved:
            continue
        review_by = date.fromisoformat(entry["expect"]["review_by"])
        if review_by <= as_of:
            due.append(entry)
    return sorted(due, key=lambda item: (item["expect"]["review_by"], item["id"]))


def _scope_one_liner(entry: dict[str, Any]) -> str:
    scope = entry.get("scope")
    if not scope:
        return "account"
    details = list(scope.get("names", [])) + [
        f"id:{item}" for item in scope.get("ids", [])
    ]
    return f"{scope['level']}: {', '.join(details)}" if details else scope["level"]


def _single_line(value: str) -> str:
    return " ".join(value.split())


def _entry_markdown(entry: dict[str, Any], include_verdict: bool = False) -> list[str]:
    heading = f"### `{entry['id']}`: {entry['type']}"
    if include_verdict:
        heading += f", {entry['verdict']}"
    lines = [heading, "", f"Scope: {_scope_one_liner(entry)}"]
    if entry.get("tags"):
        lines.append(f"Tags: {', '.join(entry['tags'])}")
    if entry.get("expect"):
        lines.append(f"Review by: {entry['expect']['review_by']}")
        lines.append(f"Expectation: {entry['expect']['statement']}")
    lines.extend(["", entry.get("body", "_No body._"), ""])
    return lines


def _config_override_markdown(entries: list[dict[str, Any]]) -> list[str]:
    """One line per overridden setting, plus its reason, sorted by setting path."""
    lines: list[str] = []
    for entry in sorted(
        entries, key=lambda item: (item["config_override"]["setting"], item["id"])
    ):
        override = entry["config_override"]
        source = entry.get("source", {})
        actor = source.get("actor", "unknown")
        ref = source.get("ref")
        approved = f"{actor} ({ref})" if ref else actor
        lines.append(
            f"- `{override['setting']}`: account `{override['account_value']}`"
            f" (baseline `{override['agency_default']}`),"
            f" scope: {override.get('applies_to', 'account-wide')},"
            f" approved by {approved} on {entry['ts'][:10]}, entry `{entry['id']}`"
        )
        body = _single_line(entry.get("body", ""))
        if body:
            lines.append(f"  {body}")
    lines.append("")
    return lines


def _note_markdown(slug: str, entries: list[dict[str, Any]]) -> str:
    source = f"{DATA_ROOT.name}/journal/{slug}.jsonl"
    resolved = _resolved_targets(entries)
    open_entries = [
        entry
        for entry in entries
        if entry.get("status") == "open" and entry.get("id") not in resolved
    ]
    overrides = [
        entry
        for entry in open_entries
        if entry.get("type") == "rule" and entry.get("config_override")
    ]
    override_ids = {entry["id"] for entry in overrides}
    rules = sorted(
        (
            entry
            for entry in open_entries
            if entry.get("type") == "rule" and entry["id"] not in override_ids
        ),
        key=lambda item: (item["ts"], item["id"]),
    )
    pending = [
        entry
        for entry in open_entries
        if entry.get("type") in {"decision", "change", "flag"}
    ]
    pending.sort(
        key=lambda item: (
            item.get("expect", {}).get("review_by", "9999-12-31"),
            item["ts"],
            item["id"],
        )
    )
    outcomes = sorted(
        (entry for entry in entries if entry.get("type") == "outcome"),
        key=lambda item: (item["ts"], item["id"]),
        reverse=True,
    )[:10]
    contexts = sorted(
        (entry for entry in open_entries if entry.get("type") == "context"),
        key=lambda item: (item["ts"], item["id"]),
    )

    lines = [
        f"<!-- GENERATED FILE: DO NOT HAND-EDIT. Source: {source} -->",
        "",
        f"# Account Notes: {slug}",
        "",
        "## Config overrides",
        "",
    ]
    if overrides:
        lines.extend(_config_override_markdown(overrides))
    else:
        lines.extend(
            [
                "_None. Every setting is expected to match `references/agency-defaults.md`._",
                "",
            ]
        )

    lines.extend(["## Standing Rules", ""])
    if rules:
        for entry in rules:
            lines.extend(_entry_markdown(entry))
    else:
        lines.extend(["_None._", ""])

    lines.extend(["## Pending", ""])
    if not pending:
        lines.extend(["_None._", ""])
    else:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for entry in pending:
            grouped[entry.get("expect", {}).get("review_by", "No review date")].append(
                entry
            )
        for review_by in sorted(
            grouped, key=lambda item: (item == "No review date", item)
        ):
            lines.extend([f"### Review by {review_by}", ""])
            for entry in grouped[review_by]:
                detail = _entry_markdown(entry)
                detail[0] = detail[0].replace("### ", "#### ", 1)
                lines.extend(detail)

    lines.extend(["## Recent Outcomes", ""])
    if outcomes:
        for entry in outcomes:
            lines.extend(_entry_markdown(entry, include_verdict=True))
    else:
        lines.extend(["_None._", ""])

    lines.extend(["## Context", ""])
    if contexts:
        for entry in contexts:
            lines.extend(_entry_markdown(entry))
    else:
        lines.extend(["_None._", ""])

    lines.extend(
        [
            "---",
            "",
            f"Generated from `{source}`. Entry count: {len(entries)}.",
            "",
        ]
    )
    return "\n".join(lines)


def _session_markdown(
    slug: str, session: str, entries: list[dict[str, Any]], journal_source: str
) -> str:
    ordered = sorted(entries, key=lambda item: (item["ts"], item["id"]))
    lines = [
        f"<!-- GENERATED FILE: DO NOT HAND-EDIT. Source: {journal_source} -->",
        "",
        f"# Session Log: {session}",
        "",
    ]
    for entry_type in TYPE_ORDER:
        grouped = [entry for entry in ordered if entry.get("type") == entry_type]
        if not grouped:
            continue
        lines.extend([f"## {entry_type.replace('_', ' ').title()}", ""])
        for entry in grouped:
            lines.extend(
                _entry_markdown(entry, include_verdict=entry_type == "outcome")
            )
    lines.extend(
        [
            "---",
            "",
            f"Generated from `{journal_source}`. Entry count: {len(entries)}.",
            "",
        ]
    )
    return "\n".join(lines)


def render(slug: str) -> tuple[Path, list[Path]]:
    entries = _loaded_valid_entries(slug)
    notes_path = DATA_ROOT / "notes" / f"{slug}.md"
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    notes_path.write_text(_note_markdown(slug, entries), encoding="utf-8", newline="\n")

    by_session: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        by_session[entry["session"]].append(entry)
    journal_source = f"{DATA_ROOT.name}/journal/{slug}.jsonl"
    session_paths: list[Path] = []
    session_dir = DATA_ROOT / "session-logs"
    session_dir.mkdir(parents=True, exist_ok=True)
    for session in sorted(by_session):
        path = session_dir / f"{session}.md"
        path.write_text(
            _session_markdown(slug, session, by_session[session], journal_source),
            encoding="utf-8",
            newline="\n",
        )
        session_paths.append(path)
    return notes_path, session_paths


def stats_lines(slug: str) -> list[str]:
    entries = _loaded_valid_entries(slug)
    by_id = {entry["id"]: entry for entry in entries}
    outcomes = [entry for entry in entries if entry.get("type") == "outcome"]
    overall = Counter(entry["verdict"] for entry in outcomes)
    per_tag: dict[str, Counter[str]] = defaultdict(Counter)
    for outcome in outcomes:
        tags = set(outcome.get("tags", []))
        for target in outcome.get("re", []):
            tags.update(by_id.get(target, {}).get("tags", []))
        for tag in tags:
            per_tag[tag][outcome["verdict"]] += 1

    def readout(counts: Counter[str]) -> str:
        return " / ".join(f"{verdict} {counts[verdict]}" for verdict in VERDICT_ORDER)

    lines = [slug, f"overall: {readout(overall)}"]
    lines.extend(f"tag={tag}: {readout(per_tag[tag])}" for tag in sorted(per_tag))
    return lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    append_parser = subparsers.add_parser("append", help="append one validated entry")
    append_parser.add_argument("slug")
    append_parser.add_argument("--ts")
    append_parser.add_argument("--platform", default="google")
    append_parser.add_argument("--type", choices=TYPE_ORDER)
    append_parser.add_argument("--status", choices=("open", "closed", "superseded"))
    append_parser.add_argument("--scope-level")
    append_parser.add_argument("--scope-id", action="append")
    append_parser.add_argument("--scope-name", action="append")
    append_parser.add_argument("--tag", action="append")
    append_parser.add_argument("--body")
    append_parser.add_argument("--expect-statement")
    append_parser.add_argument("--review-by")
    append_parser.add_argument("--re", action="append")
    append_parser.add_argument("--verdict", choices=VERDICT_ORDER)
    append_parser.add_argument("--source-actor", default="operator")
    append_parser.add_argument("--source-ref")
    append_parser.add_argument("--session")
    append_parser.add_argument("--metrics-json")
    append_parser.add_argument(
        "--config-override-json",
        help='config override object, e.g. \'{"setting":"...","account_value":"...","agency_default":"..."}\'',
    )
    append_parser.add_argument("--migrated", action="store_true")

    validate_parser = subparsers.add_parser("validate", help="validate journals")
    validate_parser.add_argument("slug", nargs="?")
    validate_parser.add_argument("--all", action="store_true")

    migrate_parser = subparsers.add_parser(
        "migrate", help="rewrite schema v1 platform values to the current enum"
    )
    migrate_parser.add_argument("slug", nargs="?")
    migrate_parser.add_argument("--all", action="store_true")

    due_parser = subparsers.add_parser("due", help="show due decisions and changes")
    due_parser.add_argument("slug")
    due_parser.add_argument("--as-of")

    render_parser = subparsers.add_parser(
        "render", help="render account and session notes"
    )
    render_parser.add_argument("slug")

    stats_parser = subparsers.add_parser("stats", help="summarize outcome verdicts")
    stats_parser.add_argument("slug", nargs="?")
    stats_parser.add_argument("--all", action="store_true")
    return parser


def _select_paths(slug: str | None, all_requested: bool) -> list[Path]:
    if bool(slug) == bool(all_requested):
        raise JournalError("provide exactly one account slug or --all")
    paths = list_journals() if all_requested else [journal_path(str(slug))]
    if not paths:
        raise JournalError("no journal files found")
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "append":
            if args.type:
                entry = entry_from_flags(args)
            else:
                raw = sys.stdin.read()
                if not raw.strip():
                    raise JournalError(
                        "stdin is empty; pipe one JSON object or use --type flags"
                    )
                try:
                    entry = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise JournalError(f"stdin JSON is invalid: {exc}") from exc
                if not isinstance(entry, dict):
                    raise JournalError("stdin JSON must be one object")
            appended = append_entry(args.slug, entry)
            print(appended["id"])
            return 0

        if args.command == "validate":
            paths = _select_paths(args.slug, args.all)
            errors, count = validate_paths(paths)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print(f"valid: {len(paths)} journal(s), {count} entries")
            return 0

        if args.command == "migrate":
            paths = _select_paths(args.slug, args.all)
            total = 0
            for path in paths:
                changed = migrate_journal(path)
                if not changed:
                    print(f"{path}: no legacy platform values")
                    continue
                moved = sum(changed.values())
                total += moved
                detail = ", ".join(
                    f"{name} ({count})" for name, count in sorted(changed.items())
                )
                print(
                    f"{path}: {moved} entries rewritten: {detail}. "
                    f"backup at {path.name}.bak"
                )
            print(f"migrated: {total} entries across {len(paths)} journal(s)")
            return 0

        if args.command == "due":
            as_of = (
                datetime.now(LOCAL_TZ).date()
                if not args.as_of
                else date.fromisoformat(args.as_of)
            )
            for entry in due_entries(args.slug, as_of):
                print(
                    " | ".join(
                        [
                            entry["id"],
                            entry["expect"]["review_by"],
                            _single_line(entry["expect"]["statement"]),
                            _scope_one_liner(entry),
                        ]
                    )
                )
            return 0

        if args.command == "render":
            note_path, session_paths = render(args.slug)
            print(f"rendered: {note_path} + {len(session_paths)} session log(s)")
            return 0

        if args.command == "stats":
            paths = _select_paths(args.slug, args.all)
            for index, path in enumerate(paths):
                if index:
                    print()
                print("\n".join(stats_lines(path.stem)))
            return 0
    except (JournalError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
