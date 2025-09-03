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

    # Look for any .cpp files without prefix number
    cpp_files = [f for f in os.listdir(".") if f.endswith(".cpp")]

    for f in cpp_files:
        # If already renamed, skip
        if any(f.startswith(f"{item['id']}.") for item in solved):
            continue

        # Assign next ID
        next_id = total + 1
        new_name = f"{next_id}. {f}"

        # Rename file
        os.rename(f, new_name)

        # Update metadata
        solved.append({
            "id": next_id,
            "filename": new_name,
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
        })
        total += 1
        print(f"Renamed {f} → {new_name}")

    # Save updated metadata
    meta["solved"] = solved
    meta["total_solved"] = total
    save_meta(meta)
    print(f"✅ Progress updated: {total} problems solved.")

if __name__ == "__main__":
    main()
