memcpy

We're given a program which does allocations using `malloc` and uses 2 functions
to copy data to the allocated chunks.
Chunks allocated with `malloc` are 8 byte aligned on `x86`.

```c
// compiled with : gcc -o memcpy memcpy.c -m32 -lm
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <sys/mman.h>
#include <math.h>

unsigned long long rdtsc(){
        asm("rdtsc");
}

char* slow_memcpy(char* dest, const char* src, size_t len){
    int i;
    for (i=0; i<len; i++) {
        dest[i] = src[i];
    }
    return dest;
}

char* fast_memcpy(char* dest, const char* src, size_t len){
    size_t i;
    // 64-byte block fast copy
    if(len >= 64){
        i = len / 64;
        len &= (64-1);
        while(i-- > 0){
            __asm__ __volatile__ (
            "movdqa (%0), %%xmm0\n"
            "movdqa 16(%0), %%xmm1\n"
            "movdqa 32(%0), %%xmm2\n"
            "movdqa 48(%0), %%xmm3\n"
            "movntps %%xmm0, (%1)\n"
            "movntps %%xmm1, 16(%1)\n"
            "movntps %%xmm2, 32(%1)\n"
            "movntps %%xmm3, 48(%1)\n"
            ::"r"(src),"r"(dest):"memory");
            dest += 64;
            src += 64;
        }
    }

    // byte-to-byte slow copy
    if(len) slow_memcpy(dest, src, len);
    return dest;
}

int main(void){

    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stdin, 0, _IOLBF, 0);

    printf("Hey, I have a boring assignment for CS class.. :(\n");
    printf("The assignment is simple.\n");

    printf("-----------------------------------------------------\n");
    printf("- What is the best implementation of memcpy?        -\n");
    printf("- 1. implement your own slow/fast version of memcpy -\n");
    printf("- 2. compare them with various size of data         -\n");
    printf("- 3. conclude your experiment and submit report     -\n");
    printf("-----------------------------------------------------\n");

    printf("This time, just help me out with my experiment and get flag\n");
    printf("No fancy hacking, I promise :D\n");

    unsigned long long t1, t2;
    int e;
    char* src;
    char* dest;
    unsigned int low, high;
    unsigned int size;
    // allocate memory
    char* cache1 = mmap(0, 0x4000, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    char* cache2 = mmap(0, 0x4000, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    src = mmap(0, 0x2000, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);

    size_t sizes[10];
    int i=0;

    // setup experiment parameters
    for(e=4; e<14; e++){    // 2^13 = 8K
        low = pow(2,e-1);
        high = pow(2,e);
        printf("specify the memcpy amount between %d ~ %d : ", low, high);
        scanf("%d", &size);
        if( size < low || size > high ){
            printf("don't mess with the experiment.\n");
            exit(0);
        }
        sizes[i++] = size;
    }

    sleep(1);
    printf("ok, lets run the experiment with your configuration\n");
    sleep(1);

    // run experiment
    for(i=0; i<10; i++){
        size = sizes[i];
        printf("experiment %d : memcpy with buffer size %d\n", i+1, size);
        dest = malloc( size );

        memcpy(cache1, cache2, 0x4000);     // to eliminate cache effect
        t1 = rdtsc();
        slow_memcpy(dest, src, size);       // byte-to-byte memcpy
        t2 = rdtsc();
        printf("ellapsed CPU cycles for slow_memcpy : %llu\n", t2-t1);

        memcpy(cache1, cache2, 0x4000);     // to eliminate cache effect
        t1 = rdtsc();
        fast_memcpy(dest, src, size);       // block-to-block memcpy
        t2 = rdtsc();
        printf("ellapsed CPU cycles for fast_memcpy : %llu\n", t2-t1);
        printf("\n");
    }

    printf("thanks for helping my experiment!\n");
    printf("flag : ----- erased in this source code -----\n");
    return 0;
}
```

More information about chunk allocation and alignment is present here:
[https://sourceware.org/glibc/wiki/MallocInternals](https://sourceware.org/glibc/wiki/MallocInternals)

There are 2 functions which are used to copy data from source to destination.

```c
char* slow_memcpy(char* dest, const char* src, size_t len){
    int i;
    for (i=0; i<len; i++) {
        dest[i] = src[i];
    }
    return dest;
}
```

and

```c
char* fast_memcpy(char* dest, const char* src, size_t len){
    size_t i;
    // 64-byte block fast copy
    if(len >= 64){
        i = len / 64;
        len &= (64-1);
        while(i-- > 0){
            __asm__ __volatile__ (
            "movdqa (%0), %%xmm0\n"
            "movdqa 16(%0), %%xmm1\n"
            "movdqa 32(%0), %%xmm2\n"
            "movdqa 48(%0), %%xmm3\n"
            "movntps %%xmm0, (%1)\n"
            "movntps %%xmm1, 16(%1)\n"
            "movntps %%xmm2, 32(%1)\n"
            "movntps %%xmm3, 48(%1)\n"
            ::"r"(src),"r"(dest):"memory");
            dest += 64;
            src += 64;
        }
    }

    // byte-to-byte slow copy
    if(len) slow_memcpy(dest, src, len);
    return dest;
}
```

`fast_memcpy` uses the `movdqa` instruction which expects the address to be on a
16-byte boundary, otherwise, a general-protection exception is generated.

We have to ensure that the chunks returned from `malloc` are on a 16-byte
boundary.

We have to decide the size of the allocations:

```
specify the memcpy amount between 8 ~ 16 : 8
specify the memcpy amount between 16 ~ 32 : 16
specify the memcpy amount between 32 ~ 64 : 32
specify the memcpy amount between 64 ~ 128 : 64
specify the memcpy amount between 128 ~ 256 : 128
specify the memcpy amount between 256 ~ 512 : 256
specify the memcpy amount between 512 ~ 1024 : 512
specify the memcpy amount between 1024 ~ 2048 : 1024
specify the memcpy amount between 2048 ~ 4096 : 2048
specify the memcpy amount between 4096 ~ 8192 : 4096
```

This particular input will cause a fault when `fast_memcpy` is called for `128`.

We can calculate the sizes which we must pass to the program for it to pass
successfully.

```py
def round8(x):
    return (x + 7) & ~(8 - 1)

def align(start):
    # (size + 4) to accomodate malloc metadata
    while round8(start + 4) % 16 != 0:
        start += 4
    return start

for sz in [64, 128, 256, 512, 1024, 2048, 4096]:
    print(align(sz))
```

Passing these sizes to the program should give us the flag.

```sh
$ nc pwnable.kr 9022
Hey, I have a boring assignment for CS class.. :(
The assignment is simple.
-----------------------------------------------------
- What is the best implementation of memcpy?        -
- 1. implement your own slow/fast version of memcpy -
- 2. compare them with various size of data         -
- 3. conclude your experiment and submit report     -
-----------------------------------------------------
This time, just help me out with my experiment and get flag
No fancy hacking, I promise :D
specify the memcpy amount between 8 ~ 16 : 8
specify the memcpy amount between 16 ~ 32 : 16
specify the memcpy amount between 32 ~ 64 : 32
specify the memcpy amount between 64 ~ 128 : 72
specify the memcpy amount between 128 ~ 256 : 136
specify the memcpy amount between 256 ~ 512 : 264
specify the memcpy amount between 512 ~ 1024 : 520
specify the memcpy amount between 1024 ~ 2048 : 1032
specify the memcpy amount between 2048 ~ 4096 : 2056
specify the memcpy amount between 4096 ~ 8192 : 4104
ok, lets run the experiment with your configuration
experiment 1 : memcpy with buffer size 8
ellapsed CPU cycles for slow_memcpy : 2068
ellapsed CPU cycles for fast_memcpy : 174

experiment 2 : memcpy with buffer size 16
ellapsed CPU cycles for slow_memcpy : 238
ellapsed CPU cycles for fast_memcpy : 182

experiment 3 : memcpy with buffer size 32
ellapsed CPU cycles for slow_memcpy : 308
ellapsed CPU cycles for fast_memcpy : 354

experiment 4 : memcpy with buffer size 72
ellapsed CPU cycles for slow_memcpy : 570
ellapsed CPU cycles for fast_memcpy : 220

experiment 5 : memcpy with buffer size 136
ellapsed CPU cycles for slow_memcpy : 1002
ellapsed CPU cycles for fast_memcpy : 130

experiment 6 : memcpy with buffer size 264
ellapsed CPU cycles for slow_memcpy : 1852
ellapsed CPU cycles for fast_memcpy : 228

experiment 7 : memcpy with buffer size 520
ellapsed CPU cycles for slow_memcpy : 3472
ellapsed CPU cycles for fast_memcpy : 228

experiment 8 : memcpy with buffer size 1032
ellapsed CPU cycles for slow_memcpy : 6996
ellapsed CPU cycles for fast_memcpy : 422

experiment 9 : memcpy with buffer size 2056
ellapsed CPU cycles for slow_memcpy : 13770
ellapsed CPU cycles for fast_memcpy : 844

experiment 10 : memcpy with buffer size 4104
ellapsed CPU cycles for slow_memcpy : 30786
ellapsed CPU cycles for fast_memcpy : 1320

thanks for helping my experiment!
flag : 1_w4nn4_br34K_th3_m3m0ry_4lignm3nt
```
