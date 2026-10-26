# 🗡️ CORS con credenciales: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Orígenes a probar uno por solicitud

```text
Origin: https://{ORIGEN_CONTROLADO}
Origin: null
Origin: https://{DOMINIO_CONFIABLE}.{ORIGEN_CONTROLADO}
Origin: http://{SUBDOMINIO_CONFIABLE}
Origin: https://{SUBDOMINIO_CONFIABLE}:8443
```

**Cuándo usarlo:** Una línea por solicitud; origen incluye esquema, host y puerto. El prefijo confiable bajo {ORIGEN_CONTROLADO} es dominio propio; HTTP confiable exige control/intercepción real. Comprobar cookies y respuesta privada.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cors).


### Cabeceras de lectura y caché

```text
Access-Control-Allow-Origin: https://{ORIGEN_CONTROLADO}
Access-Control-Allow-Credentials: true
Vary: Origin
```

**Cuándo usarlo:** ACAO exacto y ACAC:true habilitan lectura si el navegador envía la cookie y la respuesta es privada. Vary: Origin importa al cachear ACAO dinámico; ACAO:* queda bloqueado.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cors/access-control-allow-origin).


## 🧭 Payloads por contexto

### Prueba en navegador sin imprimir el perfil

```javascript
fetch("https://{ORIGEN}/api/v1/me", {credentials:"include"})
  .then(async r => console.log({status:r.status,
    canary:(await r.text()).includes("prueba-123")}))
  .catch(e => console.log(e.name));
```

**Cuándo usarlo:** Colocar prueba-123 antes en el perfil de la cuenta propia y ejecutar desde origen controlado. Registrar solo el booleano, nunca el cuerpo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cors).


## 🔥 Payloads avanzados

### Preflight para cabecera Authorization

```http
OPTIONS /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{ORIGEN_CONTROLADO}
Access-Control-Request-Method: GET
Access-Control-Request-Headers: authorization
```

**Cuándo usarlo:** Un preflight aceptado no basta: confirmar petición real y que el navegador disponga del token.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cors).


## 🔬 Pruebas guiadas por escenario

### 1. Origin ajeno con sesión

**Objetivo:** Comprobar si un origen propio se refleja con credenciales.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{ORIGEN_CONTROLADO}
Cookie: session={COOKIE_A}
```

**Interpretación:** Se necesita ACAO igual al origen, ACAC true y lectura en navegador; curl solo inspecciona cabeceras.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cors).

### 2. Lectura real desde navegador

**Objetivo:** Confirmar que JS de un origen propio lee el marcador prueba-123 del perfil de la cuenta A.

```javascript
fetch("https://{ORIGEN}/api/v1/me", {credentials:"include"}).then(async r => console.log(r.status, (await r.text()).includes("prueba-123")));
```

**Interpretación:** Ejecutar en origen controlado con cuenta propia; registrar solo el booleano, sin imprimir el cuerpo ni transmitirlo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cors).

### 3. Origen null

**Objetivo:** Verificar si se confía en documentos de origen opaco.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: null
Cookie: session={COOKIE_A}
```

**Interpretación:** ACAO:null y ACAC:true son candidatos; aún hay que reproducir lectura en navegador y política de cookies.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cors).

### 4. Prefijo de host confiable

**Objetivo:** Detectar comparación por prefijo que acepta un host propio bajo otro dominio.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{DOMINIO_CONFIABLE}.{ORIGEN_CONTROLADO}
Cookie: session={COOKIE_A}
```

**Interpretación:** El host efectivo pertenece a {ORIGEN_CONTROLADO}, no a {DOMINIO_CONFIABLE}. Requiere lectura sensible efectiva en navegador.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cors).

### 5. Esquema HTTP de host confiable

**Objetivo:** Comprobar si se confía en un origen sin TLS.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: http://{SUBDOMINIO_CONFIABLE}
Cookie: session={COOKIE_A}
```

**Interpretación:** Riesgo requiere que el subdominio HTTP pueda ser controlado/interceptado y cookies se envíen.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cors).

### 6. Puerto distinto

**Objetivo:** Verificar si la lista de orígenes ignora el puerto.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{SUBDOMINIO_CONFIABLE}:8443
Cookie: session={COOKIE_A}
```

**Interpretación:** Origen incluye esquema, host y puerto; documentar posibilidad real de operar el puerto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cors).

### 7. Preflight con cabecera de autorización

**Objetivo:** Evaluar política de solicitudes no simples.

```http
OPTIONS /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{ORIGEN_CONTROLADO}
Access-Control-Request-Method: GET
Access-Control-Request-Headers: authorization
```

**Interpretación:** Preflight permisivo por sí solo no entrega datos; contrastar solicitud real y token disponible al navegador.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cors).

### 8. Wildcard con credenciales

**Objetivo:** Descartar falso positivo de ACAO asterisco.

```text
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

**Interpretación:** El navegador rechaza esta combinación para fetch con credentials:include; no reportarla como lectura exitosa.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cors/access-control-allow-origin).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
