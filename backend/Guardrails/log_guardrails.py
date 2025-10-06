import os, json
from datetime import datetime

LOG_DIR = "backend/Reports/logs"
LOG_FILE = f"{LOG_DIR}/guardrail_log.json"

def log_guardrail_event(agent: str, issues: list):
    os.makedirs(LOG_DIR, exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "issues": issues,
    }
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r+", encoding="utf-8") as f:
            logs = json.load(f)
            logs.append(entry)
            f.seek(0)
            json.dump(logs, f, indent=2, ensure_ascii=False)
    else:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([entry], f, indent=2, ensure_ascii=False)
