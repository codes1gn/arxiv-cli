"""JSON output formatter for arxiv-cli."""
import json
import sys


def format_papers(papers):
    """Convert list of arxiv.Result objects to JSON-serializable list."""
    results = []
    for p in papers:
        results.append({
            "id": p.get_short_id(),
            "title": p.title.strip(),
            "authors": [str(a) for a in p.authors],
            "published": p.published.strftime("%Y-%m-%d") if p.published else None,
            "updated": p.updated.strftime("%Y-%m-%d") if p.updated else None,
            "summary": p.summary.replace("\n", " ").strip(),
            "categories": p.categories,
            "pdf_url": p.pdf_url,
            "abs_url": p.entry_id,
        })
    return results


def print_json(papers):
    """Print papers as JSON to stdout."""
    print(json.dumps(format_papers(papers), indent=2, ensure_ascii=False))
