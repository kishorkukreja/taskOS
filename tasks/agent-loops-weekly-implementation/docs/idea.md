# Idea: Agent Loops Weekly Implementation

Source: https://loops.elorm.xyz/install
Captured: 2026-06-09

## Source summary

loops! provides reusable agent loop patterns for coding agents such as Cursor, Claude Code, Codex, and terminal agents. Each loop is primarily a kickoff prompt that tells the agent how to self-pace:

1. run a check command between passes;
2. read the output;
3. fix, advance, or escalate;
4. stop when the exit condition passes or max iterations is reached.

Some loops also ship hook files. Browser buttons do not write to a project; hook bundles must be downloaded and extracted into a repo root by the operator/agent, then the agent/editor must be restarted so hooks register.

## Install-page mechanics

- **Use loop:** copies the kickoff prompt. Works in any agent.
- **Open in Cursor / Claude Code:** deeplinks with kickoff text only; does not install hook files.
- **Install files:** downloads `.cursor/` and `.claude/` paths; extract at project root and restart/reload agent.
- **Prompt-only loops:** copy kickoff and run manually.
- **Hook-based loops:** install bundle + optionally paste kickoff once so the agent understands loop rules.
- **Cursor `/loop`:** separate built-in recurring tick; complementary to loops! kickoffs.

## Candidate loop inventory from first browse snapshot

### Ship PR Until Green

- Category: CI
- Trigger type: manual
- Goal: PR is open with all CI checks passing
- Max iterations: 10
- Between iterations: `gh pr checks`
- Exit: all PR checks are success
- Fit: strong for GitHub PR UI as canonical review surface.

### De-Sloppify Pass

- Category: Review
- Trigger type: manual
- Goal: recent changes are clean, minimal, and convention-aligned
- Max iterations: 4
- Between iterations: `npm run lint && npm test`
- Exit: no slop and checks pass
- Fit: strong post-implementation hygiene pass.

### PR Babysitter

- Category: CI
- Trigger type: interval
- Goal: open PRs labeled `codex-watch` are healthy
- Max iterations: 20
- Between iterations: `gh pr list --label "codex-watch"`
- Exit: each watched PR is green/current or escalated
- Fit: useful if we standardize a watch label.

### Build Until Green

- Category: Testing
- Trigger type: manual
- Goal: production build succeeds
- Max iterations: 10
- Between iterations: `npm run build`
- Exit: build exits 0
- Fit: generic but useful for JS/TS projects.

### Spec-First Ship

- Category: Planning
- Trigger type: manual
- Goal: every requirement in `spec.md` is implemented and checked off
- Max iterations: 15
- Between iterations: `npm test`
- Exit: `spec.md` has no unchecked requirements
- Fit: very strong; maps directly to Self-OS taskOS → spec → implementation.

### Coverage Until Threshold

- Category: Testing
- Trigger type: manual
- Goal: coverage meets target threshold, default 80%, with all tests passing
- Max iterations: 12
- Between iterations: `npm test -- --coverage`
- Exit: coverage threshold met and tests exit 0
- Fit: useful where coverage is meaningful; avoid gaming coverage.

### E2E Until Green

- Category: Testing
- Trigger type: manual
- Goal: E2E suite passes
- Max iterations: 10
- Between iterations: `npm run test:e2e`
- Exit: E2E command exits 0
- Fit: good for Playwright/product apps.

### Pre-Commit Guard

- Category: Testing
- Trigger type: event/hook
- Goal: block git commits when tests fail
- Between iterations: `npm test`
- Exit: tests exit 0 before each commit
- Fit: useful but should be repo-specific; do not blindly install global hooks.

### PR Self-Review

- Category: Review
- Trigger type: manual
- Goal: three clean self-review passes on current diff
- Max iterations: 3
- Between iterations: `git diff main...HEAD`
- Exit: three passes complete with no critical findings
- Fit: very strong; should likely become a Hermes/Claude/Codex skill or PR workflow step.

## Open questions

- Which repo should be the first pilot?
- Should loops become Hermes skills, Git hooks, Kanban task templates, or per-repo docs?
- Which loops duplicate existing Self-OS rules and should be rejected or merged into existing skills?
- Should `codex-watch` or another label become canonical for PR babysitting?

## Proposed first Saturday action

Pilot **PR Self-Review** or **Spec-First Ship** on a real Self-OS/SupplyChainSignals/Hermes-related PR and record whether it catches issues better than our current workflow.
