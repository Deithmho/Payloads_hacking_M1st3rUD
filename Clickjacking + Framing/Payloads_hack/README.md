# 🗡️ Clickjacking y framing: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Cabeceras de la acción sensible

**Objetivo:** Revisar políticas de framing en la respuesta final.

```http
GET /account/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_A}
```

**Interpretación:** Evaluar CSP frame-ancestors y X-Frame-Options de esa ruta, no solo de la portada.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/clickjacking).

### 2. Iframe de laboratorio

**Objetivo:** Comprobar que una página sensible puede cargarse desde origen propio.

```html
<iframe src="https://{ORIGEN}/account/settings" width="900" height="600"></iframe>
```

**Interpretación:** Comprobarlo en navegador con sesión propia; un iframe bloqueado no demuestra clickjacking.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/clickjacking).

### 3. Marco con marcador visible

**Objetivo:** Relacionar coordenadas de una acción reversible con el marco.

```html
<div style="position:absolute;top:80px;left:80px">CANARY-{NONCE}</div>
<iframe src="https://{ORIGEN}/account/settings" style="width:900px;height:600px;opacity:.6"></iframe>
```

**Interpretación:** La transparencia facilita revisión; demostrar interacción real solo sobre configuración propia reversible.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/clickjacking).

### 4. CSP frame-ancestors

**Objetivo:** Comparar política declarada con el origen del PoC.

```text
Content-Security-Policy: frame-ancestors 'self' https://{ORIGEN_CONFIABLE}
```

**Interpretación:** La directiva debe llegar en la respuesta enmarcada. No inferir protección por meta tag.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/clickjacking).

### 5. X-Frame-Options

**Objetivo:** Comprobar protección heredada para navegadores relevantes.

```text
X-Frame-Options: DENY
X-Frame-Options: SAMEORIGIN
```

**Interpretación:** Son valores alternativos, no dos cabeceras simultáneas. Verificar comportamiento en navegador objetivo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/clickjacking).

### 6. Variación por ruta

**Objetivo:** Detectar si una ruta de confirmación omite política presente en la vista.

```text
GET /account/settings
GET /account/settings/confirm
```

**Interpretación:** Ambas rutas requieren sesión propia; una cabecera distinta solo importa si se puede inducir una acción.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/clickjacking).

### 7. Frame con sandbox

**Objetivo:** Verificar si una defensa JavaScript depende del contexto de frame.

```html
<iframe sandbox="allow-forms allow-scripts" src="https://{ORIGEN}/account/settings"></iframe>
```

**Interpretación:** Algunos frame busters fallan con sandbox; confirmar que cookies y acción funcionan antes de concluir.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/clickjacking).

### 8. Control de interacción

**Objetivo:** Comparar clic genuino y clic sobre marco en la misma cuenta.

```text
Control: cambiar etiqueta del objeto propio desde la página original.
Prueba: repetir con iframe y botón canary alineado.
```

**Interpretación:** Registrar estado antes/después y revertir. La posibilidad de enmarcar sin clic inducido no confirma impacto.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/clickjacking).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
