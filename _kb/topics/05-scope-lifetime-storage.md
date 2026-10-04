# Scope, lifetime, storage, memory allocation

## In plain words

Scope is the part of the program text where a name can be used. Lifetime is how long its memory exists while the program runs. They are different things. C also has three places for memory: fixed storage for globals and static variables, the stack for local variables, and the heap for memory you ask for with malloc.

**Example.** A `static int count;` inside a function can be used only inside that function (scope), but it keeps its value between calls (lifetime: the whole program).


## Short answer

* Scope = where a name is visible (lexical in C, C++, Java). Lifetime = when its storage exists. They can differ, e.g. a static local. *[slides p60]*
* Compre 2024 Q1 numbers: parameters 3, locals 2, static 2, labels 2, template parameter 4, static class members 5. *[Compre 2024 key A1]*
* Storage in C: static, automatic (stack), dynamic (heap, a library service). *[question bank Q9 (reasoned, no official key)]*


Slides: PDF p60 ("Scope Rules" – scope = the textual extent in which a name refers to one object), p51–53 (program structure), p119–125. Past: **Compre 2024 Q1** (scope table), qbank Q1, Q4–Q11. Tutorial files: `Tutorial_1_Answers.md` (info hiding).

## Same idea, different words

The slides define scope on page 60 (“Scope Rules”). The exam asks for a table of scope numbers (Compre 2024 Q1) and for static, stack and heap storage.

## Compre 2024 Q1 — official numbers

**Scope scale:** 1 expression · 2 block · 3 procedure/method · 4 class · 5 class hierarchy · 6 module · 7 package · 8 namespace · 9 program-global · 10 shell-global.
Format of answer: `α ↔ n`.

| α | kind of name | answer (all three languages unless stated) |
|---|---|---|
| a | formal parameters | **3** |
| b | local variables | **2** |
| c | static variables | **2** |
| d | labels | **2** (per key; note: ISO C gives labels *function* scope = 3 – follow the key, mention if asked to justify) |
| e | type parameter (template `T`, generic `T`) | **4** |
| f | enum type inside a class | **C/C++: 6; Java: 5** |
| g | enum type in the `.java` file outside the class | **C/C++: 6; Java: 7** |
| h | static members of a class | **5** |

## Lifetime vs scope vs binding
* **Scope** = where a *name* is visible (lexical in C/C++/Java: determined by the program text, not by call chain). **Lifetime/extent** = when the *storage* exists. They differ: a `static` local has block scope but program lifetime.
* **Lexical (static) scope** – C, C++, Java, Lisp (Common Lisp lexical by default). **Dynamic scope** – name resolved through the call chain (old Lisp, shell variables). qbank Q1(c): scope of macro parameters `a,b,c` is *lexical* (textual substitution at preprocessing time).
* **Struct/class members (qbank Q4–Q8):** member names live in the struct's own namespace (accessed via `.`/`->`), so the same member name can appear in two different structs without conflict: the compiler resolves `x.name` by the type of `x` (C: member offsets by struct type; C++: also class-qualified, methods mangled with class name; Java: resolved through the static type of the reference and the class's member table). Scope of a member is the struct (class) – not the instance, not the enclosing block, not global.

## Memory allocation kinds in C (qbank Q9)

| Kind | Where | Who does it | Binding/lifetime |
|---|---|---|---|
| Static / global / `static` local | data/bss segment | compiler lays out, linker/loader places | whole program; compile/link/load time |
| Automatic (locals, params, VLA, temporaries) | stack frame | compiler generates `sub rsp`/offsets; allocation happens at each **procedure activation** | until the function returns |
| Dynamic | heap | **library** (`malloc/free`), not the compiler; the compiler only passes sizes (`sizeof`) and types the returned `void*` | explicit; run time |
`scanf("%d",&n); int array[n];` → **automatic allocation (stack), size known only at activation/run time** (C99 VLA).

## Java vs C procedure activation (qbank Q10)
Frames look the same (params, locals, return address). The difference: Java objects are allocated by `new` on the **heap** and variables hold references, so passing an object "by value" copies the reference (call by value of a reference); C copies whole structs by value or passes pointers explicitly. Reference semantics ⇒ the callee can mutate the caller's object but cannot rebind the caller's variable.

## Java symbol-table question (qbank Q8)
Different objects with the same *variable name* in different scopes get different run-time identities (heap addresses); the name→declaration resolution is done at compile time by scope rules, not by the run-time heap. Objects don't have names, references do.

## Access control questions (Compre 2024 Q3–Q4, Q6)
* Method usable only by instances of its own class (not subclasses): make it `private`. Caveats: C++ — a derived class can redeclare a base method as private, but the base is still reachable through a base pointer cast; private on an override doesn't remove the public base method. Java — cannot weaken access on override; `private` methods are implicitly `final` (but `final` ≠ private: final methods are still callable by subclass instances).
* Calling a non-static method without an instance: C++ only via the null-pointer-cast trick `((T*)NULL)->m()` (works if `m` touches no members; undefined behaviour, compilers warn); Java/Python: not possible.
* Run-time lambda from user input: Python (`eval`), Lisp/ML/Scheme/OCaml/Ruby yes; C/C++/Java no (functions aren't first-class run-time values).
* Instance-level specialisation of storage structure/methods: **official key = only Lisp and Python** (an instance can get extra attributes/methods, e.g. `b2.tail` exists but `b1.tail` raises AttributeError). C struct function-pointer members vary methods per instance but not the storage layout; C++/Java classes fix layout for all instances.
