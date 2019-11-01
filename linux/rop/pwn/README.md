
# SKELETON

Skeleton tries to automize the shell retrieval pwnage of a binary as much as possible using

* pwntools
* ROPGadget
* readelf
* objdump

thus you only have to execute:

```
./skeleton64.py /path/to/binary JUNK_SIZE /path/to/libc [-s]
```

JUNK_SIZE represents the amount of JUNK you have to input before the binaries uses a SEGFAULT

-s is used to setuid to 0 if possible 

using 
```
echo "gdb" > .skeleton 
```
will launch gdb 

whereas 

```
echo "ssh HOST[USER:PASSWORD]" > .skeleton
```
uses remote ssh to exec the binary. 
Be aware that you have to set the addresses yourself for ssh pwnage, also do not forget the path of the binary is the path on the remote server.



