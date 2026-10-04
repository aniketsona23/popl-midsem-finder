# _kb — harness internals

Pipeline: `build.py` → (PyMuPDF text; pages with < 40 chars get OCR via rapidocr at **build time only**) → `text/*.txt` → `kb.db` (SQLite FTS5: `fts` = porter-stemmed words incl. `_`; `tri` = trigram for exact substrings) → `app.html` (all chunks embedded; JS BM25).

* **Chunking:** PDFs = one chunk per page (slide build-up pages that are strict prefixes of the next page are dropped); Markdown = per heading (≤ 3500 chars); code = 90-line windows with 20-line overlap. Identical content (by whitespace-insensitive SHA-1) is indexed once and listed as "same content also at …".
* **Kinds** come from `classify()` in `build.py` (path rules). **Ranking** = bm25 × kind boost (`BOOST` in `search.py` and `search_template.html` — keep in sync).
* **Synonyms**: `synonyms.json` groups (single words). CLI reads it live; the HTML embeds it at build time.
* **Files indexed from `_kb/`:** only `topics/`, `answers/`, `past-papers/` markdown (kind `notes`).
* `.last.json` remembers the last result list for `search.py -o N / -v N`.

Troubleshooting

| Symptom | Fix |
|---|---|
| `kb.db` missing / stale | `python _kb/build.py --no-ocr` (uses cached `text/`) |
| New PDF not found | put it anywhere outside `_kb/`, run `build.py` |
| OCR wanted but `rapidocr` missing | `pip install rapidocr-onnxruntime` (needs internet) |
| `search.py` says FTS5 unavailable | use the GUI (`start.cmd`, pure JS) |
| Unicode errors in console | `chcp 65001` or `set PYTHONIOENCODING=utf-8` |
| HTML opens but links to PDFs fail | links are relative (`../file.pdf#page=N`); keep `app.html` inside `_kb/` |
