# Schema

All paths are relative to the wiki root (the directory that contains `WIKI.md`).

## Layout

```
WIKI.md                 instance config
AGENTS.md               pointer to this skill
README.md               human landing for GitHub
LICENSE
Gemfile
_config.yml             Jekyll; `source: docs` so `raw/` is not in the site
.github/workflows/pages.yml   only when `site` is `github-pages`
raw/sources/<slug>.md   optional third-party excerpts (not published)
docs/index.md           overview
docs/catalog.md         list of every wiki page
docs/conclusions/<slug>.md
docs/runbooks/<slug>.md
docs/sources/<slug>.md  optional URL excerpts
docs/meta/log.md
docs/meta/pins.md
```

`raw/` is not part of the site. Do not put wiki prose or chat logs there.

Empty-wiki file contents for a new repo are in [init.md](init.md).

## WIKI.md

YAML frontmatter plus a short markdown body (scope, what is in/out). Required frontmatter:

```yaml
topic: <title>
slug: <slug>
github: <owner>/<repo>
site: github-pages | local
pages_url: https://<owner>.github.io/<repo>/
source_policy: excerpts-only
volatile_days: 90
```

`site`: `github-pages` (hosted Actions site) or `local` (`bundle exec jekyll serve`, or markdown only). `pages_url` is required when `site` is `github-pages`; otherwise omit it or leave it empty. GitHub Pages HTML is public to anyone with the URL; a private repo does not make Pages private. `.github/workflows/pages.yml` must exist if and only if `site` is `github-pages`.

## Links

- Between wiki pages: `[Title](../runbooks/foo.md)` (relative, include `.md`).
- Anchors allowed: `foo.md#heading`.
- External URLs allowed.
- No `[[wikilinks]]`, no leading-`/` site paths, no `{:` kramdown IAL.

`parent` in frontmatter must equal the parent page's `title` exactly (`Conclusions`, `Runbooks`, `Sources`, `Meta`).

Jekyll interprets `{{` and `{%` even inside fenced code. If a page needs those characters, wrap that fence (or the smallest block) in `{% raw %}` / `{% endraw %}`. That pair is the only Liquid allowed in page bodies.

## Wiki page frontmatter

Required on every `docs/**/*.md` file:

```yaml
title: <nav and heading title>
layout: default
nav_order: <integer>
```

Also set:

| Page | Extra keys |
| --- | --- |
| Section parent (`docs/<section>/index.md`) | `has_children: true` |
| Child page | `parent: <section title>` |
| Conclusion / runbook / source | `captured: YYYY-MM-DD` on create or update |
| Any | `last_modified_date: YYYY-MM-DD` on each edit |
| Any | `status: active` \| `disputed` \| `stub` (default `active`) |
| Any | `aliases: []` other names checked before creating a page |
| Conclusion or runbook | `sources: [<slug>, ...]` only when a `docs/sources/` page exists for a cited URL |

Do not set `pinned: true` on a page; pins live in `docs/meta/pins.md`.

`nav_order` for section parents: Home `1`, Catalog `2`, Conclusions `3`, Runbooks `4`, Sources `5`, Meta `6`. Children: 10, 20, 30, …

## Provenance

- Capture date: `captured` in frontmatter.
- Cited URLs: markdown links in the body. Write excerpts into `raw/` + `docs/sources/` only when the user asks to ingest.
- Volatile facts (versions, current SOTA, “works on my machine”): `*As of YYYY-MM-DD.*` in that section.
- Never invent a source slug. Never dump a session transcript into `raw/`.

## Raw excerpts `raw/sources/<slug>.md`

Only for ingested third-party URLs.

```yaml
---
url: <canonical URL or "local">
title: <original title>
retrieved: YYYY-MM-DD
slug: <slug>
content_type: html | pdf | text | other
---
```

Body: `# <title>`, then `## Excerpts` with blockquotes only, then optional `## Retrieval notes`.

Quoted text in one raw file must stay under 1500 words. No full-page paste, no PDF binaries, no chat logs.

## Page bodies

Use these `##` headings. Skip a heading only if it would be empty; keep the order.

**`docs/index.md`:** `# <topic>` then `## Scope`, `## Current conclusions`, `## Open questions`, `## How this wiki is organized`.

**`docs/conclusions/<slug>.md`:** `# <title>` then `## Conclusion`, `## Why`, `## Open questions`, `## See also`.

**`docs/runbooks/<slug>.md`:** `# <title>` then `## Goal`, `## Environment`, `## Procedure`, `## Verification`, `## Discarded`, `## See also`.

- **Environment:** OS, tool versions, `*As of YYYY-MM-DD.*`
- **Procedure:** working commands in fenced blocks, in order.
- **Verification:** how we knew it worked.
- **Discarded:** brief dead ends only.

**`docs/sources/<slug>.md`:** `# <title>` then `## Summary`, `## Key claims`, `## Caveats`, `## See also`. Frontmatter `url` and `retrieved`.

Section parents are one short paragraph plus children in the sidebar. Catalog is the full list.

## Catalog `docs/catalog.md`

Every file under `docs/**/*.md` except `catalog.md` itself must appear as a markdown link whose target resolves to that file. Group by section:

```markdown
## Runbooks
- [Install Postgres](runbooks/install-postgres.md) — one-line summary
```

Update on every capture, ingest, rename, or new page.

## Log `docs/meta/log.md`

Append-only, newest first. Every operation is one heading:

`## [YYYY-MM-DD] <op> | <slug-or-short-title>`

`<op>` is `init` | `capture` | `ingest` | `lint` | `pin` | `rename`. Body: a few lines of what changed.

## Pins `docs/meta/pins.md`

```markdown
## pin-001
- page: runbooks/install-postgres.md
- section: "## Procedure"
- kind: correction
- claim: "<the sentence or command that must remain true>"
- created: YYYY-MM-DD
- status: active
```

`kind`: `correction` (claim must remain true), `addition` (fact must remain present), `freeze` (do not rewrite the section). `page` is relative to `docs/`. `status`: `active` | `retired`. Never delete a pin; set `retired` if the user withdraws it.

On capture or ingest, if new work contradicts an `active` pin: do not change that claim; ask.

## Slugs

`[a-z0-9]+(-[a-z0-9]+)*`. Unique across `docs/conclusions/`, `docs/runbooks/`, `docs/sources/`, and `raw/sources/`.

## What not to create

No extra top-level sections without a `WIKI.md` change and user approval. No `wiki/` directory (the wiki is `docs/`). No second catalog file.
