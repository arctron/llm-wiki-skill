# Init files

Write these paths under `$WIKI_ROOT`. Replace `__TOPIC__` `__SLUG__` `__GITHUB_OWNER__` `__GITHUB_REPO__` `__PAGES_URL__` `__YEAR__` `__DATE__` `__COPYRIGHT_HOLDER__` in every file.

Wiki page bodies and later edits follow [schema.md](schema.md), not this file.

## `WIKI.md`

```markdown
---
topic: __TOPIC__
slug: __SLUG__
github: __GITHUB_OWNER__/__GITHUB_REPO__
pages_url: __PAGES_URL__
source_policy: excerpts-only
volatile_days: 90
---

# __TOPIC__

Scope of this wiki goes here. One paragraph: what is in, what is out.
```

## `AGENTS.md`

```markdown
This repository is an LLM wiki instance.

Before ingesting, querying, linting, or editing `docs/` or `raw/`, load the `llm-wiki` skill (`llm-wiki/SKILL.md`).

If the skill is not installed, clone https://github.com/arctron/llm-wiki-skill and copy the `llm-wiki/` directory into your agent's skills folder. Install paths are in that repository's README.

Instance config: `WIKI.md`.
```

## `README.md`

```markdown
# __TOPIC__

LLM-maintained wiki. Read it on GitHub Pages: <__PAGES_URL__>

Sources are curated one at a time. Wiki pages live in `docs/`. Immutable source snapshots (excerpts only) live in `raw/`.

Maintained with the [llm-wiki](https://github.com/arctron/llm-wiki-skill) skill. If you use an agent, see `AGENTS.md`.
```

## `LICENSE`

```text
BSD Zero Clause License

Copyright (c) __YEAR__ __COPYRIGHT_HOLDER__

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
```

## `.gitignore`

```gitignore
_site/
.sass-cache/
.jekyll-cache/
.jekyll-metadata
.bundle/
vendor/
.DS_Store
```

## `Gemfile`

```ruby
source "https://rubygems.org"

gem "jekyll", "~> 4.4.1"
gem "just-the-docs", "0.12.0"
gem "jekyll-relative-links"
```

## `_config.yml`

```yaml
title: __TOPIC__
description: __TOPIC__ — an LLM-maintained wiki
theme: just-the-docs
source: docs

url: https://__GITHUB_OWNER__.github.io
baseurl: /__GITHUB_REPO__

permalink: pretty
heading_anchors: true
search_enabled: true
color_scheme: light

aux_links:
  GitHub:
    - https://github.com/__GITHUB_OWNER__/__GITHUB_REPO__

gh_edit_link: true
gh_edit_link_text: Source on GitHub
gh_edit_repository: https://github.com/__GITHUB_OWNER__/__GITHUB_REPO__
gh_edit_branch: main
gh_edit_source: docs
gh_edit_view_mode: tree

markdown: kramdown
kramdown:
  input: GFM
  hard_wrap: false

plugins:
  - jekyll-relative-links

relative_links:
  enabled: true
  collections: true

defaults:
  - scope:
      path: ""
    values:
      layout: default
```

## `.github/workflows/pages.yml`

```yaml
name: Deploy Jekyll site to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v7
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: "3.3"
          bundler-cache: true
          cache-version: 0
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v6
      - name: Build with Jekyll
        run: bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
        env:
          JEKYLL_ENV: production
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v5

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
```

## `docs/index.md`

```markdown
---
title: Home
layout: default
nav_order: 1
last_modified_date: __DATE__
status: stub
---

# __TOPIC__

## Scope

See [WIKI.md](https://github.com/__GITHUB_OWNER__/__GITHUB_REPO__/blob/main/WIKI.md) for the instance scope. This page is the evolving public thesis.

## Current thesis

Not yet. Ingest sources first.

## Open questions

None yet.

## How this wiki is organized

- [Catalog](catalog.md) — every page
- [Sources](sources/index.md) — one page per ingested source
- [Concepts](concepts/index.md)
- [Entities](entities/index.md)
- [Analyses](analyses/index.md) — filed answers
- [Log](meta/log.md)
```

## `docs/catalog.md`

```markdown
---
title: Catalog
layout: default
nav_order: 2
last_modified_date: __DATE__
---

# Catalog

## Overview

- [Home](index.md) — evolving thesis

## Sources

- [Sources](sources/index.md) — ingested source summaries

## Concepts

- [Concepts](concepts/index.md) — ideas compiled across sources

## Entities

- [Entities](entities/index.md) — people, orgs, products, places

## Analyses

- [Analyses](analyses/index.md) — filed query answers

## Meta

- [Meta](meta/index.md) — log and pins
- [Log](meta/log.md) — operations
- [Pins](meta/pins.md) — human corrections that must survive ingest
```

## `docs/sources/index.md`

```markdown
---
title: Sources
layout: default
nav_order: 3
has_children: true
last_modified_date: __DATE__
---

# Sources

One summary page per ingested source. Full third-party text is not stored; excerpts live in `raw/sources/` in the git repo, not on this site.
```

## `docs/concepts/index.md`

```markdown
---
title: Concepts
layout: default
nav_order: 4
has_children: true
last_modified_date: __DATE__
---

# Concepts

Ideas compiled across sources. Child pages appear in the sidebar as they are created.
```

## `docs/entities/index.md`

```markdown
---
title: Entities
layout: default
nav_order: 5
has_children: true
last_modified_date: __DATE__
---

# Entities

People, organizations, products, and places. Child pages appear in the sidebar as they are created.
```

## `docs/analyses/index.md`

```markdown
---
title: Analyses
layout: default
nav_order: 6
has_children: true
last_modified_date: __DATE__
---

# Analyses

Filed answers to questions asked against this wiki. Child pages appear in the sidebar as they are created.
```

## `docs/meta/index.md`

```markdown
---
title: Meta
layout: default
nav_order: 7
has_children: true
last_modified_date: __DATE__
---

# Meta

Operation log and pins. Pins are human (or previously approved) corrections that later ingests must not clobber.
```

## `docs/meta/log.md`

```markdown
---
title: Log
parent: Meta
layout: default
nav_order: 1
last_modified_date: __DATE__
---

# Log

Append-only. Newest first.

## [__DATE__] init | wiki scaffold

Created empty wiki.
```

## `docs/meta/pins.md`

```markdown
---
title: Pins
parent: Meta
layout: default
nav_order: 2
last_modified_date: __DATE__
---

# Pins

None yet.
```

## `raw/sources/.gitkeep`

Empty file. Write a single newline.
