# This script is updated to handle the new naming convention:
# 01_day_01_problem.cpp, 02_day_01_problem.cpp, etc.
# The day counter only advances on the first commit of a new calendar day.

import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration ---
META_FILE = Path(".meta.json")
EXCLUDED_DIRS = {".git", ".github", "tools", "scripts"}
TARGET_EXTENSION = ".cpp"

def load_metadata():
    """Loads metadata from the .meta.json file, initializing if it doesn't exist or is corrupt."""
    if META_FILE.exists():
        with open(META_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Warning: .meta.json is corrupted. Starting fresh.")
    return {"solved": [], "problem_counter": 0, "day_counter": 0, "last_commit_date": ""}

def save_metadata(data):
    """Saves the updated metadata to the .meta.json file."""
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Metadata saved to {META_FILE}")

def sanitize_filename(name):
    """Cleans a filename by replacing spaces with underscores and removing special characters."""
    name = re.sub(r"[\s._-]+", "_", name)
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    return name.strip('_')

def main():
    """Finds, renames, and tracks new C++ files with the day-based naming convention."""
    print("🚀 Starting file renaming and tracking process...")
    
    meta = load_metadata()
    problem_counter = meta.get("problem_counter", 0)
    day_counter = meta.get("day_counter", 0)
    last_date_str = meta.get("last_commit_date", "")
    
    current_date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Find all new, un-renamed C++ files
    new_files_to_process = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for filename in sorted(files):
            if filename.endswith(TARGET_EXTENSION) and not re.match(r"^\d+_day_\d+.*\.cpp$", filename):
                new_files_to_process.append(Path(root) / filename)

    if not new_files_to_process:
        print("👍 No new C++ files to process.")
        return

    # If new files are found on a new calendar day, increment the day counter
    if current_date_str != last_date_str:
        day_counter += 1
        print(f"🎉 New day detected! Advancing to Day {day_counter:02d}.")

    # Process each new file found
    for current_path in new_files_to_process:
        problem_counter += 1
        sanitized_name = sanitize_filename(current_path.stem)
        
        # Create the new filename with the format: 01_day_01_xyz.cpp
        new_filename = f"{problem_counter:02d}_day_{day_counter:02d}_{sanitized_name}{TARGET_EXTENSION}"
        new_path = current_path.with_name(new_filename)
        
        os.rename(current_path, new_path)
        print(f"✅ Renamed: '{current_path.name}' -> '{new_path.name}'")
        
        # Update metadata list
        meta["solved"].append({
            "id": problem_counter,
            "filename": new_filename,
            "folder": str(current_path.parent),
            "date": current_date_str,
        })

    # Save the updated state back to the metadata file
    meta["problem_counter"] = problem_counter
    meta["day_counter"] = day_counter
    meta["last_commit_date"] = current_date_str
    save_metadata(meta)
    
    print(f"📈 Progress updated. Total problems solved: {problem_counter}")

if __name__ == "__main__":
    main()

