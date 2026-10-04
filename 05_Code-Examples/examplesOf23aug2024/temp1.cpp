#include <iostream>

// Global variable
int GLOBAL_COUNTER = 0;

int main()
{
    if (GLOBAL_COUNTER < 5)
    {
        std::cout << GLOBAL_COUNTER << std::endl;
        GLOBAL_COUNTER++;
        main(); // Recursive call
    }
    return 0;
}