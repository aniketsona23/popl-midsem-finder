#!/usr/bin/env python
"""Build the GUI: _kb/app.html (+ _kb/pages/*.webp page images).  Called automatically by build.py.

    python _kb/build_app.py            # render notes + (cached) page images + app.html
    python _kb/build_app.py --no-img   # skip page-image rendering

Needs: markdown, PyMuPDF, Pillow (build time only).  app.html itself needs only a browser.
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

import markdown
import sys as _s
_s.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent / "tools"))
from fix_md_tables import fix as fix_tables

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KB = Path(__file__).resolve().parent
ROOT = KB.parent
PAGES = KB / "pages"

NOTE_FILES = [  # (path relative to ROOT, group, label)
    ("INDEX.md", "Start", "Master index"),
    ("_kb/topics/00-exam-patterns.md", "Cheat sheets", "How the professor sets and marks"),
    ("_kb/topics/01-modules-linking-independence.md", "Cheat sheets", "Modules, linking, independence"),
    ("_kb/topics/02-binding-times-and-names.md", "Cheat sheets", "Binding times & names"),
    ("_kb/topics/03-procedure-activation-stack-frames.md", "Cheat sheets", "Activation records & stack"),
    ("_kb/topics/04-types-sizeof-layout.md", "Cheat sheets", "Types, sizeof, layout"),
    ("_kb/topics/05-scope-lifetime-storage.md", "Cheat sheets", "Scope, lifetime, storage"),
    ("_kb/topics/06-oo-design-java-cpp.md", "Cheat sheets", "OO design"),
    ("_kb/topics/07-paradigms-and-debates.md", "Cheat sheets", "Paradigms & debates"),
    ("_kb/topics/08-c-cpp-gotchas.md", "Cheat sheets", "C/C++ gotchas"),
    ("_kb/topics/09-lisp-functional.md", "Cheat sheets", "Lisp & functional"),
    ("_kb/past-papers/catalog.md", "Past papers", "Catalog of all past questions"),
    ("02_Past-Papers/PoPL-Question-Bank.md", "Past papers", "Question bank (with answers)"),
    ("03_Quizzes-Assignments/IndependentModules/Quiz-1-Answers.md", "Past papers", "Quiz 1-1/1-2/1-3 (with answers)"),
    ("05_Code-Examples/Code-Examples-Explained.md", "Past papers", "All code examples explained"),
    ("05_Code-Examples/Dictionary (2)/Dictionary-Explained.md", "Past papers", "Dictionary example explained"),
    ("03_Quizzes-Assignments/OO-Language-Comparison-Tutorial.md", "Past papers", "OO language comparison (with answers)"),
    ("_kb/answers/verified-experiments.md", "Past papers", "Experiments I ran"),
    ("_kb/answers/TEMPLATE.md", "Writing", "Answer template"),
    ("EXAM-DAY.md", "Writing", "Exam-day checklist"),
    ("RECOMMENDATIONS.md", "Meta", "Recommendations / what else"),
    ("04_Tutorials/Tutorial_1_Answers.md", "Tutorials", "Tutorial 1 (info hiding, quicksort, goto)"),
    ("04_Tutorials/Tutorial_2_Answers.md", "Tutorials", "Tutorial 2 (main recursion, printf, opaque type)"),
    ("04_Tutorials/Tutorial_3_Answers.md", "Tutorials", "Tutorial 3 (list class hierarchy)"),
]

CHOICES = [
    dict(t="Compile, link or run code", s="undefined reference · executable · independent modules · gcc -c", n="01-modules-linking-independence"),
    dict(t="Binding times and names", s="which time · what shows in the assembly · imperative lines", n="02-binding-times-and-names"),
    dict(t="Stack frames and recursion", s="activation record · stack size · draw the calls", n="03-procedure-activation-stack-frames"),
    dict(t="Types, sizes and scope", s="sizeof · struct layout · static, heap, stack · lexical scope", n="04-types-sizeof-layout"),
    dict(t="Class design and OO", s="inheritance or delegate · abstract class · fragile base", n="06-oo-design-java-cpp"),
    dict(t="Debates, paradigms, Lisp, C tricks", s="goto · paradigms · lambda · warnings and shadowing", n="07-paradigms-and-debates"),
]
WORDS = sorted("""activation address allocation assembly abstract abstraction binding bytes banana base block class compile compiler constructor contain
 declaration definition delegate delegation dijkstra dynamic encapsulation extern fragile frame function generic global goto heap hiding implicit imperative
 incomplete independent inheritance interface layout lexical linker linking loading local macro member method module mangling monkey object opaque overload
 paradigm parameter pointer polymorphism prototype recursion reference scope segfault shadowing signature sizeof stack static struct symbol template
 token type undefined variable virtual vtable""".split())




def make_refs(tag, docs, notes):
    """turn a source tag such as '2024 key A5' or 'slides p97' into a link target (or None)"""
    def doc(sub):
        return next((d["id"] for d in docs if sub in d["path"]), None)
    t = tag.strip()
    m = re.match(r"slides p(\d+)", t)
    if m and doc("Slides_"):
        return dict(l=t, d=doc("Slides_"), p=int(m.group(1)))
    m = re.match(r"(?:2024 )?(?:Mid-Sem )?key A(\d)", t) or re.match(r"2024 key A(\d)", t)
    if t.startswith("2024") and m and doc("PoPL2024MidSem1"):
        a = int(m.group(1)); return dict(l=t, d=doc("PoPL2024MidSem1"), p=3 if a <= 2 else (4 if a <= 6 else 5))
    if t.startswith("2024 Mid-Sem paper") and doc("PoPL2024MidSem1"):
        return dict(l=t, d=doc("PoPL2024MidSem1"), p=2)
    if t.startswith("2025 key") and doc("midsem-solutions"):
        return dict(l=t, d=doc("midsem-solutions"), p=3)
    if t.startswith("2025 Mid-Sem") and doc("midsem-solutions"):
        return dict(l=t, d=doc("midsem-solutions"), p=2 if "Q3" in t else 1)
    m = re.match(r"Compre 2024 key A(\d)", t)
    if m and doc("PoPL Compre Solutions"):
        a = int(m.group(1)); return dict(l=t, d=doc("PoPL Compre Solutions"), p=3 if a <= 3 else 5)
    if t.startswith("Compre 2025 key") and doc("compre-answer-key"):
        return dict(l=t, d=doc("compre-answer-key"), p=3)
    if t.startswith("Compre 2025 Q") and doc("compre-answer-key"):
        return dict(l=t, d=doc("compre-answer-key"), p=1)
    if t.startswith("report") and "Sorting_Report_Java" in notes:
        return dict(l=t, n="Sorting_Report_Java")
    if t.startswith("Quiz 2 answers") and "Quiz2_Answers" in notes:
        return dict(l=t, n="Quiz2_Answers")
    if t.startswith("question bank") and "PoPL-Question-Bank" in notes:
        return dict(l=t, n="PoPL-Question-Bank")
    if t.startswith("Goodbye OOP") and doc("Goodbye, Object Oriented"):
        return dict(l=t, d=doc("Goodbye, Object Oriented"), p=1)
    if t.startswith("Dijkstra 1968") and doc("Go To Statement Considered Harmful"):
        return dict(l=t, d=doc("Go To Statement Considered Harmful"), p=1)
    return dict(l=t)


def render_notes():
    notes = {}
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"], extension_configs={"toc": {"permalink": False}})
    slug_of = {Path(p).name: Path(p).stem for p, _, _ in NOTE_FILES}
    for rel, group, label in NOTE_FILES:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        say = []
        m_say = re.search(r"^## Short answer\s*\n(.*?)(?=^## |\Z)", text, flags=re.S | re.M)
        if m_say:
            for line in m_say.group(1).splitlines():
                if line.startswith("* "):
                    t = line[2:].strip()
                    m_src = re.search(r"\s*\*\[(.+?)\]\*\s*$", t)
                    say.append(dict(t=(t[:m_src.start()] if m_src else t), s=(m_src.group(1) if m_src else "")))
            text_for_html = text.replace(m_say.group(0), "")
        else:
            text_for_html = text
        words_txt = ""
        m_words = re.search(r"^## Same idea, different words\s*\n(.*?)(?=^## |\Z)", text_for_html, flags=re.S | re.M)
        if m_words:
            words_txt = m_words.group(1).strip()
            text_for_html = text_for_html.replace(m_words.group(0), "")
        plain_html = ""
        m_plain = re.search(r"^## In plain words\s*\n(.*?)(?=^## |\Z)", text_for_html, flags=re.S | re.M)
        if m_plain:
            md.reset()
            plain_html = md.convert(m_plain.group(1))
            text_for_html = text_for_html.replace(m_plain.group(0), "")
        md.reset()
        html = md.convert(fix_tables(text_for_html))
        toc = [(t["level"], t["id"], t["name"]) for t in md.toc_tokens for t in _flat(t)]
        base = "" if Path(rel).parent == Path(".") else ""

        def fix_href(m):
            href = m.group(1)
            if href.startswith(("http", "#", "mailto")):
                return m.group(0)
            name, _, frag = href.partition("#")
            if name.endswith(".md") and Path(name).name in slug_of:
                return f'href="#/note/{slug_of[Path(name).name]}"'
            return f'href="{_rel_to_kb(rel, name)}" target="_blank"'

        html = re.sub(r'href="([^"]+)"', fix_href, html)
        html = re.sub(r'src="(?!http|data:)([^"]+)"', lambda m: f'src="{_rel_to_kb(rel, m.group(1))}"', html)
        slides = []
        m = re.search(r"^Slides?:?\s*(.*)$", text, flags=re.M)
        if m:
            line = m.group(1).split("Files:")[0].split("Past")[0]
            for a, b in re.findall(r"p(\d+)(?:[–-](\d+))?", line):
                slides.append([int(a), int(b) if b else int(a)])
        notes[Path(rel).stem] = dict(words=words_txt, plain=plain_html, say=say, slug=Path(rel).stem, group=group, label=label, html=html, toc=toc, slides=slides, path=rel)
    return notes


def _flat(tok):
    yield tok
    for c in tok.get("children", []):
        yield from _flat(c)


def _rel_to_kb(note_rel, href):
    """href relative to the note's own folder -> url relative to _kb/app.html"""
    from urllib.parse import quote

    target = (ROOT / Path(note_rel).parent / href).resolve()
    try:
        rel = target.relative_to(ROOT).as_posix()
    except ValueError:
        return href
    return "../" + quote(rel)


def render_images(docs, enabled):
    if not enabled:
        return
    import shutil
    ids = {d["id"] for d in docs}
    if PAGES.exists():
        for d in PAGES.iterdir():  # drop page images of documents that no longer exist
            if d.is_dir() and d.name not in ids:
                shutil.rmtree(d, ignore_errors=True)
    import fitz
    from PIL import Image

    for d in docs:
        out = PAGES / d["id"]
        out.mkdir(parents=True, exist_ok=True)
        pdf = ROOT / d["path"]
        todo = [n for n in range(1, d["pages"] + 1) if not (out / f"{n}.webp").exists() or (out / f"{n}.webp").stat().st_mtime < pdf.stat().st_mtime]
        if not todo:
            continue
        print(f"  rendering {len(todo)} pages of {d['path']}")
        doc = fitz.open(pdf)
        for n in todo:
            page = doc[n - 1]
            w = page.rect.width
            target = 1150 if page.rect.width > page.rect.height else 900
            pix = page.get_pixmap(matrix=fitz.Matrix(target / w, target / w), alpha=False)
            Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(out / f"{n}.webp", "WEBP", quality=72, method=4)


def main():
    no_img = "--no-img" in sys.argv
    manifest = json.loads((KB / "manifest.json").read_text(encoding="utf-8"))
    docs = []
    for e in manifest:
        if e["path"].lower().endswith(".pdf") and not e["dup_of"] and e.get("pages"):
            docs.append(dict(id=re.sub(r"[^A-Za-z0-9]+", "_", e["path"])[:60].strip("_") + f"_{len(docs)}", path=e["path"], kind=e["kind"], pages=e["pages"]))
    render_images(docs, not no_img)
    notes = render_notes()
    con = sqlite3.connect(KB / "kb.db")
    data = [dict(p=r[0], l=r[1], k=r[2], o=r[3], a=r[4], b=r[5]) for r in con.execute("SELECT path,loc,kind,ocr,also,body FROM chunk ORDER BY id")]
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    for d in data:  # readable HTML for every markdown section (tables stay tables)
        if d["p"].lower().endswith(".md"):
            md.reset()
            d["h"] = re.sub(r"<h[1-6]>.*?</h[1-6]>", "", md.convert(fix_tables(d["b"])), count=1, flags=re.S)  # the title is shown separately
            d["h"] = re.sub(r'href="(?:[^"#]*/)?([\w-]+)\.md"', lambda m: f'href="#/note/{m.group(1)}"' if m.group(1) in notes else m.group(0), d["h"])
    for d in data:  # the "Short answer" section of a cheat sheet is searched first
        if re.match(r"##\s+(Short answer|In plain words|Same idea, different words)", d["b"]):
            d["s"] = 1
    for n in notes.values():  # make every source tag a link where we know the page
        for it in n.get("say", []):
            it["refs"] = [make_refs(tag, docs, notes) for tag in re.split(r";\s*", it["s"]) if tag.strip()]
    syn = json.loads((KB / "synonyms.json").read_text(encoding="utf-8"))
    slides = next((d["id"] for d in docs if "Slides_" in d["path"]), "")
    tpl = (KB / "app_template.html").read_text(encoding="utf-8")

    def j(x):
        return json.dumps(x, ensure_ascii=False).replace("</", "<\/")

    html = (tpl.replace("/*__DATA__*/[]", j(data)).replace("/*__SYN__*/{}", j(syn)).replace("/*__NOTES__*/{}", j(notes))
            .replace("/*__DOCS__*/[]", j(docs)).replace("/*__CHOICES__*/[]", j(CHOICES))
            .replace("/*__WORDS__*/[]", j(WORDS)).replace('/*__SLIDES__*/""', j(slides)))
    (KB / "app.html").write_text(html, encoding="utf-8")
    size = sum(f.stat().st_size for f in PAGES.rglob("*.webp")) / 1e6 if PAGES.exists() else 0
    print(f"wrote app.html ({(KB / 'app.html').stat().st_size // 1024} KB), {len(notes)} notes, {len(docs)} PDFs, page images {size:.0f} MB")


if __name__ == "__main__":
    main()
