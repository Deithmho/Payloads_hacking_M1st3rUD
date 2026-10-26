# 📖 DNS rebinding: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un nombre controlado resuelve primero a una IP pública permitida y después a una IP interna. Si un cliente valida DNS una vez pero conecta después de resolver de nuevo, la conexión puede llegar a un destino prohibido.

El límite de confianza relevante es **dominio y respuestas DNS controladas frente a validador de URL y conexión posterior**. La aplicación recibe **dominio y respuestas DNS controladas** y debería **validar IP de cada conexión y bloquear redes internas en egress**. La vulnerabilidad aparece cuando **la IP cambia entre comprobación y uso**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza dominio y respuestas DNS controladas en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en validador de URL y conexión posterior.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si la IP cambia entre comprobación y uso.
4. **Observación:** En laboratorio, un resolver y servidor propios muestran dos resoluciones y la IP efectivamente conectada; no apuntar a servicios internos reales.

## 🧭 Contextos y variantes

**Dónde buscar:** SSRF, navegadores con servicios locales, webhooks y clientes HTTP.

| Variante | Diferencia técnica |
| --- | --- |
| **TOCTOU** | Validación y conexión resuelven en momentos distintos. |
| **Redirect** | Un salto introduce otro hostname con resolución diferente. |
| **Browser rebinding** | El navegador conserva origen por nombre mientras cambia la IP. |

## 🔗 Cadenas y dependencias

DNS rebinding es un camino de bypass de SSRF cuando existe una función fetch; sin fetch o servicio local expuesto, no hay impacto demostrado.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

La severidad depende del servicio alcanzado y de sus controles propios; un TTL corto no es vulnerabilidad. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar dominio y respuestas DNS controladas y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en validador de URL y conexión posterior.
- Confirmar: En laboratorio, un resolver y servidor propios muestran dos resoluciones y la IP efectivamente conectada; no apuntar a servicios internos reales.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Fijar conexión a IP validada, revalidar redirecciones, bloquear rangos internos y autenticar servicios locales. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: SSRF](https://portswigger.net/web-security/ssrf) — variantes y confirmación.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
