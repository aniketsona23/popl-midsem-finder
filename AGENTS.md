# AGENTS.md — rules for AI agents (Claude Code, Codex, Copilot, local LLMs) working in this folder

## Mission
Help the human prepare for / sit the **CS F301 Principles of Programming Languages** mid-sem (open laptop, **no internet**). Two modes:
1. **Prep mode** (internet on): improve the knowledge base, cheat sheets, tools; verify claims by running code.
2. **Exam mode** (offline): locate the professor's own material fast, run experiments on code from the question, and help *draft* answers in the professor's style. The human decides and submits. Follow the exam's rules — if the paper or invigilator forbids AI assistance, do not assist during the exam itself.

## Working agreement
* Keep answers short, answer first, and cite the source page for every course-specific claim.
* The exam question is on paper: the user types 2-3 keywords; design for typing, not pasting.

## Ground rules
* **Never modify, move or delete original course files** (PDFs, `.c/.cpp/.java/.lisp`, the `Tutorial_*` files, etc.). Generated/own material lives only in: `INDEX.md`, `AGENTS.md`, `RECOMMENDATIONS.md`, `EXAM-DAY.md`, `start.cmd`, and `_kb/`.
* **Cite sources** for every course-specific claim: file + PDF page (or line range). Distinguish `[OFFICIAL]` (professor's papers/keys/slides) from `[STUDENT/AI]` (`Tutorial_*_Answers.md`, `POPL Eval Quiz.pdf`, `Review_ASGN1…md`). If official and student material disagree, the official one wins; say so.
* **Verify before asserting** anything about compiler/linker/run-time behaviour: run it with gcc/g++/nm directly. This laptop's gcc is **MinGW 32-bit** (pointer = 4 bytes, `_` prefixed symbols, segfault = exit code 3221225477); the professor's answers assume Linux x86-64. Prefer *symbolic* sizes (`3*sizeof(void*)`).
* **Text extraction of PDFs loses table columns and tick marks.** For any table/diagram answer key, render the page (`python _kb/tools/pdfpage.py <pdf> <page>`) and look at the image before relying on it (the 2025 Q2 key was mis-read from text once).
* Some pages are OCR'd (`[OCR]` flag in search output): numbers and punctuation may be wrong — confirm on the page image.
* **Match the professor's grading style** (see `_kb/topics/00-exam-patterns.md`): first-principles reasoning (compiler vs linker vs loader vs run time), exact answer format, brevity ("1 line each", "≤ 2 sentences"), no appeals to standards as authority, consistency with the student's own submission for assignment questions. Don't hunt syntax errors in the exam code.
* Don't invent course content. If the material has no answer (e.g. 2025 Q3 has no key), say "no official key" and give a reasoned answer labelled as such.

## Workflow for answering an exam question (do these in order)
1. **Classify** with the table in `INDEX.md §1` → open the matching `_kb/topics/NN-*.md`.
2. **Route** the whole question: `python _kb/ask.py -f q.txt`; then **search** the professor's wording: `python _kb/search.py <keywords>` (add `-k solution,past-paper,slides`; `--sub` for exact code text; `--re` for regex; `-o N` full text; `-v N` open PDF at the page). Try 2–3 phrasings; synonyms are built in (`_kb/synonyms.json`).
3. **If code is given**: write it to files (keep the exam's line numbers!), then `gcc -c -Wall`, `nm`, `gcc` (link) and run; for recursion use `_kb/tools/trace_template.c`; for sizes use the probe in `topics/04`.
4. **Draft** in `_kb/answers/qN.md` using `_kb/answers/TEMPLATE.md` (verdict → reason → evidence → exceptions). Match the paper's format instruction verbatim.
5. **Self-check**: every sub-part answered, units given, no contradictions (e.g. "necessary yet harmful"), line numbers per module, claims verified.
6. Report to the human: the answer, the evidence, the source pointers, and any uncertainty (especially machine-dependent behaviour).

## Repository map
```
INDEX.md  AGENTS.md  RECOMMENDATIONS.md  EXAM-DAY.md      human + agent entry points
start.cmd                                                   opens the GUI (_kb/app.html) in the browser
_kb/
  build.py            extract PDFs (PyMuPDF; OCR fallback via rapidocr at build time) → text/ → kb.db (SQLite FTS5) → app.html
  ask.py              paste a full question → grouped best hits (cheat sheets, slides, past papers, tutorials, code)
  search.py           CLI search (porter stemming, synonyms, bm25 + source-kind boosts, --sub trigram, --re regex)
  app.html            THE GUI (calm design; embedded index, JS BM25, page images, rendered notes) — works from file://
  app_template.html   source of the GUI; build_app.py fills it
  synonyms.json       equivalence groups used by CLI and UI
  manifest.json       every indexed source: kind, pages, chars, OCR pages, duplicate-of
  text/               extracted plain text, one file per source, pages marked "=== PAGE n ==="
  topics/             hand-written cheat sheets 00–09 (indexed as kind "notes")
  past-papers/catalog.md   every past question + key pointers
  answers/            TEMPLATE.md, verified-experiments.md, your drafts qN.md
  tools/              trace_template.c · pdfpage.py · selftest.py · fix_md_tables.py · organize.py
```
Source kinds: `notes slides solution past-paper tutorial quiz assignment code reading other`. Ranking boosts: notes 1.4, solution 1.35, past-paper 1.3, tutorial 1.25, slides 1.15 …

## Maintenance commands (prep mode)
```
python _kb/build.py            # incremental: re-extract only changed PDFs, rebuild index + html (≈2 s when nothing changed)
python _kb/build.py --reocr    # force full re-extraction incl. OCR (≈5 min)
python _kb/build.py --no-ocr   # skip OCR (offline machine without rapidocr)
python _kb/tools/selftest.py   # sanity check
```
After editing any note/synonym/PDF: re-run `build.py`, then spot-check with 3 searches. Add new resources anywhere under this folder (not `_kb/`); `build.py` finds them automatically; add a classification rule in `build.py:classify()` if the filename deserves a specific kind.

## Environment notes
Windows 11, Git-Bash/PowerShell/cmd. Python 3.10 (stdlib `sqlite3` has FTS5), PyMuPDF, gcc/g++/nm/objdump/gdb (MinGW 6.3 32-bit), JDK. No `clisp/sbcl`, no `tesseract`, no `rg`. Everything the exam-time tools need is Python-stdlib + gcc; the browser UI needs nothing but a browser.
