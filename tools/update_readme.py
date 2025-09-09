#!/usr/bin/env python3
"""
tools/update_readme.py

- Reads .meta.json
- Updates the Problems Solved badge URL in README.md:
  https://img.shields.io/badge/Problems%20Solved-[COUNT]-blue?logo=leetcode&style=for-the-badge
- Replaces content between <!-- PROGRESS_START --> and <!-- PROGRESS_END --> with
  a generated progress table that contains clickable, relative links to files.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict

ROOT = Path(".").resolve()
META_FILE = ROOT / ".meta.json"
README_FILE = ROOT / "README.md"
START_MARKER = "<!-- PROGRESS_START -->"
END_MARKER = "<!-- PROGRESS_END -->"

def load_meta() -> dict:
    if META_FILE.exists():
        with META_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"solved": [], "total_solved": 0}

def build_badge_markdown(count: int) -> str:
    url = f"https://img.shields.io/badge/Problems%20Solved-{count}-blue?logo=leetcode&style=for-the-badge"
    return f'<img src="{url}" alt="Problems Solved"/>'

def normalize_folder(folder: str) -> str:
    # Input meta stores folder like "./arrays" or "./"
    if not folder:
        return "."
    folder = str(folder)
    if folder.startswith("./"):
        folder = folder[2:]
    if folder == "":
        folder = "."
    return folder

def generate_table(solved: List[Dict]) -> str:
    count = len(solved)
    header = f"## 📊 Progress Tracking ({count} problems solved)\n\n"
    header += "| # | Problem | Date Solved |\n"
    header += "|---:|---|:---:|\n"

    # Sort solved by id (ascending)
    solved_sorted = sorted(solved, key=lambda s: int(s.get("id", 0)))

    rows = []
    for item in solved_sorted:
        fid = item.get("id", "")
        fname = item.get("filename", "")
        folder = normalize_folder(item.get("folder", ""))
        date = item.get("date", "")
        # build relative link - if folder is ".", link directly to filename
        if folder == ".":
            link = f"./{fname}"
        else:
            link = f"./{folder}/{fname}"
        # ensure link has no double slashes
        link = link.replace("//", "/")
        rows.append(f"| {fid} | [{fname}]({link}) | {date} |")

    body = "\n".join(rows) + "\n"
    return header + body

def replace_progress_section(readme_text: str, new_table: str) -> str:
    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        # Append markers at end
        return readme_text.rstrip() + f"\n\n{START_MARKER}\n{new_table}\n{END_MARKER}\n"

    before, rest = readme_text.split(START_MARKER, 1)
    _, after = rest.split(END_MARKER, 1)
    return f"{before}{START_MARKER}\n{new_table}{END_MARKER}{after}"

def replace_badge(readme_text: str, new_badge_html: str) -> str:
    """
    Find the 'Problems Solved' badge, which might exist in different forms.
    We'll replace any <img ... alt="Problems Solved"...> or markdown image that contains 'Problems' and 'Solved'.
    """
    import re
    # replace HTML img with alt Problems Solved
    pattern_html = re.compile(r'<img[^>]+alt=["\']?Problems\s+Solved["\']?[^>]*>', flags=re.IGNORECASE)
    if pattern_html.search(readme_text):
        readme_text = pattern_html.sub(new_badge_html, readme_text)
        return readme_text

    # replace markdown image like ![Problems Solved](url)
    pattern_md = re.compile(r'!\[[^\]]*Problems[^\]]*Solved[^\]]*\]\([^\)]*\)', flags=re.IGNORECASE)
    if pattern_md.search(readme_text):
        readme_text = pattern_md.sub(new_badge_html, readme_text)
        return readme_text

    # fallback: try to locate a badges block and append our badge at the top
    return readme_text.replace("\n\n", f"\n\n{new_badge_html}\n\n", 1)

def main():
    meta = load_meta()
    solved = meta.get("solved", [])
    total = int(meta.get("total_solved", len(solved)))

    # Build badge and table
    badge_html = build_badge_markdown(total)
    table_md = generate_table(solved)

    # Load README
    if not README_FILE.exists():
        print("README.md not found, creating a minimal README with progress section.")
        readme_text = "# Daily DSA Journey\n\n"
    else:
        readme_text = README_FILE.read_text(encoding="utf-8")

    # Replace badge
    readme_text = replace_badge(readme_text, badge_html)

    # Replace progress section
    readme_text = replace_progress_section(readme_text, table_md)

    # Write back
    README_FILE.write_text(readme_text, encoding="utf-8")
    print(f"✅ README.md updated with {total} problems solved and {len(solved)} entries.")

if __name__ == "__main__":
    main()
