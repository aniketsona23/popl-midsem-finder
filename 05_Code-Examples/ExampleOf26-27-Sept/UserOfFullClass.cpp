using namespace std;

class FullClass {
	private:
		char x[2*sizeof(int)+sizeof(int*)];
		// int objectId, *data, size;
		// Or try different things here, or leave this part empty, no private members at all.
	public :
		FullClass(void);
		FullClass(int);
		FullClass(int, int*);
		FullClass(const FullClass&);
		void tell(void);
		void setNthElement(int,int);
		~FullClass(void);
};

void g(FullClass fc1, FullClass fc2) {
	fc2.setNthElement(0,0b01010101010101010101010101010101);
	fc1.tell();
	fc2.tell();
}

void f(FullClass& fc) {
	fc.tell();
	g(fc,fc);
	fc.tell();
	fc.setNthElement(0,0b10101010101010101010101010101010);
	fc.tell();
}

int main(void) {
	int array[5];
	for(int i = 0; i < 5; i++) array[i] = i+1;
	FullClass fc1;
	FullClass fc2(10);
	FullClass fc3(5,array);
	FullClass fc4(fc3);
	f(fc1);
	f(fc2);
	f(fc3);
	f(fc4);
	g(fc2,fc4);
	return 0;
}
