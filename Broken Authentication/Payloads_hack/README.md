# 🗡️ Autenticación rota: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Ruta privada sin credenciales

**Objetivo:** Repetir una lectura privada propia sin cookie ni bearer token.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar con la respuesta autenticada de A. Un 200 de la SPA sin datos privados no confirma bypass.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication).

### 2. Sesión pendiente de MFA

**Objetivo:** Detener el login tras la contraseña y visitar directamente una función protegida.

```http
GET /api/account/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_MFA_PENDIENTE}
```

**Interpretación:** Solo es bypass si la sesión intermedia obtiene contenido o ejecuta acciones reservadas al estado autenticado.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication/multi-factor).

### 3. Logout y replay

**Objetivo:** Comprobar si el token propio previo sigue autorizando después de cerrar sesión.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_PROPIO_ANTES_DEL_LOGOUT}
```

**Interpretación:** Distinguir un token stateless todavía válido por diseño de una promesa explícita de revocación inmediata.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication/other-mechanisms).

### 4. Cambio de contraseña y sesión anterior

**Objetivo:** Tras cambiar la contraseña de A, intentar una request con la sesión antigua de A.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_A_ANTERIOR_AL_CAMBIO}
```

**Interpretación:** Verificar la política anunciada: algunos productos revocan todas las sesiones, otros permiten excepciones explícitas.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication/other-mechanisms).

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

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication/password-based).

### 6. Recordarme tras invalidar la sesión

**Objetivo:** Comprobar si un token remember-me propio restaura acceso cuando la sesión fue revocada.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: remember-me={TOKEN_RECORDAR_PROPIO}
```

**Interpretación:** El resultado depende de la política de revocación del producto. Documentar qué token creó la nueva sesión.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication/other-mechanisms).

### 7. Diferencia web/API

**Objetivo:** Usar el mismo estado anónimo en una ruta web y su operación API equivalente.

```http
GET /api/v1/profile HTTP/1.1
Host: {ORIGEN}
Accept: application/json
```

**Interpretación:** Una UI que redirige al login no protege automáticamente la API; confirmar datos privados en el cuerpo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
