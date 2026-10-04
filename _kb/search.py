#!/usr/bin/env python
"""Offline search over the POPL material.  Pure stdlib (sqlite3 FTS5) - works with no internet.

  python _kb/search.py binding time compile linking          # ranked chunks (AND, falls back to OR)
  python _kb/search.py -k solution,past-paper stack frame    # only some kinds
  python _kb/search.py -p 2024 module independence           # only paths containing '2024'
  python _kb/search.py --sub "extern void"                   # exact substring (trigram), good for code
  python _kb/search.py --re "sizeof\\s*\\(\\s*struct"            # regex over all chunk text
  python _kb/search.py -o 3                                   # print FULL text of result #3 of last search
  python _kb/search.py -v 3                                   # open result #3's PDF at that page in browser
  python _kb/search.py --kinds                                # list kinds + counts
  python _kb/search.py --cheat                                # list hand-written topic cheat sheets

Kinds: notes slides solution past-paper tutorial quiz assignment code reading other
Query words are stemmed (porter) and expanded with _kb/synonyms.json.
"""
import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KB = Path(__file__).resolve().parent
ROOT = KB.parent
DB = KB / "kb.db"
LAST = KB / ".last.json"
SYN = KB / "synonyms.json"

BOOST = {"notes": 1.4, "solution": 1.35, "past-paper": 1.3, "tutorial": 1.25, "slides": 1.15, "quiz": 1.1,
         "assignment": 1.0, "code": 0.95, "other": 0.9, "reading": 0.8}


def load_syn():
    if not SYN.exists():
        return {}
    raw = json.loads(SYN.read_text(encoding="utf-8"))
    syn = {}
    for group in raw.get("groups", []):  # each group is a set of mutually-equivalent terms
        for t in group:
            syn.setdefault(t.lower(), set()).update(x.lower() for x in group if x.lower() != t.lower())
    return syn


def terms_of(q):
    return re.findall(r"[A-Za-z0-9_]+", q)


def fts_term(t):
    t = t.lower()
    return f'"{t}"*' if len(t) >= 3 else f'"{t}"'


def group_expr(t, syn):
    alts = [fts_term(t)]
    for s in sorted(syn.get(t.lower(), ())):
        alts.append(" ".join(f'"{w}"' for w in terms_of(s)) if " " in s else fts_term(s))
    alts = [f"({a})" if " " in a else a for a in alts]
    return "(" + " OR ".join(alts) + ")" if len(alts) > 1 else alts[0]


def run_query(con, match, kinds, pathpat, limit):
    sql = (
        "SELECT c.id, c.path, c.loc, c.kind, c.ocr, c.also, bm25(fts) AS s, "
        "snippet(fts, 0, '[[', ']]', ' ... ', 36) AS snip "
        "FROM fts JOIN chunk c ON c.id = fts.rowid WHERE fts MATCH ? "
    )
    args = [match]
    if kinds:
        sql += "AND c.kind IN (%s) " % ",".join("?" * len(kinds))
        args += kinds
    if pathpat:
        sql += "AND lower(c.path) LIKE ? "
        args.append(f"%{pathpat.lower()}%")
    sql += "ORDER BY s LIMIT ?"
    args.append(limit * 6)
    rows = con.execute(sql, args).fetchall()
    rows = sorted(rows, key=lambda r: r[6] * BOOST.get(r[3], 1.0))  # bm25 is negative: more negative = better
    return rows


def slide_no(path, loc, body):
    if "slides_" not in path.lower():
        return ""
    m = re.search(r"(\d+)/118\s*$", body.strip())
    return f" (printed slide {m.group(1)}/118)" if m else ""


def show(rows, n, con):
    out = []
    seen = set()
    for r in rows:
        key = (r[1], r[2])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
        if len(out) >= n:
            break
    LAST.write_text(json.dumps([dict(id=r[0], path=r[1], loc=r[2]) for r in out]), encoding="utf-8")
    if not out:
        print("no hits. try: fewer words, --sub for exact text, --re for regex, or -k to widen kinds")
        return
    for i, r in enumerate(out, 1):
        cid, path, loc, kind, ocr, also, _s, snip = r
        body = con.execute("SELECT body FROM chunk WHERE id=?", (cid,)).fetchone()[0]
        flag = " [OCR]" if ocr else ""
        loc_h = f"PDF page {loc[1:]}" if loc.startswith("p") else f"lines {loc[1:]}"
        print(f"#{i}  [{kind}] {path}  -- {loc_h}{slide_no(path, loc, body)}{flag}")
        if also:
            print(f"     (same content also at: {also})")
        print("     " + re.sub(r"\s*\n\s*", " | ", snip).strip())
        print()
    print(f"-o N shows full text of result N;  -v N opens it in the browser at that page.")


def cmd_open(n, view):
    if not LAST.exists():
        sys.exit("run a search first")
    last = json.loads(LAST.read_text(encoding="utf-8"))
    if not 1 <= n <= len(last):
        sys.exit(f"result number must be 1..{len(last)}")
    r = last[n - 1]
    con = sqlite3.connect(DB)
    if view:
        import webbrowser

        url = (ROOT / r["path"]).as_uri()
        if r["loc"].startswith("p"):
            url += "#page=" + r["loc"][1:]
        print("opening", url)
        webbrowser.open(url)
        return
    body = con.execute("SELECT body FROM chunk WHERE id=?", (r["id"],)).fetchone()[0]
    print(f"===== {r['path']}  {r['loc']} =====\n{body}")


def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words", nargs="*")
    ap.add_argument("-k", "--kind", help="comma list of kinds")
    ap.add_argument("-p", "--path", help="only paths containing this text")
    ap.add_argument("-n", type=int, default=8, help="number of results (default 8)")
    ap.add_argument("--sub", action="store_true", help="exact substring search (trigram, >=3 chars)")
    ap.add_argument("--re", dest="regex", help="python regex over all chunk text")
    ap.add_argument("--or", dest="any_", action="store_true", help="match ANY word instead of ALL")
    ap.add_argument("--nosyn", action="store_true", help="disable synonym expansion")
    ap.add_argument("-o", "--open", type=int, metavar="N", help="print full text of result N of last search")
    ap.add_argument("-v", "--view", type=int, metavar="N", help="open result N in browser at its page")
    ap.add_argument("--kinds", action="store_true")
    ap.add_argument("--cheat", action="store_true", help="list topic cheat sheets")
    a = ap.parse_args()

    if a.cheat:
        for p in sorted((KB / "topics").glob("*.md")):
            first = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
            print(f"{p.relative_to(ROOT).as_posix():45} {first}")
        return
    if a.open:
        return cmd_open(a.open, False)
    if a.view:
        return cmd_open(a.view, True)

    con = sqlite3.connect(DB)
    if a.kinds:
        for k, n, files in con.execute("SELECT kind, count(*), count(DISTINCT path) FROM chunk GROUP BY kind ORDER BY 2 DESC"):
            print(f"{k:12} {n:5} chunks  {files:4} files")
        return
    if not a.words and not a.regex:
        ap.print_help()
        return
    kinds = [k.strip() for k in a.kind.split(",")] if a.kind else None
    q = " ".join(a.words)

    if a.regex:
        rx = re.compile(a.regex, re.I | re.S)
        rows = []
        for cid, path, loc, kind, ocr, also, body in con.execute("SELECT id,path,loc,kind,ocr,also,body FROM chunk"):
            if kinds and kind not in kinds:
                continue
            if a.path and a.path.lower() not in path.lower():
                continue
            m = rx.search(body)
            if m:
                s, e = max(0, m.start() - 80), min(len(body), m.end() + 80)
                rows.append((cid, path, loc, kind, ocr, also, -1.0, body[s:m.start()] + "[[" + m.group(0) + "]]" + body[m.end():e]))
        return show(rows, a.n, con)

    if a.sub:
        if len(q) < 3:
            sys.exit("--sub needs >= 3 characters")
        esc = q.replace('"', '""')
        hits = con.execute(
            "SELECT c.id,c.path,c.loc,c.kind,c.ocr,c.also,c.body FROM tri JOIN chunk c ON c.id=tri.rowid WHERE tri MATCH ?",
            (f'"{esc}"',),
        ).fetchall()
        rows = []
        for cid, path, loc, kind, ocr, also, body in hits:
            if (kinds and kind not in kinds) or (a.path and a.path.lower() not in path.lower()):
                continue
            i = body.lower().find(q.lower())
            i = max(i, 0)
            rows.append((cid, path, loc, kind, ocr, also, -BOOST.get(kind, 1.0),
                         body[max(0, i - 80):i] + "[[" + body[i:i + len(q)] + "]]" + body[i + len(q):i + len(q) + 120]))
        rows.sort(key=lambda r: r[6])
        return show(rows, a.n, con)

    ts = terms_of(q)
    if not ts:
        sys.exit("no searchable words")
    syn = {} if a.nosyn else load_syn()
    # multi-word synonym keys (e.g. 'stack frame') are matched on the whole query too
    groups = [group_expr(t, syn) for t in ts]
    and_q, or_q = " AND ".join(groups), " OR ".join(groups)
    rows = [] if a.any_ else run_query(con, and_q, kinds, a.path, a.n)
    if len({(r[1], r[2]) for r in rows}) < a.n:  # not enough strict hits -> widen with OR
        more = run_query(con, or_q, kinds, a.path, a.n)
        have = {r[0] for r in rows}
        rows += [r for r in more if r[0] not in have]
    show(rows, a.n, con)


if __name__ == "__main__":
    main()
