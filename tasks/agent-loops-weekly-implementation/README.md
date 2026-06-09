# Agent Loops Weekly Implementation

Status: backlog

**Status:** ready
**Priority:** medium
**Created:** 2026-06-09
**Source:** https://loops.elorm.xyz/install
**Kanban:** t_78cc0462

## What we are trying to do

Evaluate the loops! library of agent loop patterns and implement/adapt one useful loop per week into the Self-OS/Hermes development workflow.

Loops are kickoff prompts and, in some cases, hook bundles for coding agents. They encode a self-paced cycle: run a check command, inspect output, fix or advance one step, and stop when the exit condition passes.

## Why it matters

This maps directly onto Self-OS's manual-to-automated operating model: validate a loop manually, then turn it into a reusable Hermes skill, repo hook, Kanban workflow, or cron-assisted reminder only after it proves useful.

The important constraint is that loops should improve engineering reliability rather than add automation theatre. Each adopted loop needs an explicit trigger, check command, exit condition, and evidence that it caught or prevented real drift.

## Candidate loops to evaluate first

From the browse page snapshot:

1. **Ship PR Until Green** — implement on a branch, run tests, push, open PR, and loop on `gh pr checks` until CI passes.
2. **De-Sloppify Pass** — cleanup pass after implementation: remove debug code, tighten names, delete dead branches, align with conventions.
3. **PR Babysitter** — interval loop for PRs with a watch label; inspect health, nudge reviewers, fix CI, rebase if behind.
4. **Build Until Green** — run production build, fix compile/bundling errors until build succeeds.
5. **Spec-First Ship** — implement from `spec.md`, one unchecked requirement per iteration, verify, then mark complete.
6. **Coverage Until Threshold** — add focused tests until coverage target is met without unnecessary production changes.
7. **E2E Until Green** — run Playwright/E2E suite, fix first failing spec, repeat until green.
8. **Pre-Commit Guard** — hook-based loop to block commits when tests are red.
9. **PR Self-Review** — review the current diff like a senior reviewer for three passes before opening a PR.

## Initial recommendation

Start with **Spec-First Ship** or **PR Self-Review** because they align most strongly with current Self-OS standards:

- planning before execution
- evidence-backed verification
- small iterations
- PR/diff review as the canonical quality surface

## Implementation cadence

Every Saturday, pick one loop and do one of:

- manually test it on a real repo/task;
- adapt it into a Hermes skill;
- wire it into a repo hook if it is hook-based;
- create a Kanban workflow/template if it needs multi-step routing;
- reject it with reasons if it adds noise or duplicates existing workflows.

## Acceptance criteria

- [ ] Review the loops! install model and distinguish prompt-only loops from hook-based loops.
- [ ] Choose the first loop to pilot.
- [ ] Pilot the loop on a real repo/task with before/after evidence.
- [ ] Record whether it should become a Hermes skill, repo hook, Kanban template, cron reminder, or be rejected.
- [ ] Implement/adapt at least one loop into the active Self-OS workflow.
- [ ] Add the adopted loop to the relevant skill or repo documentation.
- [ ] Repeat weekly until the useful loops are absorbed or rejected.

## Notes

- Browser buttons do not install files; they only carry text/deeplink prompts.
- Hook-based loops require extracting an install bundle into a repo root and restarting the agent/editor so hooks load.
- Cursor `/loop` is separate from loops! but can be used for time-driven ticks.
- Avoid installing hook bundles globally or blindly; install only into the repo where the loop is being piloted.
