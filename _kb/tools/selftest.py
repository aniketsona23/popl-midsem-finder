#!/usr/bin/env python
"""Exam-day sanity check (offline).  python _kb/tools/selftest.py"""
import shutil, sqlite3, subprocess, sys
from pathlib import Path
KB = Path(__file__).resolve().parent.parent
ok = True
def check(name, cond, hint=""):
    global ok
    print(("PASS  " if cond else "FAIL  ") + name + ("" if cond else f"   -> {hint}"))
    ok &= bool(cond)
check("python >= 3.8", sys.version_info >= (3, 8))
try:
    c = sqlite3.connect(":memory:"); c.execute("create virtual table t using fts5(a)"); fts = True
except Exception: fts = False
check("sqlite FTS5 available", fts, "use the GUI (start.cmd) instead")
check("kb.db exists", (KB / "kb.db").exists(), "python _kb/build.py --no-ocr")
check("app.html exists", (KB / "app.html").exists(), "python _kb/build.py --no-ocr")
if (KB / "kb.db").exists():
    n = sqlite3.connect(KB / "kb.db").execute("select count(*) from chunk").fetchone()[0]
    check(f"index has chunks ({n})", n > 300)
    r = subprocess.run([sys.executable, str(KB / "search.py"), "binding", "time", "-n", "1"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    check("search.py returns a hit", "#1" in r.stdout, r.stderr[:200])
for tool in ("gcc", "g++", "nm", "javac", "java"):
    check(f"{tool} on PATH", shutil.which(tool) is not None, "needed only for the lab")
print("\nALL GOOD" if ok else "\nSome checks failed - see hints. the GUI needs only a browser.")
