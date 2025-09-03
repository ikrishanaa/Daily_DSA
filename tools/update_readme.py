import json
from datetime import datetime

META_FILE = ".meta.json"
README_FILE = "README.md"

START_MARKER = "<!-- PROGRESS_START -->"
END_MARKER = "<!-- PROGRESS_END -->"

def load_meta():
    try:
        with open(META_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"solved": [], "total_solved": 0}

def generate_progress_table(meta):
    solved = meta.get("solved", [])
    count = meta.get("total_solved", 0)

    table = f"### 📊 Progress Tracking ({count} problems solved)\n\n"
    table += "| # | Problem | Date Solved |\n"
    table += "|---|----------|-------------|\n"

    for item in solved:
        table += f"| {item['id']} | {item['filename']} | {item['date']} |\n"

    return table

def main():
    meta = load_meta()
    progress_table = generate_progress_table(meta)

    # Load current README
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # If markers don’t exist, add them once
    if START_MARKER not in content or END_MARKER not in content:
        content += f"\n\n{START_MARKER}\n{progress_table}\n{END_MARKER}\n"
    else:
        # Replace only the section between markers
        before = content.split(START_MARKER)[0]
        after = content.split(END_MARKER)[1]
        content = f"{before}{START_MARKER}\n{progress_table}\n{END_MARKER}{after}"

    # Save updated README
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ README.md updated with {meta['total_solved']} problems solved.")

if __name__ == "__main__":
    main()
