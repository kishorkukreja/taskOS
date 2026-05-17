# Self-OS Memory Tree v0 — Idea Capture

Created: 2026-05-17
Status: captured
Repository: /data/taskOS
Task folder: /data/taskOS/tasks/self-os-memory-tree-v0

## Request source

- Source: direct user request in Telegram
- Captured by: Hermes
- Date: 2026-05-17

## User-provided source notes

The user asked to save the source/topic/global memory model ideas in taskOS for later pickup:

> Can you save all of this in taskos please and add details there, I will pick them up when needed

The conversation was triggered by reviewing OpenHuman:

- Repository: https://github.com/tinyhumansai/openhuman
- OpenHuman pattern: source/topic/global memory trees over ingested data.
- OpenHuman stores memory locally in SQLite and an Obsidian-style Markdown vault.
- Hermes recommendation: do not adopt OpenHuman as a new core system now; use it as a strategic reference for Self-OS memory architecture.

## What we are trying to do

Add a Self-OS-native **Memory Tree v0** layer that organizes existing raw captures and operating signals into three levels:

1. **Source Memory** — what a specific stream is teaching us.
2. **Topic Memory** — the latest living state of a concept/project/person/company/workflow/theme.
3. **Global Memory** — what changed across the whole system today/this week, and what agents should do next.

This should sit on top of the existing Git-backed Self-OS wiki system rather than replacing it.

## Honest strategic position

Do **not** install or adopt OpenHuman as a core dependency right now.

Use OpenHuman as a reference implementation / architecture signal because it validates patterns already aligned with Self-OS:

- Readable local-first memory.
- Markdown vaults instead of opaque memory only.
- Source/topic/global summary trees.
- Auto-fetch from integration streams.
- Memory that can drive action, not just search.

But Self-OS should remain:

- Git-backed.
- Markdown-first.
- Telegram-operated.
- Hermes skill/cron-driven.
- PR-reviewed for interpreted knowledge.
- Raw-capture-friendly with direct commits where appropriate.

## Why it matters

Self-OS is moving from passive knowledge capture into an active daily operating layer. The current system is good at saving raw sources, running scheduled digests, and delivering Telegram summaries. The next capability is a structured memory layer that can answer:

- What has changed across my world?
- Which topics are rising or decaying?
- What needs review?
- What should agents do next?
- Which raw captures should become tasks, skills, content, or research?
- Which assumptions are stale?

The source/topic/global model is the bridge from **knowledge base** to **operating system**.

## Core model

### 1. Source Memory

Question answered:

> What happened in this specific stream?

Examples of sources:

- X bookmarks.
- GitHub trending repos.
- AI newsletters.
- X/Twitter AI blog discovery.
- YouTube videos.
- Supply-chain news feeds.
- Telegram ideas.
- Claude/Codex coding logs.
- GitHub PRs.
- Hermes cron outputs.
- NotebookLM/persona research.

Source memory pages summarize one stream over time. They should not replace raw captures; they summarize what the stream has recently contributed.

Example source memory files:

```text
/data/Self-OS/wikis/ai-research-os/memory/sources/x-bookmarks.md
/data/Self-OS/wikis/ai-research-os/memory/sources/github-trending.md
/data/Self-OS/wikis/ai-research-os/memory/sources/ai-newsletters.md
/data/Self-OS/wikis/ai-research-os/memory/sources/youtube.md
/data/Self-OS/wikis/ai-research-os/memory/sources/repos.md
/data/Self-OS/wikis/coding-projects-os/memory/sources/hermes-crons.md
/data/Self-OS/wikis/coding-projects-os/memory/sources/telegram-ideas.md
```

Example schema:

```markdown
# Source Memory: X Bookmarks

## Purpose
What this source is good for.

## Last updated
2026-05-17

## Recent signal
- New bookmarks are clustering around agent memory, MCP, and coding workflows.
- Several sources point toward local-first personal AI systems.
- Some items are content-worthy, not implementation-worthy.

## High-signal captures
### 2026-05-17 — OpenHuman
- Source: raw/repos/2026-05-17-openhuman.md
- Topics: [[memory-systems]], [[personal-ai-os]], [[obsidian]], [[agent-workflows]]
- Why it matters: validates source/topic/global memory-tree architecture.

## Decay / stale notes
- Older generic “AI assistant” captures are less useful unless tied to integration or memory architecture.

## Candidate promotions
- Promote OpenHuman pattern into Self-OS memory-tree design note.
```

### 2. Topic Memory

Question answered:

> What is the latest state of this concept, project, person, company, workflow, or theme?

Examples:

- `coding-agents`
- `mcp`
- `self-os`
- `memory-systems`
- `agent-workflows`
- `local-models`
- `openhuman`
- `claude-code`
- `tradingagents`
- `workflow-radar`
- `supply-chain-risk`
- `manufacturing-ai`

Topic memory is the highest-leverage layer. It lets Hermes answer:

- What have we learned about AI memory systems?
- What is changing in coding agents this week?
- What is the latest on MCP workflows?
- Which topic deserves content this week?
- Which raw captures should become skills?

Topic pages should be **hybrid**:

- Hermes may append dated evidence.
- Hermes may propose thesis updates.
- Hermes may add content/task/skill candidates.
- Major thesis changes should be reviewable via branch/PR.

This protects against slow AI corruption of the user’s worldview.

Example topic memory files:

```text
/data/Self-OS/wikis/ai-research-os/memory/topics/self-os.md
/data/Self-OS/wikis/ai-research-os/memory/topics/coding-agents.md
/data/Self-OS/wikis/ai-research-os/memory/topics/memory-systems.md
/data/Self-OS/wikis/ai-research-os/memory/topics/mcp.md
/data/Self-OS/wikis/ai-research-os/memory/topics/local-models.md
```

Example schema:

```markdown
---
type: topic-memory
topic: memory-systems
state: active
date_created: 2026-05-17
date_modified: 2026-05-17
confidence: mixed
allowed_agent_actions:
  - append-evidence
  - suggest-promotions
  - suggest-content
review_required_for:
  - thesis-change
  - implementation-decision
---

# Topic Memory: Memory Systems

## Current thesis
Readable, local-first memory systems are becoming the differentiator for personal AI OS products. The important pattern is not “chat history”; it is source ingestion → durable markdown → topic summaries → global operating briefs.

## Latest changes
- 2026-05-17: OpenHuman uses source/topic/global memory trees with Markdown + SQLite.
- 2026-05-14: OpenAI cookbook memory-compaction pattern suggests separating raw evidence, compacted state, and durable memory.
- 2026-05-02: Self-OS operating-loop design established wiki + cron + Telegram as durable memory surface.

## Evidence ledger
- [[raw/repos/2026-05-17-openhuman]]
- [[raw/articles/2026-05-06-openai-building-reliable-agents-memory-compaction]]
- [[coding-projects-os/raw/projects/self-os-operating-loop/...]]

## Source diversity
- GitHub repos.
- Official docs / cookbooks.
- User operating-loop decisions.
- X/Twitter posts where extractable.

## Implications for Self-OS
- Add topic-level living pages.
- Keep raw sources immutable.
- Use daily global memory to select agent actions.
- Avoid opaque vector-only memory in v0.

## Content angles
- “AI memory is not a vector DB. It is an operating discipline.”
- “The future personal AI OS is a readable wiki with agents attached.”

## Skill candidates
- `self-os-memory-tree`
- `memory-compile`

## taskOS candidates
- Build Markdown memory compiler for ai-research-os.
- Add topic hotness scoring.
- Integrate topic movement into daily Self-OS brief.

## Open questions
- Should topic pages be manually curated, auto-generated, or hybrid?
- How aggressively should Hermes update existing topic theses?

## Stale assumptions
- Generic “AI assistant” notes are less useful unless tied to memory architecture, integration, or concrete workflows.

## Agent notes
Hermes may append evidence and propose changes. Hermes must not rewrite the current thesis without PR/user review.
```

### 3. Global Memory

Question answered:

> What changed across my whole world today / this week?

Global memory should become the intelligence layer that powers daily/weekly Self-OS briefs.

Daily global pages should cover:

- Executive summary.
- What changed.
- Rising topics.
- Falling/stale topics.
- Decisions needed.
- Promotion queue updates.
- Agent actions proposed.
- Content opportunities.
- Risks / contradictions.
- Evidence paths.

Example daily file:

```text
/data/Self-OS/wikis/ai-research-os/memory/global/daily/2026-05-17.md
```

Example schema:

```markdown
---
type: global-memory-daily
date: 2026-05-17
inputs:
  raw_files_scanned: 12
  topics_updated: 5
  source_pages_updated: 4
---

# Global Memory — 2026-05-17

## Executive summary
Today’s strongest signal is that local-first personal AI systems are converging on readable memory trees: source ingestion, topic summaries, and daily global state.

## What changed
1. OpenHuman validated the source/topic/global memory architecture.
2. X Bookmark Inbox cron was installed but blocked on xurl auth.
3. Trending Workflows Radar is now scheduled for daily morning runs.
4. Supply Chain Signals pipeline continues to need visual/source discipline.

## Rising topics
### memory-systems
- Momentum: rising
- Evidence: OpenHuman, OpenAI compaction cookbook
- Action: design Self-OS memory-tree v0

### coding-agents
- Momentum: steady
- Evidence: workflow radar, GitHub trending, X blogs
- Action: continue sourcing practical workflows

## Falling/stale topics
- Generic AI assistant/productivity notes without implementation patterns.

## Decisions needed
- Do we implement memory tree as Markdown-only first?
- Should topic updates go through PR review?

## Promotion queue updates
- Task: design Markdown memory tree v0.
- Content: “AI memory is a readable wiki, not a vector DB.”
- Skill candidate: `memory-compile`.

## Agent actions proposed
1. Create `memory/` folder structure.
2. Add `memory-compile` script.
3. Run on one wiki first: `ai-research-os`.
4. Add output to daily Self-OS brief.

## Content opportunities
- “Personal AI needs memory trees, not chat history.”
- “Why Self-OS is Git-backed memory, not a dashboard.”

## Risks / contradictions
- Avoid installing OpenHuman into core stack.
- Avoid building a second database before Markdown proves enough.

## Evidence paths
- raw repos/articles/operating-loop paths.
```

Weekly global pages should become strategic reviews:

```text
/data/Self-OS/wikis/ai-research-os/memory/global/weekly/2026-W20.md
```

Weekly memory should cover:

- Strongest topic movement.
- Stale topics.
- New agent tasks.
- Content pipeline candidates.
- Skill candidates.
- Research gaps.
- Repo/cron health.
- Supply-chain/news themes.
- What to kill or deprioritize.

## Proposed folder structure

Start with `ai-research-os` only:

```text
/data/Self-OS/wikis/ai-research-os/
  raw/
    repos/
    x-bookmarks/
    x-blogs/
    youtube/
    articles/
    workflow-radar/

  memory/
    sources/
      x-bookmarks.md
      github-trending.md
      ai-newsletters.md
      youtube.md
      repos.md

    topics/
      coding-agents.md
      mcp.md
      self-os.md
      memory-systems.md
      local-models.md
      openhuman.md
      agent-workflows.md

    global/
      daily/
        2026-05-17.md
      weekly/
        2026-W20.md

    index.md
    entity-index.md
    open-questions.md
    promotion-queue.md
```

Do not roll this out to all wikis immediately. Validate it on `ai-research-os` first for one week.

## Topic state model

Each topic should have a state:

```yaml
topic_state: emerging | active | watch | mature | stale | archived
```

Examples:

- `memory-systems`: active
- `desktop-mascot-agents`: watch
- `old-prompt-libraries`: stale
- `mcp`: active
- `composio-integrations`: watch

This allows the daily brief to say:

- New active topic: memory-systems.
- Stale topic: open-design systems, no new sources in 14 days.
- Watch topic: Composio integrations, useful but not core yet.

## Confidence labels

Memory updates should distinguish confidence:

- **Observed** — directly present in source.
- **Inferred** — Hermes interpretation from multiple sources.
- **Hypothesis** — plausible but needs validation.
- **Decision** — user-approved or operating-contract-approved.

Example:

```markdown
## Current thesis
**Inferred:** Personal AI systems are converging on readable local memory trees.

## Evidence
**Observed:** OpenHuman docs describe source/topic/global memory trees.
**Observed:** OpenAI cookbook uses memory compaction for long-running agents.
**Hypothesis:** Self-OS can get 80% of the benefit with Markdown-only memory pages.
```

This prevents the wiki from becoming overconfident sludge.

## Agent affordances

Each topic page should define what agents may and may not do.

Example:

```markdown
## Agent affordances

Hermes may:
- Append dated evidence.
- Add candidate content angles.
- Add task candidates to promotion queue.

Hermes must not:
- Rewrite current thesis without PR.
- Mark implementation decisions as final without user approval.
- Create Kanban tasks unless promoted through taskOS or explicitly requested.
```

This fits the user’s preference for rigorous, reviewable, high-taste AI output.

## Promotion queue

Add:

```text
/data/Self-OS/wikis/ai-research-os/memory/promotion-queue.md
```

The memory tree should not just summarize; it should decide what happens next.

Example schema:

```markdown
# Promotion Queue

## Promote to skill
- OpenHuman memory-tree pattern → possible `self-os-memory-tree` skill.

## Promote to taskOS
- Build Markdown memory compiler for ai-research-os.
- Add topic hotness scoring.
- Integrate topic movement into daily Self-OS brief.

## Promote to content
- Personal AI memory trees article.
- Source/topic/global model explainer.

## Promote to research
- Compare OpenHuman, OpenAI compaction, Karpathy wiki, Self-OS.

## Kill / ignore
- Desktop mascot UX for now.
- Full Composio integration for now.
```

This is the bridge from knowledge capture to AI operating system.

## Hotness scoring v0

Do not start with a database. Use frontmatter and simple scoring.

Each raw capture can include or later be enriched with:

```yaml
topics:
  - memory-systems
  - self-os
  - agent-workflows
signals:
  novelty: 4
  relevance: 5
  actionability: 4
  credibility: 3
  recency: 5
promotion:
  skill_candidate: false
  task_candidate: true
  content_candidate: true
```

Simple hotness formula:

```text
hotness = count_recent_mentions
        + weighted_relevance
        + actionability
        + cross_source_diversity
        + user_mentions
```

Daily memory can then report:

```markdown
## Rising topics today
1. memory-systems — 4 new sources, 2 task candidates, 1 content candidate
2. coding-agents — 7 new mentions, mostly workflows
3. mcp — 3 new sources, 1 implementation candidate
```

This should be enough for v0.

## Minimal v0 implementation sequence

### Phase 0: Manual seed

Manually create memory pages for `ai-research-os`.

Seed topics:

- `memory-systems`
- `self-os`
- `coding-agents`
- `mcp`
- `local-models`

Use recent captures:

- OpenHuman.
- OpenAI memory compaction.
- Claude/Codex workflows.
- X Bookmark Inbox.
- Trending Workflows Radar.

### Phase 1: Folder structure

Create:

```text
/data/Self-OS/wikis/ai-research-os/memory/
  sources/
  topics/
  global/daily/
  global/weekly/
  index.md
  entity-index.md
  open-questions.md
  promotion-queue.md
```

### Phase 2: Scripted daily compiler

Create:

```text
/data/Self-OS/scripts/compile_memory_tree.py
```

Responsibilities:

1. Scan recent raw files.
2. Extract or infer topics from frontmatter/body.
3. Update source memory pages.
4. Append dated evidence to topic pages.
5. Create daily global memory page.
6. Update promotion queue.
7. Send concise Telegram summary when run via Hermes cron.

Important: v0 should **append**, not rewrite curated topic pages.

### Phase 3: Hermes skill

Create a skill such as:

```text
self-os-memory-tree
```

Potential modes:

- `compile-daily`
- `compile-weekly`
- `update-topic`
- `promote-candidates`
- `lint-memory`

### Phase 4: Cron

Add daily cron once manual/scripted run is proven.

Candidate:

```text
self-os-memory-compile 10:45pm UK
```

Reason: run before the existing 11pm Self-OS daily brief so the brief can consume global memory.

Potential Telegram output:

```markdown
## Self-OS Memory Compile — 2026-05-17

Rising topics:
1. memory-systems — OpenHuman + OpenAI compaction pattern
2. coding-agents — workflow radar sources
3. x-bookmarks — blocked on auth

Promotions:
- Task: design Markdown memory tree v0
- Content: “AI memory is a readable wiki, not a vector DB”
- Skill candidate: memory-compile

Saved:
`ai-research-os/memory/global/daily/2026-05-17.md`
```

### Phase 5: Integrate with daily Self-OS brief

The daily Self-OS brief should read:

```text
memory/global/daily/latest.md
memory/promotion-queue.md
memory/topics/*.md modified recently
```

Then the daily brief can include:

- Most active topics.
- New content candidates.
- New skill candidates.
- Research gaps.
- Tasks worth promoting.

## Wiki-specific expansion plan

### ai-research-os

Best for:

- AI agents.
- LLMs.
- Coding agents.
- MCP.
- Local models.
- Memory systems.
- Research papers.
- GitHub repos.

Example topics:

```text
coding-agents
agent-memory
mcp
local-models
evals
ai-infra
design-tools
personal-ai-os
```

### supply-chain-os

Best for:

- Ports.
- Tariffs.
- Manufacturing.
- Logistics.
- Geopolitics.
- Capacity.
- Inventories.
- Disruption signals.

Example topics:

```text
red-sea
tariffs
china-plus-one
semiconductors
freight-rates
port-congestion
inventory-risk
manufacturing-ai
```

Global weekly memory here should feed **Supply Chain Signals**.

### coding-projects-os

Best for:

- Self-OS implementation.
- Hermes skills.
- taskOS.
- Kanban.
- Codex/Claude workflows.
- PR/QA loops.

Example topics:

```text
self-os-operating-loop
night-shift-agents
kanban
taskos
hermes-skills
github-review
workspace
```

This becomes the operating memory for what agents should build next.

## Constraints and guardrails

- Do not build SQLite/vector search first.
- Do not replace raw captures.
- Do not let agents rewrite topic theses daily.
- Use append-first behavior for topic pages.
- Use branch + PR for interpreted/canonical memory changes.
- Direct commit to master is acceptable for raw captures/simple taskOS capture, but memory compiler implementation should use PRs.
- Keep Telegram as the control surface.
- Keep Git-backed Markdown as the durable record.
- Do not create a dashboard in v0.
- Do not adopt OpenHuman as a dependency.
- Do not treat all sources equally; track source credibility.
- Distinguish Observed/Inferred/Hypothesis/Decision.
- Topic changes that affect strategy should be reviewed by the user.

## Anti-goals

- Full OpenHuman clone.
- New desktop app.
- Mascot/voice/meeting-agent UX.
- Composio integration layer in v0.
- Opaque vector-only memory.
- Broad rollout across every wiki before ai-research-os pilot proves value.
- Dashboard-first implementation.

## Acceptance criteria

### v0 Pilot

- [ ] `/data/Self-OS/wikis/ai-research-os/memory/` exists with sources/topics/global folders.
- [ ] At least five seed topic pages exist:
  - [ ] `self-os.md`
  - [ ] `coding-agents.md`
  - [ ] `memory-systems.md`
  - [ ] `mcp.md`
  - [ ] `local-models.md`
- [ ] `promotion-queue.md` exists and includes skill/taskOS/content/research/kill sections.
- [ ] One daily global memory page is generated manually or by script.
- [ ] Source memory pages exist for at least three streams.
- [ ] Topic pages include current thesis, evidence ledger, implications, open questions, and agent affordances.
- [ ] Confidence labels are used for important claims.

### Scripted compiler

- [ ] `scripts/compile_memory_tree.py` can scan recent raw files.
- [ ] It can extract frontmatter topics where available.
- [ ] It can suggest/infer topics when missing.
- [ ] It appends evidence to topic pages rather than rewriting them.
- [ ] It creates a daily global memory page.
- [ ] It updates the promotion queue.
- [ ] It emits a Telegram-ready summary.
- [ ] It avoids committing if unrelated dirty repo changes exist.

### Integration

- [ ] Existing Self-OS daily brief can read latest global memory and promotion queue.
- [ ] Memory compile can run before daily brief, ideally around 10:45pm UK.
- [ ] The daily brief reports rising topics, stale topics, and promotions.
- [ ] Weekly synthesis can consume weekly/global memory.

### Review and quality

- [ ] Topic thesis changes require branch/PR or explicit user approval.
- [ ] Generated memory pages include evidence paths.
- [ ] No secrets or credentials are stored.
- [ ] The system remains inspectable as plain Markdown.

## Likely files, repos, or services involved

- `/data/Self-OS` — implementation target repo.
- `/data/Self-OS/wikis/ai-research-os/memory/` — initial pilot memory tree.
- `/data/Self-OS/scripts/compile_memory_tree.py` — future compiler script.
- `/data/Self-OS/scripts/generate_self_os_brief.py` — should later consume global memory.
- `/data/Self-OS/docs/self-os-operating-contract.md` — may need memory-tree policy additions.
- `/data/taskOS/tasks/self-os-memory-tree-v0/` — this task capture.
- Hermes skills — future `self-os-memory-tree` skill.
- Hermes cron — future `self-os-memory-compile` scheduled job.
- Telegram — summary/control surface.

## Known decisions

- Start Markdown-first; no SQLite/vector DB in v0.
- Pilot in `ai-research-os` first.
- Keep OpenHuman as strategic reference only.
- Use source/topic/global as the conceptual model.
- Use source credibility and confidence labels.
- Use append-first updates for topic pages.
- Use promotion queue to turn knowledge into action.
- Run memory compile before daily Self-OS brief if automated.

## Open questions

- Should topic pages be generated entirely from raw files, or seeded manually then appended by compiler?
- Should every raw capture require `topics` frontmatter, or should compiler infer topics opportunistically?
- Should memory pages live under each wiki or under a single repo-level `/memory/` folder?
- Should there be one global memory across all Self-OS, or one per wiki plus a top-level operating global memory?
- What should be the review threshold for topic thesis changes?
- How should hotness scores be calibrated to avoid recency bias?
- Should the compiler use deterministic heuristics first and LLM synthesis only for final summaries?
- Should daily/weekly memory pages be direct-committed or opened as PRs?

## Suggested spec outline

A future `docs/spec.md` should define:

1. Exact folder layout.
2. Markdown schemas for source/topic/global/promotion pages.
3. Frontmatter requirements.
4. Topic slug rules.
5. Hotness scoring formula.
6. Source credibility model.
7. Compiler algorithm.
8. Git commit/PR policy.
9. Daily brief integration.
10. Failure modes and rollback.
11. Test/verification plan.

## Suggested implementation plan outline

A future `docs/implementation-plan.md` should use bite-sized tasks:

1. Create pilot folders.
2. Add seed topic page templates.
3. Add promotion queue template.
4. Add source page templates.
5. Write failing tests for metadata parsing.
6. Implement raw-file scanner.
7. Implement topic extraction.
8. Implement source memory writer.
9. Implement topic evidence appender.
10. Implement daily global writer.
11. Implement promotion queue update.
12. Add repo dirty-state guard.
13. Add CLI flags.
14. Add daily brief integration.
15. Add cron.
16. Run one-week pilot and review.

## Rollback / decommissioning

If the experiment creates noise:

- Remove the cron.
- Stop daily brief integration.
- Keep generated Markdown pages as historical artifacts or archive them.
- Delete generated pilot folder only if explicitly desired:

```bash
rm -rf /data/Self-OS/wikis/ai-research-os/memory
```

Do not delete raw captures.

## Future documents to create

- `docs/spec.md` — exact technical design for memory-tree v0.
- `docs/prd.md` — product/operating requirements.
- `docs/issues.md` — implementation issue breakdown.
- `docs/implementation-plan.md` — bite-sized execution plan.
- `docs/evaluation.md` — one-week pilot review rubric.
