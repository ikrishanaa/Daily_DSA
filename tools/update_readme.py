import json

META_FILE = ".meta.json"
README_FILE = "README.md"

def load_meta():
    with open(META_FILE, "r") as f:
        return json.load(f)

def update_readme():
    meta = load_meta()
    problems_solved = meta.get("file_count", 0)

    with open(README_FILE, "r") as f:
        content = f.read()

    # Replace Problems Solved badge
    new_content = re.sub(
        r"Problems%20Solved-[^-]+-blue",
        f"Problems%20Solved-{problems_solved}-blue",
        content
    )

    with open(README_FILE, "w") as f:
        f.write(new_content)

    print(f"Updated README with {problems_solved} problems solved.")

if __name__ == "__main__":
    update_readme()
