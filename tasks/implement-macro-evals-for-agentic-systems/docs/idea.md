# Idea Notes — Implement Macro Evals for Agentic Systems

**Source:** User-shared URL — 2026-05-27  
**Reference:** https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems

## Raw source notes
The user asked to add a task in taskOS to implement the OpenAI Cookbook workflow "Macro Evals for Agentic Systems" and explicitly requested the status be kept as `ready`.

## Source summary
OpenAI's cookbook example argues that when an agentic system fails, the failure is often larger than a single bad response. The macro-eval workflow aggregates many agent traces, lower-level eval labels, and trace documents to discover repeated system-level behavior patterns.

The cookbook demonstrates this using a synthetic EV-order multi-agent workflow. It is designed to help teams move from thousands of agent events to a small number of patterns that are understandable to technical and business stakeholders.

## Relevant concepts to preserve
- Macro evals inspect the population of runs, not just individual final answers.
- Lower-level evals grade individual agents, handoffs, tools, and completed runs.
- Macro evals ask which problems repeat, where they concentrate, and where humans should inspect first.
- The output layer should include pattern views, diagnosis views, and investigation queues.
- The workflow converts trace evidence into compact trace documents before clustering/discovery.

## Four reader-facing labels
- `case_type`: generated business situation, e.g. clean order, validation block, supplier substitution, pricing exception.
- `run_outcome`: how the run ended, e.g. completed, awaiting review, blocked, failed.
- `eval_finding`: lower-level signal describing what looked wrong or risky.
- `behavior_pattern`: recurring pattern discovered across many traces.

Mental model from the article:

> `case_type` is the setup, `run_outcome` is the ending, `eval_finding` is the local symptom, and `behavior_pattern` is the population-level pattern.

## Implementation direction for Self-OS / Hermes
Build this as an inspectable local workflow first:

1. Define trace and label input schemas.
2. Create a loader for JSONL run traces and eval labels.
3. Normalize traces into compact trace documents.
4. Cluster or group recurring behavior patterns.
5. Rank by frequency, severity, workflow location, and business/operator impact.
6. Emit markdown/JSON artifacts that can be reviewed in GitHub PRs or taskOS.
7. Add a future adapter for Hermes runs, cron outputs, and multi-agent taskOS coding/research workflows.

## Constraints and assumptions
- Prefer repo-backed markdown/JSON artifacts over SaaS-only dashboards.
- Begin with offline/sample data; the cookbook does not require an OpenAI API key.
- Keep the taxonomy evolvable rather than overfitting to the EV-order example.
- Design for human review: outputs should tell reviewers where to inspect next, not just report metrics.

## Acceptance criteria copied into README
See `../README.md` for the task's acceptance criteria and open questions.

## Source memory context
The originating request included recalled memory context. It was treated as reference context rather than new task requirements. Operationally relevant preserved notes:

- taskOS canonical repository: `/data/taskOS`, GitHub `kishorkukreja/taskOS`.
- taskOS convention: `tasks/<slug>/README.md` plus `docs/idea.md`.
- The user prefers operationalized knowledge as tasks/skills, not passive notes.
- The user prefers rigorous, inspectable, repo-centric AI workflow infrastructure.
