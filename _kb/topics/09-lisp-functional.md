# Lisp, CLOS/MOP, functional ideas (mostly post-midsem; skim)

## In plain words

In Lisp and Python a function is just a value: you can store it in a variable, pass it to another function, even build it while the program runs. In C, C++ and Java the functions are fixed when the program is compiled.

**Example.** Python: `f = eval('lambda x: x*x')` then `f(5)` gives 25. The function was created from text at run time.


## Short answer

* Functions are first-class in Lisp and Python, so a lambda can be read and applied at run time. Not in C, C++ or Java. *[Compre 2024 key A5]*
* CLOS: classes, generic functions and methods; the metaobject protocol lets users change the language's behaviour. *[slides p138-142]*
* Per-instance specialisation (storage and methods) is possible in Lisp and Python only. *[Compre 2024 key A6]*


Slides: PDF p138–148 (MetaObject Protocol I–II; CLOS bucket-list; CLOS program structure; painting example; reflection; method combinations; performance vs expressive power). Files: `painting.lisp` (CLOS multiple inheritance `color-mixin` + `rectangle`, `defgeneric paint`, `defmethod`), `mergesort-final.lisp` (merge sort with a counted comparison and `funcall`), `fghc.lisp` (farmer–goat… river-crossing state search: `make-state`, `safe`, `is-visited`). No Lisp interpreter is installed on this laptop (`clisp`/`sbcl` absent) – read, don't run.

## Facts to quote
* **MOP** (Kiczales): metaobject protocols let users incrementally modify the language's behaviour/implementation – blurring designer/user; goal: elegance *and* efficiency together.
* **CLOS program** = `defclass`, `defgeneric`, `defmethod` forms among ordinary Lisp forms; executing them builds internal class/generic/method metaobjects. Features: class redefinition (propagates to subclasses and existing instances), method redefinition, forward-referenced superclasses, implicit generic-function definition, user control of method combination (before/primary/after: before-methods most-specific first, then most specific primary, then after-methods least-specific first), `eql` specialisers (methods on individual objects), class-allocated slots, integrated types and classes.
* **Reflection** (slide p144–147): `find-class`; two kinds: introspection and intercession. Naive MOP implementations are slow; optimisation relies on caching/discriminating-function tricks (p148).
* **Functional ideas**: functions first-class → run-time lambda from user input possible (`eval`); exact rational arithmetic in Lisp: `(power (/ 2 3) 5)` → `32/243`, no precision loss (Compre 2024 Q2).
* Per-instance specialisation (slots and methods per instance) is natural in Lisp and Python (Compre 2024 Q6).
* Merge sort in Lisp with an optional comparison function argument = higher-order function; a global counter via `defvar`/`setq`.

## Search shortcuts
`search.py -k slides CLOS` · `search.py -k slides reflection` · `search.py -p lisp defmethod`
