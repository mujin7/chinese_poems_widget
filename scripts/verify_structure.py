"""Verify the Phase 0 repository skeleton.

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
    "data/raw/README.md",
    "data/processed/README.md",
    "data/samples/README.md",
    "scripts/data_import/README.md",
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
        print("Missing required Phase 0 paths:")
        for path in missing:
            print(f"- {path}")
        raise SystemExit(1)

    print(f"Phase 0 structure check passed: {len(REQUIRED_PATHS)} required paths found.")


if __name__ == "__main__":
    main()
