"""Search and recent commands for arxiv-cli."""
import sys
import arxiv
from arxiv_cli.formatters.json_fmt import print_json
from arxiv_cli.formatters.human_fmt import print_human


def run_search(args):
    """Execute `arxiv search` command."""
    query = args.query

    if args.author:
        query = f"au:{args.author} AND {query}"
    if args.category:
        query = f"cat:{args.category} AND {query}"

    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=args.limit,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    try:
        results = list(client.results(search))
    except Exception as e:
        print(f"Error querying arXiv: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        if args.json:
            print("[]")
        else:
            print("No results found.")
        return

    if args.json:
        print_json(results)
    else:
        print_human(results, show_abstract=getattr(args, "abstract", False))


def run_recent(args):
    """Execute `arxiv recent` command."""
    from datetime import datetime, timedelta, timezone

    category = args.category
    days = getattr(args, "days", 7)
    limit = getattr(args, "limit", 20)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    client = arxiv.Client()
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=min(limit * 3, 300),
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    try:
        raw = client.results(search)
        results = []
        for p in raw:
            if p.published:
                pub = p.published
                # Normalize to UTC-aware if the datetime is naive
                if pub.tzinfo is None:
                    pub = pub.replace(tzinfo=timezone.utc)
                if pub < cutoff:
                    break
            results.append(p)
            if len(results) >= limit:
                break
    except Exception as e:
        print(f"Error querying arXiv: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        if args.json:
            print("[]")
        else:
            print(f"No recent papers found in {category} (last {days} days).")
        return

    if args.json:
        print_json(results)
    else:
        print_human(results, show_abstract=False)
