# Scenario 11: agent-workflow

**Scenario ID:** `11-agent-workflow`  
**Command:** Multi-step workflow  
**Goal:** Verify SKILL.md teaches complete agent workflows

## Description

AI agents need to know how to chain multiple arxiv-cli commands together to accomplish research goals. The SKILL.md should document at least one complete multi-step workflow.

## Expected Workflows

1. **Literature Review**: search → select paper by ID → get details → download PDF
2. **Daily Monitoring**: recent category → check new papers → download interesting ones
3. **Author Research**: search by author → get paper details → download

## Checks

- [ ] "Agent Workflows" or "Workflow" section in SKILL.md
- [ ] Multi-step workflow documented (Step 1, Step 2...)
- [ ] Search + download workflow combination documented
- [ ] `--json` flag used in all workflow steps
- [ ] Research/RAG workflow mentioned
- [ ] Scenario doc present
- [ ] JSON output used in agent workflows
