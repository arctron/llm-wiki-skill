---
name: llm-wiki
description: >
  Capture final research conclusions and runbooks (install steps, commands)
  from AI-agent work into a GitHub Pages wiki. Use when the user wants to
  start a wiki, record conclusions or a runbook from this session, ingest a
  URL, query the wiki, lint it, or pin a correction. Triggers: /llm-wiki,
  runbook, file this, record conclusions, install instructions, capture.
license: 0BSD
compatibility: Requires git and python3. gh is required to create GitHub repos, enable Pages, and push.
metadata:
  author: arctron
  version: "1.0"
---

# llm-wiki

Do the research and the commands in this session. When the user asks to record, file the **final** conclusions and/or runbook into the wiki. The user approves every diff.

Skill root: the directory that contains this `SKILL.md`.

Read [references/schema.md](references/schema.md) before creating or editing wiki pages, `raw/`, `WIKI.md`, `AGENTS.md`, or `docs/catalog.md`.

## Detect the instance

A wiki root is the directory that contains `WIKI.md`.

- If `WIKI.md` is missing and the user is not starting a wiki: stop and say so.
- If several `WIKI.md` files could apply: ask which root to use.
- After every `git` operation, treat that directory as the cwd for paths in this skill.

## Hard rules

1. Capture only when the user asks to record, file, or save. Never auto-file a session.
2. File the settled conclusion and/or the working procedure, not the transcript or every failed attempt. Dead ends go in a short **Discarded** section only when they stop someone repeating the same mistake.
3. Scrub secrets before any write: API keys, tokens, passwords, private keys, cookies, `Authorization` headers, connection strings with credentials. Replace machine home paths with `~` or `$HOME`. If unsure, ask.
4. `raw/` is append-only third-party excerpts (schema). Never edit or delete an existing raw file. No full pages, PDFs, binaries, or chat dumps.
5. Links and page YAML follow the schema. Never `[[wikilinks]]`.
6. Before creating a page, search `docs/catalog.md` titles, slugs, and `aliases`. Update an existing page rather than mint a near-duplicate.
7. Existing conclusions and runbooks change only through an approved diff.
8. Never contradict or drop an active pin. If new work conflicts with a pin, stop and ask.
9. Do not add `CLAUDE.md`, `.cursorrules`, or other harness-specific instruction files. `AGENTS.md` is the only always-on pointer.
10. Never write a wiki (`WIKI.md`, `docs/`, `raw/`) into `$SKILL_ROOT` or into the git repository that contains this `SKILL.md`. Wikis are always separate repos.

## Apply gate

Every change to `docs/` or `raw/` except the init scaffold:

1. `git pull --ff-only` (stop if this fails).
2. Write the working tree. Record the file list you created or modified.
3. Show `git status`, `git diff --stat`, and the full diff (for new files, show contents if that is easier to review).
4. Wait for explicit approval of that artifact.
5. If rejected: restore only the files from your list (`git restore` tracked files; delete untracked files you created). Stop.
6. If the user wants edits: change the working tree and re-show the diff. Do not commit until approval.
7. On approval, run **Apply**.

Init scaffold does not use this gate.

## Apply

From the wiki root:

1. Run `python3 "$SKILL_ROOT/scripts/lint.py"`.
2. Fix every failure. Re-run until exit 0. If you cannot fix without a content decision, stop and ask.
3. `git add` the approved files plus any lint fixes in those files and in `docs/catalog.md` / `docs/meta/log.md`.
4. Commit with a message like `capture: postgres install on macos` or `ingest: smith-2024` or `pin: use bind mount`.
5. `git pull --ff-only` then `git push`.
6. Report the commit, Pages URL from `WIKI.md`, and which pages changed.

## init

Scaffold a **new** GitHub repo. Do not capture or ingest in this operation.

1. Collect: topic title; slug (lowercase hyphenated); GitHub owner (`gh api user --jq .login` if unset); local path; copyright holder (`git config user.name`); `__DATE__` = today `YYYY-MM-DD`; `__YEAR__` = four-digit year of `__DATE__`. Remaining tokens are the names in [references/init.md](references/init.md).
   Default path when unset: `SKILL_GIT_ROOT=$(git -C "$SKILL_ROOT" rev-parse --show-toplevel)`, then `$WIKI_ROOT` = absolute `<SKILL_GIT_ROOT>/../wiki-<slug>` (sibling of the skill clone, independent of cwd). If that git command fails, ask for an absolute path.
   Resolve `$WIKI_ROOT` to an absolute path. Stop if it is `$SKILL_ROOT`, `$SKILL_GIT_ROOT`, or a subdirectory of either.
2. If the path exists and is not empty: stop.
3. Read [references/init.md](references/init.md). Write every listed file into `$WIKI_ROOT` with tokens replaced. Repo name defaults to `wiki-<slug>`. Pages URL is `https://<owner>.github.io/<repo>/`. Run the rest of init inside `$WIKI_ROOT`.
4. Fill `WIKI.md` scope in one short paragraph. If you must guess the scope, ask instead.
5. `git init -b main`, `git add -A`, commit: `init: wiki scaffold for <topic>`.
6. `gh repo create <owner>/<repo> --public --source=. --remote=origin --push`. Enable Pages from Actions: `gh api --method POST "repos/<owner>/<repo>/pages" -f build_type=workflow`. If Pages already exists, continue.
7. Stop. Tell the user they can research and run commands in later turns, then ask to record conclusions or a runbook.

If `gh` is missing or unauthenticated: leave the local repo committed and print the exact commands for the user.

## capture

Primary operation. Distill **this session** (and tool output already in context) into wiki pages.

1. Confirm what to file: conclusion, runbook, or both. If unclear, ask.
2. Distill. Do not copy the chat. One conclusion page and/or one runbook per capture unless the user named more than one topic.
3. Scrub secrets (hard rule 3).
4. Choose unique slugs (catalog + existing `docs/conclusions/` and `docs/runbooks/`). Prefer updating a catalog match.
5. Write pages per schema. External URLs may be markdown links. Do not ingest a URL unless the user asked to keep excerpts of it in `raw/`.
6. Wrap any `{{` or `{%` in fenced code with `{% raw %}` / `{% endraw %}` (schema).
7. Re-read `docs/meta/pins.md`. Drop or rewrite no pinned claim. If new work conflicts with a pin, omit that hunk and ask.
8. Update `docs/catalog.md`, `docs/index.md` if the overview should mention this, and prepend a `docs/meta/log.md` entry (`capture`).
9. Apply gate, then Apply.

## ingest

Optional. One URL the user named to keep as local excerpts in `raw/sources/` plus a short `docs/sources/` page. Live links on conclusion/runbook pages do not need this. If they want a reading list first, search and list URLs; ingest only the ones they pick, one per apply cycle.

1. If `raw/sources/` already has this URL: say so. Only continue if the user wants a refresh (new raw **file** with a distinct slug suffix such as `-2026-08-30`; never overwrite the old raw file).
2. Fetch. For PDFs, extract text with whatever the harness provides. Do not add the PDF to git.
3. Choose a unique slug.
4. Write `raw/sources/<slug>.md` and `docs/sources/<slug>.md` per schema.
5. Do not rewrite conclusions or runbooks in the same cycle unless the user asked to fold this source into a named page.
6. Re-read pins. Update catalog and prepend a log entry (`ingest`).
7. Apply gate, then Apply.

## query

When the user asks what we already know or how we already did something:

1. Read `WIKI.md` and `docs/catalog.md`. Open the matching pages. Answer with citations to wiki pages (`[title](relative.md)`).
2. If the wiki is silent, say so. Do not silently start a new research pass unless they asked to figure it out.
3. If they then do new work and want it saved, that is **capture**, not an auto-file from this answer.

## lint

After every Apply, deterministic lint always runs.

When the user asks to lint the wiki: run `python3 "$SKILL_ROOT/scripts/lint.py"` first and fix those failures via the Apply gate if needed. Then do an LLM pass:

- Runbooks whose commands or versions are older than `volatile_days` in `WIKI.md` without an `as of` date
- Conclusions that disagree across pages
- Active pins whose claim text is absent from the cited section
- Overview (`docs/index.md`) that no longer matches captured pages
- Orphans: wiki pages with no inbound link from any other wiki page except catalog

Propose fixes as a diff (Apply gate). Do not silently replace a working runbook; prefer **Discarded** plus a new procedure, or ask.

## pin

When the user corrects a conclusion or runbook:

1. Edit the page so the text is right.
2. Append an active pin in `docs/meta/pins.md` per schema.
3. Apply gate, then Apply.

## rename

`git mv` the page. Update every relative link, `docs/catalog.md`, `parent`/`title` references, aliases, and pins. Apply gate, then Apply.
