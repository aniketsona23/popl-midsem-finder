#include <stdio.h>

int fmat1(int *, int n);
int fmat2(int **, int n);
int fmat3(int *[10], int n);
int fmat4(int [][10], int n);
int fmat5(int [10][10]);
int globalN = 100;

double ff1(double x)
	{
	return x*x - 2*x + 10.0;
	}

int main(int argc, char *argv[])
	{
	int mat[10][10];
	int i, j;
	for(i = 9; i; i--)
		for(j = 9; j; j--)
			{
			if(--argc) mat[i][j] = atoi(argv[argc]);
			else
				{
				argc = 1;
				mat[i][j] = i*10+j;
				}
			}
	printf("1 : %d\n",fmat1(mat[0],10));
	printf("2 : %d\n",fmat2(mat,10));
	printf("3 : %d\n",fmat3(mat,10));
	printf("4 : %d\n",fmat4(mat,10));
	printf("5 : %d\n",fmat5(mat));
	printf("GlobalN = %d\n",globalN);
	return 0;
	}

int fmat1(int *A, int n)
	{
	int i;
	for(i = 0; i < n; i++) printf("!%d ",A[i]);
	printf("\n");
	return n;
	}

int fmat2(int **A, int n)
	{
	int i, j;
	static int k = -100;
	for(i = 0; i < n; i++)
		for(j = 0; j < n; j++) printf("@%d ",A[i][j]);
	k = k + i * j;
	printf("\n");
	return k;
	}

int fmat3(int *A[10], int n)
	{
	int i, j;
	for(i = 0; i < n; i++)
		for(j = 0; j < 10; j++) printf("#%d ",A[i][j]);
	printf("\n");
	return n*10;
	}

int fmat4(int A[][10], int n)
	{
	int i, j;
	for(i = 0; i < n; i++)
		for(j = 0; j < 10; j++) printf("$%d ",A[i][j]);
	printf("\n");
	return n*10;
	}

int fmat5(int A[10][10])
	{
	int i, j;
	for(i = 0; i < 10; i++)
		for(j = 0; j < 10; j++) printf("^%d ",A[i][j]);
	printf("\n");
	return 10*10;
	}

