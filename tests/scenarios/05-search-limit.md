# Scenario 05: search-limit

**Scenario ID:** `05-search-limit`  
**Command:** `arxiv search --limit`  
**Goal:** Verify result count limiting

## Description

The `--limit N` flag controls how many results are returned. Default is 10. This is important for agents to control API call size and processing time.

## Expected Behavior

```bash
arxiv search "neural network" --limit 3 --json
# Returns exactly 3 results (or fewer if not enough match)
```

## Checks

- [ ] `--limit` flag documented in SKILL.md
- [ ] Default value (10) mentioned in SKILL.md or cli.py
- [ ] `--limit` argument in argparse
- [ ] `max_results` passed to arxiv.Search
- [ ] `args.limit` used in run_search
- [ ] `-n` shorthand available
- [ ] Scenario doc present
