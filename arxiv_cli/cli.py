"""Main CLI entry point for arxiv-cli."""
import argparse
import sys

from arxiv_cli import __version__


def build_parser():
    parser = argparse.ArgumentParser(
        prog="arxiv",
        description="arxiv-cli — Search and download arXiv papers from the terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  arxiv search "attention mechanism" --limit 10 --json
  arxiv search "BERT" --author "Devlin" --limit 5
  arxiv search "RL" --category cs.LG --limit 20
  arxiv recent cs.LG --days 7 --limit 10 --json
  arxiv get 1706.03762 --json
  arxiv download 1706.03762 --out ./papers/
""",
    )
    parser.add_argument("--version", action="version", version=f"arxiv-cli {__version__}")

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    # --- search ---
    sp_search = subparsers.add_parser(
        "search", help="Search arXiv papers by query"
    )
    sp_search.add_argument("query", help="Search query string")
    sp_search.add_argument("--limit", "-n", type=int, default=10, metavar="N",
                           help="Max results to return (default: 10)")
    sp_search.add_argument("--author", "-a", default=None, metavar="NAME",
                           help="Filter by author name")
    sp_search.add_argument("--category", "-c", default=None, metavar="CAT",
                           help="Filter by arXiv category (e.g. cs.LG)")
    sp_search.add_argument("--json", "-j", action="store_true",
                           help="Output as JSON (for agent use)")
    sp_search.add_argument("--abstract", action="store_true",
                           help="Show abstract in human output")

    # --- recent ---
    sp_recent = subparsers.add_parser(
        "recent", help="List recent papers in a category"
    )
    sp_recent.add_argument("category", help="arXiv category (e.g. cs.LG, quant-ph)")
    sp_recent.add_argument("--days", "-d", type=int, default=7, metavar="N",
                           help="Look back N days (default: 7)")
    sp_recent.add_argument("--limit", "-n", type=int, default=20, metavar="N",
                           help="Max results (default: 20)")
    sp_recent.add_argument("--json", "-j", action="store_true",
                           help="Output as JSON (for agent use)")

    # --- get ---
    sp_get = subparsers.add_parser(
        "get", help="Get details of a paper by arXiv ID"
    )
    sp_get.add_argument("paper_id", help="arXiv paper ID (e.g. 1706.03762)")
    sp_get.add_argument("--json", "-j", action="store_true",
                        help="Output as JSON (for agent use)")

    # --- download ---
    sp_dl = subparsers.add_parser(
        "download", help="Download the PDF of a paper"
    )
    sp_dl.add_argument("paper_id", help="arXiv paper ID (e.g. 1706.03762)")
    sp_dl.add_argument("--out", "-o", default=".", metavar="DIR",
                       help="Output directory (default: current dir)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "search":
        from arxiv_cli.commands.search import run_search
        run_search(args)
    elif args.command == "recent":
        from arxiv_cli.commands.search import run_recent
        run_recent(args)
    elif args.command == "get":
        from arxiv_cli.commands.get import run_get
        run_get(args)
    elif args.command == "download":
        from arxiv_cli.commands.download import run_download
        run_download(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
