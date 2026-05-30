"""Human-readable output formatter for arxiv-cli.
Uses `rich` if available, falls back to plain text.
"""
import sys
import textwrap

_ABSTRACT_LEN = 200

try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False


def _truncate(text, length=_ABSTRACT_LEN):
    text = text.replace("\n", " ").strip()
    if len(text) > length:
        return text[:length] + "…"
    return text


def print_human(papers, show_abstract=False):
    if not papers:
        print("No results found.")
        return

    if _HAS_RICH:
        _print_rich(papers, show_abstract)
    else:
        _print_plain(papers, show_abstract)


def _print_rich(papers, show_abstract):
    console = Console()
    table = Table(box=box.ROUNDED, show_lines=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold white", max_width=50)
    table.add_column("Authors", style="green", max_width=30)
    table.add_column("Date", style="yellow", no_wrap=True)
    table.add_column("Categories", style="magenta", max_width=20)
    if show_abstract:
        table.add_column("Abstract", max_width=60)

    for p in papers:
        authors = ", ".join(str(a) for a in p.authors[:3])
        if len(p.authors) > 3:
            authors += f" +{len(p.authors) - 3}"
        date = p.published.strftime("%Y-%m-%d") if p.published else "?"
        cats = ", ".join(p.categories[:2])
        row = [p.get_short_id(), p.title.strip(), authors, date, cats]
        if show_abstract:
            row.append(_truncate(p.summary))
        table.add_row(*row)

    console.print(table)
    console.print(f"[dim]{len(papers)} result(s)[/dim]")


def _print_plain(papers, show_abstract):
    for i, p in enumerate(papers, 1):
        authors = ", ".join(str(a) for a in p.authors[:3])
        if len(p.authors) > 3:
            authors += f" +{len(p.authors) - 3}"
        date = p.published.strftime("%Y-%m-%d") if p.published else "?"
        print(f"\n[{i}] {p.get_short_id()} — {date}")
        print(f"    Title  : {p.title.strip()}")
        print(f"    Authors: {authors}")
        print(f"    URL    : {p.entry_id}")
        if show_abstract:
            print(f"    Abstract: {_truncate(p.summary)}")
    print(f"\n{len(papers)} result(s)")
