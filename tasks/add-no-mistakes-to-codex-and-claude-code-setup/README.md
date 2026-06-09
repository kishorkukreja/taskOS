# Add no-mistakes to Codex and Claude Code Setup

Status: backlog

**Status:** ready
**Priority:** high
**Created:** 2026-06-09
**Source:** https://github.com/kunchenguid/no-mistakes
**Wiki:** /data/Self-OS/wikis/ai-research-os/raw/repos/2026-06-09-kunchenguid-no-mistakes.md
**Wiki commit:** 62ad593d6b1ed2bf16dd3f2f23d7eef19283a3fe
**Kanban:** pending

## What we are trying to do

Evaluate and add `no-mistakes` to the local Codex and Claude Code coding setup as a Git/PR quality gate.

`no-mistakes` puts a local Git proxy in front of the real remote: push to `no-mistakes` instead of `origin`, and it runs a validation pipeline in a disposable worktree before pushing upstream and opening/updating a PR.

## Why it matters

This maps directly to the Self-OS quality contract: AI agents can generate large diffs, but the bottleneck is validating them. `no-mistakes` turns the finalization step into a gate with review, tests, docs, lint, push, PR, and CI before code reaches the public branch/PR flow.

It may become a useful bridge between:

- Codex/Claude Code implementation;
- Hermes Kanban task routing;
- GitHub PR as the canonical review surface;
- Self-OS Day/Night Shift QA expectations.

## Desired outcome

A documented local setup where Codex and Claude Code can both use the `/no-mistakes` workflow, with one pilot repo initialized and one harmless branch successfully gated.

## Proposed pilot approach

1. Read the wiki capture first:
   - `/data/Self-OS/wikis/ai-research-os/raw/repos/2026-06-09-kunchenguid-no-mistakes.md`
2. Decide install route:
   - safer/privacy route: `go install github.com/kunchenguid/no-mistakes/cmd/no-mistakes@latest`, because docs say this does not embed a telemetry website ID;
   - or official installer with `NO_MISTAKES_TELEMETRY=0`.
3. Run:
   ```bash
   no-mistakes doctor
   ```
4. Pick a low-risk pilot repo.
5. In the pilot repo, run:
   ```bash
   no-mistakes init
   ```
6. Verify skill files exist:
   ```text
   .claude/skills/no-mistakes/SKILL.md
   .agents/skills/no-mistakes/SKILL.md
   ```
7. Add a repo-level `.no-mistakes.yaml` with explicit commands, e.g.:
   ```yaml
   agent: codex # or claude, depending on the pilot repo
   commands:
     test: "<repo test command>"
     lint: "<repo lint command>"
     format: "<repo format command>"
   ```
8. Test validate-only flow on a harmless committed branch:
   ```bash
   /no-mistakes
   ```
9. Test push-gate flow:
   ```bash
   git push no-mistakes <branch>
   ```

## Acceptance criteria

- [ ] Install route chosen with telemetry/privacy posture documented.
- [ ] `no-mistakes doctor` passes or known blockers are recorded.
- [ ] One pilot repo initialized with `no-mistakes init`.
- [ ] Claude Code skill path exists: `.claude/skills/no-mistakes/SKILL.md`.
- [ ] Generic agent/Codex skill path exists: `.agents/skills/no-mistakes/SKILL.md`.
- [ ] Pilot repo has explicit test/lint commands in `.no-mistakes.yaml`.
- [ ] A harmless branch is gated successfully or failure mode is documented.
- [ ] Decision recorded: adopt as default final gate, keep repo-specific, or reject.

## Safety / caveats

- Do not install globally across all repos until one pilot proves it.
- Avoid unreviewed daemon/service changes on critical repos.
- Keep `ask-user` findings human-gated unless explicit unattended consent is given.
- Treat `outcome: checks-passed` as ready for human review/merge, not automatically merged.
- Preserve unrelated dirty work when running `/no-mistakes` task-first mode.

## Future documents to create

- [ ] docs/pilot-results.md
- [ ] docs/codex-setup.md
- [ ] docs/claude-code-setup.md
- [ ] docs/no-mistakes-policy.md
