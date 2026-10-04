#include<stdio.h>

int main(int argc, char *argv[]) {
	if(argc>0) {
		printf("%d %s\n",argc,argv[argc-1]);
		return main(argc-1,argv);
	}
	else return 0;
}
