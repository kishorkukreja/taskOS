# GBrain Self-OS Pipeline Integration

Status: captured
Created: 2026-05-23
Owner: Kish / Hermes
Priority: high

## Summary

Set up the high-value GBrain skills as an operational layer on top of Self-OS: Self-OS remains the canonical Git-backed knowledge base, while GBrain becomes the semantic, graph, timeline, health, and query/synthesis layer.

The goal is not to adopt every scaffolded GBrain skill. The goal is to operationalize the subset that improves Hermes' default behavior and the Self-OS compile/sync/briefing pipeline.

## Current artifact state

- Skill survey: `docs/gbrain-skill-survey.md`
- Setup plan: `docs/setup-plan.md`
- Idea capture: `docs/idea.md`
- Spec: not started
- PRD: not started
- Issues: not started
- Implementation plan: not started

## High-value GBrain skills to integrate

### Core/default behavior

- `brain-ops`
- `query`
- `capture`
- `maintain`
- `frontmatter-guard`
- `brain-taxonomist`

### High-leverage Self-OS additions

- `article-enrichment`
- `concept-synthesis`
- `perplexity-research`
- `academic-verify`
- `cross-modal-review`
- `skillpack-check`

## Desired pipeline shape

```text
Capture
→ Self-OS raw markdown
→ wiki compile
→ GBrain sync
→ GBrain maintenance
→ query/synthesis layer
→ Self-OS briefs, tasks, skills, and public outputs
```

## Next conversion step

- [ ] Convert `docs/idea.md` and `docs/setup-plan.md` into a concrete implementation spec.
- [ ] Fix GBrain health foundation: migrations, embeddings, link extraction, timeline extraction.
- [ ] Add post-sync maintenance cron after the existing GBrain sync job.
- [ ] Patch/create Hermes operating guidance so agents query GBrain before web/current research when relevant.
- [ ] Pilot `article-enrichment` on selected high-signal captures.
- [ ] Pilot weekly/monthly `concept-synthesis` for Self-OS memory tree.
- [ ] Add GBrain status to Self-OS daily/evening operating brief.

## Linked runtime state

- Self-OS repo: `/data/Self-OS`
- GBrain binary: `/root/.bun/bin/gbrain`
- GBrain MCP service: `http://127.0.0.1:8650/mcp`
- GBrain sync script: `/root/.hermes/scripts/gbrain_sync_self_os.sh`
- GBrain sync log: `/var/log/gbrain-sync.log`
- Existing sync cron: `gbrain-sync-after-wiki-compile`, daily at 02:00 UTC
