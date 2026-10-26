# 📖 Clickjacking y framing: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Las políticas de framing deciden qué sitios pueden mostrar una página en iframe. Una mala configuración importa cuando una acción sensible puede manipularse visualmente mediante clics del usuario.

El límite de confianza relevante es **cabeceras CSP frame-ancestors y X-Frame-Options frente a motor de frames del navegador**. La aplicación recibe **cabeceras CSP frame-ancestors y X-Frame-Options** y debería **restringir ancestros en páginas sensibles**. La vulnerabilidad aparece cuando **un origen no confiable puede embeber una acción**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza cabeceras CSP frame-ancestors y X-Frame-Options en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en motor de frames del navegador.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si un origen no confiable puede embeber una acción.
4. **Observación:** En un origen de prueba se embebe una página de cuenta propia y se demuestra una acción reversible con clic.

## 🧭 Contextos y variantes

**Dónde buscar:** páginas de permisos, cambios de cuenta y flujos de confirmación.

| Variante | Diferencia técnica |
| --- | --- |
| **Sin política** | El navegador puede permitir framing. |
| **ALLOW-FROM obsoleto** | Compatibilidad irregular entre navegadores. |
| **CSP en ruta equivocada** | La política protege home pero no acción sensible. |

## 🔗 Cadenas y dependencias

Una acción CSRF y clickjacking pueden coexistir, pero el hallazgo de framing necesita que el clic sea necesario y engañable.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

No valorar por ausencia de header en recurso estático. La severidad depende del efecto de la acción y la interacción requerida. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar cabeceras CSP frame-ancestors y X-Frame-Options y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en motor de frames del navegador.
- Confirmar: En un origen de prueba se embebe una página de cuenta propia y se demuestra una acción reversible con clic.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Aplicar `frame-ancestors` en cada ruta sensible y probar en navegadores soportados; añadir confirmación fuerte para acciones críticas. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: clickjacking](https://portswigger.net/web-security/clickjacking) — framing y controles.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
