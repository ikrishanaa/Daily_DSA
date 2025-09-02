import os
import json
import re
from datetime import datetime

META_FILE = ".meta.json"

def load_meta():
    if not os.path.exists(META_FILE):
        return {"file_count": 0, "current_day": 1, "last_date": ""}
    with open(META_FILE, "r") as f:
        return json.load(f)

def save_meta(meta):
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=4)

def format_filename(index, day, name):
    # Clean filename: replace spaces & symbols
    clean_name = re.sub(r'[^a-zA-Z0-9]+', '_', name).strip('_')
    return f"{index:02d}_day{day:03d}_{clean_name}.cpp"

def main():
    meta = load_meta()
    today = datetime.now().strftime("%Y-%m-%d")

    # Increment day if date changed
    if meta["last_date"] != today:
        meta["current_day"] += 1
        meta["last_date"] = today

    day = meta["current_day"]
    file_count = meta["file_count"]

    for folder in ["arrays", "dp", "graphs", "linked_list", "misc", "strings"]:
        if not os.path.exists(folder):
            continue

        for filename in os.listdir(folder):
            if filename.endswith(".cpp") and not filename.startswith(tuple("0123456789")):
                file_count += 1
                new_name = format_filename(file_count, day, filename.replace(".cpp", ""))
                src = os.path.join(folder, filename)
                dst = os.path.join(folder, new_name)
                os.rename(src, dst)
                print(f"Renamed: {filename} → {new_name}")

    meta["file_count"] = file_count
    save_meta(meta)

if __name__ == "__main__":
    main()
