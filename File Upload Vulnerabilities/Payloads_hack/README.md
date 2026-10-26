# 🗡️ Vulnerabilidades de subida de archivos: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

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

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/file-upload).

### 2. Firma de archivo frente a extensión

**Objetivo:** Comprobar si el backend mira magic bytes y formato completo.

```bash
printf "CANARY-{NONCE}" > canary.png; file canary.png
```

**Interpretación:** Subir solo a cuenta propia. Si se acepta por extensión, evaluar cómo se sirve; no declarar ejecución.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

### 3. Doble extensión

**Objetivo:** Observar cómo normaliza nombre el almacenamiento y el servidor.

```text
canary.php.jpg
```

**Interpretación:** Usar contenido inerte y registrar nombre final/Content-Type; la extensión por sí sola no prueba RCE.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/file-upload).

### 4. Mayúsculas en extensión

**Objetivo:** Detectar listas negras sensibles a capitalización.

```text
canary.PhP
```

**Interpretación:** Solo en laboratorio que permita extensiones ejecutables; no subir código activo a servicios compartidos.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

### 5. Punto o espacio final

**Objetivo:** Comprobar normalización de nombre entre sistema de archivos y servidor.

```text
canary.jpg.
canary.jpg%20
```

**Interpretación:** Comparar el nombre almacenado y el nombre servido; depende de sistema operativo y proxy.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

### 6. SVG con marcador DOM

**Objetivo:** Comprobar si SVG subido se sirve como contenido activo en mismo origen.

```xml
<svg xmlns="http://www.w3.org/2000/svg" onload="document.body.dataset.prueba='CANARY-{NONCE}'"></svg>
```

**Interpretación:** Usar solo un archivo propio; verificar ejecución en navegador y origen. `Content-Disposition: attachment` puede impedirla.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/file-upload).

### 7. Nombre con traversal

**Objetivo:** Verificar que filename no controla la ruta de almacenamiento.

```http
Content-Disposition: form-data; name="file"; filename="../canary-{NONCE}.txt"
```

**Interpretación:** El backend debe renombrar o rechazar. Comprobar únicamente directorios de laboratorio propios.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

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

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/file-upload).

### 9. Archivo comprimido con entrada segura

**Objetivo:** Establecer control antes de probar extracción.

```python
import zipfile
with zipfile.ZipFile("control.zip","w") as z:
    z.writestr("carpeta/canary.txt","CANARY-{NONCE}")
```

**Interpretación:** El contenido debe quedar dentro del directorio de extracción; ver Zip Slip para path traversal.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files).

### 10. Content-Type servido

**Objetivo:** Confirmar que el navegador no recibe HTML activo del mismo origen.

```bash
curl -I "https://{ORIGEN}/uploads/canary-{NONCE}.txt"
```

**Interpretación:** Comprobar `Content-Type`, `Content-Disposition` y origen de entrega; HEAD puede diferir de GET.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/file-upload).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
