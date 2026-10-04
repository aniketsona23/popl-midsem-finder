#include<iostream>

using namespace std;

class class1 {
	private:
		int size;
		int *a;
	public:
		class1(int);
		void tell(void);
	};

class1::class1(int n=0) { a = new int[size = n]; }

void class1::tell(void)
	{
	cout << "Size" << size << endl;
	int i;
	for(i = 0; i < size; i++)
		{
		cout << "a[" << i << "]=" << a[i] << " ";
		}
	cout << endl;
	}
