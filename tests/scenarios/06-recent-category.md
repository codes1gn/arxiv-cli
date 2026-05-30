# Scenario 06: recent-category

**Scenario ID:** `06-recent-category`  
**Command:** `arxiv recent <category>`  
**Goal:** Verify recent papers by category command

## Description

The `arxiv recent <category>` command returns the most recently submitted papers in a given arXiv category, sorted by submission date descending.

## Expected Behavior

```bash
arxiv recent cs.LG --days 7 --limit 10
# Returns up to 10 papers submitted in the last 7 days in cs.LG
```

## Checks

- [ ] `arxiv recent` command documented in SKILL.md
- [ ] `run_recent` function defined in search.py
- [ ] `recent` subparser in cli.py
- [ ] `--days` flag documented in SKILL.md
- [ ] `SubmittedDate` sort criterion used
- [ ] `args.category` used in run_recent
- [ ] Scenario doc present
