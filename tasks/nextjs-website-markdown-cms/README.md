# Next.js Website — Markdown / JSON CMS Migration

Status: backlog
Created: 2026-06-02
Owner: Kish / Hermes
Priority: medium
Stack: Next.js 14 App Router + React

## Summary

Move all website content (posts, pages, nav, footer, home, feature cards,
pricing, FAQ) from the current CMS into the website repo as files —
Markdown + frontmatter for long-form content, JSON (or typed `.ts`) for
structured settings. The site renders directly from those files via a
single typed loader. Publishing becomes a Git pull request, not a CMS
admin UI.

Goal: make the website repo-agent-legible, like `/data/Self-OS/wikis/`,
so editors, reviewers, and coding agents all read the same source of
truth.

## Current artifact state

- Idea capture: `docs/idea.md`
- Spec: not started
- PRD: not started
- Issues: not started
- Implementation plan: not started
- Code changes: not started (user explicitly asked not to build yet)

## What this task delivers

1. A `content/` contract — `posts/*.md`, `pages/*.md`, `settings/*.json`.
2. A `lib/content.ts` loader with Zod-validated frontmatter and typed
   settings getters.
3. App Router pages that render directly from the loader (no CMS calls).
4. A one-shot migration script (or runbook) for the current CMS export.
5. A documented PR-based publishing workflow.

## Key design decisions (full detail in `docs/idea.md`)

- Plain `.md` first, MDX later (only if components-in-content is needed).
- Server components read files via `node:fs/promises`; no `getStaticProps`,
  no client fetches for content.
- Zod-validated frontmatter; bad frontmatter fails the build.
- `draft: true` gate filters drafts from production.
- File contract is canonical; any UI editor (Tina / Decap / Sveltia)
  layers on top, never replaces the file shape.
- No image CDN by default; `public/` + `next/image` until traffic justifies
  a CDN.

## Folder shape (target)

```
.
├── app/
│   ├── layout.tsx           # reads nav.json + footer.json
│   ├── page.tsx             # reads home.json
│   ├── blog/
│   │   ├── page.tsx
│   │   └── [slug]/page.tsx
│   └── [other pages]/page.tsx
├── content/                 # the new "CMS"
│   ├── posts/               # .md / .mdx with frontmatter
│   ├── pages/               # .md for static pages
│   └── settings/            # .json for nav, footer, home, pricing
├── lib/
│   └── content.ts           # single loader (read + parse + validate)
├── public/                  # images
└── package.json
```

## Dependencies to add

```bash
npm i gray-matter react-markdown zod
# optional
npm i -D @tailwindcss/typography
```

(MDX adds `next-mdx-remote/rsc` later if needed.)

## Migration path (one-time)

1. Export from the current CMS (WXR / JSON / CSV depending on stack).
2. Convert to Markdown + frontmatter (e.g. `npx wordpress-export-to-markdown`).
3. Drop files into `content/posts/` and `content/pages/`.
4. Move global settings into `content/settings/*.json`.
5. Replace CMS-bound components in `app/` with loader-backed server
   components.
6. Delete CMS SDK, env keys, and remaining API code paths.
7. Deploy — Vercel builds from the repo on push.

## Acceptance criteria

A future implementation is "done" when ALL of the following hold:

- [ ] `content/posts/` has at least 3 example posts with valid frontmatter,
      renderable at `/blog/<slug>`.
- [ ] `content/pages/` has at least 2 static pages.
- [ ] `content/settings/nav.json`, `home.json`, `footer.json` exist and
      are imported by the corresponding `app/` components.
- [ ] `lib/content.ts` exposes `getAllPosts`, `getPost`, and a typed
      `getSettings<T>(name)` with Zod validation.
- [ ] `app/blog/page.tsx` and `app/blog/[slug]/page.tsx` render from the
      loader; `generateStaticParams` builds every post slug.
- [ ] `app/layout.tsx` and `app/page.tsx` read settings from
      `content/settings/*.json` with no CMS imports.
- [ ] Build fails loudly when a post has invalid frontmatter.
- [ ] `draft: true` posts do not appear in production builds but do in dev.
- [ ] No remaining CMS SDK, API key, or API call in the codebase.
- [ ] Site repo README documents the `content/` contract and the PR-based
      publishing flow.
- [ ] Preview deploys on Vercel work for content-only PRs.

## Open questions to resolve before implementation

- Which CMS is being replaced? (WordPress / Ghost / Webflow / Sanity /
  Strapi / Contentful / custom?)
- Is scheduled publishing required? (If yes, decide on flip-cron vs.
  merge-on-time.)
- Are non-technical editors involved? (If yes, pick Tina / Decap /
  Sveltia and whether it ships day-one or later.)
- Are images currently in a CDN that needs to be preserved?
- Is MDX needed from day one, or can the first cut be plain `.md`?
- Is the current site on ISR / on-demand revalidation, and is build-time
  render acceptable?

## Next conversion step

- [ ] Resolve the open questions above.
- [ ] Dry-run the CMS export on a copy of the data; spot-check the
      Markdown conversion output.
- [ ] Convert `docs/idea.md` + this README into a concrete spec.
- [ ] Land the loader + folder shape on a feature branch; cut over
      routes one at a time (settings first, then blog, then structured
      collections).
- [ ] Add a `content/README.md` documenting the frontmatter contract
      and the PR flow.
- [ ] (Optional) Layer an editor on top once the file contract is
      stable.

## Kanban

- Status: `ready` (created from this task; pick up in a future session).

## Related references

- Daniel Lee / Cursor on moving content from CMS to raw code + Markdown.
- Self-OS Git-backed wiki pattern (`/data/Self-OS/wikis/...`) — same
  mental model applied to a website.
- User's standing preference for repo-centric, inspectable, agent-legible
  systems (see Hermes peer card and User Representation).
