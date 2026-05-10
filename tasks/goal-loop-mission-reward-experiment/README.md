# Goal Loop Mission Reward Experiment

Status: in-progress
Created: 2026-05-10
Source: Self-OS kanban task `t_4e05470f`

## Summary

Practical experiment for Codex/Hermes goal-style long-running work, inspired by the AI Jason `/goal` video capture in Self-OS:

`/data/Self-OS/wikis/ai-research-os/raw/youtube/2026-05-10-ai-jason-goals-command-tips-mistakes.md`

The experiment uses `mission.md` as the durable task contract and `artifacts/` as evidence storage. It tests whether a goal loop plus a goal-buddy review produces better completion discipline than chat-only progress.

## Current next step

Run the checkpoint prompt in `artifacts/checkpoint-notes/checkpoint-001.md` after a delay or as a cron-style follow-up, then decide whether to continue, revise, or close the mission.

## Files

- `mission.md` — durable objective, definition of done, constraints, eval criteria, and current next step.
- `docs/idea.md` — source context and experiment rationale.
- `artifacts/codex-goal-feature-check.md` — `/goal` support and environment check.
- `artifacts/primary-run-prompt.md` — primary agent prompt/contract.
- `artifacts/primary-run-log.md` — primary run log and output evidence.
- `artifacts/primary-output/mission_artifact_auditor.py` — small real coding output from the experiment.
- `artifacts/eval-results/` — generated audit/eval outputs.
- `artifacts/goal-buddy-review.md` — independent review against the mission.
- `artifacts/findings.md` — workflow findings and recommendation.
- `artifacts/checkpoint-notes/checkpoint-001.md` — follow-up cycle proposal/prompt.
