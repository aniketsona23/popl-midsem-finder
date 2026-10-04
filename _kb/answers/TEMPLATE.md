# Answer template — copy to `_kb/answers/qN.md`, fill top to bottom, paste into the answer sheet

**Q__ (__ marks) — format demanded by the paper:** _(table / one line each / ≤ 2 sentences / units / line numbers — copy the instruction verbatim)_

## 1. Verdict (≤ 1 line, the thing a marker looks for first)
_e.g. "No — Module1.c alone gives no executable; the two objects together do."_

## 2. Reason in the course's vocabulary (2–4 lines)
Use the professor's words: *compile time / linking time / procedure-activation time / run time; many declarations, one unique definition; compiler vs linker vs loader; type information (size, layout) vs names; imperative code; information hiding; contain-and-delegate; fragile base class.*

## 3. Evidence (optional but cheap — marks for rigour)
```
$ gcc -c -Wall Module1.c      -> warnings only (implicit declaration of f, g)
$ nm Module1.o                -> U _f _g _Subroutine1 _Subroutine2
$ gcc Module1.o               -> undefined reference to f, g, Subroutine1, Subroutine2
```

## 4. Exceptions / assumptions (1 line — shows you saw the trap)
_e.g. "assuming all pointers have the same size"; "result of a void function is unspecified"; "on x86-64 pointer = 8 bytes, here stated symbolically"._

## 5. Source (for me, not for the paper)
_slide PDF p__ · past paper __ · tutorial __ · tool output ___

### Pre-submit checklist
- [ ] Answered exactly what was asked (every sub-part a/b/c?) 
- [ ] Format matches the instruction (table columns, one line, α↔n)
- [ ] Units stated (bytes / multiples of sizeof(void*))
- [ ] Line numbers refer to the *given* listing, per module
- [ ] No claim I didn't verify; no contradiction between sub-answers ("necessary yet harmful")
