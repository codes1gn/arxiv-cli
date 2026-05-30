# Scenario 01: search-basic

**Scenario ID:** `01-search-basic`  
**Command:** `arxiv search`  
**Goal:** Verify basic search functionality is documented and implemented

## Description

The `arxiv search "<query>"` command is the primary entry point for finding papers. It queries the arXiv API and returns a list of papers matching the query.

## Expected Behavior

```bash
arxiv search "attention mechanism"
# Returns formatted table of papers with title, authors, date, ID
```

## Checks

- [ ] `arxiv search` command is documented in SKILL.md
- [ ] A basic query example is present
- [ ] `--limit` flag is documented
- [ ] `search` subparser exists in `arxiv_cli/cli.py`
- [ ] `arxiv_cli/commands/search.py` file exists
- [ ] `run_search` function is defined
- [ ] `arxiv.Search` is used to query the API

## Pattern Assertions

| Check | Pattern | File |
|-------|---------|------|
| command docs | `arxiv search` | SKILL.md |
| example query | `attention mechanism` | SKILL.md |
| limit flag | `--limit` | SKILL.md |
| subparser | `search` | cli.py |
| search module | file exists | commands/search.py |
| run_search fn | `def run_search` | commands/search.py |
| api call | `arxiv.Search` | commands/search.py |
