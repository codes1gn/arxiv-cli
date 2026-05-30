# Scenario 08: get-by-id

**Scenario ID:** `08-get-by-id`  
**Command:** `arxiv get <id>`  
**Goal:** Verify paper lookup by arXiv ID

## Description

The `arxiv get <id>` command fetches full details of a specific paper by its arXiv ID (e.g., `1706.03762`). It shows the full abstract by default.

## Expected Behavior

```bash
arxiv get 1706.03762
# Returns full paper details with title, authors, abstract, links
```

## Checks

- [ ] `arxiv get` command documented in SKILL.md
- [ ] `run_get` function defined in commands/get.py
- [ ] `get` subparser in cli.py
- [ ] `paper_id` argument in get.py
- [ ] `id_list` used for targeted lookup
- [ ] `1706.03762` example in SKILL.md
- [ ] Scenario doc present
