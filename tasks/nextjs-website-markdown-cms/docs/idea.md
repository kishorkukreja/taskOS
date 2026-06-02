# Next.js Website — Markdown / JSON CMS Migration — Idea Capture

Created: 2026-06-02
Status: captured
Repository: /data/taskOS
Task folder: /data/taskOS/tasks/nextjs-website-markdown-cms

## Request source

- Source: Hermes conversation in Telegram (Moh Maya DM)
- Captured by: Hermes (as MiniMax-M3 via OpenRouter)
- Date: 2026-06-02

## User-provided source notes

The user has been trying to move their personal/website content from a CMS-style
setup into the repo as files (Markdown + frontmatter + JSON) so that:

- Editors and agents can read, search, and edit the same source of truth.
- The publishing workflow is a Git pull request, not a CMS admin UI.
- Nav, footer, hero, and other global content live as JSON in the repo, not
  as database rows.

The current site is built with **Next.js (App Router) + React**. They are not
asking for any code to be written right now — they want the idea captured to
taskOS and a Kanban card created with status `ready` so they can pick it up
in a future session.

Verbatim request:

> Okay so add this to taskos and then to kanban with status ready so I can pick
> up next time. You don't need to build anything just add it to task os and to
> kanban please. My current website is in nextjs and react

## Strategic position

This is the standard "content-in-the-repo" pattern that makes the site
agent-legible: the same Markdown files can be read by humans in VSCode/Obsidian
and by coding agents in the repo. The site stops being a CMS-driven artifact
and becomes a build target for a flat-file corpus.

Acceptance is structural, not visual: any migration is "done" when there is
no remaining CMS call in the rendered site and the only source of truth for
content is files committed to the repo.

## Current state (at capture)

- Stack: Next.js 14 App Router + React.
- Content layer: currently CMS-driven (specific CMS not stated).
- Workflow: editorial changes go through a CMS admin, not through PRs.
- Pain points implied by the user: trying to do this for a while, wants a
  concrete example, wants a runnable file/folder shape to follow.

## Desired outcome

- All long-form content (posts, pages) lives as `.md` / `.mdx` files under
  `content/posts/` and `content/pages/` with frontmatter.
- All structured-but-not-prose content (nav, home, footer, feature cards,
  pricing, FAQ) lives as `.json` or `.ts` files under `content/settings/`.
- A single typed loader (`lib/content.ts`) reads, validates, and exposes the
  content using Zod.
- Page templates in `app/` render directly from the loader — no CMS API
  calls, no DB, no client-side fetching for content.
- Publishing is a Git pull request, preview-deploys on the PR, and merge
  triggers a static rebuild.
- An optional editor (Tina / Decap / Sveltia) can be layered on top later
  for non-technical contributors without changing the underlying file
  contract.

## Key design decisions

1. **Markdown + JSON, not Markdown + MDX-only.** Lead with plain `.md` and
   `react-markdown` for simplicity; promote to MDX only if/when components
   inside content become necessary.
2. **Server components, not `getStaticProps`.** App Router server components
   read files directly via `node:fs/promises` and return JSX. No build-time
   data plumbing, no client fetches.
3. **Zod-validated frontmatter.** Every post is parsed and validated against
   a `PostSchema`. Bad frontmatter fails the build, not production.
4. **`draft: true` gate.** Drafts are kept in the repo, filtered out in
   production, and visible only when `NODE_ENV=development`. A small cron
   can flip a draft to published at a scheduled timestamp if scheduled
   publishing is needed later.
5. **Editor optionality.** The file contract is the source of truth; any UI
   editor sits on top of it. We do not let the editor dictate the schema.
6. **No image CDN by default.** Images go in `public/` or use `next/image`
   with remote patterns. Add a CDN only when traffic or transformation cost
   justifies it.

## Folder shape (target)

```
.
├── app/
│   ├── layout.tsx           # reads nav.json + footer.json
│   ├── page.tsx             # reads home.json
│   ├── blog/
│   │   ├── page.tsx         # lists all posts (getAllPosts)
│   │   └── [slug]/page.tsx  # renders one post (getPost + react-markdown)
│   └── [other static pages]/page.tsx
├── content/                 # the new "CMS"
│   ├── posts/               # .md / .mdx, frontmatter required
│   ├── pages/               # .md for static pages (about, faq, etc.)
│   └── settings/            # .json for nav, footer, home, pricing
│       ├── nav.json
│       ├── home.json
│       └── footer.json
├── lib/
│   └── content.ts           # the single loader (read + parse + validate)
├── public/                  # images, favicon, etc.
└── package.json
```

## Frontmatter contract

```yaml
---
title: "Why we removed our CMS"
slug: "why-we-removed-our-cms"
date: "2026-06-02T10:00:00Z"
description: "What changed when content moved into the repo"
tags: ["meta", "engineering"]
draft: false
---
```

Validated by Zod:

```ts
const PostSchema = z.object({
  title: z.string(),
  date: z.string().datetime(),
  description: z.string(),
  tags: z.array(z.string()).default([]),
  draft: z.boolean().default(false),
});
```

## Settings contract (JSON examples)

```json
// content/settings/nav.json
[
  { "label": "Home",  "href": "/" },
  { "label": "Blog",  "href": "/blog" },
  { "label": "About", "href": "/about" }
]
```

```json
// content/settings/home.json
{
  "heroTitle": "Build faster with less complexity",
  "heroSubtitle": "Your marketing site and product ship from the same repo.",
  "primaryCta":   { "label": "Read the blog",  "href": "/blog" },
  "secondaryCta": { "label": "Star on GitHub", "href": "https://github.com/you/repo" }
}
```

## Loader shape (target)

```ts
// lib/content.ts
import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';
import matter from 'gray-matter';
import { z } from 'zod';

const PostSchema = z.object({
  title: z.string(),
  date: z.string().datetime(),
  description: z.string(),
  tags: z.array(z.string()).default([]),
  draft: z.boolean().default(false),
});

export type Post = z.infer<typeof PostSchema> & {
  slug: string;
  body: string;
  readingTime: number;
};

const WPM = 200;

export async function getAllPosts(): Promise<Post[]> {
  const dir = join(process.cwd(), 'content', 'posts');
  const files = (await readdir(dir)).filter(f => /\.mdx?$/.test(f));

  const posts = await Promise.all(files.map(async (file) => {
    const raw = await readFile(join(dir, file), 'utf8');
    const { data, content } = matter(raw);
    const meta = PostSchema.parse(data);
    const slug = file.replace(/\.mdx?$/, '');
    const words = content.trim().split(/\s+/).length;
    return { ...meta, slug, body: content,
             readingTime: Math.max(1, Math.round(words / WPM)) };
  }));

  return posts
    .filter(p => !p.draft || process.env.NODE_ENV === 'development')
    .sort((a, b) => b.date.localeCompare(a.date));
}

export async function getPost(slug: string): Promise<Post | null> {
  const posts = await getAllPosts();
  return posts.find(p => p.slug === slug) ?? null;
}
```

## Migration path (one-time, scripted)

1. Export from the existing CMS:
   - WordPress: Tools → Export → WXR (`.xml`)
   - Ghost: Settings → Labs → Export (`.json`)
   - Webflow: CMS → Export → CSV
   - Contentful / Strapi / Sanity: REST/GraphQL dump to JSON
2. Convert to Markdown + frontmatter:
   - WordPress: `npx wordpress-export-to-markdown`
   - Ghost: `ghost-to-md` (community)
   - Sanity: split by `_type`, run each through a remark pipeline
3. Drop the resulting files into `content/posts/` and `content/pages/`.
4. Move nav, footer, hero, feature cards, pricing, FAQ into
   `content/settings/*.json` (or `.ts` for typed literals).
5. Replace each CMS-bound component in `app/` with a loader-backed
   server component.
6. Delete CMS SDK, env keys, and any remaining API code paths.
7. Deploy — Vercel builds from the repo on push.

## Publishing workflow (target)

```
1.  Open content/posts/<slug>.md in VSCode/Obsidian
2.  Write + set draft: true while iterating
3.  git checkout -b post/<slug>
4.  git commit -am "draft: <slug>"
5.  Open PR → preview deploy on Vercel
6.  Review → flip draft: false → merge
7.  Production rebuild runs from the merged commit
```

## Tradeoffs to capture

- **No WYSIWYG.** Edit Markdown in VSCode/Obsidian. Agents and humans see
  the same source.
- **No scheduled publishing out of the box.** Use `draft: true` + a small
  flip-cron, or merge when ready.
- **Images.** `public/` + `/<file>` or `next/image` with remote patterns.
  No image CDN by default; add one when justified.
- **MDX later.** Swap `react-markdown` for `next-mdx-remote/rsc` and rename
  files to `.mdx`. Loader stays the same.
- **Non-technical editors.** Layer Tina CMS, Decap, or Sveltia on top of
  the same Markdown files. The editor does not own the schema.

## Acceptance criteria

A future implementation is "done" when ALL of the following hold:

- [ ] `content/posts/` contains at least 3 example `.md` posts with valid
      frontmatter, renderable at `/blog/<slug>`.
- [ ] `content/pages/` contains at least 2 static pages (e.g. `about.md`,
      `faq.md`) renderable at their routes.
- [ ] `content/settings/nav.json`, `home.json`, `footer.json` exist and
      are imported by the corresponding `app/` components.
- [ ] `lib/content.ts` exposes `getAllPosts`, `getPost`, and
      `getSettings<T>(name)` with Zod-validated shapes.
- [ ] `app/blog/page.tsx` and `app/blog/[slug]/page.tsx` render from the
      loader; `generateStaticParams` builds every post slug.
- [ ] `app/layout.tsx` and `app/page.tsx` read settings from
      `content/settings/*.json` with no CMS imports.
- [ ] Build fails loudly when a post has invalid frontmatter.
- [ ] `draft: true` posts do not appear in production builds but do in dev.
- [ ] No remaining CMS SDK, API key, or API call in the codebase.
- [ ] README of the site repo documents the `content/` contract and the
      PR-based publishing flow.
- [ ] Preview deploys on Vercel work for content-only PRs.

## Likely files / services to touch

- `app/` — every page and layout that currently reads from a CMS.
- `lib/content.ts` — new loader (single source of truth for content).
- `content/` — new directory holding posts, pages, and settings.
- `package.json` — add `gray-matter`, `zod`, `react-markdown` (and later
  `next-mdx-remote/rsc` if MDX is adopted).
- `next.config.mjs` — no change required for the file-based path; only
  needs `images.remotePatterns` if external images are kept.
- `.env.example` — remove CMS keys; add no new keys.

## Open questions to resolve before implementation

- Which CMS is being replaced? (WordPress / Ghost / Webflow / Sanity /
  Strapi / Contentful / custom?) — affects the migration script choice.
- Is there a scheduled-publishing requirement? (If yes, decide on
  flip-cron vs. merge-on-time.)
- Are there non-technical editors who need a UI? (If yes, decide on
  Tina / Decap / Sveltia and whether the editor is bundled or opt-in.)
- Are images / video currently in a CDN that needs to be preserved?
- Is MDX needed from day one, or can the first cut be plain `.md`?
- Does the site currently use ISR / on-demand revalidation, and is the
  build-time-only render acceptable?

## Future conversion steps

- [ ] Convert this `docs/idea.md` + `README.md` into a concrete spec once
      the open questions are answered.
- [ ] Pick the CMS export tool and dry-run it on a copy of the data.
- [ ] Land the loader + folder shape on a feature branch first; cut over
      routes one at a time so previews stay green.
- [ ] Cut over nav/footer/home first (lowest risk), then blog, then any
      structured CMS collections.
- [ ] Add a `content/README.md` documenting the frontmatter contract and
      the PR flow.
- [ ] (Optional) Layer an editor on top once the file contract is stable.

## Related references

- Daniel Lee / Cursor blog post on moving content from CMS to raw code +
  Markdown (cited in the prior Hermes conversation).
- Self-OS pattern of Git-backed Markdown as a knowledge base
  (`/data/Self-OS/wikis/...`) — same mental model applied to a website.
- The user's broader preference for repo-centric, inspectable systems and
  agent-legible content (see Hermes peer card and User Representation).
