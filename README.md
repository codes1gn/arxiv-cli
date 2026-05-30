# arxiv-cli

> **Search, browse and download arXiv papers from your terminal — built for humans and AI agents.**

[![Tests](https://github.com/codes1gn/arxiv-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/codes1gn/arxiv-cli/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![arXiv API](https://img.shields.io/badge/arXiv-API%20v2-red.svg)](https://arxiv.org/help/api)

```
$ arxiv search "attention mechanism" --limit 5 --json
[
  {
    "id": "1706.03762",
    "title": "Attention Is All You Need",
    "authors": ["Ashish Vaswani", "Noam Shazeer", ...],
    "published": "2017-06-12",
    "categories": ["cs.CL", "cs.LG"],
    "pdf_url": "https://arxiv.org/pdf/1706.03762"
  },
  ...
]
```

---

## Why arxiv-cli?

| Problem | Before | After |
|---------|--------|-------|
| Search papers in terminal | `curl` + XML parsing | `arxiv search "query" --json` |
| Get recent papers in field | Open browser → arXiv | `arxiv recent cs.LG --days 7` |
| AI agent needs papers | Custom API code | `arxiv search --json` → parse array |
| Download a PDF | Browser → click download | `arxiv download 1706.03762` |
| RAG pipeline feed | Complex urllib code | `arxiv search --json --limit 50` |

---

## Installation

```bash
pip install arxiv-cli
```

Or from source:

```bash
git clone https://github.com/codes1gn/arxiv-cli
cd arxiv-cli
pip install .
```

**Optional: rich output (beautiful tables)**
```bash
pip install arxiv-cli "arxiv-cli[rich]"
```

Verify:
```bash
arxiv --version
# arxiv-cli 1.0.0
```

---

## Commands

### `arxiv search` — Search papers

```bash
# Basic search
arxiv search "transformer architecture"

# JSON output (recommended for agents)
arxiv search "BERT language model" --limit 10 --json

# Filter by author
arxiv search "deep learning" --author "LeCun" --limit 5

# Filter by category
arxiv search "RL policy gradient" --category cs.LG --limit 20

# Show full abstracts
arxiv search "attention" --abstract
```

### `arxiv recent` — Recent papers

```bash
# Last 7 days in Machine Learning
arxiv recent cs.LG

# Last 3 days, JSON output
arxiv recent cs.AI --days 3 --limit 10 --json

# Multiple fields
arxiv recent cs.CV --days 7 --json
```

**Popular categories:** `cs.LG` · `cs.AI` · `cs.CL` · `cs.CV` · `cs.RO` · `quant-ph` · `stat.ML`

### `arxiv get` — Get paper by ID

```bash
# Human-readable (with full abstract)
arxiv get 1706.03762

# JSON output
arxiv get 1706.03762 --json
arxiv get 2310.12567v2 --json
```

### `arxiv download` — Download PDF

```bash
# Download to current directory
arxiv download 1706.03762

# Download to specific folder
arxiv download 1706.03762 --out ./papers/
# ✅  Saved to ./papers/1706.03762.pdf
```

---

## For AI Agents (Copilot / Cursor)

arxiv-cli is designed as an agent-first tool. The `--json` flag returns structured output that agents can parse directly:

```json
[{
  "id": "1706.03762",
  "title": "Attention Is All You Need",
  "authors": ["Ashish Vaswani", ...],
  "published": "2017-06-12",
  "summary": "The dominant sequence transduction models...",
  "categories": ["cs.CL", "cs.LG"],
  "pdf_url": "https://arxiv.org/pdf/1706.03762",
  "abs_url": "https://arxiv.org/abs/1706.03762"
}]
```

**Agent workflow example:**
```bash
# 1. Find papers on a topic
arxiv search "diffusion models" --limit 10 --json > papers.json

# 2. Get full details of a specific paper
arxiv get 2006.11239 --json

# 3. Download the PDF
arxiv download 2006.11239 --out ./papers/
```

### Install the Agent Skill

Copy `SKILL.md` to your AI assistant's skills directory:

```bash
# GitHub Copilot (VS Code)
mkdir -p ~/.copilot/skills/arxiv-cli
cp SKILL.md ~/.copilot/skills/arxiv-cli/

# Cursor
mkdir -p ~/.cursor/skills/arxiv-cli
cp SKILL.md ~/.cursor/skills/arxiv-cli/
```

Or add to your Copilot instructions:
```markdown
## arxiv-cli
Use `arxiv search`, `arxiv recent`, `arxiv get`, `arxiv download` commands.
Always use `--json` for structured output. See SKILL.md for full reference.
```

---

## Platform Support

| Platform | CLI works | Agent skill | Notes |
|----------|-----------|-------------|-------|
| macOS | ✅ | ✅ Cursor + Copilot | Full support |
| Linux | ✅ | ✅ Cursor + Copilot | Full support |
| Windows | ✅ | ✅ Copilot VS Code | Full support |
| Python 3.8+ | ✅ | — | All versions |

---

## Test Results

```
13 scenarios × 91 checks/run × 8 workers × 10 runs = 910 total checks · 100% pass
```

Run the test suite yourself:
```bash
python tests/run_tests.py --workers 8 --runs 10
```

---

## No API Key Required

arXiv is fully open access. No authentication, no rate-limit worries — the `arxiv` Python library handles polite rate limiting automatically (≤3 req/sec).

---

## License

MIT © [codes1gn](https://github.com/codes1gn)

---

## Related

- [agent-handoff](https://github.com/codes1gn/agent-handoff) — Cross-session AI memory with `/handoff` and `/resume`
- [incubate](https://github.com/codes1gn/incubate) — AI-powered project incubation pipeline
- [feature-dev](https://github.com/codes1gn/feature-dev) — Feature development workflow for AI agents
