import os
import re
import json
from datetime import datetime, timedelta

# Paths
REPO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(REPO_PATH, "README.md")
DATA_PATH = os.path.join(REPO_PATH, "tools", "progress.json")

CATEGORIES = ["arrays", "strings", "dp", "graphs", "linked_list"]

def count_solved_problems():
    total = 0
    category_counts = {}

    for category in CATEGORIES:
        folder = os.path.join(REPO_PATH, category)
        if not os.path.exists(folder):
            continue

        count = len([f for f in os.listdir(folder) if f.endswith(".cpp") or f.endswith(".py")])
        category_counts[category] = count
        total += count

    return total, category_counts

def load_progress():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return {"dates": [], "best_streak": 0}

def save_progress(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

def calculate_streak(dates):
    if not dates:
        return 0, 0

    # Convert strings to date objects
    dates = sorted(set(datetime.strptime(d, "%Y-%m-%d").date() for d in dates))

    best_streak = 0
    current_streak = 1
    temp_streak = 1

    for i in range(1, len(dates)):
        if dates[i] == dates[i-1] + timedelta(days=1):
            temp_streak += 1
        else:
            temp_streak = 1
        best_streak = max(best_streak, temp_streak)

    # Check if streak is ongoing today
    if dates[-1] == datetime.utcnow().date():
        current_streak = temp_streak
    else:
        current_streak = 0

    return current_streak, best_streak

def update_readme():
    total, category_counts = count_solved_problems()
    today = datetime.utcnow().date().strftime("%Y-%m-%d")

    # Load and update progress history
    data = load_progress()
    if total > 0:
        if not data["dates"] or data["dates"][-1] != today:
            data["dates"].append(today)
    current_streak, best_streak = calculate_streak(data["dates"])
    data["best_streak"] = max(data["best_streak"], best_streak)
    save_progress(data)

    # Read README
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 🔹 Update Problems Solved badge
    badge_pattern = r"(Problems%20Solved-)(\d+)"
    content = re.sub(badge_pattern, f"Problems%20Solved-{total}", content)

    # 🔹 Update progress section
    progress_start = "<!-- PROGRESS:START -->"
    progress_end = "<!-- PROGRESS:END -->"

    category_table = "| Category | Solved |\n|----------|--------|\n"
    for cat, count in category_counts.items():
        category_table += f"| `{cat}` | {count} |\n"

    progress_text = f"""
## 📈 Progress
- **Total solved:** {total}
- **Current streak:** {current_streak} days 🔥
- **Best streak:** {data['best_streak']} days 🏆
- **Last updated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

### By Category
{category_table}
"""

    new_content = re.sub(
        f"{progress_start}.*?{progress_end}",
        f"{progress_start}\n{progress_text}\n{progress_end}",
        content,
        flags=re.DOTALL,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme()
