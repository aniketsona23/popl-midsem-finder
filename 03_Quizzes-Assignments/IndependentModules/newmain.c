#include<stdio.h>
/* #include "structure.c" */

struct x { int i; float f; };
int f(struct x);

int main(void) { struct x X; printf("%d\n",f(X));  return 0; }
