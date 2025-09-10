#!/usr/bin/env python3
"""
tools/rename_and_track.py

- Finds new .cpp files (any folder except .git, .github, tools)
- Renames them to: {problem_number}_day_{day_number:02d}_{slugified_original}.cpp
  e.g. 21_day_01_my_solution.cpp
- Updates .meta.json with new entries and counters
- Uses UTC date to decide whether to increment day_number (only once per new UTC day)
"""

from __future__ import annotations
import os
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil

ROOT = Path(".").resolve()
META_FILE = ROOT / ".meta.json"
EXCLUDE_DIRS = {".git", ".github", "tools", "__pycache__"}

# Regex to detect already-correctly-named files:
RENAMED_RE = re.compile(r"^\d+_day_\d{2}_.+\.cpp$")

def load_meta() -> dict:
    if META_FILE.exists():
        with META_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    # default meta
    return {
        "last_date": None,         # "YYYY-MM-DD" in UTC of last run that bumped day_number
        "day_number": 1,           # starts at 1
        "file_counter": 0,         # last used problem id
        "total_solved": 0,
        "solved": []
    }

def save_meta(meta: dict) -> None:
    with META_FILE.open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=4, sort_keys=False)

def slugify(name: str) -> str:
    """Create a safe slug for filenames (keep letters, numbers and underscores)."""
    # remove extension if present
    name = re.sub(r"\.cpp$", "", name, flags=re.IGNORECASE)
    # Remove any leading numeric prefixes like "10. " or "10 - "
    name = re.sub(r"^\s*\d+[\.\-\s]*", "", name)
    # Replace spaces and illegal chars with underscore
    name = re.sub(r"[^\w]+", "_", name)
    # Collapse multiple underscores
    name = re.sub(r"_+", "_", name)
    return name.strip("_") or "solution"

def iter_cpp_files(root: Path):
    """Yield Path objects for all .cpp files not in excluded dirs."""
    for p in root.rglob("*.cpp"):
        # skip files inside excluded directories
        parts = {part for part in p.parts}
        if parts & EXCLUDE_DIRS:
            continue
        # skip the tools scripts themselves
        if p.resolve() == (ROOT / "tools" / "rename_and_track.py").resolve():
            continue
        yield p

def already_renamed(p: Path) -> bool:
    return RENAMED_RE.match(p.name) is not None

def ensure_unique(path: Path) -> Path:
    """If path exists, append suffix _v2, _v3 ... to filename (before extension)."""
    if not path.exists():
        return path
    base = path.with_suffix("")  # remove .cpp
    ext = path.suffix
    i = 2
    while True:
        candidate = Path(f"{base}_v{i}{ext}")
        if not candidate.exists():
            return candidate
        i += 1

def main():
    meta = load_meta()

    # Current UTC date
    utc_today = datetime.now(timezone.utc).date().isoformat()

    # If last_date is not today's date, bump day_number by 1 and update last_date.
    last_date = meta.get("last_date")
    # If last_date is None (first run), we keep day_number as-is (default 1) and set last_date to today.
    if last_date != utc_today:
        # Only increment day_number if last_date exists (i.e., not the very first run).
        if last_date is not None:
            meta["day_number"] = int(meta.get("day_number", 1)) + 1
        # set/update last_date to today (so future runs today won't increment again)
        meta["last_date"] = utc_today

    day_number = int(meta.get("day_number", 1))
    file_counter = int(meta.get("file_counter", 0))
    total_solved = int(meta.get("total_solved", 0))
    solved = meta.get("solved", [])

    # Collect files that need renaming (sorted for deterministic behavior)
    candidates = []
    for p in iter_cpp_files(ROOT):
        # skip files that already follow naming convention
        if already_renamed(p):
            continue
        # also skip files that are inside tools folder or README generated—already handled by iter_cpp_files
        candidates.append(p)
    candidates.sort(key=lambda p: str(p).lower())

    if not candidates:
        print("No new .cpp files to rename.")
        # still save meta (we may have updated last_date / day_number)
        save_meta(meta)
        return

    for p in candidates:
        file_counter += 1
        total_solved += 1

        original_name = p.name
        slug = slugify(original_name)
        day_str = f"{day_number:02d}"
        new_name = f"{file_counter}_day_{day_str}_{slug}.cpp"

        # compute destination path: same folder as original
        dest = p.parent / new_name
        dest = ensure_unique(dest)

        # create parent just in case (should exist)
        dest.parent.mkdir(parents=True, exist_ok=True)

        # move/rename file
        try:
            shutil.move(str(p), str(dest))
            print(f"Renamed: {p} -> {dest}")
        except Exception as e:
            print(f"Failed to rename {p}: {e}")
            # continue to next file without incrementing counters further (we already incremented counters)
            continue

        # store relative folder like "./arrays" to match existing pattern (use posix style)
        folder_rel = os.path.relpath(dest.parent.as_posix(), start=ROOT.as_posix())
        if not folder_rel.startswith("."):
            folder_rel = f"./{folder_rel}"
        else:
            # relpath already returns '.', convert to './' to be consistent
            if folder_rel == ".":
                folder_rel = "./"

        solved_entry = {
            "id": file_counter,
            "filename": dest.name,
            "folder": folder_rel,
            "date": utc_today
        }
        solved.append(solved_entry)

    # Update meta and persist
    meta["file_counter"] = file_counter
    meta["total_solved"] = total_solved
    meta["solved"] = solved
    # day_number and last_date already set earlier
    meta["day_number"] = int(meta.get("day_number", day_number))
    save_meta(meta)
    print(f"✅ Renamed {len(candidates)} files. Total solved: {total_solved}. day_number: {meta['day_number']} last_date: {meta['last_date']}")

if __name__ == "__main__":
    main()
