#!/usr/bin/env python3
"""Audit a mission folder for goal-loop experiment evidence.

This is intentionally small and dependency-free so recurring checkpoint jobs can run it.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

REQUIRED_FILES = [
    "mission.md",
    "README.md",
    "docs/idea.md",
    "artifacts/codex-goal-feature-check.md",
    "artifacts/primary-run-prompt.md",
    "artifacts/primary-run-log.md",
    "artifacts/goal-buddy-review.md",
    "artifacts/findings.md",
    "artifacts/checkpoint-notes/checkpoint-001.md",
]

REQUIRED_MISSION_SECTIONS = {
    "objective": ["## Objective"],
    "definition_of_done": ["## Definition of done", "## Definition of Done"],
    "non_goals": ["## Non-goals", "## Non Goals"],
    "constraints": ["## Constraints"],
    "verification_commands": ["## Verification commands", "## Verification Commands"],
    "reward_evaluation_criteria": [
        "## Reward / evaluation criteria",
        "## Reward/evaluation criteria",
        "## Reward Evaluation Criteria",
    ],
    "current_next_step": ["## Current next step", "## Current Next Step"],
}


def contains_any(text: str, needles: Iterable[str]) -> bool:
    return any(needle in text for needle in needles)


def audit(root: Path) -> dict:
    root = root.resolve()
    missing_files = [rel for rel in REQUIRED_FILES if not (root / rel).is_file()]

    mission_path = root / "mission.md"
    mission_text = mission_path.read_text(encoding="utf-8") if mission_path.is_file() else ""
    missing_sections = [
        name
        for name, headings in REQUIRED_MISSION_SECTIONS.items()
        if not contains_any(mission_text, headings)
    ]

    required_file_points = len(REQUIRED_FILES)
    required_section_points = len(REQUIRED_MISSION_SECTIONS)
    earned = (required_file_points - len(missing_files)) + (
        required_section_points - len(missing_sections)
    )
    possible = required_file_points + required_section_points
    score = {
        "earned": earned,
        "possible": possible,
        "percent": round((earned / possible) * 100, 1) if possible else 0.0,
    }

    return {
        "root": str(root),
        "passed": not missing_files and not missing_sections,
        "missing_files": missing_files,
        "missing_mission_sections": missing_sections,
        "score": score,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Mission folder to audit")
    parser.add_argument("--json", dest="json_path", help="Write JSON report to this path")
    args = parser.parse_args()

    root = Path(args.root)
    report = audit(root)

    print(
        "PASS" if report["passed"] else "FAIL",
        f"score={report['score']['earned']}/{report['score']['possible']}",
        f"missing_files={len(report['missing_files'])}",
        f"missing_sections={len(report['missing_mission_sections'])}",
    )

    if args.json_path:
        json_path = Path(args.json_path)
        if not json_path.is_absolute():
            json_path = root / json_path
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {json_path}")

    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
