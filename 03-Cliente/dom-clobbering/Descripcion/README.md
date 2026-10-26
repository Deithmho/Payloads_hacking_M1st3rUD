# 📖 DOM clobbering: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Elementos HTML con `id` o `name` pueden aparecer como propiedades de `window` o de formularios. Si código JavaScript espera un objeto de configuración y toma en su lugar un nodo inyectado, el comportamiento cambia sin necesidad de insertar un `<script>`.

El límite de confianza relevante es **HTML permitido con id/name frente a lectura de propiedad global o de formulario**. La aplicación recibe **HTML permitido con id/name** y debería **verificar tipo y usar referencias explícitas**. La vulnerabilidad aparece cuando **un nodo inyectado sustituye una propiedad esperada**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza HTML permitido con id/name en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en lectura de propiedad global o de formulario.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si un nodo inyectado sustituye una propiedad esperada.
4. **Observación:** El script del sitio consume un nodo marcador como configuración y produce una acción observable; el nodo presente por sí solo no demuestra un gadget.

## 🧭 Contextos y variantes

**Dónde buscar:** comentarios HTML saneados, widgets y SPAs que usan globals.

| Variante | Diferencia técnica |
| --- | --- |
| **Global** | Un `id` crea una propiedad de `window`. |
| **Colección** | Dos nodos del mismo nombre forman colección con propiedades. |
| **Formulario** | Un input con nombre `submit` sustituye método del formulario. |

## 🔗 Cadenas y dependencias

Un gadget que usa `config.url` para cargar script puede convertir clobbering en XSS. Documentar la lectura y la carga, no asumirla por el HTML aceptado.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Es una primitive de confusión de objetos; la severidad nace del gadget, como carga de recurso o acción privilegiada. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar HTML permitido con id/name y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en lectura de propiedad global o de formulario.
- Confirmar: El script del sitio consume un nodo marcador como configuración y produce una acción observable; el nodo presente por sí solo no demuestra un gadget.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Comprobar tipos, evitar globals implícitos y usar sanitizadores probados que contemplen clobbering. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: DOM clobbering](https://portswigger.net/web-security/dom-based/dom-clobbering) — colisión de nombres y gadgets.
- [PortSwigger: DOM](https://portswigger.net/web-security/dom-based) — fuentes y sinks.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
