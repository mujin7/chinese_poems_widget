"""Verify the repository skeleton and Phase 1 data-planning outputs.

This script intentionally uses only the Python standard library so it can run
before backend/frontend dependencies are installed.
"""

from pathlib import Path

REQUIRED_PATHS = [
    "README.md",
    "docs/product-plan.md",
    "docs/planning-research.md",
    "docs/implementation-roadmap.md",
    "docs/github-codex-workflow.md",
    "docs/development-setup.md",
    "docs/phase-0-completion.md",
    "docs/data-schema.md",
    "docs/chinese-poetry-source-evaluation.md",
    "data/raw/README.md",
    "data/raw/source_manifest.json",
    "data/processed/README.md",
    "data/samples/README.md",
    "data/samples/poems.sample.jsonl",
    "data/samples/poems.sample.provenance.md",
    "data/processed/source_profile.chinese_poetry.json",
    "scripts/data_import/README.md",
    "scripts/data_import/inspect_chinese_poetry.py",
    "scripts/data_import/validate_poems.py",
    "scripts/evaluation/README.md",
    "backend/app/README.md",
    "backend/app/__init__.py",
    "backend/tests/README.md",
    "frontend/app/README.md",
    "frontend/tests/README.md",
    "extension/newtab/README.md",
    "experiments/recommendation/README.md",
    "experiments/agent/README.md",
    ".editorconfig",
    ".python-version",
    ".node-version",
    "pyproject.toml",
    "package.json",
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_PATHS if not (root / path).exists()]
    if missing:
        print("Missing required repository paths:")
        for path in missing:
            print(f"- {path}")
        raise SystemExit(1)

    print(f"Repository structure check passed: {len(REQUIRED_PATHS)} required paths found.")


if __name__ == "__main__":
    main()
