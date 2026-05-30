# Implement Macro Evals for Agentic Systems

Status: backlog

**Status:** ready
**Priority:** medium
**Created:** 2026-05-27
**Source:** https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems

## What we are trying to do
Implement a Self-OS / Hermes-compatible macro-evaluation workflow for agentic systems, based on the OpenAI Cookbook example "Macro Evals for Agentic Systems". The goal is to move beyond single-response evals and analyze repeated failure patterns across many agent traces, lower-level eval labels, and run outcomes.

## Why it matters
Agent failures are often system-level, not just bad final answers. A plausible response can hide routing failures, missed review gates, incorrect tool use, poor handoffs, or weak business-context grounding. Macro evals should help Hermes/Self-OS turn many runs into inspectable pattern views, diagnosis queues, and prioritized investigation targets.

## Current state
OpenAI has published a cookbook notebook showing a macro-eval workflow over a synthetic EV-order multi-agent system. Self-OS does not yet have an equivalent reusable eval layer for Hermes agents, taskOS tasks, cron jobs, or multi-agent workflows.

## Desired outcome
A reusable macro-eval implementation that can ingest trace/run artifacts, join lower-level eval labels, produce compact trace documents, cluster recurring behavior patterns, and surface high-impact investigation queues for agentic workflows.

## Constraints
- Keep the implementation repo-centric and inspectable; avoid opaque SaaS-only eval storage.
- Start with offline/local artifacts before wiring to live Hermes traces.
- Preserve safe credential handling; the cookbook example itself does not require an OpenAI API key.
- Make outputs understandable to both technical and operator/business reviewers.
- Do not treat the cookbook as a final taxonomy; use it as a workflow pattern.

## Acceptance criteria
- [ ] Review the OpenAI Cookbook notebook and identify the minimum reusable architecture for Self-OS/Hermes.
- [ ] Define the canonical input schema for agent run traces, lower-level eval labels, run summaries, and optional trace snapshots.
- [ ] Implement a local/offline prototype that loads bundled/sample trace artifacts and creates compact trace documents.
- [ ] Add macro pattern discovery over many traces, with configurable minimum cluster size / granularity.
- [ ] Produce outputs for: pattern views, diagnosis views, and investigation queues.
- [ ] Include the four reader-facing labels in the model: `case_type`, `run_outcome`, `eval_finding`, and `behavior_pattern`.
- [ ] Add a smoke-test path with a trace limit for fast validation.
- [ ] Document how this can later attach to Hermes agent runs, taskOS tasks, cron workflows, and multi-agent coding/research traces.
- [ ] Add verification commands and example output artifacts.

## Known decisions
- Status starts as `ready` per user request.
- Use OpenAI Cookbook "Macro Evals for Agentic Systems" as the reference design.
- Treat macro evals as a system-level diagnostic layer above lower-level evals such as Promptfoo-style labels.

## Open questions
- Which first live workflow should this evaluate: Hermes coding agents, Supply Chain Signals jobs, taskOS implementation agents, or general cron workflows?
- Should this become a Hermes skill, a Self-OS script, a standalone package, or a taskOS-native evaluator?
- What lower-level eval label source should be used first: Promptfoo, custom rubric JSONL, OpenAI evals, or Hermes reviewer outputs?

## Future documents to create
- [ ] docs/spec.md
- [ ] docs/input-schema.md
- [ ] docs/prototype-plan.md
- [ ] docs/example-output.md
