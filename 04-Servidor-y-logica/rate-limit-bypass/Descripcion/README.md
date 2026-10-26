# 📖 Bypass de rate limit: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un límite de frecuencia solo funciona si cuenta la identidad correcta y cubre todas las rutas equivalentes. Contadores basados en cabeceras cliente o en una sola ruta pueden dejar intentos fuera.

El límite de confianza relevante es **requests repetidas de una cuenta de prueba frente a el contador de rate limit**. La aplicación recibe **requests repetidas de una cuenta de prueba** y debería **contar por identidad y operación con límites distribuidos**. La vulnerabilidad aparece cuando **la clave del contador se manipula o no cubre una ruta**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza requests repetidas de una cuenta de prueba en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el contador de rate limit.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si la clave del contador se manipula o no cubre una ruta.
4. **Observación:** Una secuencia corta y autorizada excede el límite esperado y demuestra efecto; ausencia de cabecera no prueba falta de límite.

## 🧭 Contextos y variantes

**Dónde buscar:** login, OTP, password reset, APIs costosas y cupones.

| Variante | Diferencia técnica |
| --- | --- |
| **IP falsificada** | El backend usa `X-Forwarded-For` no confiable. |
| **Ruta alternativa** | Mismo acto por otro endpoint evita contador. |
| **Distribuido** | Nodos no comparten estado. |
| **Cuenta/objeto** | La clave no corresponde al recurso protegido. |

## 🔗 Cadenas y dependencias

En OTP, un límite ausente puede facilitar adivinación si el espacio y caducidad lo permiten. No realizar fuerza bruta ni saturación.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Varía con tamaño del espacio de búsqueda y valor de la operación. Una política 429 presente puede aún ser insuficiente, pero requiere modelar números. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar requests repetidas de una cuenta de prueba y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el contador de rate limit.
- Confirmar: Una secuencia corta y autorizada excede el límite esperado y demuestra efecto; ausencia de cabecera no prueba falta de límite.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Límites por identidad, operación y recurso, contadores compartidos, cabeceras de proxy saneadas y alertas. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [PortSwigger: autenticación](https://portswigger.net/web-security/authentication) — mecanismos y laboratorios.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
