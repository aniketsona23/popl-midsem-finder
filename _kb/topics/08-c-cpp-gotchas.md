# C / C++ / Java gotchas that this professor builds questions from

## In plain words

C lets you write things that look fine but are wrong: calling a function you never declared (only a warning), reading a variable you never set (you get leftover garbage), or using the result of a function that returns nothing. The exam code is full of these on purpose.

**Example.** `int x; printf("%d", x);` prints whatever number happened to be left in that memory. It is not 0, and it can change from run to run.


## Short answer

* Do not hunt syntax errors; the questions are about types, modules and procedure activation. *[2024 Mid-Sem paper note]*
* Implicit declaration is only a warning in C; the linker then needs the real definition. *[2024 key A1]*
* Using the result of a void function is undefined. Say what changes by semantics, not only what one machine printed. *[2024 key A6; my gcc test]*


## Things the 2024 paper exploited (all verified with gcc on this laptop; see `_kb/answers/verified-experiments.md`)
1. **Implicit declaration** – calling `f(10)` with no prior prototype: compiles with a *warning* (`-Wimplicit-function-declaration`); C assumes `int f()`. Module1 compiled alone is fine; the *linker* later needs `f`. (Newer gcc ≥ 14 / C99+ strict modes make it an error; the key assumes a warning.)
2. **Prototype mismatch across modules** – `Subroutine2(Class,const char*,int)` declared in Module1 vs defined as `(Class,const char*,float)` in Module2: C linker sees only `_Subroutine2` → links fine, wrong arguments at run time. In C++ this would be an `undefined reference` (mangled names differ).
3. **Variadic function pointer type** `void (*)(Class this, ...)` – calling through it passes args with default promotions; callee with fixed `(…, float)` reads the bits of an `int`.
4. **Shadowing** – `Class object1 = object2;` in `main` declares a *new local* `object1` hiding the global `object1`; nested block redeclarations hide again; the variable assigned on lines 31–32 is the main-block local. The global `object1` (declared `Class object1;` at file scope) is a *tentative definition* → `.comm` in the object file.
5. **Void function used as a value** – `object1 = object1->Abstract(object1)` where `Abstract` actually points to `Subroutine1` (declared `void`): the "returned" value is whatever is left in `%eax`. Using it as a pointer is undefined behaviour.
   * 2024 Q6 official answer: with `return 0` in `f`,`g` the nested `if` blocks never run, so `object1->Abstract` was never assigned (malloc garbage) → **segfault at line 31**; with `return 1` both `if`s execute, `Abstract` points to `Subroutine1`, and the program reaches `return sizeof(object1)` (= pointer size).
   * ⚠ **On this laptop (MinGW 32-bit, gcc 6.3) the `return 1` variant still segfaults – at line 32**, because line 31 stores garbage `%eax` into `object1` and line 32 dereferences it (gdb: `eip=0x8955c35d`). On the professor's machine the leftover register happened to be harmless. In the exam: give the semantic reasoning (what changes: the branches taken → `Abstract` assigned) and say the final outcome after line 31 depends on the unspecified return value of a `void` function. Re-run on your own machine before writing "it runs".
6. **`sizeof(object1)`** is the size of the *pointer type* `Class`, not of `struct Abstract`.
7. **Token rule for whitespace** (2024 Q3b): a space is needed only between two tokens that would otherwise lex as one – after an identifier or constant, unless a non-space delimiter follows.
8. **`#define ClassSize sizeof(struct Abstract)`** – macro; no storage, no type; replaced at preprocessing time.

## Other recurring traps

| Trap | Truth |
|---|---|
| `main` recursion | legal in C (`recurmain.c`), illegal in C++ (standard) – g++ only warns |
| `printf` re-implementation | declare `extern int printf(const char*, int)` and define your own body in another module: linker picks the first definition (`05_Code-Examples/examplesOf23aug2024/printf.c`); duplicates → multiple definition |
| `#include "structure.c"` in two modules that are linked together | duplicates every definition → *multiple definition of f* (`IndependentModules`) |
| Uninitialised struct passed by value | garbage output (`-1253039104` in Explanation.txt) – not repeatable guarantee |
| Array overrun `int a[11][3]; a[12][1]=1;` | C/C++: no compile error; writes flat element 12·3+1 = **37** of 33 → undefined behaviour (crash or silent corruption); Java: `ArrayIndexOutOfBoundsException` (OO Language Comparison Tut Q2) |
| Same header, different class layouts between modules (`class1.cpp` vs `class1bad.cpp`) | compiles, links, misbehaves – C++ gives no link-time check of member layout |
| Dangling `else` | binds to the nearest unmatched `if` |
| `struct` members with the same name in two structs | allowed – member namespace is per-struct |
| `static` at file scope | gives internal linkage: the name is invisible to the linker/other modules |
| Header guard / `extern` | `extern` = declaration only (no storage); a definition with initialiser is the one definition |
| Java `import` vs C `#include` | include = textual copy at preprocessing; import = name resolution against compiled class files |
| Overloaded names | C++ mangles parameter types; Java mangles in the class file descriptor; C does not overload |

## Tools to confirm a hunch in seconds
```
gcc -c -Wall -fstack-usage A.c B.c            # compile each module (+ frame sizes in .su)
nm A.o B.o ; gcc A.o B.o -o ab && ab           # symbols, link, run
gcc -Wall -Wextra -c A.c                         # all warnings
gcc -E A.c | tail -40                            # what the preprocessor made of it
nm A.o ; objdump -d A.o | more                   # symbols / disassembly
gdb -batch -ex run -ex bt ./a.exe                # where did it crash
```
