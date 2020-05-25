#### random

We are given the following C file.

```c
#include <stdio.h>

int main(){
        unsigned int random;
        random = rand();        // random value!

        unsigned int key=0;
        scanf("%d", &key);

        if( (key ^ random) == 0xdeadbeef ){
                printf("Good!\n");
                system("/bin/cat flag");
                return 0;
        }

        printf("Wrong, maybe you should try 2^32 cases.\n");
        return 0;
}
```

The following is mentioed in the man page of `rand`.

```
If no seed value is provided, the rand() function  is  automatically  seeded
with  a value of 1.
```

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    unsigned int random;
    random = rand();
    printf("random ^ 0xdeadbeef = %u\n", random ^ 0xdeadbeef);

    return 0;
}
```

Running with this value should give us the flag.

```sh
random@pwnable:~$ ./random
3039230856
Good!
Mommy, I thought libc random is unpredictable...
```
