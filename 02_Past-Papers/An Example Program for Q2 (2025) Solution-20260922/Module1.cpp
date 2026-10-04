#include<iostream>
#include "class1.hpp"

int globalSrNo = 0;

void function(Class1 c) {
	std::cout << c.SrNo() << std::endl;
}
