# 🗡️ Límites insuficientes de recursos en API: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Bordes de paginación de bajo impacto

```text
?limit=1
?limit=51
?limit=0
?page=2&limit=2
```

**Cuándo usarlo:** Elegir una línea de base y una variante por vez; reemplazar 51 por el límite publicado más uno, si se conoce. Verificar rechazo o truncado sin solicitar conjuntos grandes.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).


### Tamaño de lote mínimo

```text
[{"id":"{ID_PROPIO_1}"},{"id":"{ID_PROPIO_2}"}]
{"ids":["{ID_PROPIO_1}","{ID_PROPIO_2}"]}
```

**Cuándo usarlo:** Son dos formatos alternativos, no una carga alta; medir cuota por elemento si el endpoint acepta lotes.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).


## 🧭 Payloads por contexto

### GraphQL profundidad y alias acotados

```graphql
query { viewer { projects(first:1) { nodes { id } } } }
query { a: viewer { id } b: viewer { id } }
```

**Cuándo usarlo:** Adaptar al esquema; no generar consultas recursivas ni elevar volumen.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/graphql).


## 🔥 Payloads avanzados

### Expansión y cursor inválido

```text
GET /api/v1/items?limit=2&expand=children
GET /api/v1/items?cursor=canary-{NONCE}&limit=2
```

**Cuándo usarlo:** Comparar tamaño y tiempo con solicitudes válidas bajo un presupuesto seguro; una latencia aislada no prueba DoS.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).


## 🔬 Pruebas guiadas por escenario

### 1. Límite de página

**Objetivo:** Comparar respuesta para límites pequeños, sin agotar recursos.

```text
GET /api/v1/items?limit=1
GET /api/v1/items?limit=51
```

**Interpretación:** Hacer solo dos solicitudes y verificar tope documentado; un 200 con 51 ítems no demuestra impacto.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).

### 2. Límite negativo

**Objetivo:** Comprobar que valores fuera de rango se rechazan.

```http
GET /api/v1/items?limit=-1 HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** No inferir consumo excesivo del código de estado: comprobar tamaño y tiempo dentro de un umbral seguro.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).

### 3. Profundidad GraphQL acotada

**Objetivo:** Verificar profundidad máxima con una consulta de tres niveles.

```graphql
query { viewer { projects(first:1) { nodes { id } } } }
```

**Interpretación:** Adaptar al esquema. No generar consultas recursivas ni elevar profundidad hasta saturar el servicio.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 4. Alias doble

**Objetivo:** Comprobar si dos operaciones en una petición cuentan para la cuota.

```graphql
query { a: viewer { id } b: viewer { id } }
```

**Interpretación:** Solo dos alias; medir coste/cupo en cuenta propia sin hacer pruebas de carga.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).

### 5. Lote JSON de dos elementos

**Objetivo:** Verificar límite de tamaño de lote y autorización por elemento.

```json
[{"id":"{ID_PROPIO_1}"},{"id":"{ID_PROPIO_2}"}]
```

**Interpretación:** Aceptar lotes puede ser correcto; informar solo si se evita una cuota o se produce efecto medible.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).

### 6. Tamaño de subida permitido

**Objetivo:** En un laboratorio con máximo publicado de 1 KiB, enviar solo un byte adicional.

```bash
head -c 1025 /dev/zero | curl -i -X POST -H "Authorization: Bearer {TOKEN_A}" -H "Content-Type: application/octet-stream" --data-binary @- "https://{ORIGEN}/api/v1/uploads"
```

**Interpretación:** Ejecutar solo si 1 KiB es el límite publicado en el lab; adaptar a un máximo pequeño y comprobar rechazo temprano.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).

### 7. Expansión de relaciones acotada

**Objetivo:** Comprobar que expand no omite el límite de elementos.

```http
GET /api/v1/items?limit=2&expand=children HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar con limit=2 sin expansión. Una relación de dos hijos puede ser legítima; medir tope y coste.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).

### 8. Paginación por cursor

**Objetivo:** Comprobar que un cursor inválido no causa trabajo excesivo.

```http
GET /api/v1/items?cursor=canary-{NONCE}&limit=2 HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar latencia con cursor válido una sola vez; variación aislada no prueba agotamiento.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).

### 9. Página fuera del rango documentado

**Objetivo:** Comprobar rechazo o truncado de paginación sin carga alta.

```http
GET /api/v1/items?page=1001&limit=2 HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Ejecutar solo si el máximo de página publicado es 1000 y el backend usa paginación por página.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/).

### 10. Costo GraphQL con dos campos

**Objetivo:** Comprobar si el límite de complejidad suma campos anidados.

```graphql
query { viewer { projects(first:1) { nodes { id } } teams(first:1) { nodes { id } } } }
```

**Interpretación:** Consulta pequeña de control; adaptar al esquema y no inducir recursión ni pruebas de carga.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
