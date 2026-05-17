# Multimodal Memory Layer as an LLM Wiki — taskOS Addendum

Created: 2026-05-17
Status: source addendum
Parent task: `/data/taskOS/tasks/self-os-memory-tree-v0/`
Wiki source: `/data/Self-OS/wikis/ai-research-os/raw/resources/multimodal-memory-layer-llm-wiki-2026-05-17.md`

## Why this belongs in the existing memory-tree task

This source should extend the existing **Self-OS Memory Tree v0** work rather than become a parallel task.

The existing task already defines a source/topic/global memory layer for Self-OS. This addendum adds the missing multimodal/evidence-grounding dimension:

- raw multimodal artifacts must be preserved,
- semantic memory pages must stay linked to source evidence,
- retrieval should route by intent and modality,
- provenance, confidence, privacy, and retention metadata must be designed early.

The strategic heuristic is:

> Store the thing, store the meaning, and store the links.

## Source summary

The source frames a multimodal memory layer as a **compiled knowledge system**, not just a vector retrieval system. It extends the LLM Wiki pattern into multimodal memory: the semantic wiki is the navigable spine, while raw artifacts remain the evidence graph beneath it.

The recommended architecture has three layers:

1. **Raw evidence layer** — original files and source data: images, videos, audio, documents, screenshots, transcripts, browser traces.
2. **Semantic memory layer** — durable summaries, entities, facts, preferences, event records, and relations.
3. **Retrieval/orchestration layer** — intent classification, retriever selection, ranking, evidence grounding, and answer construction.

## Design requirements to add to Self-OS Memory Tree v0

### 1. Evidence pointers in memory pages

Source/topic/global memory pages should include links back to raw evidence, not only links to interpreted summaries.

A minimal v0 can use Markdown fields such as:

```yaml
source_pointers:
  - artifact_id: "optional-stable-id"
    artifact_path: "relative/path/to/raw-or-artifact"
    modality: text | image | audio | video | document | browser_trace | screenshot
    pointer_type: file | transcript_span | timestamp | frame_range | bounding_box | ocr_span | document_section
    pointer_value: "human-readable pointer"
    confidence: high | medium | low
    privacy_label: public | internal | sensitive | private
```

### 2. Evidence memory as a first-class type

The current task distinguishes source/topic/global layers. This source adds an orthogonal memory type: **evidence memory**.

Evidence memory is not another summary layer. It is the system’s ability to return from an interpreted claim to the raw sensory/file artifact behind it.

Examples:

- transcript timestamp behind a meeting claim,
- screenshot path behind a UI observation,
- browser trace path behind a debugging conclusion,
- PDF page/section behind a research claim,
- image region/bounding box behind a visual claim.

### 3. Governance fields from the start

Multimodal memory is more privacy-sensitive than text-only capture. The v0 schema should include governance fields before large-scale accumulation:

- `privacy_label`,
- `retention_policy`,
- `confidence`,
- `provenance`,
- `created_at`,
- `actor`,
- `session_id`,
- `delete_or_redact_workflow`.

### 4. Retrieval should route by intent

The implementation should avoid a single blind vector-search path. Retrieval should classify intent first:

- fact lookup,
- preference recall,
- temporal/event reasoning,
- cross-session synthesis,
- visual grounding,
- source audit/provenance lookup.

Each mode should activate different ranking signals:

- semantic similarity,
- graph/entity proximity,
- recency,
- modality match,
- confidence,
- provenance strength.

## V0 implementation implications

Do **not** jump straight to a database, graph store, or vector system. Preserve the existing Self-OS principle: Markdown-first, Git-backed, reviewable.

Recommended v0 additions:

1. Add a Markdown evidence-ledger convention:

```text
/data/Self-OS/wikis/ai-research-os/memory/evidence-ledger.md
/data/Self-OS/wikis/coding-projects-os/memory/evidence-ledger.md
```

2. Add `source_pointers` to topic/source/global memory frontmatter or body sections.

3. Extend the future `compile_memory_tree.py` design so it can:

- detect source files with attached artifacts,
- preserve artifact paths,
- include evidence links in generated memory pages,
- mark low-confidence or missing evidence,
- propose promotion candidates when a source implies a task, skill, content piece, or research request.

4. Define an artifact path convention before implementation, for example:

```text
/data/Self-OS/artifacts/<domain>/<source-slug>/<artifact-file>
/data/Self-OS/wikis/<wiki>/raw/<type>/<source-file>.md
```

or, if artifacts should remain closer to raw captures:

```text
/data/Self-OS/wikis/<wiki>/raw/artifacts/<source-slug>/<artifact-file>
```

Decision needed: pick one convention before coding.

## Acceptance criteria to add to the memory-tree task

A future implementation should be considered incomplete unless it can demonstrate:

- [ ] A source memory page can link to at least one raw artifact.
- [ ] A topic memory page can cite source evidence, not just a summary.
- [ ] At least one multimodal source type is represented, e.g. screenshot, video transcript, audio transcript, browser trace, or PDF.
- [ ] Evidence pointers include modality, pointer type, confidence, and privacy label.
- [ ] The daily/global memory output can surface sources with weak/missing evidence.
- [ ] The system can distinguish semantic recall from evidence-grounded recall.
- [ ] Deletion/redaction implications are documented for sensitive artifacts.

## Open design questions

1. Should artifacts live under `/data/Self-OS/artifacts/` globally, or inside each wiki under `raw/artifacts/`?
2. Should `source_pointers` be YAML frontmatter, body sections, or separate sidecar files?
3. How should browser traces, screenshots, audio clips, and PDFs be assigned stable artifact IDs?
4. Which modalities matter first for Self-OS v0: screenshots/browser traces, PDFs, YouTube/audio transcripts, or user-uploaded images?
5. Should evidence-ledger files be generated by script, hand-maintained, or both?
6. What privacy labels are enough for v0: `public`, `internal`, `sensitive`, `private`?

## Next conversion step

When converting `self-os-memory-tree-v0` into a spec, fold this addendum into the architecture section as:

- **Evidence Memory / Multimodal Grounding**,
- **Evidence Pointer Schema**,
- **Artifact Storage Convention**,
- **Governance and Redaction**,
- **Intent-Routed Retrieval**.
