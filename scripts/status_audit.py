#!/usr/bin/env python3
"""Audit taskOS task statuses.

Policy:
- Every open task must be one of: backlog, in-progress, blocked.
- Terminal done tasks may stay done.
- Legacy open statuses are normalized to backlog.
- in-progress tasks with no non-audit touch in the last 7 days are downgraded to blocked.

The audit is intentionally conservative: it only edits the `Status:` line in each
`tasks/<slug>/README.md` so existing task content is preserved.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

OPEN_STATUSES = {"backlog", "in-progress", "blocked"}
TERMINAL_STATUSES = {"done"}
CANONICAL_STATUSES = OPEN_STATUSES | TERMINAL_STATUSES
LEGACY_OPEN_STATUSES = {
    "captured",
    "ready-for-spec",
    "specified",
    "ready-for-issues",
    "ready-for-implementation",
    "implemented-awaiting-review",
    "awaiting-review",
    "review",
    "todo",
    "open",
    "active",
}
STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
AUDIT_MARKER = "taskOS status audit"


def run_git(repo: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        return ""
    return proc.stdout.strip()


def parse_git_timestamp(raw: str) -> dt.datetime | None:
    raw = raw.strip()
    if not raw:
        return None
    try:
        # git %cI is ISO 8601 with timezone, e.g. 2026-05-30T12:34:56+00:00
        return dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def last_human_touch(repo: Path, task_dir: Path) -> dt.datetime | None:
    rel = task_dir.relative_to(repo).as_posix()
    # Ignore commits whose subject clearly identifies this automated audit, so the
    # audit itself does not keep an in-progress task fresh forever.
    lines = run_git(repo, ["log", "--format=%cI%x09%s", "--", rel]).splitlines()
    for line in lines:
        if "\t" in line:
            when_raw, subject = line.split("\t", 1)
        else:
            when_raw, subject = line, ""
        if AUDIT_MARKER.lower() in subject.lower():
            continue
        when = parse_git_timestamp(when_raw)
        if when:
            return when

    # Fallback for uncommitted/new task dirs: latest filesystem mtime. This makes
    # newly captured uncommitted tasks count as touched.
    mtimes: list[dt.datetime] = []
    for path in task_dir.rglob("*"):
        if path.is_file():
            try:
                mtimes.append(dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc))
            except OSError:
                pass
    return max(mtimes) if mtimes else None


def read_status(text: str) -> str | None:
    match = STATUS_RE.search(text)
    return match.group(1).strip().lower() if match else None


def write_status(text: str, new_status: str) -> str:
    if STATUS_RE.search(text):
        return STATUS_RE.sub(f"Status: {new_status}", text, count=1)
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join([lines[0], "", f"Status: {new_status}", *lines[1:]]) + ("\n" if text.endswith("\n") else "")
    return f"Status: {new_status}\n\n{text}"


def decide_status(current: str | None, age_days: int | None, max_in_progress_days: int) -> tuple[str, str]:
    if current in TERMINAL_STATUSES:
        return current, "terminal"
    if current == "in-progress" and age_days is not None and age_days > max_in_progress_days:
        return "blocked", f"in-progress stale for {age_days} days"
    if current in OPEN_STATUSES:
        return current, "ok"
    if current in LEGACY_OPEN_STATUSES or current is None:
        return "backlog", f"normalized from {current or 'missing'}"
    return "backlog", f"unknown open status normalized from {current}"


def audit(repo: Path, dry_run: bool, max_in_progress_days: int) -> dict[str, Any]:
    tasks_root = repo / "tasks"
    now = dt.datetime.now(dt.timezone.utc)
    changes: list[dict[str, Any]] = []
    counts: dict[str, int] = {"backlog": 0, "in-progress": 0, "blocked": 0, "done": 0}
    unknown: list[str] = []

    for readme in sorted(tasks_root.glob("*/README.md")):
        task_dir = readme.parent
        slug = task_dir.name
        text = readme.read_text(encoding="utf-8")
        current = read_status(text)
        touched = last_human_touch(repo, task_dir)
        age_days = None if touched is None else (now - touched).days
        new_status, reason = decide_status(current, age_days, max_in_progress_days)
        counts[new_status] = counts.get(new_status, 0) + 1
        if current not in CANONICAL_STATUSES and current is not None:
            unknown.append(f"{slug}: {current}")
        if new_status != current:
            changes.append(
                {
                    "slug": slug,
                    "from": current or "missing",
                    "to": new_status,
                    "reason": reason,
                    "last_touched": touched.isoformat() if touched else None,
                    "age_days": age_days,
                    "file": str(readme),
                }
            )
            if not dry_run:
                readme.write_text(write_status(text, new_status), encoding="utf-8")

    return {
        "repo": str(repo),
        "dry_run": dry_run,
        "policy": {
            "open_statuses": sorted(OPEN_STATUSES),
            "terminal_statuses": sorted(TERMINAL_STATUSES),
            "max_in_progress_days": max_in_progress_days,
        },
        "counts": counts,
        "changed": changes,
        "legacy_or_unknown_seen": unknown,
    }


def format_report(result: dict[str, Any]) -> str:
    counts = result["counts"]
    changed = result["changed"]
    mode = "DRY RUN" if result["dry_run"] else "APPLIED"
    lines = [
        f"# taskOS status audit — {mode}",
        "",
        "Policy: open tasks must be `backlog`, `in-progress`, or `blocked`; `in-progress` auto-downgrades to `blocked` after 7 days untouched.",
        "",
        "## Status counts",
        f"- backlog: {counts.get('backlog', 0)}",
        f"- in-progress: {counts.get('in-progress', 0)}",
        f"- blocked: {counts.get('blocked', 0)}",
        f"- done: {counts.get('done', 0)}",
        "",
        f"## Changes ({len(changed)})",
    ]
    if not changed:
        lines.append("- No status changes needed.")
    else:
        for item in changed:
            age = "unknown age" if item["age_days"] is None else f"{item['age_days']}d old"
            lines.append(f"- `{item['slug']}`: `{item['from']}` → `{item['to']}` ({item['reason']}; {age})")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit taskOS statuses.")
    parser.add_argument("--repo", default=os.environ.get("TASKOS_REPO", "/data/taskOS"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown report")
    parser.add_argument("--max-in-progress-days", type=int, default=7)
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    result = audit(repo, dry_run=args.dry_run, max_in_progress_days=args.max_in_progress_days)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(format_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
