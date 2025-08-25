#!/usr/bin/env python3
import os, re, subprocess, datetime
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATEGORIES = ["arrays","strings","linked_list","stack","queue","hashing","two_pointers",
              "sliding_window","binary_search","bit_manip","math","recursion","tree",
              "graph","greedy","heap","dp","prefix_sum","intervals","matrix","misc"]

def list_solutions():
    counts = defaultdict(int)
    total = 0
    for cat in CATEGORIES:
        d = os.path.join(ROOT, cat)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.endswith((".cpp",".py",".java",".ts",".js",".go")):
                total += 1
                counts[cat] += 1
    return total, counts

def make_progress_bar(done, goal=200, width=30):
    done_slots = min(width, int((done/goal)*width))
    return f"[{'█'*done_slots}{'░'*(width-done_slots)}] {done}/{goal}"

def get_repo_dates():
    # commit dates (local tz of runner); we only need YYYY-MM-DD
    try:
        out = subprocess.check_output(
            ["git","log","--pretty=%cs"], cwd=ROOT, text=True
        ).strip().splitlines()
    except subprocess.CalledProcessError:
        return set()
    return set(out)

def current_streak(commit_dates: set):
    # count consecutive days ending today
    today = datetime.date.today()
    streak = 0
    d = today
    while d.strftime("%Y-%m-%d") in commit_dates:
        streak += 1
        d -= datetime.timedelta(days=1)
    return streak

def longest_streak(commit_dates: set):
    if not commit_dates:
        return 0
    days = sorted(datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in commit_dates)
    best = cur = 1
    for i in range(1,len(days)):
        if (days[i]-days[i-1]).days == 1:
            cur += 1
        else:
            best = max(best, cur)
            cur = 1
    return max(best, cur)

def render_table(counts):
    rows = []
    for cat in CATEGORIES:
        if counts.get(cat,0):
            rows.append(f"| `{cat}` | {counts[cat]} |")
    if not rows:
        rows = ["| _No categories yet_ | 0 |"]
    return "\n".join(["| Category | Solved |","|---|---|", *rows])

def update_readme(new_block):
    readme = os.path.join(ROOT, "README.md")
    with open(readme, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"(<!-- PROGRESS:START -->)(.*?)(<!-- PROGRESS:END -->)"
    repl = r"\1\n" + new_block + r"\n\3"
    new_content = re.sub(pattern, repl, content, flags=re.S)
    if new_content != content:
        with open(readme, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def main():
    total, counts = list_solutions()
    commit_dates = get_repo_dates()
    streak_now = current_streak(commit_dates)
    streak_best = longest_streak(commit_dates)

    block = []
    block.append("## 📈 Progress")
    block.append(f"- **Total solved:** {total}")
    block.append(f"- **Current streak:** {streak_now} days")
    block.append(f"- **Best streak:** {streak_best} days")
    block.append("")
    block.append(make_progress_bar(total, goal=200, width=34))
    block.append("")
    block.append("### By Category")
    block.append(render_table(counts))
    block.append("")
    block.append("_Last updated: " + datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC") + "_")

    changed = update_readme("\n".join(block))
    if changed:
        # commit back if README changed
        subprocess.run(["git","config","user.name","github-actions[bot]"], cwd=ROOT)
        subprocess.run(["git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT)
        subprocess.run(["git","add","README.md"], cwd=ROOT, check=False)
        subprocess.run(["git","commit","-m","chore: auto-update progress in README"], cwd=ROOT, check=False)
        subprocess.run(["git","push"], cwd=ROOT, check=False)

if __name__ == "__main__":
    main()
