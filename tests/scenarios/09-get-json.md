# Scenario 09: get-json

**Scenario ID:** `09-get-json`  
**Command:** `arxiv get --json`  
**Goal:** Verify JSON output for get command

## Description

The `arxiv get <id> --json` variant returns the paper as a JSON object, suitable for agent processing.

## Expected Behavior

```bash
arxiv get 1706.03762 --json
# Returns JSON array with one paper object (same schema as search)
```

## Checks

- [ ] `arxiv get 1706.03762 --json` in SKILL.md
- [ ] `args.json` handled in run_get
- [ ] `print_json` called in run_get
- [ ] `print_human` called in run_get (for non-JSON mode)
- [ ] `show_abstract=True` in human output call for get
- [ ] Paper not found error is handled with exit(1)
- [ ] Scenario doc present
