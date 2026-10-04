#include<malloc.h>
struct Abstract;
typedef struct Abstract *Class;
extern void Subroutine1(Class, const char *, int);
extern void Subroutine2(Class, const char *, int);
struct Abstract{
	void *abstractData;
	Class (*Abstract)(void *abstractData);
	void (**abstractMethod)(Class this, ...);
};
#define ClassSize sizeof(struct Abstract)
Class object1;
int main(void) {
	object1 = (Class)malloc(ClassSize);
	object1->abstractData = malloc(256);
	object1->abstractMethod = (void (**)(Class,...))malloc(2*sizeof(void(*)(Class,...)));
	object1->abstractMethod[0] = ((void(*)(Class,...))&Subroutine1);
	object1->abstractMethod[1] = (void(*)(Class,...))&Subroutine2;
	object1->abstractMethod[0](object1,"",0);
	object1->abstractMethod[1](object1,"",0);
	Class object2 = object1;
	Class object1 = object2;
	if(f(10)) {
		Class object1 = object2;
		object2->Abstract = (Class(*)(void*))&Subroutine1;
		if(g(10)) {
			Class object2 = object1;
			Class object1 = object2;
		}
	}
	object1 = object1->Abstract(object1);
	object2 = object1->Abstract(object2);
	return sizeof(object1);
}
