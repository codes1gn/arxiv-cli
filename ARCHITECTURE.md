# Architecture Design — arxiv-cli

**Version:** 1.0  
**Status:** Final  
**Review findings applied:** ✅

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        arxiv-cli                                │
│                                                                 │
│   User/Agent Input                                              │
│       │                                                         │
│       ▼                                                         │
│   CLI Entry Point (arxiv_cli/__main__.py)                       │
│       │                                                         │
│       ├──▶ SearchCommand  ──────▶ arXiv API (via arxiv lib)    │
│       ├──▶ RecentCommand  ──────▶ arXiv API (date-filtered)    │
│       ├──▶ GetCommand     ──────▶ arXiv API (by ID)            │
│       └──▶ DownloadCommand ─────▶ arXiv PDF download           │
│                                                                 │
│   Output Formatters                                             │
│       ├──▶ JSONFormatter  (machine-readable, --json flag)       │
│       └──▶ HumanFormatter (rich table or plain text fallback)   │
│                                                                 │
│   Memory Layer (optional, JSONL)                                │
│       └──▶ data/user-memory.jsonl                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Module Structure

```
arxiv-cli/
├── arxiv_cli/
│   ├── __init__.py       # version
│   ├── __main__.py       # python -m arxiv_cli entry
│   ├── cli.py            # argparse setup + command dispatch
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── search.py     # search + recent commands
│   │   ├── get.py        # get command (by ID)
│   │   └── download.py   # download command
│   ├── formatters/
│   │   ├── __init__.py
│   │   ├── json_fmt.py   # JSON output formatter
│   │   └── human_fmt.py  # rich table or plain text
│   └── memory.py         # JSONL memory read/write
├── tests/
│   ├── run_tests.py      # pattern-based test runner (no live API needed)
│   └── scenarios/        # 13+ .md scenario docs
├── data/
│   └── user-memory.jsonl # seed empty
├── docs/
│   └── index.html        # GitHub Pages
├── SKILL.md              # Agent skill file (Copilot + Cursor)
├── README.md
├── setup.py              # or pyproject.toml
├── requirements.txt
├── LICENSE
├── .gitignore
└── .github/
    └── workflows/
        ├── tests.yml     # CI tests
        └── pages.yml     # GitHub Pages deploy
```

---

## 3. Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.8+ | Cross-platform, arXiv library ecosystem |
| CLI framework | `argparse` (stdlib) | Zero extra dependency, widely understood |
| arXiv API | `arxiv>=2.1` PyPI | Official wrapper, handles XML/Atom feed parsing, PDF download |
| Human output | `rich` (optional) → plain text fallback | Nice tables; degrades gracefully if not installed |
| JSON output | stdlib `json` | Reliable, zero-dep |
| Testing | Pattern matching on SKILL.md + scenario docs (no live API) | Fast, deterministic, agent-readable |
| Memory | JSONL (append-only) | Same format as incubate memory layer |

---

## 4. CLI Interface Spec

```bash
# Search papers
arxiv search "attention mechanism" --limit 10 --json
arxiv search "transformer language model" --author "Vaswani" --limit 5
arxiv search "quantum computing" --category quant-ph --limit 20

# Recent papers by category
arxiv recent cs.LG --days 7 --limit 20 --json
arxiv recent cs.AI --days 3

# Get paper by ID
arxiv get 1706.03762 --json
arxiv get 2310.12567

# Download PDF
arxiv download 1706.03762
arxiv download 1706.03762 --out ./papers/

# Meta
arxiv --version
arxiv --help
arxiv search --help
```

---

## 5. JSON Output Schema

```json
[
  {
    "id": "1706.03762",
    "title": "Attention Is All You Need",
    "authors": ["Ashish Vaswani", "Noam Shazeer"],
    "published": "2017-06-12",
    "updated": "2023-08-02",
    "summary": "The dominant sequence transduction models...",
    "categories": ["cs.CL", "cs.LG"],
    "pdf_url": "https://arxiv.org/pdf/1706.03762",
    "abs_url": "https://arxiv.org/abs/1706.03762"
  }
]
```

---

## 6. Date Filtering Strategy

The `arxiv` Python library (v2.x) uses `arxiv.SortCriterion.SubmittedDate` for sorting. The `recent` command will:

1. Query with `sort_by=SortCriterion.SubmittedDate, sort_order=SortOrder.Descending`
2. Fetch results and filter client-side where `published >= today - N days`
3. Stop fetching when `published < cutoff` (results are date-ordered)
4. Default `--days 7`, default `--limit 20`

This approach is reliable and doesn't require a special API filter.

---

## 7. Agent Skill Design

The SKILL.md will teach agents:

1. **When to use**: paper lookup, literature review, RAG document fetching
2. **Preferred workflow for agents**: always use `--json`, never parse human output
3. **Command examples with expected JSON shapes**
4. **Download workflow**: `arxiv download <id> --out ./papers/` → then read PDF
5. **Error signals**: non-zero exit code, empty `[]` JSON response
6. **Rate limiting note**: arXiv asks for ≤3 req/sec; the `arxiv` library handles this automatically

---

## Decision Log

| # | Decision | Why |
|---|----------|-----|
| 1 | Entry point = `arxiv` (command name) | Intuitive; no conflict since it's a script entry, not Python module import |
| 2 | Package name = `arxiv-cli` in PyPI | Distinguishes from `arxiv` Python library |
| 3 | `argparse` over `click` | Zero deps; click adds weight for a small CLI |
| 4 | Pattern-based tests (no live API) | Deterministic, fast, agent-compatible — tests verify skill/scenario document completeness |
| 5 | `rich` optional | Avoids hard dependency on colorized output; graceful fallback to plain text |
| 6 | Client-side date filter for `recent` | arXiv API v2 doesn't have native date range param; sort + filter is reliable |
| 7 | JSONL memory (same format as incubate) | Consistency across skills ecosystem |
