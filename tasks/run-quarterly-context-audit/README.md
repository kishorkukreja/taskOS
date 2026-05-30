# Run Quarterly Context Audit — August 2026

Status: backlog

**Status:** backlog
**Priority:** medium
**Created:** 2026-05-21

## What we are trying to do
Run the context-audit skill in Claude to surface stale memory assumptions, correct them via a structured MCQ interview, update memory, and generate an HTML report with AI workflow next steps.

## Why it matters
Memory drift compounds over time. Without a regular reset, Claude over-weights old project context (closed clients, shelved builds, resolved blockers), reducing the quality of every session.

## Current state
First audit completed 2026-05-21. context-audit.skill packaged and ready to install. Memory updated with corrected picture.

## Desired outcome
Memory reflects current state. HTML report generated. New corrections captured. Next audit date set.

## Constraints
- Requires context-audit.skill installed in Cowork skill library
- Needs ask_user_input_v0 and memory_user_edits tools available in session

## Acceptance criteria
- [ ] context-audit skill triggered successfully
- [ ] All 4 interview rounds completed via MCQ tool
- [ ] Memory updated with date-stamped corrections
- [ ] HTML report generated and presented
- [ ] Next audit date set (November 2026)

## Known decisions
- Quarterly cadence (every 3 months)
- MCQ format via ask_user_input_v0 — not plain text questions
- Report uses dark editorial HTML design (IBM Plex Mono + Fraunces)

## Open questions
- None — process is fully defined in the skill

## Future documents to create
- [ ] docs/spec.md
