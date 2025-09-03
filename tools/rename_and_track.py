import os
import json
import re
from datetime import datetime

META_FILE = ".meta.json"

def load_meta():
    if not os.path.exists(META_FILE):
        return {"day_counter": 1, "problems_solved": 0}
    with open(META_FILE, "r") as f:
        return json.load(f)

def save_meta(meta):
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=4)

def normalize_name(filename):
    # Remove spaces and special characters
    return re.sub(r'[^A-Za-z0-9_]', '_', filename)

def main():
    meta = load_meta()
    today = datetime.now().strftime("%Y-%m-%d")

    problems_added = 0
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".cpp") and not re.match(r"^\d+_day\d+_", file):
                problems_added += 1
                meta["problems_solved"] += 1
                file_num = str(meta["problems_solved"]).zfill(2)
                day_num = str(meta["day_counter"]).zfill(3)
                clean_name = normalize_name(file.replace(".cpp", ""))
                new_name = f"{file_num}_day{day_num}_{clean_name}.cpp"
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {file} → {new_name}")

    if problems_added > 0:
        save_meta(meta)

if __name__ == "__main__":
    main()
