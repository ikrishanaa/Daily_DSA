# This is the fully rewritten and improved script for renaming files and tracking progress.
# It's more robust, uses modern libraries, and provides clearer output.

import os
import json
import re
from datetime import datetime
from pathlib import Path

# --- Configuration ---
# The file to store metadata about solved problems.
META_FILE = Path(".meta.json")
# Directories to exclude from the file search.
EXCLUDED_DIRS = {".git", ".github", "tools", "scripts"}
# File extension to look for.
TARGET_EXTENSION = ".cpp"

def load_metadata():
    """Loads the metadata from the .meta.json file."""
    if META_FILE.exists():
        with open(META_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Warning: .meta.json is corrupted. Starting fresh.")
                return {}
    return {}

def save_metadata(data):
    """Saves the updated metadata to the .meta.json file."""
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Metadata saved to {META_FILE}")

def sanitize_filename(name):
    """
    Cleans up a filename by replacing spaces and special characters with underscores,
    and removes any existing numeric prefixes like "1.", "01.", etc.
    """
    # Remove existing numbering like "1. ", "02_"", etc.
    name = re.sub(r"^\d+[\s._-]*", "", name)
    # Replace spaces and common separators with a single underscore
    name = re.sub(r"[\s._-]+", "_", name)
    # Remove any other non-alphanumeric characters (except underscores)
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    return name

def main():
    """
    Main function to find, rename, and track new C++ files.
    """
    print("🚀 Starting file renaming and tracking process...")
    
    # Load existing metadata or initialize it.
    meta = load_metadata()
    solved_list = meta.get("solved", [])
    total_solved = meta.get("total_solved", 0)
    
    # Create a set of already processed filenames for quick lookup.
    processed_filenames = {Path(item["folder"]) / item["filename"] for item in solved_list}
    
    new_files_found = 0
    
    # Walk through the current directory.
    for root, dirs, files in os.walk("."):
        # Modify the list of directories in-place to prevent os.walk from descending into them.
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for filename in files:
            if not filename.endswith(TARGET_EXTENSION):
                continue

            current_path = Path(root) / filename
            
            # Check if the file looks like it has already been renamed by our script.
            # This regex checks for a pattern like "1. file.cpp" or "123. file.cpp".
            if re.match(r"^\d+\.\s.*", filename):
                continue
                
            print(f"🔍 Found new file: {current_path}")
            new_files_found += 1
            total_solved += 1
            
            # Sanitize the base name of the file (without extension).
            sanitized_name = sanitize_filename(current_path.stem)
            
            # Create the new filename with a numeric prefix.
            new_filename = f"{total_solved}. {sanitized_name}{TARGET_EXTENSION}"
            new_path = current_path.with_name(new_filename)
            
            # Rename the file.
            os.rename(current_path, new_path)
            print(f"✅ Renamed: '{current_path.name}' -> '{new_path.name}'")
            
            # Add the new file's information to our tracking list.
            solved_list.append({
                "id": total_solved,
                "filename": new_filename,
                "folder": str(Path(root)),
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
            })

    if new_files_found == 0:
        print("👍 No new C++ files to process.")
    else:
        # Update the metadata dictionary and save it to the file.
        meta["solved"] = solved_list
        meta["total_solved"] = total_solved
        save_metadata(meta)
        print(f"📈 Progress updated. Total problems solved: {total_solved}")

if __name__ == "__main__":
    main()
