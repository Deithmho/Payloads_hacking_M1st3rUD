# 📖 Vulnerabilidades de postMessage: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

`window.postMessage` cruza orígenes deliberadamente. Un receptor que no valida `event.origin` y `event.source`, o un emisor que usa `*` con datos privados, rompe esa frontera.

El límite de confianza relevante es **mensajes entre ventanas o frames frente a handler `message` y destino de envío**. La aplicación recibe **mensajes entre ventanas o frames** y debería **validar origen, emisor y esquema de mensaje**. La vulnerabilidad aparece cuando **se acepta o envía contenido sensible hacia origen inesperado**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza mensajes entre ventanas o frames en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en handler `message` y destino de envío.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se acepta o envía contenido sensible hacia origen inesperado.
4. **Observación:** Una ventana de prueba recibe un mensaje propio o provoca una acción inocua solo cuando su origen se acepta indebidamente.

## 🧭 Contextos y variantes

**Dónde buscar:** SSO en popups, widgets, iframes, pagos y SPAs.

| Variante | Diferencia técnica |
| --- | --- |
| **Receptor laxo** | Procesa mensajes desde cualquier origen. |
| **Emisor comodín** | Envía secretos con targetOrigin `*`. |
| **Parser de datos** | Inserta `event.data` en un sink DOM inseguro. |

## 🔗 Cadenas y dependencias

Un receptor laxo unido a `innerHTML` puede convertirse en DOM XSS; se necesitan tanto el origen no confiable como el sink ejecutable.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Depende de datos filtrados o acciones realizadas. El mero uso de `postMessage` no es hallazgo. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar mensajes entre ventanas o frames y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en handler `message` y destino de envío.
- Confirmar: Una ventana de prueba recibe un mensaje propio o provoca una acción inocua solo cuando su origen se acepta indebidamente.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Fijar `targetOrigin` exacto, validar `event.origin/source` y schema de `event.data`, evitar sinks HTML. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: DOM](https://portswigger.net/web-security/dom-based) — fuentes y sinks.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
