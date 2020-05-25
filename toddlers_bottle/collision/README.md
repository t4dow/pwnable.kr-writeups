##### collision

The following source code is given:

```c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
        int* ip = (int*)p;
        int i;
        int res=0;
        for(i=0; i<5; i++){
                res += ip[i];
        }
        return res;
}

int main(int argc, char* argv[]){
        if(argc<2){
                printf("usage : %s [passcode]\n", argv[0]);
                return 0;
        }
        if(strlen(argv[1]) != 20){
                printf("passcode length should be 20 bytes\n");
                return 0;
        }

        if(hashcode == check_password( argv[1] )){
                system("/bin/cat flag");
                return 0;
        }
        else
                printf("wrong passcode.\n");
        return 0;
}
```

We are supposed to pass a 20 byte input. The input is then read as 5 `int`s and
added together. The sum is compared to `0x21DD09EC`.

Also, our input can't have null bytes in it.

```py
>>> import struct
>>> def p32(x): return struct.pack('<I', x)
...
>>> 0x21DD09EC % 5
4
>>> 0x21DD09EC / 5
113626824
>>> p32(113626824) * 4 + p32(0x21DD09EC - 4 * 113626824)
'\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xcc\xce\xc5\x06'
```

We can pass this as input and hopefully get the flag.

```sh
col@pwnable:~$ ./col `echo -ne '\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xcc\xce\xc5\x06'`
daddy! I just managed to create a hash collision :)
```
