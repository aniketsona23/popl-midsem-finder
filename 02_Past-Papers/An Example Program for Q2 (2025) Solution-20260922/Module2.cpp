#include<iostream>
#include "class1.hpp"

class Class2 : public Class1 { // The inheritance is to allow the call to function function
	public:
		~Class2() {
			globalSrNo+=(1<<25);		
		}
};

//extern void function(Class2); Line commented out to allow linking with Module1.cpp
extern void function(Class1); // Line added to allow the call below with polymorphism

int main(void) {
	int i;
	for(i=0; i<1000; i++) {
		Class2 c; // c is also a Class1 instance due to inheritance
		std::cout << "Cycle " << i << "pre gSrNo " << globalSrNo << std::endl;
		function(c); // Call to void function(Class1)
		std::cout << "Cycle " << i << "post gSrNo " << globalSrNo << std::endl;
	}
}
