# 📖 Cross-Site WebSocket Hijacking: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

El handshake WebSocket puede incluir cookies de sesión. Si el servidor no valida `Origin` y la sesión llega desde un sitio externo, JavaScript de ese sitio puede abrir el canal y leer mensajes.

El límite de confianza relevante es **`Origin` del handshake y cookie del navegador frente a el upgrade WebSocket**. La aplicación recibe **`Origin` del handshake y cookie del navegador** y debería **validar origen, sesión y autorización por mensaje**. La vulnerabilidad aparece cuando **se acepta un handshake cruzado con sesión válida**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza `Origin` del handshake y cookie del navegador en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el upgrade WebSocket.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se acepta un handshake cruzado con sesión válida.
4. **Observación:** Una página de origen controlado recibe un mensaje propio tras abrir WebSocket con cookies del navegador.

## 🧭 Contextos y variantes

**Dónde buscar:** chats, notificaciones, paneles en tiempo real y dashboards.

| Variante | Diferencia técnica |
| --- | --- |
| **Handshake** | Se omite validación de origen. |
| **Mensajes** | El upgrade se autoriza pero comandos individuales no. |
| **SameSite** | La política de cookie puede impedir que se envíe sesión cross-site. |

## 🔗 Cadenas y dependencias

Si además un mensaje permite IDOR, el canal puede leer datos ajenos; primero probar origen y luego autorización por objeto.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Depende de datos y acciones accesibles por canal. Un `101 Switching Protocols` sin cookie ni mensajes sensibles no basta. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar `Origin` del handshake y cookie del navegador y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el upgrade WebSocket.
- Confirmar: Una página de origen controlado recibe un mensaje propio tras abrir WebSocket con cookies del navegador.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Validar `Origin` en handshake, cookies adecuadas y permisos en cada mensaje. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: WebSockets](https://portswigger.net/web-security/websockets) — handshake y autorización.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
