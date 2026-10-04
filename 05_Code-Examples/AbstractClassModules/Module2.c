struct Abstract;
typedef struct Abstract *Class;
void Subroutine1(Class c, const char *s, int i) { return; }
void Subroutine2(Class c, const char *s, float f) { return; }
int f(int n){if(n>0)return f(n-1)>g(n-1)?g(n-2):f(n-2);return 0;}
int g(int n){if(n>0)return g(n-1)<f(n-1)?f(n-2):g(n-2);return 0;}
