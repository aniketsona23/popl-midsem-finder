#include <stdio.h>

struct ll {
    int key;
    struct ll *next;
    };

extern void func(struct ll*);


int main(void)
    {
		struct ll l = { 1, &l };
    printf("%d %d\n",l.key,l.next->key);
    func(&l);
    return 0;
    }
