"""Validate canonical poem JSONL records for Phase 1 Step 2."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "poem_id",
    "title",
    "author",
    "dynasty",
    "genre",
    "content",
    "features",
    "ai_annotations",
    "source",
    "review",
}

REQUIRED_FEATURE_GROUPS = {
    "raw_mapped",
    "rule_derived",
    "weak_signals",
    "semantic",
    "behavior_derived",
}

REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "source_name",
    "source_file",
    "source_record_index",
    "license",
    "data_entry_method",
    "source_verification_status",
    "provenance_note",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate_record(record: dict[str, Any], line_no: int, seen_ids: set[str]) -> None:
    missing = REQUIRED_TOP_LEVEL - record.keys()
    if missing:
        fail(f"line {line_no}: missing top-level fields: {sorted(missing)}")

    if record["schema_version"] != "poem.v0":
        fail(f"line {line_no}: schema_version must be poem.v0")

    poem_id = record["poem_id"]
    if not isinstance(poem_id, str) or not poem_id.startswith("poem_"):
        fail(f"line {line_no}: poem_id must be a stable string starting with poem_")
    if poem_id in seen_ids:
        fail(f"line {line_no}: duplicate poem_id {poem_id}")
    seen_ids.add(poem_id)

    author = record["author"]
    if not isinstance(author, dict) or not author.get("name"):
        fail(f"line {line_no}: author.name is required")

    content = record["content"]
    if not isinstance(content, dict):
        fail(f"line {line_no}: content must be an object")
    paragraphs = content.get("paragraphs")
    lines = content.get("lines")
    if not isinstance(paragraphs, list) or not paragraphs:
        fail(f"line {line_no}: content.paragraphs must be a non-empty list")
    if not isinstance(lines, list) or not lines:
        fail(f"line {line_no}: content.lines must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in lines):
        fail(f"line {line_no}: content.lines must contain non-empty strings")

    features = record["features"]
    if not isinstance(features, dict):
        fail(f"line {line_no}: features must be an object")
    missing_groups = REQUIRED_FEATURE_GROUPS - features.keys()
    if missing_groups:
        fail(f"line {line_no}: missing feature groups: {sorted(missing_groups)}")

    rule_derived = features["rule_derived"]
    if not isinstance(rule_derived, dict):
        fail(f"line {line_no}: features.rule_derived must be an object")
    if rule_derived.get("line_count") != len(lines):
        fail(
            f"line {line_no}: rule_derived.line_count "
            f"{rule_derived.get('line_count')} does not match content.lines {len(lines)}"
        )
    if "char_count" not in rule_derived:
        fail(f"line {line_no}: rule_derived.char_count is required")

    for object_field in ("source", "review", "ai_annotations"):
        if not isinstance(record[object_field], dict):
            fail(f"line {line_no}: {object_field} must be an object")

    source = record["source"]
    missing_source_fields = REQUIRED_SOURCE_FIELDS - source.keys()
    if missing_source_fields:
        fail(f"line {line_no}: missing source fields: {sorted(missing_source_fields)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="data/samples/poems.sample.jsonl")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        fail(f"file not found: {path}")

    seen_ids: set[str] = set()
    count = 0
    with path.open(encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {line_no}: invalid JSON: {exc}") from exc
            if not isinstance(record, dict):
                fail(f"line {line_no}: expected a JSON object")
            validate_record(record, line_no=line_no, seen_ids=seen_ids)
            count += 1

    if count == 0:
        fail("no records found")
    print(f"Validated {count} poem records from {path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
