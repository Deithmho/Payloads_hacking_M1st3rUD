# 📖 CORS mal configurado: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

CORS permite a JavaScript leer respuestas de otro origen cuando el servidor devuelve una autorización de origen. Reflejar cualquier `Origin` junto con credenciales puede exponer datos autenticados al sitio atacante.

El límite de confianza relevante es **`Origin` de una página externa frente a la política CORS de la respuesta**. La aplicación recibe **`Origin` de una página externa** y debería **autorizar solo orígenes concretos y recursos adecuados**. La vulnerabilidad aparece cuando **se refleja un origen no confiable con credenciales**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza `Origin` de una página externa en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en la política CORS de la respuesta.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se refleja un origen no confiable con credenciales.
4. **Observación:** Desde un navegador en origen controlado se lee un dato de una cuenta propia; cabeceras observadas solo por curl no demuestran lectura.

## 🧭 Contextos y variantes

**Dónde buscar:** APIs consumidas por SPAs, widgets, subdominios y entornos de desarrollo.

| Variante | Diferencia técnica |
| --- | --- |
| **Reflejo** | `Access-Control-Allow-Origin` copia el origen enviado. |
| **null** | Se confía en origen opaco. |
| **Subdominio** | Una comparación por sufijo acepta dominios no controlados. |
| **Credenciales** | `Access-Control-Allow-Credentials: true` habilita lectura con cookies si el navegador las envía. |

## 🔗 Cadenas y dependencias

CORS permisivo más sesión con cookies enviadas cross-site puede permitir lectura; XSS en un origen autorizado produce un camino distinto. Confirmar SameSite y contenido sensible.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Una política amplia en endpoint público no demuestra vulnerabilidad. El impacto aparece cuando un origen no confiable lee datos privados. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar `Origin` de una página externa y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en la política CORS de la respuesta.
- Confirmar: Desde un navegador en origen controlado se lee un dato de una cuenta propia; cabeceras observadas solo por curl no demuestran lectura.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Mantener allowlist exacta, evitar `null` salvo necesidad justificada, configurar credenciales por recurso y usar `Vary: Origin` cuando corresponda. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: CORS](https://portswigger.net/web-security/cors) — orígenes, credenciales y lectura.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
