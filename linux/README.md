# Linux Pen Testing scripts and tutorials

## Return Oriented Programming and Buffer Overflow

Basic Attack Idea (x64):

needed: A binary which is vulnurable to Buffer Overflow. 

If the binary has input, we can test if it results into a Seg Fault if we overflow the space it was assigned to. 

We can check that using GDBs pattern create and offset 

for example if the offset is 500: 

```python
python -c 'print("A"*500+"B"*8+"C"*8)'
```
Ideally we check with gdb the registers which contain 0x4242424242 (B) and 0x4343434343 (C)
Then we can look if we can overtake the next address pointer: rsp. 
If we can do this we ca check if we can either call the libc system operative directly or if we have to caculate the adress.
If the binary uses system somewhere we can get the adress using Ghidra, or more lightweight objdump.

Then we only need to figure a gadget `pop rdi;` ideally `pop rdi; ret;` using Ropper. 
this will result in an hex adress we need to keep. 
If the binary has a string which contains /bin/sh or ends with sh we can use that as a shell. 
Simply search the adress using strings and keep it. 

Then we can construct our payload:

"A"*500 + pop_rdi_addr + shell_string_addr + sys_addr

Executing and we have a shell.



However if the system is not been called, we can leak the adress of any other libc call, as long as we have an output function and pop rdi

For example puts. 
We will search for puts using objdump. 

This will result into an plt_put_address and a got_put_address
f.e. 

```
  #PLT									#GOT
  401030:       ff 25 e2 2f 00 00       jmpq   *0x2fe2(%rip)        # 404018 <puts@GLIBC_2.2.5>
```

then we can leak the adress using the payload

"A"*500 + pop_rdi_addr + got_put_addr + plt_put_addr + plt_main

this will put the actual libc puts address into rdi and then will put it on screen from rdi using the puts command. 

By having the actual leaked puts adress, we can calculate the offset of the  other libc address. 

Thus we search the libc.so.6 file and search for puts, and the other addresses using readelf

```
offset = leaked_puts_addr - libc_puts 
sys = offset + libc_sys
sh = offset +libc_binsh
suid = offset + libc_suid
```

using these we can calculate our new payload.


"A"*500 + pop_rdi + p64(0) + suid + pop_rdi + sh + sys

thus setting rdi to 0, as suid will take the value of rdi to set the new uid to (0=root) and then put the /bin/sh string address in libc to rdi and call system with what is in rdi. 
Hence we have a root shell, if the s bit was set for the binary. 

Be aware that the leak adress will change each execution, so we have to add for an initial leak the main adress at the end too, to obtain a running system again in which we can overflow another time with the current leaked adress


The whole thing is pretty much doable in a simple pythin pwn tool script

### Putting User Input in .data 

If we have user input, but we cannot really search the libc addresses, as we are remote, we have to figure a way to gain a shell either way. 
We can do this, by simply adding /bin/sh\x00 to our input at the beginning, and using a ROP Chain to move this to a data segement where we know the adress of.  
This might be a little bit complicated, but we mostly need something like 

```
pop r14; 
pop r15; 
ret;
```
as a gadget and

```
MOV [r14] r15 
```

which will put the object in r15 at the address of r14. 

We have to search a good spoot for this though using readelf, so we wont override existing data. We are searching for 8 * 0x0 

### Objdump

If we search fo the libc system call we can use:

```
objdump -D binary | grep "system"
```

### pwntools

see pwn/skeleton.py for a the leak and pwn/skeleton_sys.py for the easy system /bin/sh script


### Ropper

ropper --search "pop rdi" -f binary

### gdb

### Ghidra

### strings

### readelf

## SSH 



