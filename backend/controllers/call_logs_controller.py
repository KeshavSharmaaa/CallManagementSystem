import os
import json

CALL_LOGS_DIR = "/uploads/results"

def get_call_logs():
    logs = []

    for file in os.listdir(CALL_LOGS_DIR):
        if file.endswith(".json"):
            with open(os.path.join(CALL_LOGS_DIR, file), "r", encoding="utf-8") as f:
                logs.append(json.load(f))

    return logs