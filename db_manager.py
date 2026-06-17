# db_manager.py
import json
import os
from filelock import FileLock

def load_user_data(username: str):
    filename = f"user_{username.lower()}.json"
    lock = FileLock(f"{filename}.lock")
    with lock:
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                    data["bets"] = {int(k): v for k, v in data.get("bets", {}).items()}
                    data["processed_payouts"] = [int(x) for x in data.get("processed_payouts", [])]
                    if "parlays" not in data: data["parlays"] = []
                    if "favorite_country" not in data: data["favorite_country"] = ""
                    if "fun_bets" not in data: data["fun_bets"] = {}
                    return data
            except: pass
        return {"password": "", "balance": 1000.0, "bets": {}, "processed_payouts": [], "parlays": [], "favorite_country": "", "fun_bets": {}}

def save_user_data(username: str, data: dict):
    filename = f"user_{username.lower()}.json"
    lock = FileLock(f"{filename}.lock")
    with lock:
        with open(filename, "w") as f: json.dump(data, f)