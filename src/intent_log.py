# src/tools.py
import os
import json
from datetime import datetime
from pathlib import Path

INTENT_LOG = "logs/intent_log.json"


def log_intent(user_message, plan, answer=None):
    Path(INTENT_LOG).parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user_message": user_message,
        "plan": plan,
        "answer": answer,          # 👈 added
    }

    if os.path.exists(INTENT_LOG):
        with open(INTENT_LOG, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(entry)

    with open(INTENT_LOG, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

    print(f"🧾 Intent logged → {INTENT_LOG}")
    return INTENT_LOG
