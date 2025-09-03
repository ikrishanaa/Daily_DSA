import json
from datetime import datetime

META_FILE = ".meta.json"
README_FILE = "README.md"

HEADER = """# 📘 Daily DSA Journey  

<p align="center">
  <img src="https://img.shields.io/badge/Language-C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" />
  <img src="https://img.shields.io/badge/Progress-Ongoing🚀-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/github/last-commit/ikrishanaa/Daily_DSA?style=for-the-badge&logo=github" />
  <img src="https://img.shields.io/badge/Problems%20Solved-{count}-blue?logo=leetcode&style=for-the-badge" />
  <img src="https://komarev.com/ghpvc/?username=ikrishanaa&label=Profile%20Views&color=0e75b6&style=for-the-badge" />
</p>

---
"""

ABOUT = """## ✨ About This Repository  

This repository tracks my **daily problem-solving journey in Data Structures & Algorithms (DSA)**.  
Each commit is a small step towards mastering problem-solving and building a solid foundation for **competitive programming & technical interviews**.  

- 🧑‍💻 Written in **C++**  
- 🔄 **Automatic file renaming** keeps everything neat (`N. Problem_Name.cpp`)  
- 📈 Consistent **daily practice log**  

---
"""

PROGRESS_HEADER = """## 📊 Progress Tracking  

| # | Problem | Date Solved |
|---|----------|-------------|
"""

FOOTER = """
---

<p align="center">  
  💡 Built with discipline, automation, and lots of debugging.  
</p>
"""

def load_meta():
    try:
        with open(META_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"solved": [], "total_solved": 0}

def generate_readme(meta):
    solved = meta.get("solved", [])
    count = meta.get("total_solved", 0)

    # Replace {count} in header
    content = HEADER.replace("{count}", str(count))
    content += ABOUT
    content += PROGRESS_HEADER

    # Add rows for each problem
    for item in solved:
        content += f"| {item['id']} | {item['filename']} | {item['date']} |\n"

    content += FOOTER
    return content

def main():
    meta = load_meta()
    new_readme = generate_readme(meta)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print(f"✅ README.md updated with {meta['total_solved']} problems solved.")

if __name__ == "__main__":
    main()
