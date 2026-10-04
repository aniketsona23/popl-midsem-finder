# OO Language Comparison Tutorial — questions with answers

*Replaces `OO Language Comparison Tut.pdf` (a Moodle page: "Last Year's Tutorial for OO Language Comparisons: C/C++ `#include` v/s Java `import` demonstration").*
*The assignment asks for **example programs you find or write yourself, with comments**. The answers below give the reasoning and a tested program for each; ✔ = I ran it on this laptop (gcc 6.3 32-bit MinGW, g++, JDK 17+). There is **no official key**.*

---

## Q1 — Two headers that declare the same type differently

> Find an example of two headers (C/C++ `.h` files) in the libc/libc++ implementation on any platform that shows the same type declared differently, with one declaration consistent with the type's implementation in the binary library and the other consistent with but restricted to the API available to you (as programmers). If there are no such headers in your opinion and search, argue why.

**Say this**
- **The classic case is `FILE`.** On glibc (Linux), `<stdio.h>` has `typedef struct _IO_FILE FILE;` — the programmer sees only an *incomplete* type — while the full layout is in `<bits/types/struct_FILE.h>`, which the library implementation (and old `getc`/`putc` macros) include. Same type, **a restricted API view and a full implementation view**. *(Known from glibc; to check on a Linux box: `grep -rn "struct _IO_FILE" /usr/include`.)*
- **On this laptop (MinGW)** I searched `C:\MinGW\include`: `FILE` is `typedef struct _iobuf {...} FILE;` fully defined in `stdio.h` (line 210), so here there is *no* restricted view — the hiding is by convention only. ✔ For `struct stat` MinGW provides several declarations of one concept (`struct _stat`, `struct _stati64`, selected by macros, `sys/stat.h`).
- **If you find none, argue:** one platform ships one header set matching its binary; two *different* declarations of the same type would be an ODR/layout hazard, so libraries avoid it and rely on **opaque (incomplete) types** instead. That is exactly the "partially hidden class" danger on slides p79–84: nothing in C/C++ forces user and library modules to agree on a layout.

---

## Q2 — `int a[11][3];` then `a[12][1] = 1;`

> Possible outcomes: (a) compilation error, (b) run-time crash — no exception catch, (c) run-time exception, (d) some "n"th element becomes 1 (give n). Answer for C, C++ and Java, each justified.

![a[11][3] is 33 ints in a row; a[12][1] is flat element 37](img/oo-array-overflow.svg)

| Language | Outcome | Why |
|---|---|---|
| **C** | **(d)**, n = **37** (0-based flat index; 4 ints beyond the last element, index 32) | no bounds check; `a[12][1]` = address `a + 12·3 + 1`. Undefined behaviour in the standard, but in practice it silently writes whatever memory follows. ✔ In my test (array followed by another `int` array) the **5th int after the array** became 1. It crashes only if that address is unmapped or holds something critical. |
| **C++** | same as C — **(d)**, n = 37 | built-in arrays are not checked either (`std::array::at`/`vector::at` would throw). ✔ g++ compiled and ran silently. |
| **Java** | **(c)** `ArrayIndexOutOfBoundsException` | `new int[11][3]` is an array of 11 row *objects*; every index is checked at run time, the first one fails: "Index 12 out of bounds for length 11". ✔ Compiles without error. |

Caveat to state: optimisers may warn (`-Warray-bounds`) when the index is a constant, but the language does not require an error.

---

## Q3 — A Java SDK class with two different implementations in two packages

**Say this** — **`java.util.Date` and `java.sql.Date`**: same simple name `Date`, different classes in different packages (the SQL one *extends* the util one). ✔
Other pairs: `java.awt.List` / `java.util.List`; `javax.swing.Timer` / `java.util.Timer`.

---

## Q4 — Instantiate both in the same method and block?

**Say this** — **Yes, using fully qualified names.** You cannot `import` both simple names (compile error: the names clash), but you do not need to:

```java
public class D {
    public static void main(String[] args) {
        java.util.Date a = new java.util.Date();
        java.sql.Date  b = new java.sql.Date(0);
        System.out.println(a.getClass().getName() + " / " + b.getClass().getName()
                           + " / " + (b instanceof java.util.Date));
    }
}
// prints: java.util.Date / java.sql.Date / true      ✔
```
Why it works: Java's class identity is the **package-qualified name**; `import` is only a shorthand for the compiler (unlike C's `#include`, which pastes text).

---

## Q5 — The same in C++? Without namespaces?

**Say this**
- **With namespaces: yes** — `ns1::Date` and `ns2::Date` are different types and can coexist in one block (this is what namespaces are for).
- **Without namespaces**, two classes with the same name **in the same scope** are one name for one type; a second definition is an error. What *does* work is **other scopes**:
  1. **Class scope (nested classes)** ✔
     ```cpp
     struct A { struct Date { int x; }; };
     struct B { struct Date { double y; }; };
     A::Date a;  B::Date b;      // two unrelated types, different sizes ✔
     ```
  2. **Different translation units** with internal linkage (an *unnamed* namespace is a namespace, but needs no name) — and, dangerously, two same-named external classes in two modules with different layouts: it often *compiles and links*, which is the module-independence trap from slides p79–84.
  3. **Macro renaming at include time** (`#define Date Date_one` around one header) — works but is a hack.
