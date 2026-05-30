# Scenario 03: search-author

**Scenario ID:** `03-search-author`  
**Command:** `arxiv search --author`  
**Goal:** Verify author filtering capability

## Description

The `--author NAME` flag restricts results to papers by a specific author using the `au:` prefix in the arXiv query syntax.

## Expected Behavior

```bash
arxiv search "language model" --author "Vaswani" --limit 5 --json
# Returns only papers with Vaswani as an author
```

## Checks

- [ ] `--author` flag documented in SKILL.md
- [ ] Author filter example present in SKILL.md
- [ ] `--author` argument in cli.py argparse
- [ ] `au:` query prefix used in search.py
- [ ] `args.author` handled in `run_search`
- [ ] Author filter mentioned in skill
- [ ] `AND` combinator used to combine author+query
