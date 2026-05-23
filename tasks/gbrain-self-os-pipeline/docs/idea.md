# GBrain Self-OS Pipeline Integration — Idea Capture

Created: 2026-05-23
Status: captured
Repository: /data/taskOS
Task folder: /data/taskOS/tasks/gbrain-self-os-pipeline

## Request source

- Source: direct user request in Hermes conversation
- Captured by: Hermes
- Date: 2026-05-23

## User-provided source notes

After reviewing the installed GBrain skills and deciding the recommended subset looked good, the user asked:

> okay so these are good- can we save them sonewher maybe in taskos and then create a task in kanban to set thgem up later ;

## Context

GBrain has been installed and connected to Hermes as a persistent MCP service. The current architecture decision is:

- Self-OS remains the durable Git-backed system of record.
- GBrain becomes the semantic/search/graph/timeline/health/query layer over Self-OS.
- Hermes remains the operator/orchestrator that decides when to read, write, sync, enrich, brief, and create follow-up work.

This task captures the skill survey and setup plan so it can be implemented later rather than trying to wire everything up immediately.

## Current GBrain state at capture time

Known runtime facts from the setup/survey session:

- GBrain binary: `/root/.bun/bin/gbrain`
- Version observed: `v0.40.6.0`
- Self-OS repo: `/data/Self-OS`
- GBrain MCP service: `gbrain.service` on `127.0.0.1:8650`
- Hermes MCP URL: `http://127.0.0.1:8650/mcp`
- Existing sync cron: `gbrain-sync-after-wiki-compile`, daily at `02:00 UTC`
- Sync command must explicitly use `--repo /data/Self-OS`
- GBrain skills were found under `/root/gbrain/skills`
- 46 GBrain skill directories were surveyed
- GBrain MCP discovered 67 tools

Known health gaps from the survey session:

- Pending migrations: `gbrain apply-migrations --yes`
- Brain score observed: `44`
- Missing embeddings: 35 chunks
- Link graph problem: 1020 pages but 0 links
- Timeline extraction problem: 0 structured timeline entries

## Strategic position

Do not adopt every scaffolded GBrain skill just because it exists.

The important distinction:

- GBrain skills are operational manuals for GBrain-aware agents.
- Hermes skills remain the procedural memory layer for Hermes itself.
- Self-OS wiki remains canonical for durable knowledge.
- taskOS captures implementation/backlog work.
- Hermes Kanban is for executable follow-up work.

The target is a selective integration that improves the Self-OS operating loop without creating a second, conflicting knowledge pipeline.

## Desired outcome

Create a reliable GBrain-enhanced Self-OS loop:

```text
Capture
→ Self-OS raw markdown
→ wiki compile
→ GBrain sync
→ GBrain maintenance
→ GBrain query/synthesis layer
→ Self-OS briefs, tasks, skills, and public outputs
```

## Non-goals

- Do not replace Self-OS raw capture with direct GBrain ingestion by default.
- Do not duplicate existing Self-OS daily/weekly brief systems with GBrain's briefing/task-manager skills.
- Do not create a dashboard for v0.
- Do not let GBrain direct writes split the canonical knowledge base unless there is a writeback/sync convention.
- Do not run expensive GBrain dream/concept synthesis loops unattended without budget/cost controls.

## Acceptance criteria

- GBrain migrations, embeddings, link extraction, and timeline extraction are healthy or explicitly documented as blocked.
- Existing daily post-compile GBrain sync remains working with `--repo /data/Self-OS`.
- A post-sync maintenance job exists and logs/report failures cleanly.
- Hermes has reusable guidance/skill memory for using GBrain in Self-OS workflows.
- High-value GBrain skills are mapped to concrete trigger points in the Self-OS pipeline.
- GBrain query is used before web/current research when the question overlaps existing Self-OS knowledge.
- Self-OS daily/evening brief includes a compact GBrain status section if useful.
- Direct GBrain capture rules are clear: quick thoughts may go to GBrain, canonical source capture goes to Self-OS.

## Open questions

- Which embedding provider/key should GBrain use for unattended embedding jobs?
- Should post-sync maintenance run every day or only after successful wiki compile/sync?
- Should `concept-synthesis` run weekly, monthly, or manually?
- Should `article-enrichment` operate on a curated shortlist only, or all pages marked `needs_enrichment`?
- Should GBrain health reports be saved in Self-OS, taskOS, or only logs?
- Should Hermes create a dedicated `gbrain-self-os-pipeline` skill, or patch `knowledge-base-operations` with a GBrain submode?
