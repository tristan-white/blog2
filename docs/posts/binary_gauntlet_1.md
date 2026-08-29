---
tags:
    - ctf
    - binex
date: 2024-10-15
---

# Binary Gauntlet 1

CTF write up for cylabacademy's [Binary Guantlet 1](https://learn.cylabacademy.org/library/126?page=1)

## Security Mitigations 

We have a binary called `gauntlet`.

Check security mitigations on the binary (using checksec in [gef](https://github.com/hugsy/gef)):

```
gef➤  checksec
[+] checksec for '/home/tristan/Downloads/gauntlet'
Canary                        : ✘
NX                            : ✘
PIE                           : ✘
Fortify                       : ✘
RelRO                         : Partial
```

All the mitigations are disabled, so it's likely we'll write shellcode directly to the stack then overwrite a return pointer to jump to our shellcode.

## RE the binary

Looking at decompilation in ghidra (I renamed the variables):

```c title="Ghidra Decompilation of gauntlet" hl_lines="6 14"
undefined8 main(void) {
    char stack_buf [104];
    char *heap_buf;

    heap_buf = malloc(1000);
    printf("%p\n",stack_buf);
    fflush(stdout);
    fgets(heap_buf,1000,stdin);
    heap_buf[999] = '\0';
    printf(heap_buf);
    fflush(stdout);
    fgets(heap_buf,1000,stdin);
    heap_buf[999] = '\0';
    strcpy(stack_buf,heap_buf);
    return 0;
}  
```

Key information to note:

- There's a `strcpy` that copies our input to the `stack_buf` without any bounds checking.
- The address of `stack_buf` is printed, so we can use this address to calculate the address of the return pointer we need to overwrite

The disassembly of `main` shows that the function prologue is saving `rbp` to the stack:

```python hl_lines="3-4 11"
gef➤  disassemble main
Dump of assembler code for function main:
   0x0000000000400687 <+0>:     push   rbp
   0x0000000000400688 <+1>:     mov    rbp,rsp  # (1)!
   0x000000000040068b <+4>:     add    rsp,0xffffffffffffff80
   0x000000000040068f <+8>:     mov    DWORD PTR [rbp-0x74],edi
   0x0000000000400692 <+11>:    mov    QWORD PTR [rbp-0x80],rsi
   0x0000000000400696 <+15>:    mov    edi,0x3e8
   0x000000000040069b <+20>:    call   0x400580 <malloc@plt>
   0x00000000004006a0 <+25>:    mov    QWORD PTR [rbp-0x8],rax
   0x00000000004006a4 <+29>:    lea    rax,[rbp-0x70]   # (2)!
   0x00000000004006a8 <+33>:    mov    rsi,rax
   0x00000000004006ab <+36>:    lea    rdi,[rip+0x122]        # 0x4007d4
   0x00000000004006b2 <+43>:    mov    eax,0x0
   0x00000000004006b7 <+48>:    call   0x400560 <printf@plt>
```

1.  `rbp` is pushed to the stack in the function prologue, so we'll need to account for this 8 byte offset we calculate the address of the return pointer.
2.  In the same way that the program uses `rbp` to calculate the address of `stack_buf`, we can add `0x70` to the printed `stack_buf` address to get the address in `rbp`.

## Craft the Payload

```python
--8<-- "./docs/assets/code/picoctf/gauntlet_1/solution.py"
```

Run it and get the flag:

```console
$ uv run solution.py
[+] Opening connection to wily-courier.picoctf.net on port 52996: Done
[*] Switching to interactive mode
$ ls
Dockerfile
Makefile
Solution
flag.txt
gauntlet
gauntlet.c
start.sh
$ cat flag.txt
5ef0ab218aa1da49ee3255611be97bea
```



*[CTF]: Capture the Flag. CTFs are challenges for computer hackers.
*[NX]: Non eXecutable stack
*[PIE]: Position Independent Executable.
