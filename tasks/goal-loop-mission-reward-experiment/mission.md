# Mission: Goal Loop + Goal Buddy + Reward Cycle Experiment

Created: 2026-05-10T22:20:45Z
Owner: Hermes Kanban task `t_4e05470f`
Workspace: `/data/taskOS/tasks/goal-loop-mission-reward-experiment/`

## Objective

Run a minimal but real experiment with Codex/Hermes goal-style long-running work. The experiment should determine whether a durable `mission.md`, artifact evidence, a goal-buddy review layer, and a follow-up reward/evaluation checkpoint reduce premature completion and drift.

## Definition of done

The mission is complete when all of these are true:

1. A minimal experiment folder exists under `/data/taskOS/tasks/goal-loop-mission-reward-experiment/`.
2. This `mission.md` defines objective, definition of done, non-goals, constraints, verification commands, reward/eval criteria, and current next step.
3. The `/goal` feature has been practically checked or attempted, with environment limitations recorded rather than hidden.
4. A small real primary-agent task has produced an artifact, not just chat progress.
5. The primary run has written evidence into `artifacts/`.
6. A goal-buddy review has checked for early stopping, drift, and proxy-completion mistakes.
7. A recurring checkpoint mechanism is proposed or created.
8. A short findings note states whether this should become a reusable Self-OS/Hermes workflow or skill.

## Non-goals

- Do not build a full production orchestration system.
- Do not modify user-wide Codex configuration unless explicitly necessary and documented.
- Do not treat a single passing command as the whole reward signal.
- Do not create noisy long-running cron jobs without a bounded experiment rationale.
- Do not move this from taskOS to Kanban execution until the workflow is clearer.

## Constraints

- Keep the first experiment small and auditable.
- Prefer files over chat-only state.
- Store logs, prompts, outputs, and evals under `artifacts/`.
- If Codex `/goal` cannot run because of installed version, auth, or TUI limitations, record that as an experiment result and continue with a Hermes-compatible goal-loop approximation.
- Avoid secrets in artifacts.

## Primary task for the goal loop

Build a tiny mission artifact auditor that checks this experiment folder for expected files and emits a JSON report with pass/fail signals. This is intentionally small but real: future checkpoint jobs can run it to detect whether the mission contract and artifact evidence are complete.

Expected output:

`artifacts/primary-output/mission_artifact_auditor.py`

## Verification commands

Run from `/data/taskOS/tasks/goal-loop-mission-reward-experiment/`:

```bash
python artifacts/primary-output/mission_artifact_auditor.py . --json artifacts/eval-results/latest-audit.json
python -m json.tool artifacts/eval-results/latest-audit.json >/tmp/goal-loop-audit-json-ok.txt
```

Optional git evidence:

```bash
git -C /data/taskOS status --short --branch
```

## Reward / evaluation criteria

Score each checkpoint on a 0–2 scale:

- Contract clarity: objective and done criteria are specific enough to judge.
- Artifact discipline: prompts, logs, outputs, evals, and reviews are written to disk.
- Objective fidelity: outputs match the mission, not an easier proxy task.
- Verification quality: checks inspect required artifacts and produce machine-readable evidence.
- Goal-buddy quality: review identifies premature-completion risks and concrete next steps.
- Continuation quality: next step is explicit and small enough for the next run.

Close the mission only if total score is at least 10/12 and no required artifact is missing.

## Current state

Initialized. Codex `/goal` support must be checked, then the primary task should produce the auditor and evidence.

## Current next step

Run the primary goal-style task, save a transcript/log under `artifacts/primary-run-log.md`, then run the auditor and goal-buddy review.
