# Scenario 04: search-category

**Scenario ID:** `04-search-category`  
**Command:** `arxiv search --category`  
**Goal:** Verify category filtering with arXiv subject codes

## Description

The `--category CAT` flag restricts results to a specific arXiv subject category (e.g., `cs.LG`, `cs.AI`, `quant-ph`) using the `cat:` prefix in the query.

## Expected Behavior

```bash
arxiv search "reinforcement learning" --category cs.LG --limit 20 --json
# Returns only papers in the cs.LG (Machine Learning) category
```

## Checks

- [ ] `--category` flag documented in SKILL.md
- [ ] `cat:` prefix used in query construction
- [ ] `--category` argument in cli.py
- [ ] `cs.LG` example in SKILL.md
- [ ] Category table in SKILL.md (cs.AI, cs.CV etc.)
- [ ] `args.category` handled in run_search
- [ ] Scenario doc present
