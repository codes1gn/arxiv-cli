# Scenario 07: recent-json

**Scenario ID:** `07-recent-json`  
**Command:** `arxiv recent --json`  
**Goal:** Verify JSON output for recent command

## Description

The `arxiv recent` command supports `--json` flag for agent-friendly output, returning the same JSON schema as `arxiv search --json`.

## Expected Behavior

```bash
arxiv recent cs.LG --days 3 --limit 5 --json
# Returns JSON array of paper objects
```

## Checks

- [ ] `recent cs.LG ... --json` example in SKILL.md
- [ ] `args.json` handled in run_recent
- [ ] `print_json` called in run_recent
- [ ] Empty result (`[]`) handled in run_recent
- [ ] `--days` argument in argparse
- [ ] Date cutoff calculation present (timedelta or cutoff)
- [ ] Scenario doc present
