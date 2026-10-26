# 📖 Header injection: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Cabeceras de request o response se convierten en datos de confianza para un componente posterior. El riesgo concreto depende del encabezado afectado y de cómo lo interpreta el siguiente sistema.

El límite de confianza relevante es **una cabecera controlada o valor reflejado frente a proxy, framework o respuesta HTTP**. La aplicación recibe **una cabecera controlada o valor reflejado** y debería **normalizar, limitar y autenticar cabeceras de confianza**. La vulnerabilidad aparece cuando **un valor cliente se trata como metadato interno**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza una cabecera controlada o valor reflejado en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en proxy, framework o respuesta HTTP.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si un valor cliente se trata como metadato interno.
4. **Observación:** Una modificación de una sola cabecera produce un efecto protegido, repetible y ausente en el control.

## 🧭 Contextos y variantes

**Dónde buscar:** reverse proxies, balanceadores, CDN y aplicaciones con múltiples capas.

| Variante | Diferencia técnica |
| --- | --- |
| **Request header** | Una cabecera como `X-Forwarded-For` cambia una decisión. |
| **Response header** | CRLF crea o altera un encabezado de salida. |
| **Confianza proxy** | La app acepta cabeceras que solo debería crear el proxy. |

## 🔗 Cadenas y dependencias

Una cabecera de IP confiada puede afectar rate limits; debe probarse que cambia el contador de backend, no solo el texto de logs.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

El impacto depende de la decisión alterada: un encabezado reflejado es informativo; un control de acceso alterado puede ser grave. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar una cabecera controlada o valor reflejado y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en proxy, framework o respuesta HTTP.
- Confirmar: Una modificación de una sola cabecera produce un efecto protegido, repetible y ausente en el control.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Configurar lista de proxies de confianza, sobrescribir cabeceras entrantes y validar cada uso de metadatos HTTP. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [PortSwigger: Host header](https://portswigger.net/web-security/host-header) — enrutamiento y generación de URL.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
