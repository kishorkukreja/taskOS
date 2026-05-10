# Findings: Goal Loop Mission Reward Experiment

## Result

The experiment should become a reusable Self-OS/Hermes workflow, but as a lightweight mission-folder pattern first, not a heavy always-on orchestration system.

## What worked

- `mission.md` made completion criteria explicit and reviewable.
- `artifacts/` prevented the run from becoming chat-only progress.
- Trying Codex `/goal` surfaced real operational prerequisites: current installed Codex was old (`0.125.0`), latest Codex exposes `goals` as an experimental feature, interactive `/goal` needs a real TTY, and Codex execution needs auth.
- A tiny mission auditor is a useful primitive for future reward/checkpoint loops.

## What did not work

- Codex `/goal` itself did not complete in this environment:
  - interactive attempt failed with `stdin is not a terminal`;
  - non-interactive fallback reached Codex but failed with OpenAI 401 auth.
- The experiment therefore validates the surrounding mission/review/evidence pattern more than the Codex goal feature itself.

## Reusable workflow candidate

For substantial agent work, create:

```text
tasks/<slug>/
  mission.md
  artifacts/
    primary-run-prompt.md
    primary-run-log.md
    eval-results/
    goal-buddy-review.md
    checkpoint-notes/
```

Then run:

1. Primary agent executes from `mission.md` and writes evidence.
2. Goal buddy reviews against the mission, not the primary agent's claims.
3. Auditor/eval command creates machine-readable pass/fail evidence.
4. Checkpoint decides continue, revise, or close.

## Skill recommendation

Patch the existing `codex` skill with lessons from this experiment rather than create a narrow one-off skill:

- `/goal` currently requires Codex `0.128.0+` / latest Codex and the `goals` feature flag.
- Interactive `/goal` needs a real terminal/TUI path; non-interactive agent tool contexts can fail with `stdin is not a terminal`.
- `codex exec --enable goals` is not the same as an interactive `/goal` loop; treat it as a fallback and record that distinction.
- Always pair long goals with a mission file, artifacts folder, and independent review.

A separate class-level skill may be warranted later if this pattern is repeated across multiple Self-OS missions.
