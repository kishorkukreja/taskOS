# Setup Plan — GBrain Self-OS Pipeline

Created: 2026-05-23

## Phase 0 — Preconditions

- Confirm `/root/.bun/bin/gbrain` exists.
- Confirm `/data/Self-OS` is the canonical repo path.
- Confirm `gbrain.service` is active on `127.0.0.1:8650`.
- Confirm Hermes MCP server `gbrain` connects successfully.
- Confirm existing GBrain sync cron uses explicit `--repo /data/Self-OS`.

## Phase 1 — Fix GBrain health foundation

Run from `/data/Self-OS` unless command docs say otherwise.

Potential commands:

```bash
/root/.bun/bin/gbrain apply-migrations --yes
/root/.bun/bin/gbrain sync --repo /data/Self-OS --strategy code
/root/.bun/bin/gbrain embed --stale
/root/.bun/bin/gbrain extract links --dir /data/Self-OS
/root/.bun/bin/gbrain extract timeline --dir /data/Self-OS
/root/.bun/bin/gbrain features --json
```

Acceptance criteria:

- migrations no longer pending
- missing embeddings are resolved or explicitly blocked by provider/key configuration
- link graph is non-zero
- timeline entries are non-zero or limitation is documented
- feature/health output is logged

Known possible blocker:

- Embeddings may require an embedding provider/API key. Earlier session reported: `OpenAI embedding requires OPENAI_API_KEY`.

## Phase 2 — Add post-sync maintenance cron

Existing sync cron:

- `gbrain-sync-after-wiki-compile`
- daily at `02:00 UTC`

Add a later job, e.g. `02:30` or `03:00 UTC`, that runs:

1. skillpack/features check
2. stale embeddings
3. link extraction
4. timeline extraction
5. health report/logging

Suggested properties:

- script-only/no-agent if deterministic and quiet-on-success
- append logs to `/var/log/gbrain-sync.log` or a separate `/var/log/gbrain-maintenance.log`
- avoid Telegram spam unless failures occur
- include explicit `--repo /data/Self-OS` wherever supported

## Phase 3 — Patch Hermes operating guidance

Create or patch a Hermes skill so future agents know the architecture:

- Self-OS is canonical durable knowledge.
- GBrain is the semantic/graph/timeline/query/health layer.
- taskOS is the backlog/spec capture repo.
- Kanban is for executable follow-up work.
- For Self-OS-relevant research, query GBrain before web/current search.
- For direct source capture, use Self-OS raw wiki first, then sync to GBrain.
- Use direct GBrain capture only for quick thoughts or when explicitly requested.

Candidate approaches:

- Patch `knowledge-base-operations` with a GBrain submode.
- Create a dedicated Hermes skill: `gbrain-self-os-pipeline`.

## Phase 4 — Integrate into brief/research flows

Daily/evening Self-OS brief additions:

- GBrain health score/status
- sync freshness
- embeddings/link/timeline status
- notable new concepts/entities if cheap to compute
- failures requiring user review

Research flow additions:

```text
GBrain query
→ identify existing context
→ web/current research if needed
→ compare new vs known
→ save useful sources/findings to Self-OS
→ resync/maintain GBrain later
```

## Phase 5 — Pilot enrichment/synthesis

### Article enrichment pilot

Start with a small curated list of high-signal article pages, not all captures.

Acceptance criteria:

- executive summary
- why it matters to the user's projects/interests
- verbatim quotable lines
- key insights
- surprising/counterintuitive points
- standard markdown cross-links
- raw content preserved

### Concept synthesis pilot

Start weekly/monthly or manually with one domain.

Acceptance criteria:

- duplicate concepts merged or marked as aliases
- T1/T2/T3/T4 tiers assigned
- T1/T2 pages have real synthesis
- concept map/README updated
- source evidence remains traceable

## Phase 6 — Quality gates for public/high-stakes output

Use selectively:

- `academic-verify` for academic/model claims
- `cross-modal-review` for public newsletters, important strategy memos, and high-stakes recommendations
- `article-enrichment` shape for transforming raw content into quotable, actionable notes

## Risks

- Direct GBrain writes could split the canonical knowledge base if writeback is unclear.
- Daily concept synthesis could become expensive/noisy.
- Running all scaffolded skills would duplicate existing Hermes/Self-OS workflows.
- Link/timeline extraction commands may need repo-specific path testing.
- Embedding jobs may silently fail if provider credentials are missing.

## Implementation checklist

- [ ] Re-run `gbrain features --json` and record baseline.
- [ ] Apply migrations.
- [ ] Configure/verify embedding provider.
- [ ] Run stale embedding job.
- [ ] Run link extraction.
- [ ] Run timeline extraction.
- [ ] Verify health score improves.
- [ ] Add deterministic maintenance script.
- [ ] Add Hermes cron for maintenance.
- [ ] Patch/create Hermes GBrain operating skill.
- [ ] Add GBrain section to Self-OS daily/evening brief generator.
- [ ] Pilot article enrichment on selected captures.
- [ ] Pilot concept synthesis on one domain.
- [ ] Document final routing rules in taskOS and Hermes skill memory.
