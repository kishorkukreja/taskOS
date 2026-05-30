# Idea Notes — MCP Multi-Agent PR Review

**Source:** User voice note — 2026-05-28

## Raw source interpretation
The user described a workflow where MCP can autonomously run multiple code agents — interpreted as Claude Code, Codex, and Gemini — to review PRs in a new way. The core idea is that MCP should be part of our operating view: a beautiful coordination layer for understanding a PR from many different angles, and a pattern to use in future sessions.

## Preserved thesis
MCP is not only a way to expose tools to agents. In Self-OS, MCP can also become a coordination surface for multi-agent judgement. For code review, that means giving the same PR context to multiple reviewer agents and asking each to inspect from a different lens.

## Why this is useful
- Different models catch different failure modes.
- Different prompts/lenses reduce review monoculture.
- PR review benefits from independent perspectives before synthesis.
- The human should receive one concise consolidated packet, not three noisy model dumps.
- GitHub PR UI remains the best place to anchor review evidence.

## Candidate reviewer lanes
- Correctness and edge cases
- Security and credential risk
- Architecture and module boundaries
- Test coverage and regressions
- Maintainability and simplicity
- Product/UX intent, where relevant
- Migration/deployment/runtime risk

## Candidate architecture
1. Hermes receives a PR URL or local branch.
2. GitHub tooling gathers metadata, changed files, diff, checks, and test context.
3. MCP exposes shared context/tools to reviewer agents.
4. Reviewer agents run independently:
   - Claude Code reviewer
   - Codex reviewer
   - Gemini reviewer
   - optional deterministic reviewer lane
5. Findings are normalized into a common schema.
6. A consolidation step deduplicates, ranks, and resolves conflicts.
7. Hermes posts a Telegram summary and optionally submits GitHub PR comments/review.

## Finding schema sketch
- `reviewer`: source agent/lane
- `severity`: critical | warning | suggestion | note
- `path`: file path
- `line`: optional line number
- `claim`: issue or observation
- `evidence`: diff/context snippet or test output
- `confidence`: low | medium | high
- `suggested_fix`: optional concrete change
- `blocking`: boolean

## Design principles
- Multi-agent outputs are evidence candidates, not truth.
- Deterministic checks still matter: tests, lint, typecheck, secret scans, changed-file stats.
- Reviewer lanes should be modular and replaceable.
- Final output should be operator-grade: short, ranked, actionable, and anchored to files/lines.
- Avoid sending credentials or private context to untrusted MCP servers or remote agents.

## Related context
- Existing Hermes skills: `github-code-review`, `native-mcp`, `claude-code`, `codex`, `opencode`.
- User preference: GitHub PR UI is the best tool for code review.
- User preference: rigorous multi-stage QA beats vibe coding.
- User preference: useful workflows should become operational Hermes skills.

## Next step
Turn this into a spec for an MCP-backed PR review fan-out workflow, then pilot it on a low-risk PR before making it a reusable Hermes skill or taskOS command.
