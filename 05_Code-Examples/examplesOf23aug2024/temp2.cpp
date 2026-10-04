#include <stdio.h>
#include <iostream>
using namespace std;

int main(int argc, char *argv[])
{
    if (argc <= 1)
        return 0;
    int index = argc - 1;
    cout << argv[index] << endl;
    main(argc - 1, argv);
    return 0;
}