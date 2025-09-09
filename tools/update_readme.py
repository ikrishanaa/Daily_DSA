# This script is updated to dynamically change the number in the
# "Problems Solved" badge in addition to updating the progress table.

import json
import re
from pathlib import Path

# --- Configuration ---
META_FILE = Path(".meta.json")
README_FILE = Path("README.md")
START_MARKER = "<!-- PROGRESS_START -->"
END_MARKER = "<!-- PROGRESS_END -->"

def load_metadata():
    """Loads metadata, returns an empty dict if file not found or invalid."""
    if not META_FILE.exists():
        print(f"Error: Metadata file '{META_FILE}' not found.")
        return {}
    with open(META_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{META_FILE}'.")
            return {}

def generate_progress_table(metadata):
    """Generates a Markdown table from the solved problems metadata."""
    solved_list = metadata.get("solved", [])
    total_solved = metadata.get("problem_counter", 0)

    if not solved_list:
        return f"## 📊 Progress Tracking (0 problems solved)\n\nNo problems solved yet. Keep going!\n"

    solved_list.sort(key=lambda x: x["id"])
    header = f"## 📊 Progress Tracking ({total_solved} problems solved)\n\n"
    table = "| # | Problem | Date Solved |\n"
    table += "|---|---|---|\n"

    for item in solved_list:
        file_path = Path(item['folder']) / item['filename']
        link = f"[{item['filename']}]({file_path.as_posix()})"
        table += f"| {item['id']} | {link} | {item['date']} |\n"
        
    return header + table

def main():
    """Updates the README with the latest progress table and solved count badge."""
    print("🚀 Starting README update process...")
    
    metadata = load_metadata()
    if not metadata:
        print("Aborting README update due to missing or invalid metadata.")
        return

    if not README_FILE.exists():
        print(f"Error: '{README_FILE}' not found. Cannot update.")
        return

    with open(README_FILE, "r", encoding="utf-8") as f:
        readme_content = f.read()

    total_solved = metadata.get("problem_counter", 0)
    
    # Update the "Problems Solved" badge count using regex
    badge_pattern = r"(img.shields.io/badge/Problems%20Solved-)\d+(-blue\?logo=leetcode&style=for-the-badge)"
    new_badge_url = rf"\g<1>{total_solved}\g<2>"
    readme_content = re.sub(badge_pattern, new_badge_url, readme_content)
    
    progress_table = generate_progress_table(metadata)
    new_progress_section = f"{START_MARKER}\n\n{progress_table}\n{END_MARKER}"

    if START_MARKER in readme_content and END_MARKER in readme_content:
        before_marker = readme_content.split(START_MARKER)[0]
        after_marker = readme_content.split(END_MARKER)[1]
        new_content = before_marker + new_progress_section + after_marker
    else:
        new_content = readme_content.strip() + "\n\n" + new_progress_section

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ README.md updated successfully with {total_solved} problems.")

if __name__ == "__main__":
    main()

