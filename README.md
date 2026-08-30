# llm-wiki-skill

Bare [Agent Skill](https://agentskills.io) for **init and maintain** of topic wikis. This repo is not a wiki. Each wiki is a separate GitHub repo the skill creates.

License: [0BSD](LICENSE). Pattern: [Karpathy, LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

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

Needs `git`, `python3`, and `gh` (logged in) to create and push wiki repos.

## Use

With the skill installed, in any repo *except this one*: “start a wiki on \<topic\>”. The skill scaffolds a new public GitHub repo, enables Pages, proposes sources, and stops. Then: ingest, query, lint, pin — always against that wiki repo.
