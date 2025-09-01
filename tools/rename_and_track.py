#!/usr/bin/env python3
import os, sys, json, datetime, subprocess

META_FILE = ".meta.json"

def load_meta():
    if not os.path.exists(META_FILE):
        return {"last_day": str(datetime.date.today()), "current_day_count": 1, "file_counter": 0}
    with open(META_FILE, "r") as f:
        return json.load(f)

def save_meta(meta):
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)

def main():
    meta = load_meta()
    today = str(datetime.date.today())

    # Check if new day → increment streak day count
    if today != meta["last_day"]:
        meta["last_day"] = today
        meta["current_day_count"] += 1

    staged_files = subprocess.check_output(["git", "diff", "--cached", "--name-only"]).decode().splitlines()

    for fname in staged_files:
        if not fname.endswith(".cpp"):
            continue
        # Skip already renamed files
        if fname.startswith(tuple(str(i).zfill(2) for i in range(1, 200))):
            continue  

        meta["file_counter"] += 1
        new_name = f"{str(meta['file_counter']).zfill(2)}_day{str(meta['current_day_count']).zfill(3)}_" + fname.replace(" ", "_")

        os.rename(fname, new_name)
        subprocess.run(["git", "add", new_name])
        subprocess.run(["git", "reset", fname])  # remove old staged name

        print(f"Renamed: {fname} → {new_name}")

    save_meta(meta)

if __name__ == "__main__":
    main()
