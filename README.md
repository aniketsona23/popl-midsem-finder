# POPL (CS F301) exam finder

An offline search tool for the **Principles of Programming Languages** mid-sem (open laptop, no internet). Type 2–3 words from a question and it shows the right topic, the professor's slide pages, and the past-paper answers.

## Use it (nothing to install)
- **Windows:** double-click **`start.cmd`**.
- **Mac / Linux:** open **`_kb/app.html`** in Chrome or Edge.

It works offline. Keep the folders as they are: the page images, fonts and PDF links are found by relative path.

**On Windows,** if `git clone` says *Filename too long*, clone into a short folder such as `C:\popl`, or run `git config --global core.longpaths true` first. (You can also use the green **Code → Download ZIP** button.)

## What you get
- **Search box** — type words from the question (typos are fine). Results are grouped: *Start here* (a topic with a plain explanation and the short answer to write), *the professor's slides*, *past papers and answer keys*.
- **Topic pages** — "In plain words", "Short answer — what to write" (every line names its source and links to the page), "Same idea, different words" (the slides and the exam word things differently), and the full cheat sheet.
- **Answers and notes** — the question bank with answers, the quiz answers, the Dictionary example and all other code examples explained.

## What is in the folders
| Folder | Contents |
|---|---|
| `01_Slides` | lecture slides |
| `02_Past-Papers` | mid-sem and compre papers with keys, question bank |
| `03_Quizzes-Assignments` | quizzes and answers |
| `04_Tutorials` | tutorial answers |
| `05_Code-Examples` | lecture code, with `Code-Examples-Explained.md` |
| `06_Readings` | the debate papers |
| `_kb` | the app (`app.html`), cheat sheets (`topics/`), tools |

`INDEX.md` is the master index. Everything the app shows is also plain Markdown, so you can read it on GitHub.

## Rebuilding (optional)
Only needed if you add or change files. Needs Python 3 and `pip install pymupdf markdown pillow`:
```
python _kb/build.py --no-ocr
```
(Add `rapidocr-onnxruntime` and drop `--no-ocr` to read scanned PDFs.)

## Please note
- The course material (slides, papers, readings) belongs to its authors; it is shared here for study only. If you own something here and want it removed, open an issue.
- The "Short answer" lines are study aids written from the slides and answer keys. Check them against the slides before relying on them in the exam, and follow your exam rules about what you may use.
