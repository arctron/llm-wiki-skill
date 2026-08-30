# llm-wiki-skill

Portable [Agent Skill](https://agentskills.io) that maintains a **topic wiki** as a GitHub repo with GitHub Pages.

You pick the topic and approve every source and every diff. The agent searches, files, cross-references, and publishes.

Pattern: [Karpathy, LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). This repository is the skill, not a wiki. Each topic is its own public repo.

License: [0BSD](LICENSE).

## Install

Copy or symlink the `llm-wiki/` folder (the directory that contains `SKILL.md`) into your agent's skills directory:

| Agent | Directory |
| --- | --- |
| Claude Code | `~/.claude/skills/llm-wiki` |
| Codex | `~/.agents/skills/llm-wiki` |
| Cursor | `~/.cursor/skills/llm-wiki` |
| OpenCode | `~/.config/opencode/skills/llm-wiki` |
| Grok | `~/.grok/skills/llm-wiki` |
| Portable fallback | `~/.agents/skills/llm-wiki` |

```bash
git clone git@github.com:arctron/llm-wiki-skill.git
ln -s "$(pwd)/llm-wiki-skill/llm-wiki" ~/.agents/skills/llm-wiki
```

Repeat the `ln -s` line for each agent you use, or copy instead of symlink. The folder name must be `llm-wiki`.

Needs `git`, `python3` (stdlib only), and `gh` to create/push repos and enable Pages.

## Use

In any agent, with the skill installed:

- “Start a wiki on \<topic\>”
- “Propose sources for this wiki”
- “Ingest this URL”
- “What does the wiki say about X?”
- “Lint the wiki”
- “Pin this correction”

Each wiki repo contains `WIKI.md` (instance config) and `AGENTS.md` (load this skill). Wiki pages are `docs/` (the site). Source snapshots are `raw/` (git only, excerpts only).

The first GitHub Actions run may wait for you to approve the `github-pages` environment on the repo.

## What this skill will not do

- Ingest more than one source per approval
- Scrape full articles or commit PDFs into a public repo
- Overwrite existing claims or pins without an approved diff
- Auto-file chat answers into the wiki
- Depend on Obsidian, MkDocs, embeddings, or MCP
