# Scenario 02: search-json

**Scenario ID:** `02-search-json`  
**Command:** `arxiv search --json`  
**Goal:** Verify JSON output mode for agent consumption

## Description

AI agents must use `--json` flag to get machine-readable output. The JSON output is an array of paper objects with a defined schema.

## Expected Behavior

```bash
arxiv search "attention mechanism" --limit 5 --json
# Output: JSON array of paper objects
[
  {
    "id": "...",
    "title": "...",
    "authors": [...],
    "published": "YYYY-MM-DD",
    "pdf_url": "...",
    "abs_url": "..."
  }
]
```

## Checks

- [ ] `--json` flag documented in SKILL.md
- [ ] JSON output shape documented with schema
- [ ] `arxiv_cli/formatters/json_fmt.py` exists
- [ ] `print_json` function is defined
- [ ] `format_papers` function is defined
- [ ] `pdf_url` in JSON schema documentation
- [ ] `abs_url` in JSON schema documentation
