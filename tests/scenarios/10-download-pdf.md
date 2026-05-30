# Scenario 10: download-pdf

**Scenario ID:** `10-download-pdf`  
**Command:** `arxiv download <id>`  
**Goal:** Verify PDF download functionality

## Description

The `arxiv download <id>` command downloads the PDF of a paper to the specified directory (default: current directory). It creates the output directory if it doesn't exist.

## Expected Behavior

```bash
arxiv download 1706.03762 --out ./papers/
# Downloads: ./papers/1706.03762.pdf
# Prints: ✅  Saved to ./papers/1706.03762.pdf
```

## Checks

- [ ] `arxiv download` command documented in SKILL.md
- [ ] `run_download` function defined in commands/download.py
- [ ] `download` subparser in cli.py
- [ ] `--out` flag documented in SKILL.md
- [ ] `download_pdf` method called on paper object
- [ ] `os.makedirs` used to create output directory
- [ ] Scenario doc present
