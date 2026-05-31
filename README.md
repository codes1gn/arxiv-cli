<div align="center">

# &#x1F4DA; arxiv-cli

### Search, browse and download arXiv papers — built for humans and AI agents

[![Tests](https://img.shields.io/github/actions/workflow/status/codes1gn/arxiv-cli/tests.yml?label=tests&style=flat-square)](https://github.com/codes1gn/arxiv-cli/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white&style=flat-square)](https://www.python.org)
[![arXiv API](https://img.shields.io/badge/arXiv-open%20access-red?style=flat-square)](https://arxiv.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)](LICENSE)

[&#x1F310; Website](https://codes1gn.github.io/arxiv-cli) &bull;
[&#x2753; Why](#why-arxiv-cli) &bull;
[&#x1F680; Quick Start](#installation) &bull;
[&#x1F4DC; Commands](#commands) &bull;
[&#x1F916; For Agents](#for-ai-agents) &bull;
[&#x1F9EA; Tests](#test-results)

</div>

---

## Why arxiv-cli?

| Problem | Before | After |
|---------|--------|-------|
| Search papers in terminal | `curl` + XML parsing | `arxiv search "query" --json` |
| Get recent papers in field | Open browser → arXiv | `arxiv recent cs.LG --days 7` |
| AI agent needs papers | Custom API code | `arxiv search --json` → parse array |
| Download a PDF | Browser → click download | `arxiv download 1706.03762` |
| RAG pipeline feed | Complex urllib code | `arxiv search --json --limit 50` |

No API key required. arXiv is fully open access.

---

## Installation

```bash
pip install arxiv-cli
# or from source:
git clone https://github.com/codes1gn/arxiv-cli && cd arxiv-cli && pip install .
```

---

## Commands

### `arxiv search` — Search papers

```bash
arxiv search "attention mechanism"
arxiv search "BERT" --limit 10 --json       # structured output for agents
arxiv search "deep learning" --author "LeCun" --limit 5
arxiv search "RL" --category cs.LG --limit 20
arxiv search "diffusion models" --abstract  # show full abstracts
```

### `arxiv recent` — Recent papers

```bash
arxiv recent cs.LG                          # last 7 days in ML
arxiv recent cs.AI --days 3 --json          # 3 days, JSON
```

Popular categories: `cs.LG` · `cs.AI` · `cs.CL` · `cs.CV` · `cs.RO` · `quant-ph` · `stat.ML`

### `arxiv get` — Get paper by ID

```bash
arxiv get 1706.03762            # human-readable
arxiv get 1706.03762 --json    # structured output
```

### `arxiv download` — Download PDF

```bash
arxiv download 1706.03762 --out ./papers/
# ✅  Saved to ./papers/1706.03762.pdf
```

---

## For AI Agents

arxiv-cli is designed as an **agent-first** tool. The `--json` flag returns structured output agents can parse directly:

```json
[{
  "id": "1706.03762",
  "title": "Attention Is All You Need",
  "authors": ["Ashish Vaswani", "..."],
  "published": "2017-06-12",
  "summary": "The dominant sequence transduction models...",
  "categories": ["cs.CL", "cs.LG"],
  "pdf_url": "https://arxiv.org/pdf/1706.03762"
}]
```

**Agent workflow:**
```bash
arxiv search "diffusion models" --limit 10 --json > papers.json
arxiv get 2006.11239 --json
arxiv download 2006.11239 --out ./papers/
```

### Install the Agent Skill

```bash
# GitHub Copilot (VS Code)
mkdir -p ~/.copilot/skills/arxiv-cli && cp SKILL.md ~/.copilot/skills/arxiv-cli/

# Cursor
mkdir -p ~/.cursor/skills/arxiv-cli && cp SKILL.md ~/.cursor/skills/arxiv-cli/
```

---

## Platform Support

| Platform | CLI works | Agent skill | Notes |
|----------|:---------:|:-----------:|-------|
| macOS | ✅ | ✅ Cursor + Copilot | Full support |
| Linux | ✅ | ✅ Cursor + Copilot | Full support |
| Windows | ✅ | ✅ Copilot VS Code | Full support |
| Python 3.8+ | ✅ | — | All versions |

---

## Test Results

```bash
python tests/run_tests.py --workers 8 --runs 10
```

```
13 scenarios × 7 checks × 8 workers × 10 runs = 7,280 checks
Pass rate: 100.0% ✅
```

---

## License

MIT © [codes1gn](https://github.com/codes1gn)

---

## Related

- [agent-handoff](https://github.com/codes1gn/agent-handoff) — Cross-session AI memory
- [workflows](https://github.com/codes1gn/workflows) — Multi-agent workflow orchestration
- [incubate](https://github.com/codes1gn/incubate) — Autonomous project incubation pipeline

---

<div align="center">
  <sub>No API key required &bull; open access &bull; agent-first design &bull; GitHub Copilot + Cursor</sub>
</div>
