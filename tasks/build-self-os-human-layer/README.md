# Build Self-OS Human Layer

**Status:** ready
**Priority:** high
**Created:** 2026-06-15

## What we are trying to do
Build the human layer of Self-OS — the active, judgment-driven side of the system that makes accumulated knowledge compound rather than just accumulate. This layer captures decisions, files back query outputs, synthesises cross-wiki signals, prunes stale content, and closes the weekly review loop.

## Why it matters
Without this layer, Self-OS is a passive archive. The human layer is what makes it a learning loop — human capital and token capital generating compound interest over time (Nadella framing). The system currently has excellent write/read paths but no feedback signal.

## Current state
Write path (Hermes → GitHub → wiki compile) and read path (gbrain + pgvector) are both live. No decision capture, no query filed-back, no cross-wiki synthesis, no staleness pruning, no structured weekly review loop.

## Desired outcome
A fully active human layer where Kish's judgment enters the system explicitly, query outputs compound back into the wiki, cross-domain signals surface weekly, stale content is flagged and pruned, and the weekly review loop is closed.

## Constraints
- Must route through Hermes for all writes
- Android (HTTP Shortcuts) and Windows (bookmarklet) are the capture surfaces
- gbrain signal-detector and briefing skills are installed but not configured
- Weekly Hermes cron skeleton already exists

## Acceptance criteria
- [ ] Decision capture pipeline live (voice/text → personal-os/raw/decisions/)
- [ ] Query filed-back mechanism implemented (one-tap save from gbrain response)
- [ ] Cross-wiki weekly synthesis skill running on Saturday cron
- [ ] signal-detector and briefing skills configured and wired to cron
- [ ] Weekly review briefing delivered to Telegram with response capture
- [ ] Confidence scoring rolled out to all four wikis and updated during lint pass

## Sub-tasks
- [ ] **1. Voice/text → decision capture** — New capture mode in HTTP Shortcuts routing to `decision` type in webhook; Hermes enriches and commits to `personal-os/raw/decisions/`. Distinct from external content clipping.
- [ ] **2. Query filed-back loop** — One-tap mechanism to save a gbrain query + response back as a raw file into the relevant wiki. Needs new endpoint or flag on existing Railway webhook.
- [ ] **3. Cross-wiki weekly synthesis skill** — Saturday Hermes skill reads recent activity across all four wikis and produces a cross-domain signal report to `personal-os/wiki/syntheses/weekly-YYYY-MM-DD.md`.
- [ ] **4. Configure signal-detector and briefing skills** — Wire both dormant gbrain skills to the lint cron. signal-detector flags stale/conflicting content; briefing surfaces it to Telegram.
- [ ] **5. Weekly review briefing → response loop** — Extend weekly Hermes cron to produce structured briefing (ingested, syntheses ran, signals flagged, open decisions) delivered to Telegram. Inline responses captured back as decisions.
- [ ] **6. Confidence scoring rollout** — Roll `confidence` and `source_count` frontmatter fields out to supply-chain-os, personal-os, coding-projects-os. Hermes updates scores during lint pass based on source count and recency.

## Known decisions
- All writes route through Hermes, not web Claude
- Capture surfaces: Android HTTP Shortcuts + Windows bookmarklet
- Weekly review cron skeleton already exists — extend don't replace

## Open questions
- What is the right gbrain skill config format for signal-detector?
- Does query filed-back need a new Railway webhook endpoint or can it reuse existing with a mode flag?
- Should cross-wiki synthesis be a new Hermes skill or an extension of the existing midnight cron?
