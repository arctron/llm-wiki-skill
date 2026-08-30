# llm-wiki-skill

Bare [Agent Skill](https://agentskills.io) that files **final research conclusions and runbooks** from AI-agent work into a GitHub Pages wiki. This repo is not a wiki. Each wiki is a separate GitHub repo the skill creates.

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

Needs `git`, `python3` (stdlib only), and `gh` (logged in) to create/push wiki repos and enable Pages.

## Use

You can run init from this clone. The wiki path must be outside this git root; if you do not pass a path, the skill uses a sibling of this clone named `wiki-<slug>`.

Work in the agent (search, read repos, run commands). When the result is settled, ask to record the conclusion and/or runbook. The skill proposes a diff; you approve; it lints, commits, and pushes.

The first GitHub Actions run may wait for you to approve the `github-pages` environment on the wiki repo.
