"""Inspect selected upstream files from chinese-poetry/chinese-poetry.

This script is Phase 1 Step 1: it probes the source schema and writes a
source-profile JSON that documents what the upstream corpus provides and what
must be produced by our own canonical schema / feature pipeline.

It intentionally samples only representative files instead of cloning the full
upstream repository.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

UPSTREAM_REPO = "https://github.com/chinese-poetry/chinese-poetry"
RAW_BASE = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master"

SOURCES = [
    {
        "source_id": "quantangshi_poet_tang_0",
        "kind": "poem",
        "dynasty": "唐",
        "genre": "诗",
        "url": f"{RAW_BASE}/%E5%85%A8%E5%94%90%E8%AF%97/poet.tang.0.json",
        "expected_join_key": "id",
    },
    {
        "source_id": "quantangshi_poet_song_0",
        "kind": "poem",
        "dynasty": "宋",
        "genre": "诗",
        "url": f"{RAW_BASE}/%E5%85%A8%E5%94%90%E8%AF%97/poet.song.0.json",
        "expected_join_key": "id",
    },
    {
        "source_id": "song_ci_0",
        "kind": "ci",
        "dynasty": "宋",
        "genre": "词",
        "url": f"{RAW_BASE}/%E5%AE%8B%E8%AF%8D/ci.song.0.json",
        "expected_join_key": None,
    },
    {
        "source_id": "authors_tang",
        "kind": "author",
        "dynasty": "唐",
        "genre": None,
        "url": f"{RAW_BASE}/%E5%85%A8%E5%94%90%E8%AF%97/authors.tang.json",
        "expected_join_key": "name",
    },
    {
        "source_id": "strains_poet_tang_0",
        "kind": "strains",
        "dynasty": "唐",
        "genre": "诗",
        "url": f"{RAW_BASE}/strains/json/poet.tang.0.json",
        "expected_join_key": "id",
    },
    {
        "source_id": "rank_poet_tang_0",
        "kind": "rank",
        "dynasty": "唐",
        "genre": "诗",
        "url": f"{RAW_BASE}/rank/poet/poet.tang.rank.0.json",
        "expected_join_key": "author+title",
    },
    {
        "source_id": "rank_ci_song_0",
        "kind": "rank",
        "dynasty": "宋",
        "genre": "词",
        "url": f"{RAW_BASE}/rank/ci/ci.song.rank.0.json",
        "expected_join_key": "author+rhythmic",
    },
]

TARGET_FEATURES = [
    "themes",
    "styles",
    "mood",
    "imagery",
    "difficulty",
    "familiarity",
    "quality",
    "suitable_contexts",
    "recommendation_seed",
    "translation",
    "annotations",
    "user_behavior",
    "embedding",
]


def fetch_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8-sig"))


def summarize_records(records: list[dict[str, Any]], sample_size: int) -> dict[str, Any]:
    field_counter: Counter[str] = Counter()
    type_examples: dict[str, str] = {}
    list_lengths: dict[str, list[int]] = defaultdict(list)

    for record in records:
        for key, value in record.items():
            field_counter[key] += 1
            type_examples.setdefault(key, type(value).__name__)
            if isinstance(value, list):
                list_lengths[key].append(len(value))

    total = len(records)
    fields = []
    for key, count in sorted(field_counter.items()):
        field: dict[str, Any] = {
            "name": key,
            "presence_ratio": round(count / total, 4) if total else 0,
            "example_type": type_examples[key],
        }
        if key in list_lengths:
            lengths = list_lengths[key]
            field["list_length"] = {
                "min": min(lengths),
                "max": max(lengths),
                "avg": round(sum(lengths) / len(lengths), 2),
            }
        fields.append(field)

    return {
        "record_count_in_sample_file": total,
        "fields": fields,
        "sample_records": records[:sample_size],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="data/processed/source_profile.chinese_poetry.json",
        help="Where to write the generated source profile JSON.",
    )
    parser.add_argument("--sample-size", type=int, default=2)
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    inspected_sources: list[dict[str, Any]] = []
    all_observed_fields: set[str] = set()

    for source in SOURCES:
        data = fetch_json(source["url"])
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data[:20]):
            raise TypeError(f"Expected a list of objects for {source['source_id']}")
        summary = summarize_records(data, sample_size=args.sample_size)
        all_observed_fields.update(field["name"] for field in summary["fields"])
        inspected_sources.append({**source, **summary})

    profile = {
        "profile_id": "chinese_poetry_source_profile_v0",
        "generated_at": datetime.now(UTC).isoformat(),
        "upstream_repo": UPSTREAM_REPO,
        "license_observed_in_repo": "MIT",
        "inspection_scope": "Representative upstream files only; not a full corpus import.",
        "inspected_sources": inspected_sources,
        "observed_raw_fields": sorted(all_observed_fields),
        "directly_usable_fields": [
            "author",
            "title",
            "paragraphs",
            "id",
            "rhythmic",
            "desc",
            "strains",
            "baidu",
            "so360",
            "bing",
            "bing_en",
            "google",
        ],
        "missing_target_features": TARGET_FEATURES,
        "gap_summary": {
            "content_body_layer": "Mostly covered for title/author/content, with Song Ci requiring rhythmic-to-cipai mapping.",
            "recommendation_feature_layer": "Not covered; must be generated through rule-derived, curated, LLM/Agent and behavior-derived pipelines.",
            "annotation_translation_layer": "Not covered; must be separately authored or AI-assisted and reviewed.",
            "behavior_layer": "Not covered; produced only by our product event system.",
            "embedding_layer": "Not covered; generated by our embedding pipeline.",
            "upstream_sparse_tags": "Observed in some poem files with low coverage; useful only as weak reference, not as the product feature taxonomy.",
        },
        "step1_decisions": [
            "Treat chinese-poetry as raw corpus, not as final product database.",
            "Treat sparse upstream tags as weak reference only; keep product themes/styles/mood in our own feature schema.",
            "Preserve upstream source_id/source_file/upstream_id instead of exposing upstream shape to clients.",
            "Keep rule-derived feature inputs in canonical schema: dynasty, genre, cipai, paragraphs, lines, char_count, line_count and optional strains/rank joins.",
            "Allow semantic features to be pending in Step 2; generate them in later enrichment steps.",
        ],
    }

    output_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote source profile to {output_path}")
    print(f"Inspected {len(inspected_sources)} representative upstream files.")
    print(f"Missing target feature groups: {', '.join(TARGET_FEATURES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
