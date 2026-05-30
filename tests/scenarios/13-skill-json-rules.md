# Scenario 13: skill-json-rules

**Scenario ID:** `13-skill-json-rules`  
**Command:** SKILL.md agent rules  
**Goal:** Verify SKILL.md contains critical agent usage rules

## Description

SKILL.md must contain explicit rules for AI agent behavior — specifically around JSON mode, error handling, and rate limiting. Agents must know to ALWAYS use `--json`, never parse human output, handle empty results, and not add artificial rate limiting.

## Required Rules

1. **Always use `--json`** in agent workflows
2. **Never parse human output** (table format is not stable)
3. **Handle empty results** (`[]` JSON response)
4. **Check exit code** for error detection
5. **No manual rate limiting** needed (handled automatically)

## Checks

- [ ] "Agent Rules" or "CRITICAL RULES" section in SKILL.md
- [ ] "Always use --json" rule documented
- [ ] "Never parse human output" rule documented  
- [ ] Empty result handling documented (`[]`)
- [ ] Exit code rule documented
- [ ] Rate limiting handled automatically
- [ ] Scenario doc present
