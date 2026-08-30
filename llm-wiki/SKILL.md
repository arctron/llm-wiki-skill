---
name: llm-wiki
description: >
  Build and maintain a persistent markdown wiki for a dedicated topic,
  published as GitHub Pages. Use when the user wants to start a topic wiki,
  research or propose sources, ingest a source, query the wiki, lint it,
  pin a correction, rename a page, or publish wiki updates. Triggers:
  /llm-wiki, llm wiki, topic wiki, ingest source, wiki lint, knowledge base.
license: 0BSD
compatibility: Requires git and python3. gh is required to create GitHub repos, enable Pages, and push.
metadata:
  author: arctron
  version: "1.0"
---

# llm-wiki

Compile a topic into a compounding markdown wiki. The user curates sources and approves diffs. This agent does the filing.

Skill root: the directory that contains this `SKILL.md`.

Read [references/schema.md](references/schema.md) before creating or editing wiki pages, `raw/`, `WIKI.md`, `AGENTS.md`, or `docs/catalog.md`.

## Detect the instance

A wiki root is the directory that contains `WIKI.md`.

- If `WIKI.md` is missing and the user is not starting a wiki: stop and say so.
- If several `WIKI.md` files could apply: ask which root to use.
- After every `git` operation, treat that directory as the cwd for paths in this skill.

## Hard rules

1. One source per ingest apply cycle.
2. Search and propose sources when asked to research. Ingest only URLs or files the user picked.
3. Query answers come from the wiki. Do not web-search to fill an answer unless the user asked to find sources.
4. `raw/` is append-only. Never edit or delete an existing raw file. Snapshot contents follow the schema (excerpts only; no full pages, PDFs, or binaries in git).
5. Links and page YAML follow the schema. Never `[[wikilinks]]`.
6. Before creating a page, search `docs/catalog.md` titles, slugs, and `aliases`. Update an existing page rather than mint a near-duplicate.
7. Never silently overwrite an existing claim. Existing pages change only through an approved diff.
8. Never contradict or drop an active pin. If new evidence conflicts with a pin, stop and ask.
9. Do not add `CLAUDE.md`, `.cursorrules`, or other harness-specific instruction files. `AGENTS.md` is the only always-on pointer.

## Apply gate

Every change to `docs/` or `raw/` except the init scaffold:

1. `git pull --ff-only` (stop if this fails).
2. Write the working tree. Record the file list you created or modified.
3. Show `git status`, `git diff --stat`, and the full diff (for new files, show contents if that is easier to review).
4. Wait for explicit approval of that artifact.
5. If rejected: restore only the files from your list (`git restore` tracked files; delete untracked files you created). Stop.
6. If the user wants edits: change the working tree and re-show the diff. Do not commit until approval.
7. On approval, run **Apply**.

Init scaffold does not use this gate. Filing a query uses this gate.

## Apply

From the wiki root:

1. Run `python3 "$SKILL_ROOT/scripts/lint.py"`.
2. Fix every failure. Re-run until exit 0. If you cannot fix without a content decision, stop and ask.
3. `git add` the approved files plus any lint fixes in those files and in `docs/catalog.md` / `docs/meta/log.md`.
4. Commit with a message like `ingest: smith-2024 sulfide electrolytes` or `query: file comparison of X vs Y` or `pin: threshold per shipment`.
5. `git pull --ff-only` then `git push`.
6. Report the commit, Pages URL from `WIKI.md`, and which pages changed.

## init

Scaffold a **new** GitHub repo. Do not ingest in this operation.

1. Collect: topic title; slug (lowercase hyphenated); GitHub owner (`gh api user --jq .login` if unset); local path (default `./wiki-<slug>` next to the current workspace if the user did not specify); copyright holder (`git config user.name`).
2. If the path exists and is not empty: stop.
3. Copy `assets/wiki-template/` into the path (`cp -R "$SKILL_ROOT/assets/wiki-template/." "$WIKI_ROOT/"`). Run the rest of init inside `$WIKI_ROOT`.
4. Replace every schema token in the copied files. Repo name defaults to `wiki-<slug>`. Pages URL is `https://<owner>.github.io/<repo>/`.
5. Fill `WIKI.md` scope in one short paragraph. If you must guess the scope, ask instead.
6. `git init -b main`, `git add -A`, commit: `init: wiki scaffold for <topic>`.
7. `gh repo create <owner>/<repo> --public --source=. --remote=origin --push`. Enable Pages from Actions: `gh api --method POST "repos/<owner>/<repo>/pages" -f build_type=workflow`. If Pages already exists, continue.
8. Web-search the topic. Run **propose-sources** and **stop**. Do not ingest.

If `gh` is missing or unauthenticated: leave the local repo committed and print the exact commands for the user.

## propose-sources

Build a pick-list. Do not write wiki pages.

1. Read `WIKI.md`, `docs/catalog.md`, `docs/index.md`, and existing `raw/sources/*.md` URLs so you do not propose duplicates.
2. Search. Prefer dated, attributable sources. Prefer primary over secondary over tertiary. Wikipedia is tertiary and may appear as a map of the topic, not as the only support for a claim.
3. If the wiki already has a thesis, include at least one source that could challenge it.
4. Present a numbered table and wait for picks:

   `# | slug | title | url | date | type | why | challenges_thesis`

   `type` is `primary` | `secondary` | `tertiary` | `news` | `other`.
5. After the user picks, ingest **one** picked source per apply cycle, in their order, each with its own Apply gate.

## ingest

One picked URL or user-supplied URL/file.

1. If `raw/sources/` already has this URL: say so. Only continue if the user wants a refresh (new raw **file** with a distinct slug suffix such as `-2026-08-30`; never overwrite the old snapshot).
2. Fetch. For PDFs, extract text with whatever the harness provides. Do not add the PDF to git.
3. Choose a unique slug (catalog + `raw/sources/` + `docs/sources/`).
4. Write `raw/sources/<slug>.md` per schema (excerpts only).
5. Write `docs/sources/<slug>.md` per schema.
6. Draft updates to affected `docs/concepts/`, `docs/entities/`, `docs/index.md`. Create a concept or entity page only when the catalog has no matching title/alias and the idea/entity is load-bearing (appears as a real topic, not a passing mention).
7. Re-read `docs/meta/pins.md`. Drop or rewrite no pinned claim. If the new source conflicts with a pin, omit that hunk and ask.
8. Update `docs/catalog.md` and prepend a `docs/meta/log.md` entry.
9. Apply gate, then Apply.

## query

1. Read `WIKI.md` and `docs/catalog.md`. Open the matching pages. Answer with citations to wiki pages (`[title](relative.md)`).
2. If the wiki is silent, say what is missing. Propose sources only if the user wants that.
3. If the answer is a reusable synthesis (comparison, timeline, thesis update), propose filing it as `docs/analyses/<slug>.md` and/or updates to existing pages. Same Apply gate. Do not file unless they approve.

## lint

After every Apply, deterministic lint always runs.

When the user asks to lint the wiki (health check): run `python3 "$SKILL_ROOT/scripts/lint.py"` first and fix those failures via the Apply gate if needed. Then do an LLM pass:

- Claims that disagree across pages
- Volatile claims whose `as of` date is older than `volatile_days` in `WIKI.md`
- Concepts mentioned often but lacking a page
- Overview (`docs/index.md`) that no longer matches concept pages
- Active pins whose claim text is absent from the cited section
- Orphans: wiki pages with no inbound link from any other wiki page except catalog

Propose fixes as a diff (Apply gate). Do not resolve a dispute by picking a winner; add a **Disputed** section unless the user tells you which claim to keep.

## pin

When the user corrects the wiki:

1. Edit the page so the text is right.
2. Append an active pin in `docs/meta/pins.md` per schema.
3. Apply gate, then Apply.

## rename

`git mv` the page. Update every relative link, `docs/catalog.md`, `parent`/`title` references, aliases, and pins. Apply gate, then Apply.
