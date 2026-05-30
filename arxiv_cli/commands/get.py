"""Get command — fetch a single paper by arXiv ID."""
import sys
import arxiv
from arxiv_cli.formatters.json_fmt import print_json
from arxiv_cli.formatters.human_fmt import print_human


def run_get(args):
    """Execute `arxiv get <id>` command."""
    paper_id = args.paper_id.strip()
    # Normalize: strip version suffix for search, keep for display
    base_id = paper_id.split("v")[0] if "v" in paper_id else paper_id

    client = arxiv.Client()
    search = arxiv.Search(id_list=[base_id])

    try:
        results = list(client.results(search))
    except Exception as e:
        print(f"Error querying arXiv: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print(f"Paper not found: {paper_id}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print_json(results)
    else:
        print_human(results, show_abstract=True)
