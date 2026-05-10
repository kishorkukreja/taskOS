# Checkpoint 001: Continue / Revise / Close Decision

Suggested schedule: run once after the primary experiment has settled, then reuse manually or as a bounded cron if this workflow graduates.

## Proposed recurring mechanism

Use a short-lived Hermes cron or manual Kanban follow-up, not an indefinite daemon, until the workflow proves useful.

Candidate Hermes cron prompt:

```text
Review the mission folder `/data/taskOS/tasks/goal-loop-mission-reward-experiment/`.
Load `mission.md`, run `python artifacts/primary-output/mission_artifact_auditor.py . --json artifacts/eval-results/checkpoint-$(date -u +%Y%m%dT%H%M%SZ).json`, inspect `artifacts/`, then write `artifacts/checkpoint-notes/<timestamp>-review.md` with: continue/revise/close, score against reward criteria, missing evidence, and next concrete step. Do not create a recurring child job from inside the cron run.
```

Suggested schedule if created later:

- One-shot: `in 2h` or `tomorrow 09:00 UK`, once the user wants the mission revisited.
- Recurring only for active long-running missions: every 6–24 hours with an explicit repeat cap.

## Checkpoint rubric

Score 0–2 each:

1. Contract clarity.
2. Artifact discipline.
3. Objective fidelity.
4. Verification quality.
5. Goal-buddy quality.
6. Continuation quality.

Close only when score is at least 10/12 and the auditor passes.

## Current recommendation

Do not create an indefinite cron yet. For v0, use a one-shot follow-up checkpoint per mission or a Kanban reviewer task. Promote to reusable cron only after two or three missions show repeated value.
