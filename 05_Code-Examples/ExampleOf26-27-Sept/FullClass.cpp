using namespace std;

#include<iostream>

int gFullClassSerialNumber = 0;
class FullClass {
	private :
		int objectId, *data, size;
	public :
		FullClass(void);
		FullClass(int);
		FullClass(int, int*);
		FullClass(const FullClass&);
		void tell(void);
		void setNthElement(int,int);
		~FullClass(void);
};

FullClass::FullClass(void) {
	objectId = ++gFullClassSerialNumber;
	size = 0; data = NULL;
	cout << "Constructed by method 1: ";
	tell();
}

FullClass::FullClass(int inputSize) {
	objectId = ++gFullClassSerialNumber;
	size = inputSize; data = new int[inputSize];
	cout << "Constructed by method 2: ";
	tell();
}

FullClass::FullClass(int inputSize, int *input) {
	objectId = ++gFullClassSerialNumber;
	size = inputSize; data = new int[inputSize];
	for(int i = 0; i < inputSize; i++) data[i] = input[i];
	cout << "Constructed by method 3: ";
	tell();
}

FullClass::FullClass(const FullClass& fc) {
	objectId = ++gFullClassSerialNumber;
	size = fc.size;
	data = new int[size];
	for(int i = 0; i < size; i++) data[i] = fc.data[i];
	cout << "Constructed by method 4: ";
	tell();
}

void FullClass::tell(void) {
	cout << " ObjectId : " << objectId << endl;
	cout << "Size : " << size << endl << "data : ";
	if(size <= 0 || data == NULL) cout << "NONE" << endl;
	else {
		for(int i = 0; i < size; i++) cout << "[" << i << "] : " << data[i] << " ";
		cout << "#" << endl;
	}
}

void FullClass::setNthElement(int n, int i) {
	if(n >= 0 && n < size) {
		data[n] = i;
	}
}

FullClass::~FullClass(void) {
	cout << "Destroying: "; tell();
	if(data != NULL) delete data;
}

