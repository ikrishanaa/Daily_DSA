import json

META_FILE = ".meta.json"
README_FILE = "README.md"

def load_meta():
    with open(META_FILE, "r") as f:
        return json.load(f)

def update_readme(meta):
    solved = meta.get("problems_solved", 0)
    day = meta.get("day_counter", 1)

    new_content = f"""# 📘 Daily DSA Journey  

<p align="center">
  <img src="https://img.shields.io/badge/Language-C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" />
  <img src="https://img.shields.io/badge/Progress-Day%20{day}-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/github/last-commit/ikrishanaa/Daily_DSA?style=for-the-badge&logo=github" />
  <img src="https://img.shields.io/badge/Problems%20Solved-{solved}-blue?logo=leetcode&style=for-the-badge" />
</p>

---

## ✨ About This Repository  

This repo tracks my **daily problem-solving journey in Data Structures & Algorithms (DSA)**.  
Each commit is a small step towards mastering problem-solving and building a solid foundation for **competitive programming & technical interviews**.  

- 🧑‍💻 Written in **C++**  
- 🔄 **Automatic file renaming** keeps everything neat  
- 📈 Consistent **daily progress tracking**  

---

## 📊 Stats  

- **Day:** {day}  
- **Problems Solved:** {solved}  

---

<p align="center">  
💡 Built with discipline, automation, and lots of debugging.  
</p>
"""
    with open(README_FILE, "w") as f:
        f.write(new_content)

def main():
    meta = load_meta()
    update_readme(meta)

if __name__ == "__main__":
    main()
