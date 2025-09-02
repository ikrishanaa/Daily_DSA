import os
import json
from datetime import datetime

META_FILE = ".meta.json"
README_FILE = "README.md"

def load_meta():
    if os.path.exists(META_FILE):
        with open(META_FILE, "r") as f:
            return json.load(f)
    return {"days": {}, "last_update": None}

def save_meta(meta):
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)

def update_readme(meta):
    today = datetime.now().strftime("%Y-%m-%d")
    day_number = len(meta["days"]) + 1

    # If already updated today → don't add duplicate
    if meta.get("last_update") == today:
        return False  

    # If no new problems today, still log "Daily Commit ✅"
    meta["days"][today] = {
        "day": day_number,
        "problems": ["Daily Commit ✅ (No new problem solved today)"]
    }
    meta["last_update"] = today
    save_meta(meta)

    # Generate README content dynamically
    lines = []
    lines.append("# 📘 Daily DSA Journey\n")
    lines.append("This repository tracks my **daily problem-solving journey in Data Structures & Algorithms (DSA)**.\n")
    lines.append("---\n")
    lines.append("## 📊 Progress Log\n")
    lines.append("| Day | Date | Problems Solved |\n")
    lines.append("|-----|------|-----------------|\n")

    for date, entry in sorted(meta["days"].items(), key=lambda x: x[1]["day"]):
        problems = ", ".join(entry["problems"])
        lines.append(f"| {entry['day']:03} | {date} | {problems} |\n")

    with open(README_FILE, "w") as f:
        f.writelines(lines)

    return True

if __name__ == "__main__":
    meta = load_meta()
    updated = update_readme(meta)
    if updated:
        print("✅ README updated with today's progress.")
    else:
        print("ℹ️ README already up to date for today.")
