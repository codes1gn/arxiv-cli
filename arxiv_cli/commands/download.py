"""Download command — fetch PDF for an arXiv paper."""
import os
import sys
import arxiv


def run_download(args):
    """Execute `arxiv download <id>` command."""
    paper_id = args.paper_id.strip()
    base_id = paper_id.split("v")[0] if "v" in paper_id else paper_id
    out_dir = getattr(args, "out", ".") or "."

    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

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

    paper = results[0]
    filename = f"{paper.get_short_id().replace('/', '_')}.pdf"
    out_path = os.path.join(out_dir, filename)

    print(f"Downloading: {paper.title[:60]}...")
    print(f"  ID  : {paper.get_short_id()}")
    print(f"  Dest: {out_path}")

    try:
        paper.download_pdf(dirpath=out_dir, filename=filename)
        print(f"  ✅  Saved to {out_path}")
    except Exception as e:
        print(f"  ❌  Download failed: {e}", file=sys.stderr)
        sys.exit(1)
