# POPL (CS F301) Mid-Sem — Master Index

**Exam = open laptop, no internet.** Everything below works offline. Keep this file open in a tab.

## Open it

Double-click **`start.cmd`**. The POPL Finder opens in your browser (offline, nothing else to start). Type 2–3 words from the question, or pick the closest description.

## 1 · Which question is this? → where to look

| The question asks about… | Cheat sheet | Professor's slides (PDF page) | Past appearance |
|---|---|---|---|
| compile alone? link? executable? undefined / multiple definition? "independent"? | [01](_kb/topics/01-modules-linking-independence.md) | 54–56, 79–86 | 2024 Q1–2; 2025 Q1–2; Quiz 1; IndependentModules |
| binding time of identifiers; what shows in assembly; imperative code lines | [02](_kb/topics/02-binding-times-and-names.md) | 88, 97, 99, 125 | 2024 Q4–5 |
| stack frame / activation record / recursion depth / drawing frames | [03](_kb/topics/03-procedure-activation-stack-frames.md) | 99–125 | 2024 Q7; Compre 2025 Q4 |
| `sizeof`, struct layout, padding, pointers, incomplete types, "type = set of values" | [04](_kb/topics/04-types-sizeof-layout.md) | 69, 79–86 | 2024 Q3 |
| scope tables, lifetime, static/auto/heap, VLA, Java vs C frames | [05](_kb/topics/05-scope-lifetime-storage.md) | 60, 119–125 | Compre 2024 Q1; qbank |
| base class vs contain-and-delegate; abstract class; vtable; fragile base; Parnas | [06](_kb/topics/06-oo-design-java-cpp.md) | 71–86, 127–136 | 2025 Q3; Eval quiz |
| Dijkstra goto, Böhm–Jacopini, structured programming, paradigms, language choice | [07](_kb/topics/07-paradigms-and-debates.md) | 7–68 | Compre 2025 Q1–3 |
| implicit declaration, shadowing, void result, whitespace rule, traps | [08](_kb/topics/08-c-cpp-gotchas.md) | — | 2024 Q3b, Q6 |
| Lisp / CLOS / lambda / MOP | [09](_kb/topics/09-lisp-functional.md) | 138–148 | Compre 2024 Q5–6 |
| "How does this professor grade?" | [00](_kb/topics/00-exam-patterns.md) | — | all |
| Every old question + key in one place | [past-papers/catalog.md](_kb/past-papers/catalog.md) | — | — |
| Things I actually ran, with outputs | [answers/verified-experiments.md](_kb/answers/verified-experiments.md) | — | — |

## 2 · Slide deck map (`Slides_17Sept2026-TILL ENDSEM (HALF FOR MIDSEM - MOSTLY TILL PROCEDURE).pdf`)
PDF page ≠ printed "n/118" slide number (bullet build-ups repeat a slide over several PDF pages; e.g. PDF 81 = printed 66, PDF 119 = printed 95). Always cite/open the **PDF page**; the search tool prints both.

| PDF pages | Section |
|---|---|
| 1–6 | title, course content, ToC |
| 7–27 | Preliminaries: languages & abstraction levels, abstraction, programmability |
| 28–48 | Programming-language design: linguistics of programming, Dijkstra debate, pedagogy, paradigms ↔ models |
| 49–69 | **Imperative paradigm**: structured programming, **modular programming (54–56)**, control flow, Böhm–Jacopini, top-down/bottom-up, types as sets of values |
| 70–74 | Principles of imperative languages: what vs how, encapsulation, Parnas |
| 75–86 | **Procedural to OO**: encapsulation, simulation, partially hidden class (79–84), Objective-C, conclusion |
| 87–125 | **Procedure activation**: times of a program (88, 97), six features (99), euclid.c/.s (100–118), **stack frame (119–124)**, lessons (125) |
| 126–136 | OOP in Java: when / when not; Banana–Monkey–Jungle; exercises |
| 137–148 | Generics / MOP / CLOS / reflection |
| 149–152 | section list, references |

## 3 · Folder layout (organised; originals unchanged)

| Folder | Contents |
|---|---|
| `01_Slides/` | the lecture deck |
| `02_Past-Papers/` | Mid-Sem 2024 & 2025 (+ keys, + the professor's 2025 example code), Compre 2024 & 2025 keys, question bank |
| `03_Quizzes-Assignments/` | quizzes, practice assignment, OO tasks, language-comparison tutorial, mid-sem assignment |
| `04_Tutorials/` | Tutorial 1–3 answers (+ diagrams) |
| `05_Code-Examples/` | exam modules (`AbstractClassModules`), `IndependentModules`, lecture demos, Lisp files, GCD, `params`, `Dictionary` — **all explained in `Code-Examples-Explained.md`** |
| `06_Readings/` | the debates papers, Stroustrup chapter, Goodbye-OOP |
| `_kb/` | the search/GUI/lab machinery and my notes (generated) |
Undo the whole layout any time: `python _kb/tools/organize.py --undo`.

## 3b · Every resource, by trust level
**[OFFICIAL — professor]** (quote these)

| File | What |
|---|---|
| `PoPL2024MidSem1.pdf` | Mid-Sem 2024 paper **+ solution** (p3–5) |
| `midsem-solutions.pdf` ≡ `02_Past-Papers/02_Past-Papers/midsem-solutions.pdf` | Mid-Sem 2025 paper + solution (Q1, Q2; Q3 has no key) |
| `02_Past-Papers/An Example Program for Q2 (2025) Solution-20260922/{class1.hpp,Module1.cpp,Module2.cpp}` | professor's example for 2025 Q2 |
| `PoPL Compre Solutions.pdf` (Dec 2024), `compre-answer-key.pdf` (Dec 2025) | Compre papers + keys |
| `PoPL-Question-Bank.md` (questions + answers; replaced the two identical PDFs) | tutorial question bank (no key) |
| `Slides_17Sept2026-…pdf` | the lecture slides (152 PDF pages) |
| `05_Code-Examples/AbstractClassModules/Module1.c, Module2.c` | the 2024 exam modules |
| `05_Code-Examples/examplesOf23aug2024/`, `05_Code-Examples/ExampleOf26-27-Sept/`, `03_Quizzes-Assignments/IndependentModules/`, `05_Code-Examples/params/`, `05_Code-Examples/dynamicBindingJava/`, `Dictionary (2)/` | demo code from lectures/tutorials (dup folders de-duplicated in the index) |
| `Example Program GCD.pdf` (euclid.c), `05_Code-Examples/params/params.pdf` (assembly), `fghc.lisp`, `painting.lisp`, `mergesort-final.lisp` | example programs |
| `Bjarne Stroustrup On Abstract Classes.pdf` | Tour of C++ §4.3–4.5 |
| `06_Readings/Debates/*.pdf` | readings: Dijkstra, Böhm–Jacopini, Parnas, Nygaard, Naur, Kandel, Glass, Carlson, Du Works, Chatelier C++→ObjC |
**[GENERATED by us]** `_kb/` (index, notes, tools), `start.cmd`, `AGENTS.md`, `INDEX.md`, `RECOMMENDATIONS.md`, `EXAM-DAY.md`

## 4 · The ten sentences to have in your head
1. Compilation units are independent: *many declarations, one unique definition*.
2. Compiler needs size/layout only where objects are created, copied, passed by value or dereferenced; pointers to incomplete types need none.
3. The linker matches **names** (C: plain; C++: mangled with parameter types), never types, members or parameter names.
4. Undefined reference = declared, never defined; multiple definition = defined twice (even identically).
5. Binding times: preprocessing → compile (types, members, offsets) → linking (global/function names) → loading → **procedure activation** (params, locals, `this`) → run (values).
6. A call pushes an activation record (params, return address, saved BP, locals/temps); max stack = depth × frame size.
7. Class methods are functions with `this` as hidden first parameter.
8. Information hiding (Parnas): modules hide design decisions likely to change; interface = contract.
9. Contain-and-delegate gives two-way flexibility and avoids fragile base class / banana-monkey-jungle, at the price of boilerplate and no automatic substitutability.
10. Reason from first principles (compiler / linker / loader / run time), follow the answer format exactly, be brief.

## 5 · How the material is organised (for maintainers)
See [AGENTS.md](AGENTS.md) (rules for AI agents working here), [RECOMMENDATIONS.md](RECOMMENDATIONS.md) (what else to build), [EXAM-DAY.md](EXAM-DAY.md) (checklist), `_kb/README.md` (harness internals).
