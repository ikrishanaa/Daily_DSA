# This is the fully rewritten and improved script for updating the README.md file.
# It reliably replaces the progress section using markers.

import json
from pathlib import Path

# --- Configuration ---
# The file where metadata is stored.
META_FILE = Path(".meta.json")
# The main README file to be updated.
README_FILE = Path("README.md")
# Markers to identify the auto-generated progress section in the README.
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
    total_solved = metadata.get("total_solved", 0)

    if not solved_list:
        return f"### 📊 Progress Tracking (0 problems solved)\n\nNo problems solved yet. Keep going!\n"

    # Sort problems by ID to ensure consistent order.
    solved_list.sort(key=lambda x: x["id"])

    # Table header
    header = f"### 📊 Progress Tracking ({total_solved} problems solved)\n\n"
    table = "| # | Problem | Date Solved |\n"
    table += "|---|---------|-------------|\n"

    # Table rows
    for item in solved_list:
        # Create a relative path for the link in the table.
        file_path = Path(item['folder']) / item['filename']
        # Ensure the link is formatted correctly for Markdown.
        link = f"[{item['filename']}]({file_path.as_posix()})"
        table += f"| {item['id']} | {link} | {item['date']} |\n"
        
    return header + table

def main():
    """
    Main function to update the README with the latest progress.
    """
    print("🚀 Starting README update process...")
    
    metadata = load_metadata()
    if not metadata:
        print("Aborting README update due to missing or invalid metadata.")
        return

    # Ensure the README file exists.
    if not README_FILE.exists():
        print(f"Warning: '{README_FILE}' not found. Creating it.")
        README_FILE.touch()

    # Read the current content of the README file.
    with open(README_FILE, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Generate the new progress table in Markdown format.
    progress_table = generate_progress_table(metadata)
    
    # Construct the full block to be inserted, including markers.
    new_progress_section = f"{START_MARKER}\n\n{progress_table}\n{END_MARKER}"

    # Check if the markers already exist in the README.
    if START_MARKER in readme_content and END_MARKER in readme_content:
        # If they do, replace the content between them.
        before_marker = readme_content.split(START_MARKER)[0]
        after_marker = readme_content.split(END_MARKER)[1]
        new_content = before_marker + new_progress_section + after_marker
    else:
        # If they don't, append the new section to the end of the file.
        print("Markers not found in README. Appending progress to the end.")
        new_content = readme_content.strip() + "\n\n" + new_progress_section

    # Write the updated content back to the README file.
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ README.md updated successfully with {metadata.get('total_solved', 0)} problems.")

if __name__ == "__main__":
    main()
