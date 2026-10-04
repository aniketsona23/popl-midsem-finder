#!/usr/bin/env python
"""Insert the blank line markdown needs before a table (a table directly under a paragraph is NOT rendered as a table).
    python _kb/tools/fix_md_tables.py            # fixes my own notes in place, prints what changed
"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
FILES = [*ROOT.glob("*.md"), *(ROOT / "_kb").rglob("*.md"),
         ROOT / "02_Past-Papers/PoPL-Question-Bank.md", ROOT / "03_Quizzes-Assignments/OO-Language-Comparison-Tutorial.md",
         ROOT / "03_Quizzes-Assignments/IndependentModules/Quiz-1-Answers.md"]

def fix(text):
    out, prev, fence = [], "", False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        is_row = (not fence) and line.lstrip().startswith("|")
        prev_row = prev.lstrip().startswith("|")
        if is_row and not prev_row and prev.strip() != "":
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)

if __name__ == "__main__":
    n = 0
    for f in FILES:
        if f.exists() and "text" not in f.parts[-3:-1]:
            s = f.read_text(encoding="utf-8"); t = fix(s)
            if t != s:
                f.write_text(t, encoding="utf-8"); n += 1; print("fixed", f.relative_to(ROOT))
    print(n, "files changed")
