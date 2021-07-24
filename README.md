# pen-testing
Pen Testing Scripts and install stuff


## Attacks

### SNMP
scan via UDP on port 161 

snmpwalk -v 1 (or 2c) -c $FUZZ (public is often)  IP
check OIDs and check for right side OIDS

### Pass the Hash
https://en.wikipedia.org/wiki/Pass_the_hash

https://blog.stealthbits.com/passing-the-hash-with-mimikatz


## Interesting CVEs 

### WhatsApp
CVE-2019-11932 - https://awakened1712.github.io/hacking/hacking-whatsapp-gif-rce/ and https://www.youtube.com/watch?v=loCq8OTZEGI - patched in version >= 2.19.244 
