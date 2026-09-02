import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

import journal


class JournalTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.original_data_root = journal.DATA_ROOT
        journal.DATA_ROOT = Path(self.tempdir.name) / "GoogleAds"
        (journal.DATA_ROOT / "journal").mkdir(parents=True)
        (journal.DATA_ROOT / "journal" / "vocab.json").write_text(
            journal.BUNDLED_VOCAB_PATH.read_text(encoding="utf-8"), encoding="utf-8"
        )

    def tearDown(self):
        journal.DATA_ROOT = self.original_data_root
        self.tempdir.cleanup()

    def entry(self, **overrides):
        data = {
            "id": "example-family-law-20260701-01",
            "ts": "2026-07-01T09:00:00+07:00",
            "account": "example-family-law",
            "platform": "google",
            "type": "obs",
            "status": "closed",
            "source": {"actor": "operator", "ref": None},
            "session": "2026-07-01-example-family-law",
            "tags": ["watch"],
            "body": "Synthetic observation.",
        }
        data.update(overrides)
        return data

    def test_schema_happy_path(self):
        self.assertEqual(
            journal._schema_errors(self.entry(), journal.load_schema()), []
        )

    def test_schema_decision_requires_complete_expect(self):
        missing = self.entry(type="decision", status="open")
        errors = journal._schema_errors(missing, journal.load_schema())
        self.assertTrue(any("expect" in error for error in errors))
        missing["expect"] = {"statement": "Hold CPL.", "review_by": "not-a-date"}
        errors = journal._schema_errors(missing, journal.load_schema())
        self.assertTrue(any("valid ISO date" in error for error in errors))

    def test_schema_outcome_requires_re_and_verdict(self):
        outcome = self.entry(type="outcome")
        errors = journal._schema_errors(outcome, journal.load_schema())
        self.assertTrue(any("re" in error for error in errors))
        self.assertTrue(any("verdict" in error for error in errors))

    def test_append_assigns_per_day_sequence(self):
        first = self.entry()
        first.pop("id")
        second = self.entry(body="Second synthetic observation.")
        second.pop("id")
        appended_one = journal.append_entry("example-family-law", first)
        appended_two = journal.append_entry("example-family-law", second)
        self.assertEqual(appended_one["id"], "example-family-law-20260701-01")
        self.assertEqual(appended_two["id"], "example-family-law-20260701-02")

    def test_due_date_math_and_outcome_closure(self):
        decision = self.entry(
            type="decision",
            status="open",
            expect={"statement": "Hold CPL.", "review_by": "2026-07-08"},
        )
        journal.append_entry("example-family-law", decision)
        self.assertEqual(
            [
                item["id"]
                for item in journal.due_entries("example-family-law", date(2026, 7, 8))
            ],
            [decision["id"]],
        )
        outcome = self.entry(
            id="example-family-law-20260708-01",
            ts="2026-07-08T09:00:00+07:00",
            type="outcome",
            status="closed",
            re=[decision["id"]],
            verdict="met",
            session="2026-07-08-example-family-law",
        )
        journal.append_entry("example-family-law", outcome)
        self.assertEqual(
            journal.due_entries("example-family-law", date(2026, 7, 9)), []
        )

    def test_render_is_byte_deterministic(self):
        fixture = Path(__file__).parent / "fixtures" / "example-family-law.jsonl"
        target = journal.DATA_ROOT / "journal" / "example-family-law.jsonl"
        target.write_bytes(fixture.read_bytes())
        note_path, session_paths = journal.render("example-family-law")
        first = {note_path: note_path.read_bytes()}
        first.update({path: path.read_bytes() for path in session_paths})
        note_path, session_paths = journal.render("example-family-law")
        second = {note_path: note_path.read_bytes()}
        second.update({path: path.read_bytes() for path in session_paths})
        self.assertEqual(first, second)

    def test_referential_failure_reports_missing_target(self):
        outcome = self.entry(
            type="outcome",
            re=["example-family-law-20260630-99"],
            verdict="unclear",
        )
        path = journal.DATA_ROOT / "journal" / "example-family-law.jsonl"
        errors = journal.validate_records(path, [(outcome, 1)])
        self.assertTrue(any("re target does not exist" in error for error in errors))

    def test_unknown_tag_and_duplicate_id_fail(self):
        first = self.entry(tags=["not-in-vocab"])
        second = self.entry(body="Duplicate id.")
        path = journal.DATA_ROOT / "journal" / "example-family-law.jsonl"
        errors = journal.validate_records(path, [(first, 1), (second, 2)])
        self.assertTrue(any("unknown vocabulary tag" in error for error in errors))
        self.assertTrue(any("duplicate id" in error for error in errors))

    def config_override_entry(self, **overrides):
        data = {
            "type": "rule",
            "status": "open",
            "tags": ["config-override"],
            "config_override": {
                "setting": "campaign.geo_target_type_setting.positive_geo_target_type",
                "account_value": "PRESENCE",
                "agency_default": "PRESENCE_OR_INTEREST",
                "applies_to": "Search - Family Law",
            },
            "body": "Presence-only on this campaign only; interest traffic produced no intake contact.",
        }
        data.update(overrides)
        return self.entry(**data)

    def test_config_override_schema_and_tag_pairing(self):
        entry = self.config_override_entry()
        self.assertEqual(journal._schema_errors(entry, journal.load_schema()), [])

        path = journal.DATA_ROOT / "journal" / "example-family-law.jsonl"
        self.assertEqual(journal.validate_records(path, [(entry, 1)]), [])

        untagged = self.config_override_entry(tags=["watch"])
        errors = journal.validate_records(path, [(untagged, 1)])
        self.assertTrue(
            any("requires the 'config-override' tag" in error for error in errors)
        )

        objectless = self.entry(type="rule", status="open", tags=["config-override"])
        errors = journal.validate_records(path, [(objectless, 1)])
        self.assertTrue(
            any("requires a config_override object" in error for error in errors)
        )

        wrong_type = self.config_override_entry(type="obs", status="closed")
        errors = journal._schema_errors(wrong_type, journal.load_schema())
        self.assertTrue(any("must equal 'rule'" in error for error in errors))

    def test_config_overrides_render_in_their_own_section(self):
        journal.append_entry("example-family-law", self.config_override_entry())
        note_path, _ = journal.render("example-family-law")
        rendered = note_path.read_text(encoding="utf-8")
        self.assertIn("## Config overrides", rendered)
        self.assertIn(
            "campaign.geo_target_type_setting.positive_geo_target_type", rendered
        )
        self.assertIn("account `PRESENCE` (baseline `PRESENCE_OR_INTEREST`)", rendered)
        self.assertIn("scope: Search - Family Law", rendered)
        self.assertIn("approved by operator on 2026-07-01", rendered)
        overrides_block, rules_block = rendered.split("## Standing Rules", 1)
        self.assertIn("example-family-law-20260701-01", overrides_block)
        self.assertNotIn("example-family-law-20260701-01", rules_block)

    def test_note_without_overrides_says_so(self):
        journal.append_entry("example-family-law", self.entry())
        note_path, _ = journal.render("example-family-law")
        rendered = note_path.read_text(encoding="utf-8")
        self.assertIn("## Config overrides", rendered)
        self.assertIn("agency-defaults.md", rendered)

    def test_jsonl_parse_error_has_line_number(self):
        path = journal.DATA_ROOT / "journal" / "example-family-law.jsonl"
        path.write_text(json.dumps(self.entry()) + "\n{broken\n", encoding="utf-8")
        records, errors = journal.read_journal(path)
        self.assertEqual(len(records), 1)
        self.assertTrue(any("line 2" in error for error in errors))

    def test_id_date_must_match_bangkok_timestamp(self):
        wrong_day = self.entry(id="example-family-law-20260630-01")
        path = journal.DATA_ROOT / "journal" / "example-family-law.jsonl"
        errors = journal.validate_records(path, [(wrong_day, 1)])
        self.assertTrue(
            any("does not match Bangkok ts date" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
