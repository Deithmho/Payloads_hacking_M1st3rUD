# 🗡️ DOM clobbering: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. ID como global implícito

**Objetivo:** Comprobar si un nodo propio se expone como window.configPrueba.

```html
<a id="configPrueba" href="#prueba-123">marcador</a>
```

**Interpretación:** Observar typeof window.configPrueba; solo hay hallazgo si el JavaScript del sitio lo usa como configuración.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 2. name como global

**Objetivo:** Probar exposición mediante name en un elemento permitido.

```html
<form name="configPrueba"><input value="prueba-123"></form>
```

**Interpretación:** Verificar si window.configPrueba resuelve al formulario y si interfiere con un global esperado.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 3. Colección de anchors

**Objetivo:** Sobrescribir una propiedad de objeto mediante dos elementos con el mismo id.

```html
<a id="someObject"></a><a id="someObject" name="url" href="https://{CONTROLLED_HOST}/marcador.js"></a>
```

**Interpretación:** Este patrón requiere código que use someObject.url como fuente de script o recurso; una colección DOM sola no basta.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 4. Método submit sombreado

**Objetivo:** Comprobar si un input homónimo cambia la propiedad form.submit.

```html
<form id="formPrueba"><input name="submit" value="prueba-123"></form>
```

**Interpretación:** En DevTools, typeof formPrueba.submit puede dejar de ser function; el impacto depende de un uso real del método.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 5. Atributo de sanitizador sombreado

**Objetivo:** Reproducir en laboratorio el patrón documentado de properties clobbered.

```html
<form onclick="document.body.dataset.clobber=123"><input id="attributes">Prueba</form>
```

**Interpretación:** Solo aplica a un sanitizador cliente que itera element.attributes sin validar el tipo; confirmar ejecución controlada.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 6. Propiedad action de formulario

**Objetivo:** Medir colisión con propiedad de un formulario antes de buscar un gadget.

```html
<form id="formPrueba" action="/seguro"><input name="action" value="prueba-123"></form>
```

**Interpretación:** Comparar formPrueba.action con el atributo action; no inferir redirección ni exfiltración sin un uso posterior.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/dom-clobbering).

### 7. Tres niveles con form

**Objetivo:** Comprobar la cadena de propiedades HTMLCollection.form.input en Chrome.

```html
<form id="configPrueba" name="ruta"><input id="marcaPrueba" value="prueba-123"></form><form id="configPrueba"></form>
```

**Interpretación:** En Chrome, inspeccionar window.configPrueba.ruta.marcaPrueba.value. Otros navegadores pueden resolver distinto; requiere un gadget que use la cadena.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/research/dom-clobbering-strikes-back).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
