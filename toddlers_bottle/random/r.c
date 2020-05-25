#include <stdio.h>
#include <stdlib.h>

int main() {
    unsigned int random;
    random = rand();
    printf("random ^ 0xdeadbeef = %u\n", random ^ 0xdeadbeef);

    return 0;
}
