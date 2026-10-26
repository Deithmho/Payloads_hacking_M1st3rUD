# 🗡️ Configuración de seguridad incorrecta: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Cabeceras de respuestas relevantes

```text
Strict-Transport-Security
Content-Security-Policy
X-Content-Type-Options
Cache-Control
X-Frame-Options
```

**Cuándo usarlo:** Revisar respuestas finales de funciones sensibles; ausencia aislada no demuestra impacto.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html).


### Lectura rápida de cabeceras

```bash
curl -s -D - -o /dev/null "https://{ORIGEN}/account"
curl -s -D - -o /dev/null "https://{ORIGEN}/api/v1/me"
```

**Cuándo usarlo:** La ruta privada requiere sesión propia; la respuesta anónima puede ser distinta.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html).


## 🧭 Payloads por contexto

### Cache de una respuesta autenticada

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Cuándo usarlo:** Observar Cache-Control, Vary y una lectura desde B propio antes de declarar mezcla de sesiones.

**Fuente:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa8-security-misconfiguration/).


## 🔥 Payloads avanzados

### Método TRACE y debug acotado

```text
TRACE / HTTP/1.1
Host: {ORIGEN}
X-Canary: {NONCE}

GET /{RUTA_PROPIA}?debug=true
```

**Cuándo usarlo:** Un eco TRACE o stack genérico no basta: documentar efecto explotable y política del programa.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).


## 🔬 Pruebas guiadas por escenario

### 1. HSTS en respuesta HTTPS

**Objetivo:** Revisar política de transporte del host final.

```http
HEAD / HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Evaluar Strict-Transport-Security en HTTPS; ausencia sola no demuestra explotación.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html).

### 2. CSP en página sensible

**Objetivo:** Revisar directivas que protegen recursos y framing.

```http
GET /account HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar Content-Security-Policy real con cargas de la página; CSP ausente es defensa faltante, no XSS.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html).

### 3. Cache-Control en datos de sesión

**Objetivo:** Comprobar almacenamiento compartido de una respuesta privada.

```http
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Registrar Cache-Control y comportamiento del caché; header ausente sin mezcla de usuarios no basta.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html).

### 4. Método TRACE

**Objetivo:** Verificar exposición del método en el servidor bajo prueba.

```http
TRACE / HTTP/1.1
Host: {ORIGEN}
X-Canary: {NONCE}
```

**Interpretación:** Eco de una cabecera no prueba por sí mismo robo de sesión; correlacionar con navegador y controles.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).

### 5. Modo debug

**Objetivo:** Observar si un error de aplicación revela configuración interna.

```http
GET /{RUTA_DE_PRUEBA}?debug=true HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Debe documentarse dato sensible real o funcionalidad peligrosa; un stack trace genérico no siempre es crítico.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure).

### 6. Métodos anunciados

**Objetivo:** Comparar OPTIONS con métodos efectivamente permitidos y autorizados.

```http
OPTIONS /api/v1/items/{ID_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Allow es inventario; probar controles por método con objeto propio para concluir.

**Fuente técnica:** [OWASP API Security](https://api-security.owasp.org/editions/2023/en/0xa8-security-misconfiguration/).

### 7. Content-Type y nosniff

**Objetivo:** Comprobar el tipo de recursos que aceptan carga de usuario.

```http
GET /uploads/{ARCHIVO_PROPIO}.txt HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Buscar Content-Type adecuado y X-Content-Type-Options; confirmar un contexto de ejecución real.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
