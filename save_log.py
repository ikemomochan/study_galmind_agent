# save_log.py

import json
from datetime import datetime
import os

LOG_FILE = "conversation_log.json"

def save_conversation_log(question: str, answer: str):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer
    }

    # ファイルがなければ作成、あれば追記
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
