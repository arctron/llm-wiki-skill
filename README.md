# llm-wiki-skill

Bare [Agent Skill](https://agentskills.io) that files **final research conclusions and runbooks** from AI-agent work into a markdown wiki. This repo is not a wiki. Each wiki is a separate GitHub repo the skill creates. Read it as GitHub Pages, a local Jekyll server, or the `docs/` markdown on GitHub.

License: [0BSD](LICENSE). Pattern: [Karpathy, LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), specialized for session capture rather than source-ingest encyclopedias.

## Install

Symlink or copy `llm-wiki/` (the folder that contains `SKILL.md`) into the agent skills directory. The folder name must stay `llm-wiki`.

| Agent | Directory |
| --- | --- |
| Claude Code | `~/.claude/skills/llm-wiki` |
| Codex | `~/.agents/skills/llm-wiki` |
| Cursor | `~/.cursor/skills/llm-wiki` |
| OpenCode | `~/.config/opencode/skills/llm-wiki` |
| Grok | `~/.grok/skills/llm-wiki` |
| Fallback | `~/.agents/skills/llm-wiki` |

```bash
git clone git@github.com:arctron/llm-wiki-skill.git
ln -s "$(pwd)/llm-wiki-skill/llm-wiki" ~/.agents/skills/llm-wiki
```

Needs `git`, `python3` (stdlib only), and `gh` (logged in) to create/push wiki repos. Ruby and Bundler are needed only to preview the site locally.

## Use

You can run init from this clone. The wiki path must be outside this git root; if you do not pass a path, the skill uses a sibling of this clone named `wiki-<slug>`.

Work in the agent (search, read repos, run commands). When the result is settled, ask to record the conclusion and/or runbook. The skill proposes a diff; you approve; it lints, commits, and pushes.

GitHub Pages is optional. Personal Free accounts cannot enable Pages on a **private** repo. If Pages is enabled, the built HTML is **public** to anyone with the URL even when the git repo is private (login-gated Pages is GitHub Enterprise Cloud only). On a plan or visibility that cannot host Pages, the skill sets `site: local`, skips the Pages workflow, and you can ask the agent to **serve** the wiki (`bundle exec jekyll serve`, then `http://127.0.0.1:4000/<repo>/`). You can always read `docs/` on GitHub or in an editor.

## Published site search

Each wiki’s Just the Docs site (GitHub Pages or `jekyll serve`) uses [theme search](https://just-the-docs.com/docs/search/): Jekyll writes a JSON corpus at build time; **lunr.js builds the index in the visitor’s browser** on every page load. There is no search server (GitHub Pages only serves files).

Keep that default. Move index construction into CI (prebuilt lunr index or [Pagefind](https://pagefind.app/)) only when a real wiki is slow: search JSON in the megabyte range, or the tab hitching for a second or more on every visit.

The agent does not use this index. It reads `docs/catalog.md` and the markdown files.
