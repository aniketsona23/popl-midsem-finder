#!/usr/bin/env python
"""Paste a WHOLE exam question; get where to look.   (offline, stdlib only)

    python _kb/ask.py "Will each module compile independently (gcc -c)? Justify why not, how each is processed"
    python _kb/ask.py -f question.txt          # question saved in a file (best for long text with code)
    clipboard -> file:  in PowerShell:  Get-Clipboard | Set-Content q.txt -Encoding utf8

It drops filler words, weights rare words, searches with OR + bm25 and prints, per source kind:
the best cheat-sheet sections, slides, past questions/keys, tutorials and code examples.
Use search.py afterwards to drill into one hit (-o N).
"""
import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KB = Path(__file__).resolve().parent
sys.path.insert(0, str(KB))
import search as S  # noqa: E402

STOP = set("""a an the of to in on at for from by with without and or not no is are was were be been being this that these those it its as if then than
so such into over under again further once only own same too very can will just should now what which who whom why how all any both each few more most other some
do does did done have has had having would could may might must shall we you your they them their he she his her our us i me my there here
explain justify answer question marks mark following given suppose consider whether yes also give write state show using use used via per etc eg ie one two three
will""".split())
GROUPS = [("notes", 3, "CHEAT SHEETS / my notes"), ("slides", 4, "PROFESSOR'S SLIDES (open the PDF page)"),
          ("solution,past-paper", 4, "PAST PAPERS & KEYS (closest earlier questions)"),
          ("tutorial,quiz,assignment", 3, "TUTORIALS / QUIZZES"), ("code", 3, "CODE EXAMPLES")]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text", nargs="*")
    ap.add_argument("-f", "--file")
    ap.add_argument("-n", type=int, default=0, help="override results per group")
    a = ap.parse_args()
    q = Path(a.file).read_text(encoding="utf-8", errors="replace") if a.file else " ".join(a.text)
    if not q.strip():
        ap.print_help()
        return
    words = [w for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]+", q) if len(w) > 2 and w.lower() not in STOP]
    seen, uniq = set(), []
    for w in words:
        if w.lower() not in seen:
            seen.add(w.lower())
            uniq.append(w)
    # keep the 14 rarest-looking terms: prefer longer words and ones that exist in the index
    con = sqlite3.connect(S.DB)
    def df(w):
        try:
            return con.execute("SELECT count(*) FROM fts WHERE fts MATCH ?", (S.fts_term(w),)).fetchone()[0]
        except sqlite3.Error:
            return 0
    scored = sorted(((df(w), w) for w in uniq), key=lambda t: (t[0] == 0, t[0]))
    terms = [w for d, w in scored if d > 0][:14]
    if not terms:
        sys.exit("no usable terms found in the question")
    print("key terms:", ", ".join(terms), "\n")
    syn = S.load_syn()
    match = " OR ".join(S.group_expr(t, syn) for t in terms)
    best, num = {}, 0
    for kinds, n, title in GROUPS:
        ks = kinds.split(",")
        rows = S.run_query(con, match, ks, None, 10)
        out, seen_loc = [], set()
        for r in rows:
            k = (r[1], r[2])
            if k in seen_loc:
                continue
            seen_loc.add(k)
            out.append(r)
            if len(out) >= (a.n or n):
                break
        print("=" * 6, title)
        if not out:
            print("  (nothing)")
        for r in out:
            cid, path, loc, kind, ocr, also, _s, snip = r
            body = con.execute("SELECT body FROM chunk WHERE id=?", (cid,)).fetchone()[0]
            num += 1
            where = f"p{loc[1:]}" if loc.startswith("p") else f"lines {loc[1:]}"
            print(f"  #{num} [{kind}] {path} {where}{S.slide_no(path, loc, body)}")
            print("      " + re.sub(r"\s*\n\s*", " | ", snip).strip()[:230])
        print()
        best[title] = [dict(id=r[0], path=r[1], loc=r[2]) for r in out]
    flat = [x for v in best.values() for x in v]
    S.LAST.write_text(json.dumps(flat), encoding="utf-8")
    print("tip: results are numbered 1..N in the order printed; `search.py -o N` shows full text, `-v N` opens the PDF page.")


if __name__ == "__main__":
    main()
