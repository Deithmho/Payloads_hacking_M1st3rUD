# 📖 Cross-Site Request Forgery (CSRF): descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un navegador puede enviar cookies de una sesión al visitar otra página. Si una acción de estado acepta esa solicitud sin una prueba ligada a la sesión, el sitio de origen externo puede inducirla.

El límite de confianza relevante es **una acción autenticada que cambia estado frente a el navegador con cookies de sesión**. La aplicación recibe **una acción autenticada que cambia estado** y debería **validar token CSRF, origen y SameSite según flujo**. La vulnerabilidad aparece cuando **el servidor acepta la acción solo por la cookie adjunta**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza una acción autenticada que cambia estado en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el navegador con cookies de sesión.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el servidor acepta la acción solo por la cookie adjunta.
4. **Observación:** Una cuenta propia realiza una acción reversible iniciada desde un origen de prueba diferente.

## 🧭 Contextos y variantes

**Dónde buscar:** formularios web, endpoints JSON permisivos y acciones GET con efectos.

| Variante | Diferencia técnica |
| --- | --- |
| **Sin token** | La acción no exige secreto por solicitud. |
| **Token desligado** | Token de otra sesión se acepta. |
| **SameSite** | Lax/Strict cambian cuándo se envía cookie, pero no reemplazan diseño seguro. |

## 🔗 Cadenas y dependencias

XSS en el mismo origen permite leer o solicitar tokens y puede superar la protección CSRF; se reporta el eslabón XSS por separado.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Depende de la acción inducida. Cambiar preferencias menores difiere de cambiar email o transferir fondos. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar una acción autenticada que cambia estado y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el navegador con cookies de sesión.
- Confirmar: Una cuenta propia realiza una acción reversible iniciada desde un origen de prueba diferente.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Exigir tokens impredecibles ligados a sesión, validar `Origin`/`Referer` cuando aplique y evitar efectos en GET. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: CSRF](https://portswigger.net/web-security/csrf) — precondiciones y mitigaciones.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
