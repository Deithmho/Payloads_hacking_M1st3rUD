# 📖 Host header injection: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

`Host` y sus variantes de proxy seleccionan virtual host y pueden construir URLs absolutas. Si se confía en un valor no validado, aparecen redirecciones, enlaces falsos o confusión de enrutamiento.

El límite de confianza relevante es **`Host` y `X-Forwarded-Host` frente a router y generador de URL**. La aplicación recibe **`Host` y `X-Forwarded-Host`** y debería **aceptar hosts conocidos y usar base URL fija**. La vulnerabilidad aparece cuando **el host enviado por cliente gobierna la URL o ruta**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza `Host` y `X-Forwarded-Host` en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en router y generador de URL.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el host enviado por cliente gobierna la URL o ruta.
4. **Observación:** Una URL generada, redirección o contenido propio usa el host controlado; se identifica la capa responsable.

## 🧭 Contextos y variantes

**Dónde buscar:** password reset, enlaces de invitación, caché y virtual hosting.

| Variante | Diferencia técnica |
| --- | --- |
| **Host directo** | Valor no permitido llega a la aplicación. |
| **Proxy host** | El backend confía en `X-Forwarded-Host`. |
| **Duplicación** | Dos parsers escogen cabeceras distintas. |

## 🔗 Cadenas y dependencias

El enlace de reset envenenado requiere un token real en correo propio; un `Location` controlado puede encadenarse con open redirect.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Un reflejo de host sin token ni efecto de caché suele ser bajo; generar un enlace secreto hacia origen controlado puede ser alto. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar `Host` y `X-Forwarded-Host` y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en router y generador de URL.
- Confirmar: Una URL generada, redirección o contenido propio usa el host controlado; se identifica la capa responsable.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Validar hosts en edge y aplicación, usar URL canónica configurada y no confiar en cabeceras de proxy externas. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: Host header](https://portswigger.net/web-security/host-header) — enrutamiento y generación de URL.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
