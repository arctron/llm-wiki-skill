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
.github/workflows/pages.yml
raw/sources/<slug>.md   immutable snapshots (not published)
docs/index.md           overview / evolving thesis (Pages home)
docs/catalog.md         list of every wiki page
docs/sources/index.md   section parent
docs/sources/<slug>.md  one page per ingested source
docs/concepts/...
docs/entities/...
docs/analyses/...
docs/meta/index.md
docs/meta/log.md
docs/meta/pins.md
```

`raw/` is not part of the site. Do not put wiki prose there.

## Tokens (init only)

Replace in the template: `__TOPIC__` `__SLUG__` `__GITHUB_OWNER__` `__GITHUB_REPO__` `__PAGES_URL__` `__YEAR__` `__COPYRIGHT_HOLDER__`.

## WIKI.md

YAML frontmatter plus a short markdown body (scope, what is in/out). Required frontmatter:

```yaml
topic: <title>
slug: <slug>
github: <owner>/<repo>
pages_url: https://<owner>.github.io/<repo>/
source_policy: excerpts-only
volatile_days: 90
```

Optional `source_quality` list, highest first, e.g. `peer-reviewed`, `primary data`, `books`, `specialist reporting`, `blogs/social`.

## Links

- Between wiki pages: `[Title](../concepts/foo.md)` (relative, include `.md`).
- Anchors allowed: `foo.md#heading`.
- External URLs allowed on source pages and in `raw/`.
- No `[[wikilinks]]`, no leading-`/` site paths, no `{:` / `{%` in page bodies.

`parent` in frontmatter must equal the parent page's `title` exactly (`Sources`, `Concepts`, `Entities`, `Analyses`, `Meta`).

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
| Source / concept / entity / analysis | `sources: [<slug>, ...]` (source slugs; empty only on stubs and section parents) |
| Any | `last_modified_date: YYYY-MM-DD` on each edit |
| Any | `status: active` \| `disputed` \| `stub` (default `active`) |
| Any | `aliases: []` other names checked before creating a page |

Do not set `pinned: true` on a page; pins live in `docs/meta/pins.md`.

`nav_order` for section parents: Home `1`, Catalog `2`, Sources `3`, Concepts `4`, Entities `5`, Analyses `6`, Meta `7`. Children: 10, 20, 30, …

## Provenance

- Page-level: `sources` in frontmatter.
- Section-level: every `##` section that states facts ends with `*Sources: [Title](../sources/<slug>.md)*` (one or more links). Synthesis that does not add facts still lists the pages it drew from.
- Load-bearing or disputed claims: short quoted excerpt plus the source link, in the body.
- Volatile facts (current SOTA, prices, versions, "as of now"): include `*As of YYYY-MM-DD.*` in that section.

Never invent a source slug. If the raw snapshot has no excerpt for a claim, do not present the claim as sourced.

## Raw snapshot `raw/sources/<slug>.md`

```yaml
---
url: <canonical URL or "local">
title: <original title>
retrieved: YYYY-MM-DD
slug: <slug>
content_type: html | pdf | text | other
---
```

Body: `# <title>`, then `## Excerpts` with blockquotes only, then optional `## Retrieval notes` (paywall, language, fetch errors).

Quoted text in one raw file must stay under 1500 words. Prefer the sentences that support claims you will file. No full-page paste, no PDF binaries.

## Page bodies

Use these `##` headings. Skip a heading only if it would be empty; keep the order.

**`docs/index.md`:** `# <topic>` then `## Scope`, `## Current thesis`, `## Open questions`, `## How this wiki is organized`.

**`docs/sources/<slug>.md`:** `# <title>` then `## Summary`, `## Key claims`, `## Caveats`, `## See also`. Frontmatter `url` and `retrieved` plus `sources: [<slug>]`.

**`docs/concepts/<slug>.md` and `docs/entities/<slug>.md`:** `# <title>` then `## Summary`, `## What we know`, `## Disputed`, `## Open questions`, `## See also`.

**`docs/analyses/<slug>.md`:** `# <question>` then `## Answer`, `## Sources used`, `## What would change this`.

**Disputed** (section or in-body): state both sides, each with a source link. Do not pick a winner unless the user does.

Section parents (`docs/<section>/index.md`) are one short paragraph plus children in the sidebar. Catalog is the full list.

## Catalog `docs/catalog.md`

Every file under `docs/**/*.md` except `catalog.md` itself must appear as a markdown link whose target resolves to that file. Group by section:

```markdown
## Sources
- [Smith 2024](sources/smith-2024.md) — one-line summary
```

One-line summaries are optional but preferred. Update on every ingest, file, rename, or new page.

## Log `docs/meta/log.md`

Append-only, newest first. Every operation is one heading:

`## [YYYY-MM-DD] <op> | <slug-or-short-title>`

`<op>` is `init` | `ingest` | `query` | `lint` | `pin` | `rename`. Body: a few lines of what changed.

## Pins `docs/meta/pins.md`

```markdown
## pin-001
- page: concepts/foo.md
- section: "## What we know"
- kind: correction
- claim: "<the sentence that must remain true>"
- created: YYYY-MM-DD
- status: active
```

`kind`: `correction` (claim must remain true), `addition` (fact must remain present), `freeze` (do not rewrite the section). `page` is relative to `docs/`. `status`: `active` | `retired`. Never delete a pin; set `retired` if the user withdraws it.

On ingest, if new evidence contradicts an `active` pin: do not change that claim; ask.

## Slugs

`[a-z0-9]+(-[a-z0-9]+)*`. Unique across `docs/sources/`, `docs/concepts/`, `docs/entities/`, `docs/analyses/`, and `raw/sources/`. Source slugs may match their source page; do not reuse a source slug for a concept.

## What not to create

No extra top-level sections without a `WIKI.md` change and user approval. No `wiki/` directory (the wiki is `docs/`). No second catalog file.
