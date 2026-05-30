# Scenario 12: skill-commands

**Scenario ID:** `12-skill-commands`  
**Command:** SKILL.md validation  
**Goal:** Verify SKILL.md documents all 4 main commands

## Description

The SKILL.md must comprehensively document all 4 commands in the arxiv-cli: `search`, `recent`, `get`, and `download`. This ensures agents have complete command knowledge.

## Required Commands

1. `arxiv search` — search papers
2. `arxiv recent` — recent papers by category
3. `arxiv get` — get paper by ID
4. `arxiv download` — download PDF

## Checks

- [ ] `arxiv search` command documented
- [ ] `arxiv recent` command documented
- [ ] `arxiv get` command documented
- [ ] `arxiv download` command documented
- [ ] All 4 commands appear in SKILL.md
- [ ] "Command Reference" section present
- [ ] Scenario doc present
