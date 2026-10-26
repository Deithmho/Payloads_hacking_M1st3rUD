# 📖 Envenenamiento del enlace de recuperación: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

El servidor puede construir un enlace de recuperación a partir de `Host` u otros encabezados controlables. Si envía ese enlace al usuario, el token termina en un origen ajeno.

El límite de confianza relevante es **encabezados de la request frente al generador de correo**. La aplicación recibe **Host o encabezados de proxy** y debería **usar una URL pública configurada y validar host**. La vulnerabilidad aparece cuando **se incorpora un host no confiable al enlace enviado**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se solicita recuperación para una cuenta propia.
2. **Procesamiento:** Se modifica solo un encabezado de host con un dominio controlado.
3. **Ruptura del control:** Se inspecciona el correo de prueba y la URL resultante.
4. **Observación:** Se comprueba si el token se dirige realmente al dominio controlado.

## 🧭 Contextos y variantes

**Dónde buscar:** flujos de password reset, invitaciones, verificaciones de email y enlaces absolutos.

| Variante | Diferencia técnica |
| --- | --- |
| **Host directo** | La aplicación usa `Host` de la solicitud. |
| **Proxy header** | Confía en `X-Forwarded-Host` sin lista de proxies. |
| **Caché** | Un enlace manipulado puede quedar guardado y afectar solicitudes posteriores. |

## 🔗 Cadenas y dependencias

Una inyección de Host solo se convierte en toma de cuenta si el enlace contiene un token canjeable y llega al origen controlado. Las protecciones de un solo uso y vinculación a usuario determinan el impacto.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Posible captura de token y toma de cuenta; un reflejo del host en una página sin token no demuestra ese impacto. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Usar exclusivamente el correo propio.
- Comparar `Host` y `X-Forwarded-Host` por separado.
- Inspeccionar enlace recibido sin abrir ni registrar el token completo.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Construir URLs desde configuración fija, validar host en el proxy y proteger tokens con caducidad y un solo uso. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: Host header](https://portswigger.net/web-security/host-header) — enrutamiento y generación de URL.
- [PortSwigger: autenticación](https://portswigger.net/web-security/authentication) — mecanismos y laboratorios.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
