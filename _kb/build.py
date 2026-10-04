#!/usr/bin/env python
"""Build the offline search knowledge base for the POPL exam.

    python _kb/build.py            # extract (with OCR fallback) + index + html
    python _kb/build.py --reocr    # force re-extraction of every PDF
    python _kb/build.py --no-ocr   # skip OCR (fast; image-only pages stay empty)

Outputs (all inside _kb/):
    text/*.txt      one plain-text file per source, pages marked '=== PAGE n ==='
    kb.db           SQLite FTS5 index (used by search.py)
    app.html        the GUI (open by double-click start.cmd; no server, no internet)
    manifest.json   source list with kind/pages/chars/ocr info

Needs: PyMuPDF (fitz). OCR needs rapidocr-onnxruntime (only at build time, NOT at exam time).
"""
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KB = Path(__file__).resolve().parent
ROOT = KB.parent
TEXT = KB / "text"
DB = KB / "kb.db"
MANIFEST = KB / "manifest.json"

CODE_EXT = {".c", ".cpp", ".hpp", ".h", ".java", ".lisp", ".s", ".sh", ".m", ".py", ".bat"}
TEXT_EXT = {".md", ".txt"}
SKIP_DIRS = {"_kb", ".playwright-mcp", ".git", "__pycache__"}
MIN_PAGE_CHARS = 40  # fewer chars than this on a PDF page => try OCR


# --------------------------------------------------------------------------- classification
def classify(rel: str) -> str:
    """kind drives result filtering and ranking. Order matters."""
    r = re.sub(r"^\d\d_[^/]*/", "", rel.lower())  # ignore the numbered group folder name
    if rel.startswith("_kb/"):
        return "notes"
    if "slides_" in r:
        return "slides"
    if "comparison-tutorial" in r or "-explained" in r:
        return "tutorial"
    if r.startswith("params/") or "example program gcd" in r:
        return "code"
    if "explanation.txt" in r:
        return "tutorial"
    if "midsem" in r and ("solution" in r or "answer" in r):
        return "solution"
    if "compre" in r and ("solution" in r or "answer" in r or "key" in r):
        return "solution"
    if re.search(r"popl20\d\d|midsem1|midsem-assignment|compre", r) or "pre-midsem" in r or "qbank" in r or "question-bank" in r:
        return "past-paper"
    if "tutorial_" in r and r.endswith(".md"):
        return "tutorial"
    if "quiz" in r or "eval quiz" in r:
        return "quiz"
    if "asgn" in r or "assignment" in r or "tasks for" in r:
        return "assignment"
    if r.startswith("debates") or "stroustrup" in r or "goodbye" in r or "comparison" in r:
        return "reading"
    if r in {"index.md", "agents.md", "recommendations.md", "exam-day.md"}:
        return "notes"
    if Path(r).suffix in CODE_EXT:
        return "code"
    return "other"


# --------------------------------------------------------------------------- extraction
_ocr_engine = None


def ocr_engine():
    global _ocr_engine
    if _ocr_engine is None:
        from rapidocr_onnxruntime import RapidOCR

        _ocr_engine = RapidOCR()
    return _ocr_engine


def ocr_page(page) -> str:
    import numpy as np

    pix = page.get_pixmap(matrix=__import__("fitz").Matrix(2.5, 2.5), alpha=False)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    result, _ = ocr_engine()(img)
    if not result:
        return ""
    # result: [ [box, text, conf], ... ]; sort into reading order by y then x
    rows = sorted(result, key=lambda r: (round(r[0][0][1] / 18), r[0][0][0]))
    lines, cur_y, cur = [], None, []
    for box, txt, _conf in rows:
        y = round(box[0][1] / 18)
        if cur_y is not None and y != cur_y:
            lines.append(" ".join(cur))
            cur = []
        cur_y = y
        cur.append(txt)
    if cur:
        lines.append(" ".join(cur))
    return "\n".join(lines)


def extract_pdf(path: Path, use_ocr: bool):
    import fitz

    doc = fitz.open(path)
    pages, ocr_pages = [], []
    for i, page in enumerate(doc, 1):
        t = page.get_text("text").strip()
        if len(t) < MIN_PAGE_CHARS and use_ocr:
            try:
                o = ocr_page(page).strip()
            except Exception as e:  # noqa: BLE001
                print(f"    OCR failed p{i}: {e}")
                o = ""
            if len(o) > len(t):
                t = o
                ocr_pages.append(i)
        pages.append(t)
    return pages, ocr_pages


def svg_text(path: Path) -> str:
    s = path.read_text(encoding="utf-8", errors="replace")
    return "\n".join(re.sub(r"<[^>]+>", "", m).strip() for m in re.findall(r">([^<>]+)<", s) if m.strip())


def slugify(rel: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", rel.replace("\\", "/").replace("/", "__"))


def iter_sources():
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if rel.parts[0] == "_kb":  # index only my hand-written notes, never the generated stuff
            if not (len(rel.parts) > 2 and rel.parts[1] in {"topics", "answers", "past-papers"} and p.suffix == ".md"):
                continue
        elif set(rel.parts) & SKIP_DIRS:
            continue
        if p.suffix.lower() in {".pdf", ".svg"} | CODE_EXT | TEXT_EXT or p.name == "Makefile":
            yield p


def extract_all(use_ocr: bool, reocr: bool):
    TEXT.mkdir(exist_ok=True)
    manifest = []
    seen_hash = {}
    for p in iter_sources():
        rel = p.relative_to(ROOT).as_posix()
        ext = p.suffix.lower()
        out = TEXT / (slugify(rel) + ".txt")
        entry = {"path": rel, "kind": classify(rel), "txt": out.name, "ocr_pages": [], "dup_of": None}
        if ext == ".pdf":
            fresh = out.exists() and out.stat().st_mtime >= p.stat().st_mtime and not reocr
            if fresh:
                body = out.read_text(encoding="utf-8")
                pages = re.split(r"^=== PAGE \d+ ===\n", body, flags=re.M)[1:]
                m = re.search(r"^# ocr_pages: (.*)$", body, flags=re.M)
                entry["ocr_pages"] = [int(x) for x in m.group(1).split(",") if x.strip()] if m else []
            else:
                print(f"extract {rel}")
                pages, ocr_pages = extract_pdf(p, use_ocr)
                entry["ocr_pages"] = ocr_pages
                out.write_text(
                    f"# source: {rel}\n# ocr_pages: {','.join(map(str, ocr_pages))}\n"
                    + "".join(f"=== PAGE {i} ===\n{t}\n" for i, t in enumerate(pages, 1)),
                    encoding="utf-8",
                )
            entry["pages"] = len(pages)
            entry["chars"] = sum(len(t) for t in pages)
            h = hashlib.sha1(re.sub(r"\s+", "", "".join(pages)).encode()).hexdigest()
            if entry["chars"] > 200 and h in seen_hash:
                entry["dup_of"] = seen_hash[h]
            elif entry["chars"] > 200:
                seen_hash[h] = rel
        else:
            body = svg_text(p) if ext == ".svg" else p.read_text(encoding="utf-8", errors="replace")
            if ext == ".txt" and len(body) > 6000:  # bulky test-data dumps: keep only the head
                body = body[:2000] + "\n[... truncated bulk data file ...]"
            h = hashlib.sha1(re.sub(r"\s+", "", body).encode()).hexdigest()
            if h in seen_hash:
                entry["dup_of"] = seen_hash[h]
            else:
                seen_hash[h] = rel
                out.write_text(f"# source: {rel}\n" + body, encoding="utf-8")
            entry["pages"] = 1
            entry["chars"] = len(body)
        manifest.append(entry)
    MANIFEST.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    keep = {e["txt"] for e in manifest}
    for f in TEXT.glob("*.txt"):  # drop cached text of files that were moved, renamed or deleted
        if f.name not in keep:
            f.unlink()
    return manifest


# --------------------------------------------------------------------------- chunking
def chunks_for(entry):
    """yield (loc, text). loc is 'p12' for PDF pages, 'L1-80' for line windows."""
    txt = (TEXT / entry["txt"]).read_text(encoding="utf-8")
    txt = re.sub(r"^# source:.*\n", "", txt)
    txt = re.sub(r"^# ocr_pages:.*\n", "", txt, flags=re.M)
    if entry["path"].lower().endswith(".pdf"):
        parts = re.split(r"^=== PAGE (\d+) ===\n", txt, flags=re.M)
        pages = [(n, b.strip()) for n, b in zip(parts[1::2], parts[2::2])]
        for i, (n, body) in enumerate(pages):
            if not body:
                continue
            # slide decks repeat a page while bullets build up: keep only the final (fullest) build
            if entry["kind"] == "slides" and i + 1 < len(pages):
                nxt = pages[i + 1][1]
                if nxt.split("\n")[0] == body.split("\n")[0] and len(nxt) >= len(body):
                    continue
            yield f"p{n}", body
        return
    lines = txt.splitlines()
    ext = Path(entry["path"]).suffix.lower()
    if ext == ".md":  # split on headings so a hit lands on its section
        starts = [i for i, l in enumerate(lines) if re.match(r"#{1,3} ", l)] or [0]
        if starts[0] != 0:
            starts.insert(0, 0)
        for a, b in zip(starts, starts[1:] + [len(lines)]):
            seg = "\n".join(lines[a:b]).strip()
            for k in range(0, len(seg), 3500):  # keep chunks small
                if seg[k : k + 3500].strip():
                    yield f"L{a + 1}", seg[k : k + 3500]
        return
    W, S = 90, 70
    for a in range(0, max(len(lines), 1), S):
        seg = "\n".join(lines[a : a + W]).strip()
        if seg:
            yield f"L{a + 1}-{min(a + W, len(lines))}", seg
        if a + W >= len(lines):
            break


# --------------------------------------------------------------------------- index
def build_index(manifest):
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript(
        """
        CREATE TABLE chunk(id INTEGER PRIMARY KEY, path TEXT, loc TEXT, kind TEXT, ocr INTEGER, also TEXT, body TEXT);
        CREATE VIRTUAL TABLE fts USING fts5(body, path, content='chunk', content_rowid='id',
            tokenize="porter unicode61 remove_diacritics 2 tokenchars '_'");
        CREATE VIRTUAL TABLE tri USING fts5(body, content='chunk', content_rowid='id', tokenize='trigram');
        """
    )
    dups = {}
    for e in manifest:
        if e["dup_of"]:
            dups.setdefault(e["dup_of"], []).append(e["path"])
    n = 0
    for e in manifest:
        if e["dup_of"]:
            continue
        also = "; ".join(dups.get(e["path"], []))
        for loc, body in chunks_for(e):
            page = int(loc[1:]) if loc.startswith("p") else 0
            con.execute(
                "INSERT INTO chunk(path,loc,kind,ocr,also,body) VALUES(?,?,?,?,?,?)",
                (e["path"], loc, e["kind"], int(page in e["ocr_pages"]), also, body),
            )
            n += 1
    con.execute("INSERT INTO fts(rowid,body,path) SELECT id,body,path FROM chunk")
    con.execute("INSERT INTO tri(rowid,body) SELECT id,body FROM chunk")
    con.commit()
    con.execute("INSERT INTO fts(fts) VALUES('optimize')")
    con.commit()
    con.close()
    print(f"indexed {n} chunks from {sum(1 for e in manifest if not e['dup_of'])} sources -> {DB.name}")


# --------------------------------------------------------------------------- html
def build_html():
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT id,path,loc,kind,ocr,also,body FROM chunk ORDER BY id").fetchall()
    con.close()
    data = [dict(i=r[0], p=r[1], l=r[2], k=r[3], o=r[4], a=r[5], b=r[6]) for r in rows]
    syn_path = KB / "synonyms.json"
    syn = json.loads(syn_path.read_text(encoding="utf-8")) if syn_path.exists() else {}
    tpl = (KB / "search_template.html").read_text(encoding="utf-8")
    html = tpl.replace("/*__DATA__*/[]", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    html = html.replace("/*__SYN__*/{}", json.dumps(syn, ensure_ascii=False))
    HTML.write_text(html, encoding="utf-8")
    print(f"wrote {HTML.name} ({HTML.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    t0 = time.time()
    args = set(sys.argv[1:])
    man = extract_all(use_ocr="--no-ocr" not in args, reocr="--reocr" in args)
    build_index(man)
    if (KB / "app_template.html").exists():
        import build_app

        sys.argv = [sys.argv[0]] + (["--no-img"] if "--no-img" in args else [])
        build_app.main()
    print(f"done in {time.time() - t0:.1f}s")
