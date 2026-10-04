#include <stdio.h>
struct llbad {
    struct llbad *next;
    int key;
    };

void func(struct llbad *l)
    {
    printf("%d %d\n",l->key,l->next->key);
    }
