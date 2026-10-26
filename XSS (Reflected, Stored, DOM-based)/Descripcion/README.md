# 📖 Cross-Site Scripting (XSS): descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

XSS ocurre cuando datos no confiables se insertan en un contexto HTML o JavaScript sin codificación adecuada. El navegador interpreta esos datos como código con el origen de la aplicación.

El límite de confianza relevante es **un parámetro, contenido guardado o fuente DOM frente a un sink HTML/JS del navegador**. La aplicación recibe **un parámetro, contenido guardado o fuente DOM** y debería **codificar según contexto y sanear HTML permitido**. La vulnerabilidad aparece cuando **el dato alcanza un sink ejecutable**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un parámetro, contenido guardado o fuente DOM en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en un sink HTML/JS del navegador.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el dato alcanza un sink ejecutable.
4. **Observación:** Un marcador ejecuta una acción inocua en el origen afectado; el reflejo de etiquetas sin ejecución no basta.

## 🧭 Contextos y variantes

**Dónde buscar:** formularios, comentarios, perfiles, SPAs y renderizado de respuestas API.

| Variante | Diferencia técnica |
| --- | --- |
| **Reflected** | La entrada vuelve en la respuesta inmediata. |
| **Stored** | Se guarda y se muestra a otra vista o sesión. |
| **DOM-based** | JavaScript cliente mueve datos desde una fuente a un sink sin pasar por HTML servidor. |

## 🔗 Cadenas y dependencias

XSS puede ejecutar requests como la víctima y eludir controles CSRF dentro del mismo origen. El robo de cookie requiere que no sea `HttpOnly`; no debe afirmarse por defecto.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Depende de origen, CSP, privilegios e interacción. Un XSS en un panel administrativo puede elevar impacto si un administrador renderiza el contenido. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un parámetro, contenido guardado o fuente DOM y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en un sink HTML/JS del navegador.
- Confirmar: Un marcador ejecuta una acción inocua en el origen afectado; el reflejo de etiquetas sin ejecución no basta.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Codificar por contexto, usar APIs DOM seguras, sanitizar HTML enriquecido y configurar CSP como defensa adicional. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

El [informe divulgado #3943339 de Basecamp](https://hackerone.com/reports/3943339) describe XSS reflejado encadenado con un token de escritura y una acción entre cuentas. Ilustra por qué un reporte sólido prueba el paso desde ejecución en navegador hasta el permiso concreto afectado.

## 📚 Fuentes

- [PortSwigger: XSS](https://portswigger.net/web-security/cross-site-scripting) — contextos y variantes.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [HackerOne: Basecamp, informe 3943339](https://hackerone.com/reports/3943339) — reporte divulgado sobre XSS y cadena de impacto.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
