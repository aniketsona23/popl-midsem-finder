#include<iostream>

using namespace std;

class class1 {
	public:
		double x;
		int key;
		class1(int);
		void tell(void);
	};

int main(void)
	{
	class1 c1(2);
	c1.tell();
	c1.key = 1;
	c1.tell();
	c1.x = 0.45;
	c1.tell();
	}
