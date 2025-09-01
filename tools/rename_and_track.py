#!/usr/bin/env python3
import os, json, datetime, subprocess, re

META_FILE = ".meta.json"

def load_meta():
    if not os.path.exists(META_FILE):
        return {"last_day": str(datetime.date.today()), "current_day_count": 1, "file_counter": 0}
    with open(META_FILE, "r") as f:
        return json.load(f)

def save_meta(meta):
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)

def get_all_cpp_files():
    files = []
    for root, _, fnames in os.walk("."):
        for fname in fnames:
            if fname.endswith(".cpp") and not fname.startswith("."):
                files.append(os.path.join(root, fname))
    return files

def already_renamed(fname):
    # Matches 01_day008_filename.cpp
    return bool(re.match(r"^\d{2}_day\d{3}_", os.path.basename(fname)))

def main():
    meta = load_meta()
    today = str(datetime.date.today())

    # Check if new day → increment streak day count
    if today != meta["last_day"]:
        meta["last_day"] = today
        meta["current_day_count"] += 1

    changed = False
    all_cpp = get_all_cpp_files()

    for fname in all_cpp:
        if already_renamed(fname):
            continue

        meta["file_counter"] += 1
        base = os.path.basename(fname).replace(" ", "_")
        new_name = f"{str(meta['file_counter']).zfill(2)}_day{str(meta['current_day_count']).zfill(3)}_{base}"

        new_path = os.path.join(os.path.dirname(fname), new_name)
        os.rename(fname, new_path)

        print(f"Renamed: {fname} → {new_path}")
        changed = True

    save_meta(meta)

    if changed:
        # Stage files if inside a Git repo (local hook or GitHub Action)
        try:
            subprocess.run(["git", "add", "."], check=False)
        except Exception:
            pass

if __name__ == "__main__":
    main()
