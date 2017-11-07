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
