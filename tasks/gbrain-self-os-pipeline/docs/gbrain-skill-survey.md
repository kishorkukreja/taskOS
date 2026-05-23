# GBrain Skill Survey for Self-OS

Created: 2026-05-23

## Executive recommendation

The valuable GBrain skills for the Self-OS pipeline are not primarily the duplicate daily-task or briefing skills. The most important ones are the skills that make GBrain a semantic, graph, timeline, health, and synthesis layer over the existing Git-backed Self-OS wiki.

Recommended core set:

1. `brain-ops`
2. `query`
3. `capture`
4. `maintain`
5. `frontmatter-guard`
6. `brain-taxonomist`
7. `article-enrichment`
8. `concept-synthesis`
9. `perplexity-research`
10. `academic-verify`
11. `cross-modal-review`
12. `skillpack-check`

## Architectural fit

Self-OS remains the durable Git-backed memory.

GBrain becomes:

- semantic query layer
- graph layer
- timeline layer
- maintenance/health layer
- synthesis layer over existing notes

Hermes remains:

- operator/orchestrator
- cron manager
- task/Kanban creator
- skill maintainer
- bridge between GBrain, Self-OS, taskOS, and user-facing outputs

## Must-use / core behavior skills

### `brain-ops`

Purpose: brain-first lookup, read/enrich/write loop, citations, backlinks.

How it should affect Hermes:

- When the user asks “what do we know about X?”, “have we seen this before?”, “who is this?”, or asks for background on a known topic, query GBrain before answering from memory or the web.
- Use GBrain as the living query layer over the compiled Self-OS corpus.

Pipeline role:

```text
User asks / agent researches
→ query GBrain first
→ answer with citations/context
→ optionally write useful finding back
```

### `query`

Purpose: 3-layer brain search and synthesis.

How it should affect Hermes:

- Main read interface for GBrain.
- Use for recall across Self-OS, not as a replacement for `session_search` when the question is about prior conversations.

Pipeline role:

```text
Question
→ GBrain keyword/hybrid search
→ read top pages
→ cite gaps/conflicts
```

### `capture`

Purpose: simple “save this thought/content” front door.

How it should affect Hermes:

- Use for quick thought capture.
- Do not replace formal Self-OS source capture.

Routing rule:

- “Save this thought / remember this / quick note” → GBrain capture may be appropriate.
- “Add this article/repo/thread to wiki/Self-OS” → Self-OS raw capture first, then GBrain sync.

### `maintain`

Purpose: brain health, links, timeline, citations, stale pages, dream/consolidation.

How it should affect Hermes:

- Main post-sync health layer.
- Especially important because survey state showed pages but no links/timeline entries.

Pipeline role:

```text
wiki compile
→ gbrain sync
→ migrations/embeddings/link extraction/timeline extraction/health report
```

### `frontmatter-guard`

Purpose: prevent malformed YAML/frontmatter from entering GBrain.

How it should affect Hermes:

- Use as a guardrail after Self-OS raw/wiki writes and before/around sync.
- Complement existing wiki compile/lint checks.

### `brain-taxonomist`

Purpose: filing gate before GBrain page writes.

How it should affect Hermes:

- Use when writing directly into GBrain.
- Less important for Self-OS raw captures because Self-OS already owns routing.

Routing rule:

```text
Direct GBrain write
→ brain-taxonomist decides destination
```

## High-value Self-OS additions

### `article-enrichment`

Purpose: turn raw article dumps into useful pages with executive summary, quotes, key insights, why-it-matters, and cross-links.

Why it matters:

- Prevents archive rot.
- Converts raw captures into operationally useful knowledge.
- Strong fit with the user's preference for high-signal, useful, quotable notes.

Best fit:

```text
raw article capture
→ wiki compile
→ gbrain sync
→ article-enrichment for selected high-signal articles
→ write enriched page/concept links
```

Do not run on every article by default. Use a shortlist or `needs_enrichment` marker.

### `concept-synthesis`

Purpose: dedupe and synthesize concept stubs into a tiered intellectual map.

Why it matters:

- Strong fit with Self-OS source/topic/global memory.
- Converts scattered repeated notes into living concepts.
- Useful for AI research, agent OS ideas, supply-chain patterns, and strategy notes.

Best fit:

- Weekly or monthly, not daily.
- Start with one wiki or one concept domain before broad automation.

### `perplexity-research`

Purpose: brain-augmented web research; identify what is new versus already known.

Why it matters:

- Avoids duplicate research.
- Makes research more cumulative.

Best fit:

```text
GBrain query
→ web/current research
→ compare known vs new
→ Self-OS capture/update
```

### `academic-verify`

Purpose: verify academic claims/citations.

Best fit:

- AI paper claims.
- Model/eval claims.
- Newsletter/public output claims.
- Use selectively for high-stakes claims.

### `cross-modal-review`

Purpose: second-model quality gate.

Best fit:

- Sunday AIResearch brief.
- Supply Chain Signals newsletter.
- Major concept synthesis.
- Public-facing articles or high-stakes recommendations.

### `skillpack-check`

Purpose: health report over GBrain skills and migrations.

Best fit:

- Add to daily/weekly GBrain health checks.
- Use after GBrain upgrades.

## Useful but not central yet

- `smoke-test`: useful after service restarts/upgrades.
- `cron-scheduler`: helpful scheduling hygiene; Hermes cron remains primary.
- `reports`: useful if GBrain health reports need timestamped storage.
- `minion-orchestrator`: defer until GBrain jobs clearly beat Hermes cron/delegate_task.

## Ingestion skills: use carefully

Relevant but should not replace Self-OS raw capture by default:

- `ingest`
- `idea-ingest`
- `media-ingest`
- `meeting-ingestion`
- `voice-note-ingest`
- `webhook-transforms`
- `archive-crawler`
- `book-mirror`

Recommended rule:

- Self-OS remains canonical for source capture.
- GBrain can handle quick thoughts and query/synthesis.
- Specialized GBrain ingestion can be piloted for voice notes, meetings, and archive crawling only after writeback/sync conventions are explicit.

## Low priority / defer

- `publish`
- `brain-pdf`
- `daily-task-manager`
- `daily-task-prep`
- `briefing`
- `soul-audit`
- `skill-creator`
- `skillify`
- `skillpack-harvest`
- `testing`
- `functional-area-resolver`
- `migrate`
- `cold-start`
- `setup`

Reason: they are either one-time setup utilities, duplicate existing Self-OS/Hermes capabilities, or become useful only after the core GBrain layer is healthy.
