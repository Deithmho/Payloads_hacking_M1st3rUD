# 📖 Clickjacking: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una página puede embeber otra en un iframe y superponer elementos visuales para inducir un clic en controles que la víctima no percibe. Se requieren framing permitido y una acción susceptible de engaño.

El límite de confianza relevante es **una página sensible embebible frente a la composición visual del navegador**. La aplicación recibe **una página sensible embebible** y debería **restringir ancestros de frame**. La vulnerabilidad aparece cuando **el documento permite ser enmarcado por origen no confiable**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza una página sensible embebible en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en la composición visual del navegador.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el documento permite ser enmarcado por origen no confiable.
4. **Observación:** El iframe carga la página bajo un origen de prueba y el control queda accionable sin intervención de scripts del sitio.

## 🧭 Contextos y variantes

**Dónde buscar:** configuración de cuenta, permisos, paneles y confirmaciones con un solo clic.

| Variante | Diferencia técnica |
| --- | --- |
| **Superposición** | El control real se alinea bajo un señuelo. |
| **Multietapa** | Se necesitan varios clics o cambios de estado. |
| **Prellenado** | Parámetros de URL preparan una acción antes del clic. |

## 🔗 Cadenas y dependencias

Si existe XSS o una acción CSRF, clickjacking puede ampliar la entrega; no es necesario para explotar acciones que ya aceptan requests cruzadas.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Una página embebible sin acción sensible suele ser informativa. Demostrar un clic reversible y su efecto. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar una página sensible embebible y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en la composición visual del navegador.
- Confirmar: El iframe carga la página bajo un origen de prueba y el control queda accionable sin intervención de scripts del sitio.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Usar `Content-Security-Policy: frame-ancestors` con ancestros permitidos y `X-Frame-Options` de respaldo. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: clickjacking](https://portswigger.net/web-security/clickjacking) — framing y controles.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
