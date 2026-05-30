"""Memory module — JSONL-based session memory for arxiv-cli."""
import json
import os
from datetime import datetime

_DEFAULT_PATH = os.path.join(
    os.path.expanduser("~"), ".copilot", "skills", "arxiv-cli", "data", "user-memory.jsonl"
)


def _get_path():
    return os.environ.get("ARXIV_CLI_MEMORY_PATH", _DEFAULT_PATH)


def load_memory():
    path = _get_path()
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def save_entry(entry_type, data):
    """Append a memory entry to the JSONL file."""
    path = _get_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": entry_type,
        **data,
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def record_search(query, result_count):
    save_entry("search", {"query": query, "result_count": result_count})


def record_download(paper_id, title, out_path):
    save_entry("download", {"paper_id": paper_id, "title": title, "out_path": out_path})
