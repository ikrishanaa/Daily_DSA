import os
import json
from datetime import datetime

# Metadata file
META_FILE = ".meta.json"

def load_meta():
    if os.path.exists(META_FILE):
        with open(META_FILE, "r") as f:
            return json.load(f)
    return {"solved": [], "total_solved": 0}

def save_meta(data):
    with open(META_FILE, "w") as f:
        json.dump(data, f, indent=4)

def main():
    meta = load_meta()
    solved = meta.get("solved", [])
    total = meta.get("total_solved", 0)

    # Walk through all subfolders
    for root, _, files in os.walk("."):
        # Skip hidden dirs like .git and tools
        if root.startswith("./.git") or root.startswith("./tools") or root.startswith("./.github"):
            continue

        for f in files:
            if not f.endswith(".cpp"):
                continue

            old_path = os.path.join(root, f)

            # Skip if already renamed (starts with "<number>. ")
            if f.split()[0].rstrip(".").isdigit():
                continue

            # Assign next ID
            next_id = total + 1
            new_name = f"{next_id}. {f}"
            new_path = os.path.join(root, new_name)

            # Rename file
            os.rename(old_path, new_path)

            # Update metadata
            solved.append({
                "id": next_id,
                "filename": new_name,
                "folder": root,
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
            })
            total += 1
            print(f"Renamed {old_path} → {new_path}")

    # Save updated metadata
    meta["solved"] = solved
    meta["total_solved"] = total
    save_meta(meta)
    print(f"✅ Progress updated: {total} problems solved.")

if __name__ == "__main__":
    main()
