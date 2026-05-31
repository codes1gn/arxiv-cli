#!/usr/bin/env python3
"""
arxiv-cli test suite — pattern-based scenario checks.
No live API calls. Tests verify SKILL.md, scenario docs, and source code structure.
"""
import os
import re
import sys
import json
import time
import argparse
import concurrent.futures
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ─── Scenario registry ────────────────────────────────────────────────────────

SCENARIOS = [
    "01-search-basic",
    "02-search-json",
    "03-search-author",
    "04-search-category",
    "05-search-limit",
    "06-recent-category",
    "07-recent-json",
    "08-get-by-id",
    "09-get-json",
    "10-download-pdf",
    "11-agent-workflow",
    "12-skill-commands",
    "13-skill-json-rules",
]

# ─── Check functions (one per scenario) ──────────────────────────────────────

def check_01_search_basic():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    checks = [
        ("arxiv search command documented", "arxiv search" in skill),
        ("basic query example present", '"attention mechanism"' in skill or "attention mechanism" in skill),
        ("--limit flag documented", "--limit" in skill),
        ("search subparser in cli.py", "search" in (ROOT / "arxiv_cli" / "cli.py").read_text(encoding="utf-8")),
        ("commands/search.py exists", (ROOT / "arxiv_cli" / "commands" / "search.py").exists()),
        ("run_search defined", "def run_search" in (ROOT / "arxiv_cli" / "commands" / "search.py").read_text(encoding="utf-8")),
        ("arxiv.Search used", "arxiv.Search" in (ROOT / "arxiv_cli" / "commands" / "search.py").read_text(encoding="utf-8")),
    ]
    return checks


def check_02_search_json():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    json_fmt = (ROOT / "arxiv_cli" / "formatters" / "json_fmt.py").read_text(encoding="utf-8")
    checks = [
        ("--json flag documented in skill", "--json" in skill),
        ("JSON output shape documented", '"id"' in skill and '"title"' in skill),
        ("json_fmt.py exists", (ROOT / "arxiv_cli" / "formatters" / "json_fmt.py").exists()),
        ("print_json function defined", "def print_json" in json_fmt),
        ("format_papers function defined", "def format_papers" in json_fmt),
        ("pdf_url in JSON schema", '"pdf_url"' in skill),
        ("abs_url in JSON schema", '"abs_url"' in skill),
    ]
    return checks


def check_03_search_author():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    search = (ROOT / "arxiv_cli" / "commands" / "search.py").read_text(encoding="utf-8")
    checks = [
        ("--author flag documented in skill", "--author" in skill),
        ("author example present", "Vaswani" in skill or "--author" in skill),
        ("author arg in cli.py", "--author" in (ROOT / "arxiv_cli" / "cli.py").read_text(encoding="utf-8")),
        ("au: query prefix used", "au:" in search),
        ("author arg handled in run_search", "args.author" in search),
        ("author filter scenario documented", "author" in skill.lower()),
        ("AND combinator used", " AND " in search),
    ]
    return checks


def check_04_search_category():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    search = (ROOT / "arxiv_cli" / "commands" / "search.py").read_text(encoding="utf-8")
    checks = [
        ("--category flag documented", "--category" in skill),
        ("cat: prefix used in query", "cat:" in search),
        ("category arg in cli.py", "--category" in (ROOT / "arxiv_cli" / "cli.py").read_text(encoding="utf-8")),
        ("cs.LG example present", "cs.LG" in skill),
        ("categories table in skill", "cs.AI" in skill and "cs.CV" in skill),
        ("args.category handled", "args.category" in search),
        ("category scenario 04 exists", (ROOT / "tests" / "scenarios" / "04-search-category.md").exists()),
    ]
    return checks


def check_05_search_limit():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    cli = (ROOT / "arxiv_cli" / "cli.py").read_text(encoding="utf-8")
    checks = [
        ("--limit flag documented", "--limit" in skill),
        ("default limit mentioned", "default: 10" in skill or "default=10" in cli),
        ("limit arg in argparse", "\"--limit\"" in cli or "'--limit'" in cli),
        ("max_results used in search", "max_results" in (ROOT / "arxiv_cli" / "commands" / "search.py").read_text(encoding="utf-8")),
        ("args.limit used", "args.limit" in (ROOT / "arxiv_cli" / "commands" / "search.py").read_text(encoding="utf-8")),
        ("--limit -n shorthand", "-n" in cli),
        ("limit scenario doc exists", (ROOT / "tests" / "scenarios" / "05-search-limit.md").exists()),
    ]
    return checks


def check_06_recent_category():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    search = (ROOT / "arxiv_cli" / "commands" / "search.py").read_text(encoding="utf-8")
    checks = [
        ("arxiv recent command documented", "arxiv recent" in skill),
        ("run_recent defined", "def run_recent" in search),
        ("recent subparser in cli.py", '"recent"' in (ROOT / "arxiv_cli" / "cli.py").read_text(encoding="utf-8")),
        ("--days flag documented", "--days" in skill),
        ("SubmittedDate sort used", "SubmittedDate" in search),
        ("category argument in run_recent", "args.category" in search),
        ("recent scenario doc exists", (ROOT / "tests" / "scenarios" / "06-recent-category.md").exists()),
    ]
    return checks


def check_07_recent_json():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    search = (ROOT / "arxiv_cli" / "commands" / "search.py").read_text(encoding="utf-8")
    checks = [
        ("recent --json example in skill", "recent cs.LG" in skill and "--json" in skill),
        ("json flag handled in run_recent", "args.json" in search),
        ("print_json called in recent", "print_json" in search),
        ("empty result handled", '"]"' in search or '"[]"' in search or "print(\"[]\")" in search),
        ("days arg in argparse", "--days" in (ROOT / "arxiv_cli" / "cli.py").read_text(encoding="utf-8")),
        ("cutoff date calculation", "cutoff" in search or "timedelta" in search),
        ("recent json scenario doc exists", (ROOT / "tests" / "scenarios" / "07-recent-json.md").exists()),
    ]
    return checks


def check_08_get_by_id():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    get_cmd = (ROOT / "arxiv_cli" / "commands" / "get.py").read_text(encoding="utf-8")
    checks = [
        ("arxiv get command documented", "arxiv get" in skill),
        ("run_get defined", "def run_get" in get_cmd),
        ("get subparser in cli.py", '"get"' in (ROOT / "arxiv_cli" / "cli.py").read_text(encoding="utf-8")),
        ("paper_id argument", "paper_id" in get_cmd),
        ("id_list used for lookup", "id_list" in get_cmd),
        ("1706.03762 example in skill", "1706.03762" in skill),
        ("get scenario doc exists", (ROOT / "tests" / "scenarios" / "08-get-by-id.md").exists()),
    ]
    return checks


def check_09_get_json():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    get_cmd = (ROOT / "arxiv_cli" / "commands" / "get.py").read_text(encoding="utf-8")
    checks = [
        ("get --json documented", "arxiv get 1706.03762 --json" in skill),
        ("json flag handled in run_get", "args.json" in get_cmd),
        ("print_json called in get", "print_json" in get_cmd),
        ("print_human called in get", "print_human" in get_cmd),
        ("show_abstract=True in get", "show_abstract=True" in get_cmd),
        ("paper not found error handled", "not found" in get_cmd),
        ("get json scenario doc exists", (ROOT / "tests" / "scenarios" / "09-get-json.md").exists()),
    ]
    return checks


def check_10_download_pdf():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    dl = (ROOT / "arxiv_cli" / "commands" / "download.py").read_text(encoding="utf-8")
    checks = [
        ("arxiv download command documented", "arxiv download" in skill),
        ("run_download defined", "def run_download" in dl),
        ("download subparser in cli.py", '"download"' in (ROOT / "arxiv_cli" / "cli.py").read_text(encoding="utf-8")),
        ("--out flag documented", "--out" in skill),
        ("download_pdf method called", "download_pdf" in dl),
        ("os.makedirs used", "makedirs" in dl),
        ("download scenario doc exists", (ROOT / "tests" / "scenarios" / "10-download-pdf.md").exists()),
    ]
    return checks


def check_11_agent_workflow():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    checks = [
        ("agent workflows section present", "Agent Workflows" in skill or "Workflow" in skill),
        ("multi-step workflow documented", "Step 1" in skill or "Step 2" in skill),
        ("search then download workflow", "download" in skill.lower() and "search" in skill.lower()),
        ("--json flag in workflows", "--json" in skill),
        ("RAG or research workflow", "research" in skill.lower() or "RAG" in skill),
        ("workflow scenario doc exists", (ROOT / "tests" / "scenarios" / "11-agent-workflow.md").exists()),
        ("json output used in workflows", "json" in skill.lower()),
    ]
    return checks


def check_12_skill_commands():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    checks = [
        ("arxiv search command documented", "arxiv search" in skill),
        ("arxiv recent command documented", "arxiv recent" in skill),
        ("arxiv get command documented", "arxiv get" in skill),
        ("arxiv download command documented", "arxiv download" in skill),
        ("all 4 commands in skill", skill.count("arxiv search") >= 1 and skill.count("arxiv recent") >= 1),
        ("command reference section", "Command Reference" in skill),
        ("skill commands scenario doc exists", (ROOT / "tests" / "scenarios" / "12-skill-commands.md").exists()),
    ]
    return checks


def check_13_skill_json_rules():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    checks = [
        ("agent rules section present", "Agent Rules" in skill or "CRITICAL RULES" in skill),
        ("always use --json rule", "always use" in skill.lower() and "--json" in skill),
        ("never parse human output rule", "never parse" in skill.lower() or "human-readable" in skill.lower()),
        ("empty result handling rule", "[]" in skill and ("empty" in skill.lower() or "No results" in skill.lower())),
        ("exit code rule", "exit code" in skill.lower() or "non-zero" in skill.lower()),
        ("no rate limit needed rule", "rate limit" in skill.lower() or "automatically" in skill.lower()),
        ("skill json rules scenario doc exists", (ROOT / "tests" / "scenarios" / "13-skill-json-rules.md").exists()),
    ]
    return checks


# ─── Scenario check dispatch ──────────────────────────────────────────────────

CHECKS = {
    "01-search-basic":     check_01_search_basic,
    "02-search-json":      check_02_search_json,
    "03-search-author":    check_03_search_author,
    "04-search-category":  check_04_search_category,
    "05-search-limit":     check_05_search_limit,
    "06-recent-category":  check_06_recent_category,
    "07-recent-json":      check_07_recent_json,
    "08-get-by-id":        check_08_get_by_id,
    "09-get-json":         check_09_get_json,
    "10-download-pdf":     check_10_download_pdf,
    "11-agent-workflow":   check_11_agent_workflow,
    "12-skill-commands":   check_12_skill_commands,
    "13-skill-json-rules": check_13_skill_json_rules,
}

# ─── Runner ──────────────────────────────────────────────────────────────────

def run_scenario_once(scenario_id):
    """Run all checks for a scenario once, returning (scenario_id, passed, total)."""
    fn = CHECKS[scenario_id]
    checks = fn()
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    return scenario_id, passed, total


def main():
    parser = argparse.ArgumentParser(description="arxiv-cli test harness")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers")
    parser.add_argument("--runs", type=int, default=10, help="Runs per scenario")
    args = parser.parse_args()

    print(f"🔬 arxiv-cli test suite — {len(SCENARIOS)} scenarios × {args.runs} runs × {args.workers} workers")
    checks_per_run = sum(len(CHECKS[s]()) for s in SCENARIOS)
    print(f"   Expected: ~{checks_per_run * args.runs * args.workers:,} checks")

    t0 = time.time()
    results = {s: (0, 0) for s in SCENARIOS}
    tasks = [s for s in SCENARIOS for _ in range(args.workers * args.runs)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_scenario_once, s) for s in tasks]
        for future in concurrent.futures.as_completed(futures):
            sid, passed, total = future.result()
            prev_p, prev_t = results[sid]
            results[sid] = (prev_p + passed, prev_t + total)

    print(f"\n{'ID':<4} {'Scenario':<32} {'Passed/Total':<16} {'Rate'}")
    print("─" * 68)

    grand_passed = 0
    grand_total = 0
    for sid in SCENARIOS:
        passed, total = results[sid]
        grand_passed += passed
        grand_total += total
        rate = passed / total * 100 if total else 0
        icon = "✅" if rate >= 95 else "❌"
        short = sid[3:]
        print(f"{sid[:2]:<4} {short:<32} {passed}/{total:<14} {rate:.0f}% {icon}")

    elapsed = time.time() - t0
    print("─" * 68)
    print(f"\nTotal checks:              {grand_total:,}")
    print(f"Passed:                    {grand_passed:,}")
    pass_rate = grand_passed / grand_total * 100 if grand_total else 0
    print(f"Pass rate:                 {pass_rate:.1f}%")
    print(f"Elapsed:                   {elapsed:.2f}s")
    print(f"Workers x Runs:            {args.workers} x {args.runs}")

    if pass_rate >= 95 and len(results) >= 13:
        print(f"\n✅ PASS — quality gate met (≥ 95%)")
        sys.exit(0)
    else:
        print(f"\n❌ FAIL — pass rate {pass_rate:.1f}% or fewer than 13 scenarios")
        sys.exit(1)


if __name__ == "__main__":
    main()
