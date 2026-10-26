# 📖 SSRF mediante webhooks: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un webhook configurable recibe una URL y el servidor envía eventos a ella. Aunque la URL inicial esté validada, DNS o redirecciones pueden llevar el envío a otro destino; además el payload puede incluir datos sensibles.

El límite de confianza relevante es **URL de callback configurada por usuario frente a worker de webhooks**. La aplicación recibe **URL de callback configurada por usuario** y debería **validar destino y limitar egress en cada entrega**. La vulnerabilidad aparece cuando **el worker conecta a host no autorizado o adjunta secretos**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza URL de callback configurada por usuario en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en worker de webhooks.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el worker conecta a host no autorizado o adjunta secretos.
4. **Observación:** El endpoint propio recibe un evento de prueba y se inspeccionan redirecciones y datos mínimos, sin solicitar redes internas.

## 🧭 Contextos y variantes

**Dónde buscar:** SaaS, pagos, CI/CD, automatización e integraciones.

| Variante | Diferencia técnica |
| --- | --- |
| **Entrega inicial** | La URL se solicita al registrarla. |
| **Entrega de evento** | El worker envía datos cuando ocurre un evento. |
| **Redirección** | El cliente HTTP sigue Location a host distinto. |
| **DNS rebinding** | La IP cambia entre validación y entrega. |

## 🔗 Cadenas y dependencias

Una URL de webhook que acepta redirecciones puede permitir SSRF; un token enviado en el evento puede incrementar exposición aunque el destino sea externo.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Solo callback a host propio puede ser funcionalidad esperada. Impacto requiere destino prohibido o datos enviados indebidamente. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar URL de callback configurada por usuario y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en worker de webhooks.
- Confirmar: El endpoint propio recibe un evento de prueba y se inspeccionan redirecciones y datos mínimos, sin solicitar redes internas.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Allowlist de destinos cuando sea posible, resolver y validar IP en cada conexión, bloquear redes internas y limitar datos del evento. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: SSRF](https://portswigger.net/web-security/ssrf) — variantes y confirmación.
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) — clasificación de riesgos API.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
