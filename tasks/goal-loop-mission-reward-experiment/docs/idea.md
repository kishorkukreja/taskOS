# Idea: Goal-style long-running agent work with mission files

## Source context

This task came from the AI Jason video capture saved in Self-OS:

`/data/Self-OS/wikis/ai-research-os/raw/youtube/2026-05-10-ai-jason-goals-command-tips-mistakes.md`

The key pattern is a standing goal loop where the agent continues until the actual goal is complete, not merely until it can plausibly claim progress.

## Hypothesis

A goal loop becomes operationally useful when it has three external anchors:

1. `mission.md` as durable contract and resumption state.
2. `artifacts/` as evidence that can be inspected by agents and humans.
3. A goal-buddy review pass that judges against the mission rather than the primary agent's confidence.

## Smallest real task

Create a mission artifact auditor script for this folder. It is small enough to finish in one run, but useful enough to support future recurring checkpoints.

## Acceptance criteria

- Codex `/goal` support or limitations are explicitly recorded.
- The primary run creates a reusable audit script.
- The script writes JSON eval results.
- A goal-buddy pass reviews completion quality.
- Findings recommend whether to promote the workflow into a Hermes skill.

## Open questions

- Should future missions be managed as taskOS folders, Kanban tasks, Hermes cron jobs, or a combination?
- Should goal-buddy be a separate Kanban reviewer profile or a recurring checkpoint prompt?
- What threshold makes a goal loop worth the overhead versus normal agent execution?
