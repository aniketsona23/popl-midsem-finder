/* Call-tree / activation-record tracer.  Copy, paste YOUR function between the markers, run.
 *   gcc -g trace_template.c -o t && ./t
 * Prints each call indented by depth, the stack snapshot (chain of live frames), total calls, max depth.
 * It also prints each frame's base-pointer address so you can SEE frames growing (stack grows to lower addresses on x86).
 * Trick: wrap the call sites with TRACE_CALL so you don't edit the body much.
 */
#include <stdio.h>
static int depth = 0, maxdepth = 0, ncalls = 0;
static int live[256];                       /* live[d] = argument of the frame at depth d */
#define ENTER(arg)  do { live[depth] = (arg); ncalls++; \
        printf("%*scall #%d  f(%d)  depth=%d  frame-base=%p   stack: ", 2*depth, "", ncalls, (arg), depth+1, __builtin_frame_address(0)); \
        for (int _i = 0; _i <= depth; _i++) printf("%d%s", live[_i], _i<depth?" > ":"\n"); \
        if (++depth > maxdepth) maxdepth = depth; } while (0)
#define LEAVE(ret)  (depth--, (ret))        /* use: return LEAVE(value); */

/* ---------- paste/adapt your function here (example: compre 2025 Q4, fiboDP) ---------- */
int fiboDP(int n) {
    static int fib[100];
    ENTER(n);
    if (n > 1 && n < 100) {
        if (fib[n] == 0) {
            if (fib[n-2] == 0) fib[n-2] = fiboDP(n-2);
            if (fib[n-1] == 0) fib[n-1] = fiboDP(n-1);
            fib[n] = fib[n-2] + fib[n-1];
        }
        return LEAVE(fib[n]);
    }
    return LEAVE(1);
}
/* ---------------------------------------------------------------------------------------- */
int main(void) {
    int r = fiboDP(5);
    printf("result=%d  total calls=%d  max simultaneous frames=%d\n", r, ncalls, maxdepth);
    return 0;
}
