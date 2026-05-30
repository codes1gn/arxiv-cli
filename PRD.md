# Product Requirements Document — arxiv-cli

**Project:** arxiv-cli  
**Slug:** arxiv-cli  
**Version:** 1.0  
**Status:** Draft  
**Platform:** GitHub Copilot (VS Code) + Cursor IDE  
**Date:** 2025-05-29  
**Author:** AI Agent (autonomous /incubate pipeline)

---

## 1. Problem Statement

AI agents frequently need to search, browse, and download academic papers from arXiv — to support research tasks, literature reviews, code implementations, and RAG pipelines. Currently:

- No official arXiv CLI exists.
- Python `urllib` or `requests` calls to the arXiv API are verbose and error-prone for agents.
- Tools like `curl | xmllint` are fragile and hard to parse.
- Human users also lack a fast terminal-native tool for paper search/download.

**Gap:** There is no lightweight, agent-friendly, terminal-native CLI that wraps arXiv search with structured output (JSON) for programmatic agent consumption AND human-readable output for terminal users.

---

## 2. Target Users

| User Type | Need |
|-----------|------|
| **AI Agents** (Copilot, Cursor) | Search for papers, retrieve metadata, download PDFs — via JSON output |
| **Developers / Researchers** | Fast terminal paper lookup without browser; `arxiv search` + `arxiv download` |
| **RAG Pipeline builders** | Bulk metadata harvesting with `--json --limit N` |

---

## 3. Goals

1. **G1 — Core search**: `arxiv search "<query>" [--limit N] [--json]` — returns papers by relevance
2. **G2 — Author filter**: `arxiv search "<query>" --author "<name>"` — filter by author
3. **G3 — Category filter**: `arxiv search "<query>" --category cs.LG` — arXiv subject categories
4. **G4 — Recent papers**: `arxiv recent <category> [--days N]` — last N days (default: 7)
5. **G5 — Paper detail**: `arxiv get <arxiv_id>` — metadata for a specific paper
6. **G6 — Download PDF**: `arxiv download <arxiv_id> [--out <path>]` — save PDF locally
7. **G7 — Agent skill**: Copilot/Cursor skill file teaching agents which commands to use and how to parse output
8. **G8 — Zero auth**: arXiv public API, no API key required

---

## 4. Non-Goals

- Real-time paper streaming / webhooks
- Full-text search (arXiv API does not support it natively)
- Citation management / bibliography export
- GUI / web interface
- Any non-arXiv source (Semantic Scholar, PubMed, etc.)

---

## 5. Features

### 5.1 CLI Commands

```
arxiv search "<query>" [--limit 10] [--json] [--author NAME] [--category CAT]
arxiv recent <category> [--days 7] [--limit 20] [--json]
arxiv get <arxiv_id> [--json]
arxiv download <arxiv_id> [--out ./papers/]
arxiv version
arxiv --help
```

### 5.2 Output Modes

- **Human mode** (default): Formatted table with title, authors, date, ID, abstract (truncated)
- **JSON mode** (`--json`): Array of paper objects — fields: `id`, `title`, `authors`, `published`, `updated`, `summary`, `categories`, `pdf_url`, `abs_url`

### 5.3 Agent Skill File

A `SKILL.md` / agent instruction that teaches:
- What commands exist
- When to use `--json` vs human mode
- How to parse JSON output for further processing
- How to use `arxiv download` to fetch PDFs into workspace
- Example agent workflows (find paper → download → summarize)

### 5.4 Memory Integration

- `data/user-memory.jsonl` tracks: queries run, papers downloaded, categories explored
- Platform: `~/.copilot/skills/arxiv-cli/data/user-memory.jsonl`

---

## 6. Technical Requirements

| Requirement | Spec |
|------------|------|
| Language | Python 3.8+ |
| arXiv API library | `arxiv` PyPI package (official, wraps arXiv API v2) |
| CLI framework | `argparse` (stdlib, zero dependency) |
| Human output | `rich` library (tables, colors) — optional fallback to plain text |
| JSON output | stdlib `json` |
| PDF download | Built into `arxiv` library (`paper.download_pdf()`) |
| Install | `pip install arxiv-cli` or `pip install .` from repo |
| Entry point | `arxiv` console script |
| Python compat | 3.8, 3.9, 3.10, 3.11, 3.12 |

---

## 7. Success Metrics

| Metric | Target |
|--------|--------|
| Test scenarios | ≥ 13 |
| Total batch checks | ≥ 1,000 |
| Pass rate | ≥ 95% |
| CLI commands working | 6/6 |
| Agent skill teaching all commands | Yes |
| Zero-auth operation | Yes |
| JSON output parseable by agents | Yes |

---

## 8. Milestones

| Phase | Deliverable | Status |
|-------|------------|--------|
| 0 | PRD (this document) | ✅ |
| 1 | Architecture design | ⬜ |
| 2 | Development (CLI + skill) | ⬜ |
| 3 | Ship to codes1gn/arxiv-cli | ⬜ |
| 4 | Test suite (≥13 scenarios) | ⬜ |
| 5 | Batch test (≥1000 checks) | ⬜ |
| 6 | README | ⬜ |
| 7 | GitHub Pages website | ⬜ |
| 8 | Verify + memory save | ⬜ |
