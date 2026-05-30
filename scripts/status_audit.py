#!/usr/bin/env python3
"""Audit taskOS task statuses.

Policy:
- Every open task must be one of: backlog, in-progress, blocked.
- Terminal done tasks may stay done.
- Legacy open statuses are normalized to backlog.
- in-progress tasks with no non-audit touch in the last 7 days are downgraded to blocked.

Human-in-the-loop review mode:
- Weekly cron creates a pending proposal and asks for review.
- If the user does not reply within 48 hours, a finalizer applies the original proposal.
- If the user asks for changes, Hermes should push back until the rationale is strong,
  then amend/apply the proposal explicitly.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
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
    "ready",
}
STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
AUDIT_MARKER = "taskOS status audit"
DEFAULT_PROPOSAL_DIR = ".taskos/status-audit"


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


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


def run_git_checked(repo: Path, args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def parse_timestamp(raw: str) -> dt.datetime | None:
    raw = raw.strip()
    if not raw:
        return None
    try:
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
        when = parse_timestamp(when_raw)
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
    now = utc_now()
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


def proposal_dir(repo: Path, raw: str | None) -> Path:
    path = raw or DEFAULT_PROPOSAL_DIR
    p = Path(path)
    if not p.is_absolute():
        p = repo / p
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_proposal(repo: Path, result: dict[str, Any], review_hours: int, raw_dir: str | None) -> Path | None:
    if not result["changed"]:
        return None
    now = utc_now()
    proposal = {
        "schema_version": 1,
        "id": now.strftime("%Y%m%dT%H%M%SZ"),
        "status": "pending_review",
        "proposed_at": now.isoformat(),
        "expires_at": (now + dt.timedelta(hours=review_hours)).isoformat(),
        "review_hours": review_hours,
        "result": result,
        "review_contract": "Send results to Telegram and ask Kishor to review. If no reply within 48h, apply the original proposal. If he asks to change something, push back until the rationale is strong, then apply the agreed shift.",
    }
    out = proposal_dir(repo, raw_dir) / f"{proposal['id']}.json"
    out.write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


def format_report(result: dict[str, Any], mode: str | None = None, proposal_path: Path | None = None, expires_at: str | None = None) -> str:
    counts = result["counts"]
    changed = result["changed"]
    report_mode = mode or ("DRY RUN" if result["dry_run"] else "APPLIED")
    lines = [
        f"# taskOS status audit — {report_mode}",
        "",
        "Policy: open tasks must be `backlog`, `in-progress`, or `blocked`; `in-progress` auto-downgrades to `blocked` after 7 days untouched.",
        "",
        "## Status counts",
        f"- backlog: {counts.get('backlog', 0)}",
        f"- in-progress: {counts.get('in-progress', 0)}",
        f"- blocked: {counts.get('blocked', 0)}",
        f"- done: {counts.get('done', 0)}",
        "",
        f"## Proposed changes ({len(changed)})" if report_mode == "PENDING REVIEW" else f"## Changes ({len(changed)})",
    ]
    if not changed:
        lines.append("- No status changes needed.")
    else:
        for item in changed:
            age = "unknown age" if item["age_days"] is None else f"{item['age_days']}d old"
            lines.append(f"- `{item['slug']}`: `{item['from']}` → `{item['to']}` ({item['reason']}; {age})")
    if report_mode == "PENDING REVIEW":
        lines.extend([
            "",
            "## Review request",
            "Please review these status calls.",
            "- If you do not reply within 48 hours, I will keep and apply this original proposal.",
            "- If you ask me to change a status, I will push back until the evidence/rationale is strong enough that we both agree, then I will make the shift.",
        ])
        if proposal_path:
            lines.append(f"- Proposal file: `{proposal_path}`")
        if expires_at:
            lines.append(f"- Auto-apply after: `{expires_at}`")
    return "\n".join(lines) + "\n"


def apply_proposal(repo: Path, proposal_path: Path, commit: bool) -> dict[str, Any]:
    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    applied: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    staged_paths: list[str] = []

    for change in proposal["result"]["changed"]:
        readme = Path(change["file"])
        if not readme.is_absolute():
            readme = repo / readme
        text = readme.read_text(encoding="utf-8")
        current = read_status(text) or "missing"
        # Exact precondition avoids silently overriding human edits made during review.
        if current != change["from"]:
            skipped.append({**change, "current": current, "skip_reason": "current status no longer matches proposal precondition"})
            continue
        readme.write_text(write_status(text, change["to"]), encoding="utf-8")
        applied.append(change)
        staged_paths.append(readme.relative_to(repo).as_posix())

    commit_result: dict[str, Any] | None = None
    if commit and staged_paths:
        run_git_checked(repo, ["add", *staged_paths])
        rc, out, err = run_git_checked(repo, ["commit", "-m", "chore: taskOS status audit apply"])
        commit_result = {"returncode": rc, "stdout": out, "stderr": err}

    proposal["status"] = "applied" if applied and not skipped else "partially_applied" if applied else "skipped"
    proposal["applied_at"] = utc_now().isoformat()
    proposal["applied"] = applied
    proposal["skipped"] = skipped
    proposal["commit"] = commit_result
    proposal_path.write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return proposal


def finalize_pending(repo: Path, raw_dir: str | None, commit: bool) -> str:
    directory = proposal_dir(repo, raw_dir)
    now = utc_now()
    outputs: list[str] = []
    for path in sorted(directory.glob("*.json")):
        proposal = json.loads(path.read_text(encoding="utf-8"))
        if proposal.get("status") != "pending_review":
            continue
        expires = parse_timestamp(proposal.get("expires_at", ""))
        if not expires or expires > now:
            continue
        applied = apply_proposal(repo, path, commit=commit)
        outputs.append(format_finalize_report(path, applied))
    return "\n".join(outputs)


def format_finalize_report(path: Path, proposal: dict[str, Any]) -> str:
    applied = proposal.get("applied", [])
    skipped = proposal.get("skipped", [])
    lines = [
        "# taskOS status audit — 48h review window expired",
        "",
        "No review override was recorded, so I kept the original audit result and applied it.",
        "",
        f"- Proposal file: `{path}`",
        f"- Applied: {len(applied)}",
        f"- Skipped due to intervening edits: {len(skipped)}",
    ]
    commit = proposal.get("commit")
    if commit:
        lines.append(f"- Git commit: `{commit.get('stdout') or commit.get('stderr')}`")
    if applied:
        lines.append("")
        lines.append("## Applied changes")
        for item in applied:
            lines.append(f"- `{item['slug']}`: `{item['from']}` → `{item['to']}`")
    if skipped:
        lines.append("")
        lines.append("## Skipped")
        for item in skipped:
            lines.append(f"- `{item['slug']}`: proposal expected `{item['from']}`, current is `{item['current']}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit taskOS statuses.")
    parser.add_argument("--repo", default=os.environ.get("TASKOS_REPO", "/data/taskOS"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown report")
    parser.add_argument("--max-in-progress-days", type=int, default=7)
    parser.add_argument("--propose", action="store_true", help="Create a pending review proposal instead of applying changes")
    parser.add_argument("--review-hours", type=int, default=48)
    parser.add_argument("--proposal-dir", default=None)
    parser.add_argument("--finalize-pending", action="store_true", help="Apply expired pending review proposals")
    parser.add_argument("--apply-proposal", default=None, help="Apply one proposal JSON file")
    parser.add_argument("--commit", action="store_true", help="Commit applied proposal status changes")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()

    if args.finalize_pending:
        output = finalize_pending(repo, args.proposal_dir, commit=args.commit)
        if output:
            print(output, end="")
        return 0

    if args.apply_proposal:
        applied = apply_proposal(repo, Path(args.apply_proposal), commit=args.commit)
        print(format_finalize_report(Path(args.apply_proposal), applied), end="")
        return 0

    if args.propose:
        result = audit(repo, dry_run=True, max_in_progress_days=args.max_in_progress_days)
        proposal_path = save_proposal(repo, result, args.review_hours, args.proposal_dir)
        expires_at = None
        if proposal_path:
            proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
            expires_at = proposal["expires_at"]
        print(format_report(result, mode="PENDING REVIEW", proposal_path=proposal_path, expires_at=expires_at), end="")
        return 0

    result = audit(repo, dry_run=args.dry_run, max_in_progress_days=args.max_in_progress_days)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(format_report(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
