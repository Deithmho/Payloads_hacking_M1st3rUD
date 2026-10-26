# 🗡️ SSRF mediante webhooks: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Callback HTTPS controlado

**Objetivo:** Confirmar si el servicio solicita la URL configurada.

```json
{"callbackUrl":"https://{RECEPTOR_PROPIO}/webhook/{NONCE}"}
```

**Interpretación:** Un callback esperado no es SSRF. Anotar método, cabeceras y origen de conexión sin guardar secretos.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa7-server-side-request-forgery/).

### 2. URL en parámetro alterno

**Objetivo:** Comprobar si un parámetro de prueba inicia una segunda solicitud servidor.

```http
POST /api/v1/webhooks/test?url=https%3A%2F%2F{RECEPTOR_PROPIO}%2Falt%2F{NONCE} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Solo usar el parámetro si existe. Un DNS aislado sin HTTP no prueba acceso a recursos internos.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/ssrf/blind).

### 3. Redirección a segundo host propio

**Objetivo:** Determinar si se sigue un 302 y se revalida el destino.

```text
callbackUrl = https://{RECEPTOR_PROPIO}/redir/{NONCE}
302 Location: https://{SEGUNDO_RECEPTOR_PROPIO}/final/{NONCE}
```

**Interpretación:** Ambos destinos bajo control y dentro del alcance. Seguir 302 puede ser funcionalidad esperada; evaluar política.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/ssrf).

### 4. Esquema no permitido

**Objetivo:** Confirmar que solo se aceptan esquemas HTTP(S).

```json
{"callbackUrl":"file:///tmp/canary-propio.txt"}
```

**Interpretación:** No leer archivos sensibles; rechazo de file: confirma una validación concreta, no todas las rutas SSRF.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa7-server-side-request-forgery/).

### 5. Loopback de laboratorio

**Objetivo:** Probar bloqueo de destinos locales sin usar servicios de terceros.

```json
{"callbackUrl":"http://127.0.0.1:{PUERTO_CANARY_LAB}/health"}
```

**Interpretación:** Solo en laboratorio o entorno propio con servicio canary. No explorar puertos internos ajenos.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/ssrf).

### 6. Destino en campo anidado

**Objetivo:** Comprobar validación también cuando la URL está en un objeto de eventos.

```json
{"event":"canary","delivery":{"target":"https://{RECEPTOR_PROPIO}/nested/{NONCE}"}}
```

**Interpretación:** Usar únicamente si el esquema acepta delivery.target; comparar con callbackUrl legítimo.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa7-server-side-request-forgery/).

### 7. Credenciales en URL

**Objetivo:** Comprobar que se rechazan URL con userinfo ambiguo.

```json
{"callbackUrl":"https://usuario@{RECEPTOR_PROPIO}/userinfo/{NONCE}"}
```

**Interpretación:** Observar destino real en receptor propio. Una discrepancia de parser requiere un límite de destino relevante.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/ssrf).

### 8. Fragmento en URL

**Objetivo:** Verificar normalización de la URL antes del filtro de destinos.

```json
{"callbackUrl":"https://{RECEPTOR_PROPIO}/fragmento%23canary"}
```

**Interpretación:** Comparar URL aceptada y solicitud recibida; diferencias de codificación por sí solas no prueban SSRF.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/ssrf).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
