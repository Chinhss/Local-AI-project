import json
from pathlib import Path

DATA_DIR = Path.home() / ".son"
HISTORY_FILE = DATA_DIR / "history.json"

def load_history() -> list:
    if not HISTORY_FILE.exists():
        return []

    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

def save_history(messages: list) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(messages, indent=2), encoding="utf-8")