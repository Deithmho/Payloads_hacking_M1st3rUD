# 📖 Tabnabbing y engaño de pestañas: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una página abierta en una pestaña nueva podría conservar referencia a `window.opener`. Si el destino es no confiable, puede navegar la pestaña original hacia una página señuelo. Los navegadores modernos suelen aplicar `noopener` de forma implícita a ciertos enlaces, por lo que hay que probar el contexto real.

El límite de confianza relevante es **enlaces externos con nueva pestaña frente a `window.opener` en destino**. La aplicación recibe **enlaces externos con nueva pestaña** y debería **usar `rel=noopener` y no confiar en contenido externo**. La vulnerabilidad aparece cuando **el destino conserva capacidad de navegar la pestaña origen**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza enlaces externos con nueva pestaña en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en `window.opener` en destino.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el destino conserva capacidad de navegar la pestaña origen.
4. **Observación:** En un sitio de prueba, la pestaña nueva puede leer `window.opener` y cambiar solo una página propia de laboratorio.

## 🧭 Contextos y variantes

**Dónde buscar:** enlaces de perfiles, comentarios y contenido externo generado por usuarios.

| Variante | Diferencia técnica |
| --- | --- |
| **Reverse tabnabbing** | La nueva pestaña modifica la original. |
| **Enlace inyectado** | Un usuario coloca URL externa en contenido permitido. |
| **Clickbait** | El señuelo persuade a abrir el enlace; no es vulnerabilidad técnica por sí solo. |

## 🔗 Cadenas y dependencias

Un XSS puede insertar enlaces que inducen navegación, pero la posibilidad de tabnabbing depende del aislamiento real de `opener`.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Por sí solo suele ser riesgo de phishing condicionado a interacción. No declararlo por ver `target=_blank` sin comprobar navegador y `opener`. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar enlaces externos con nueva pestaña y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en `window.opener` en destino.
- Confirmar: En un sitio de prueba, la pestaña nueva puede leer `window.opener` y cambiar solo una página propia de laboratorio.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Añadir `rel=noopener noreferrer` cuando corresponda y diseñar enlaces externos claros. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
