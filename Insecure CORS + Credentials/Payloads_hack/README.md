# 🗡️ CORS con credenciales: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Origin ajeno con sesión

**Objetivo:** Comprobar si un origen propio se refleja con credenciales.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{ORIGEN_CONTROLADO}
Cookie: session={COOKIE_A}
```

**Interpretación:** Se necesita ACAO igual al origen, ACAC true y lectura en navegador; curl solo inspecciona cabeceras.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 2. Lectura real desde navegador

**Objetivo:** Confirmar que JS de un origen propio lee datos de la cuenta A.

```javascript
fetch("https://{ORIGEN}/api/v1/me", {credentials:"include"}).then(r=>r.text()).then(t=>console.log(t.slice(0,80)));
```

**Interpretación:** Ejecutar en origen controlado con cuenta propia; no transmitir el cuerpo a terceros.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 3. Origen null

**Objetivo:** Verificar si se confía en documentos de origen opaco.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: null
Cookie: session={COOKIE_A}
```

**Interpretación:** ACAO:null y ACAC:true son candidatos; aún hay que reproducir lectura en navegador y política de cookies.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 4. Subdominio parecido

**Objetivo:** Detectar comparación de sufijo no anclada.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{DOMINIO_CONFIABLE}.{ORIGEN_CONTROLADO}
Cookie: session={COOKIE_A}
```

**Interpretación:** Solo si el servidor refleja el origen y el navegador lee respuesta sensible hay impacto.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 5. Esquema HTTP de host confiable

**Objetivo:** Comprobar si se confía en un origen sin TLS.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: http://{SUBDOMINIO_CONFIABLE}
Cookie: session={COOKIE_A}
```

**Interpretación:** Riesgo requiere que el subdominio HTTP pueda ser controlado/interceptado y cookies se envíen.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 6. Puerto distinto

**Objetivo:** Verificar si la lista de orígenes ignora el puerto.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{SUBDOMINIO_CONFIABLE}:8443
Cookie: session={COOKIE_A}
```

**Interpretación:** Origen incluye esquema, host y puerto; documentar posibilidad real de operar el puerto.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

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

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 8. Wildcard con credenciales

**Objetivo:** Descartar falso positivo de ACAO asterisco.

```text
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

**Interpretación:** El navegador rechaza esta combinación para fetch con credentials:include; no reportarla como lectura exitosa.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors/access-control-allow-origin).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
