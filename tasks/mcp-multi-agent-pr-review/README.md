# MCP Multi-Agent PR Review

Status: backlog

**Status:** ready
**Priority:** medium
**Created:** 2026-05-28

## What we are trying to do
Design and implement a repo-centric workflow where MCP can orchestrate multiple independent coding/review agents — such as Claude Code, Codex, and Gemini — to review the same GitHub PR from different angles before merge.

## Why it matters
A single reviewer agent can miss important issues or overfit to one model's style. Running several agents against the same PR creates a richer review surface: correctness, architecture, security, tests, maintainability, and product intent can be inspected from multiple independent perspectives.

The key view to preserve: MCP is not just a tool bridge; it can become the coordination layer that lets Self-OS understand a PR from many angles.

## Current state
Hermes already has GitHub PR review workflows, MCP support, and autonomous coding-agent skills/profiles. The missing piece is a clean orchestration pattern that fans out PR review to multiple agents, normalizes their findings, deduplicates overlap, and produces one high-signal review packet for the human or GitHub PR UI.

## Desired outcome
A reusable MCP-backed multi-agent PR review workflow that can be invoked from Hermes/taskOS. It should run multiple reviewer agents independently, gather their findings, reconcile conflicts, and publish a concise operator-grade summary plus optional inline GitHub comments.

## Constraints
- Keep GitHub/the PR UI as the canonical review surface.
- Preserve repo-centric artifacts and audit trails.
- Treat agent outputs as advisory until verified by deterministic checks, tests, or human review.
- Avoid leaking repo secrets or credentials to untrusted MCP servers or agent runtimes.
- Prefer modular reviewer lanes over one monolithic review prompt.

## Acceptance criteria
- [ ] Define the target MCP orchestration architecture for PR review fan-out.
- [ ] Specify reviewer lanes, e.g. correctness, security, architecture, tests, product/UX, maintainability.
- [ ] Define how Claude Code, Codex, Gemini, and future agents receive identical PR context.
- [ ] Define normalized finding schema: severity, file, line, claim, evidence, confidence, suggested fix, reviewer source.
- [ ] Implement a prototype that reviews a local PR diff with at least two reviewer agents or simulated reviewer lanes.
- [ ] Add deduplication and conflict reconciliation across reviewers.
- [ ] Produce a final review packet suitable for Telegram and GitHub PR comments.
- [ ] Include deterministic verification hooks: tests, lint, typecheck, secret scan, changed-file summary.
- [ ] Document safe credential handling and MCP server trust boundaries.
- [ ] Decide when to approve, comment, or request changes based on consolidated findings.

## Known decisions
- MCP is treated as the coordination layer for multi-agent review, not just a generic tool adapter.
- The workflow should help understand a PR from many angles.
- GitHub PR UI remains the best final review surface.
- Status starts as `ready` because the idea is actionable.

## Open questions
- Should this live as a Hermes skill, a taskOS command, a GitHub Action, or a local CLI wrapper?
- Which first repo should be used for a pilot review?
- Should reviewers be different models, different prompts on the same model, or both?
- Should MCP call agents directly, or should Hermes spawn each reviewer as a profile/subagent and use MCP only for shared context/tools?

## Future documents to create
- [ ] docs/spec.md
- [ ] docs/reviewer-lanes.md
- [ ] docs/finding-schema.md
- [ ] docs/mcp-architecture.md
- [ ] docs/pilot-results.md
