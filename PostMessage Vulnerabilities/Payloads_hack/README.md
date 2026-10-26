# 🗡️ Vulnerabilidades de postMessage: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Mensaje desde origen externo

**Objetivo:** Comprobar si un receptor procesa eventos sin validar Origin.

```html
<iframe id="destino" src="https://{ORIGEN}/widget"></iframe><script>const f=document.getElementById('destino');f.onload=()=>f.contentWindow.postMessage({type:'probe',value:'prueba-123'},'https://{ORIGEN}')</script>
```

**Interpretación:** Observar una acción concreta; el hecho de enviar un mensaje no implica que el receptor lo acepte.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 2. Bypass de contains

**Objetivo:** Probar validador que usa indexOf/contains sobre event.origin.

```text
https://{SUBDOMINIO_PERMITIDO}.{CONTROLLED_HOST}
```

**Interpretación:** Hospedar el emisor en ese dominio propio y verificar que el receptor actúa; requiere observar comparación defectuosa.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 3. Bypass de endsWith

**Objetivo:** Probar validador que acepta sufijo textual sin frontera DNS.

```text
https://{PREFIJO_CONTROLADO}{DOMINIO_PERMITIDO}
```

**Interpretación:** El host debe estar realmente bajo control del auditor; solo tiene sentido si el código usa endsWith sin delimitador.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 4. Datos hacia HTML

**Objetivo:** Probar un sink innerHTML del receptor con canary inocuo.

```js
destino.contentWindow.postMessage('<img src=x onerror="document.body.dataset.msg=123">','https://{ORIGEN}')
```

**Interpretación:** Confirmar ejecución en el origen receptor; el mensaje puede ser rechazado por esquema o CSP.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 5. Datos hacia eval

**Objetivo:** Probar solo si el código del receptor llama eval con event.data.

```js
destino.contentWindow.postMessage("document.body.dataset.msg='prueba-123'",'https://{ORIGEN}')
```

**Interpretación:** Un dato textual reflejado no basta; observar el sink y el efecto bajo la sesión de prueba.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 6. Destino wildcard del emisor

**Objetivo:** Registrar si la app entrega datos privados a un popup no confiable.

```js
addEventListener('message', e => console.log(e.origin, typeof e.data, JSON.stringify(e.data).length));
```

**Interpretación:** Usar un flujo propio que abra la ventana controlada; no registrar contenido privado completo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 7. Confusión de ventana source

**Objetivo:** Enviar el mismo tipo de mensaje desde dos iframes de origen distinto.

```js
marcoA.contentWindow.postMessage({type:'probe',value:'A'},'https://{ORIGEN}'); marcoB.contentWindow.postMessage({type:'probe',value:'B'},'https://{ORIGEN}');
```

**Interpretación:** Comparar event.origin y event.source en el receptor; se requiere que la aplicación confíe en la ventana incorrecta.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

### 8. URL recibida

**Objetivo:** Comprobar navegación inducida por un mensaje no confiable.

```js
destino.contentWindow.postMessage({type:'navigate',url:'https://{CONTROLLED_HOST}/prueba'},'https://{ORIGEN}')
```

**Interpretación:** Adaptar el tipo al handler observado. Un cambio de Location confirma el sink; valorar open redirect por separado.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
