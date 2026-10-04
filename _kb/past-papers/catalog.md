# Catalog of every question seen so far (official papers first)  ·  "KEY" = professor's solution is in the file

Legend – trust: **[OFFICIAL]** professor's paper/solution/slides · **[COURSE]** professor's tutorials/quizzes (no key) · **[STUDENT/AI]** written by you/AI; verify.

## A. Mid-Sem papers  [OFFICIAL]
### A1. 2024-25 Sem I Mid-Sem – `PoPL2024MidSem1.pdf` (paper p1–3, KEY p3–5); code also in `05_Code-Examples/AbstractClassModules/Module1.c, Module2.c`

| Q | Marks | Asks | KEY (short) | Cheat sheet |
|---|---|---|---|---|
| 1 | 10 | Will each module compile independently (`gcc -c`)? why/how | Yes; all type info needed is in the module; only implicit-prototype warnings; Module2 needs only "Class is a pointer" | 01 |
| 2 | 10 | `gcc Module1.c` alone an executable? both objects linked? | Alone: no (4 undefined: f, g, Subroutine1, Subroutine2). Together: yes | 01 |
| 3a/b | 5+5 | value of `ClassSize`, return of main (units!); one-sentence rule for needed spaces | `3*sizeof(void*)`; returns `sizeof(void*)`; space needed after identifier/constant unless followed by non-space delimiter | 02, 04 |
| 4 | 10 | which lines produce imperative code, module-wise | M1 13–28, 31–33; M2 3–6; declarations/static definitions give none | 02 |
| 5 | 10 | classify identifiers by binding time; which appear in assembly | table in 02 | 02 |
| 6 | 10 | effect of `return 0`→`return 1` in f,g | now: segfault at l.31 (Abstract uninitialised); after: if-blocks run, returns pointer size. ⚠ see 08 (#5) | 08 |
| 7 | 10 | max total stack frame from `f(n)` | `(n+1)*(sizeof(int)+3*sizeof(void*))` | 03 |

### A2. 2025-26 Sem I Mid-Sem (8 Oct 2025, 60 marks) – `midsem-solutions.pdf` = `02_Past-Papers/02_Past-Papers/midsem-solutions.pdf` (same content). Prof's example code in that folder: `class1.hpp`, `Module1.cpp`, `Module2.cpp`.

| Q | Marks | Asks | KEY |
|---|---|---|---|
| 1 | 3×5 | (i)–(v) independence of size, layout, member-function names/number, signatures, sequence – 1 line each | Yes, Yes, No, No, Yes (details in 01) |
| 2 | 3×10 | C++ `function(Class2)` call vs body: necessary/sufficient/harmful for 10 additions | 1 S · 2 S · 3 N+S · 4 H · 5 H · 6–10 irrelevant (if Class2 declaration kept) – verified, see 01 + `answers/verified-experiments.md` |
| 3 | 2+5+8 | your last assignment's list hierarchy: storage as base class or member? why? which is better for two-way flexibility? | **No key in the file.** Use 06 (contain-and-delegate; answer consistent with *your* code) |

## B. Compre papers  [OFFICIAL, out of mid-sem scope but same style]
### B1. Dec 2024 (80) – `PoPL Compre Solutions.pdf` (paper p1–2, KEY p3–5)
Q1 scope of 8 kinds of names (KEY: a3 b2 c2 d2 e4 f C6/J5 g C6/J7 h5) · Q2 precision-safe money arithmetic (fixed-point/rational; table i Mostly, ii Always, iii–v Mostly not) · Q3 method usable only by own-class instances (private + caveats; sample C++ in key) · Q4 call non-static method without instantiating (C++ null-pointer cast; others no) · Q5 read a lambda at run time (Python eval; Lisp etc. yes; C/C++/Java no) · Q6 per-instance specialisation (Lisp and Python only). → 05, 09
### B2. Dec 2025 (70) – `compre-answer-key.pdf` (paper p1–2, KEY p3–5)
Q1 paradigm+language per use-case (FMS/autopilot: Modular-OO C++/Fortran; diagnostics: Functional-OO any) · Q2 REPL vs event-loop vs your assignment (answer consistent with your submission; 5+2+5) · Q3 Python vs C quicksort in 5 respects · Q4 draw activation records of `fiboDP(5)` (⚠ key says 9 calls/17 frames; run gives 6 calls) → 07, 03

## C. Practice / question bank  [OFFICIAL question set, no key]  – `02_Past-Papers/PoPL-Question-Bank.md`
Q1 macro `Permute` + `Exchange` prototype: compiles? implicit-declaration warning? scope of a,b,c lexical/dynamic · Q2 each ASCII char a token – parser possible? · Q4 scope of struct member names · Q5 same member name in two structs? · Q6,7 same for C++/Java · Q8 Java objects, symbol table, same names · Q9 kinds of memory allocation in C and the compiler's role · Q10 Java vs C procedure activation records · Q11 allocation type of `scanf("%d",&n); int array[n];` → 05, 03, 08
*(My suggested answers live in 05; Q1: macro args are substituted textually at preprocessing time so `a,b,c` have no scope of their own (lexical); `Exchange` is declared before the macro is *used*, so no implicit-declaration warning provided the expansion occurs after the extern line; it compiles if `Print`/`Exchange` are declared and linked.)*
Q2 note (suggested): with one-character tokens a grammar would have to recognise identifiers/numbers/keywords through the parser itself (lexical structure folded into syntax) → huge ambiguity, no lookahead lexing (`<` vs `<=`, `int` vs `i`+`n`+`t`), much larger and slower grammar; possible in principle (scannerless parsing) but impractical.

## D. Quizzes / assignments  [COURSE]
* `Quiz 1 - Procedural to OO _ Corrected Quiz_ Attempt review.pdf` – (Sept 2024) 3 questions on two C++ modules without a common header: they compile independently and together, link, and print `10` (type independence between modules).
* `03_Quizzes-Assignments/IndependentModules/Quiz 1-1/1-2/1-3.pdf` (Last year's quiz) – compile+link `structure.c` with `newmain.c`, run 5 times, explain output (uninitialised `X`); then set `X.f = X.i`; then change `f`'s body. Files: `structure.c, main.c, newmain.c, compile.sh, Explanation.txt`.
* `OO Language Comparison Tut.pdf` – (1) headers declaring the same type differently, (2) `int a[11][3]; a[12][1]=1;` in C/C++/Java, (3–5) same class name in two Java packages / C++ without namespaces.
* `Quiz 2 - Post-Mid-Sem Quiz_ Attempt review.pdf` – Java `MyClass` features (reflection, deep/shallow copy), `CloneNotSupportedException`, occurrences formula (`4n` per key), tree class design.
* `Tutorial_1/2/3_Answers.md` [STUDENT/AI, compiled & tested]: T1 information hiding (opaque `FILE`), in-place/stable quicksort naming, Python stable quicksort, de-goto; T2 recursion on `main`, reverse argv, unpredictable mutual recursion, own `printf`, opaque type, assignment-free integer printing; T3 list-container class hierarchy.

## E. Likely exam themes for the 2026 Mid-Sem (slides cover "mostly till Procedure", PDF p1–125 + OOP in Java to p136)
Ranked by repetition in the past papers: (1) module compile/link independence (every year) · (2) procedure activation / stack frames · (3) binding times / names in assembly · (4) type size/layout, incomplete types · (5) OO design trade-off essay (base vs member; Fragile base class; Parnas) · (6) scope/lifetime tables · (7) paradigm debates (Dijkstra, Böhm–Jacopini). Practise by **writing your own two-module variants** and predicting `gcc -c / nm / link / run` before checking with gcc/nm.
