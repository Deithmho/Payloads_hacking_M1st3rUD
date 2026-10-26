# 📖 Web Cache Deception: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una caché cree que una URL es estática mientras el origen la trata como recurso dinámico privado. La respuesta autenticada puede guardarse y entregarse a alguien sin sesión.

El límite de confianza relevante es **una URL privada con sufijo o delimitador ambiguo frente a caché y router del origen**. La aplicación recibe **una URL privada con sufijo o delimitador ambiguo** y debería **evitar cachear respuestas privadas y alinear parsing de ruta**. La vulnerabilidad aparece cuando **la caché clasifica la URL como pública y el origen devuelve datos privados**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza una URL privada con sufijo o delimitador ambiguo en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en caché y router del origen.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si la caché clasifica la URL como pública y el origen devuelve datos privados.
4. **Observación:** Una segunda sesión propia anónima recibe exactamente el dato de la primera cuenta de prueba en una URL única.

## 🧭 Contextos y variantes

**Dónde buscar:** perfiles, páginas de cuenta, rutas con extensiones y CDN.

| Variante | Diferencia técnica |
| --- | --- |
| **Extensión** | Un sufijo `.css` o similar induce regla de estático. |
| **Delimitador** | CDN y origen separan ruta en posiciones distintas. |
| **Cache key** | La cookie no forma parte de la clave de respuesta privada. |

## 🔗 Cadenas y dependencias

Puede combinarse con open redirect o URL compartible para inducir a otra persona a llenar caché; no hacerlo fuera de cuentas controladas.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Exposición de contenido privado si una respuesta autenticada queda accesible sin sesión. Un `Cache-Control` faltante sin fuga no basta. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar una URL privada con sufijo o delimitador ambiguo y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en caché y router del origen.
- Confirmar: Una segunda sesión propia anónima recibe exactamente el dato de la primera cuenta de prueba en una URL única.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Enviar `Cache-Control: private, no-store` en respuestas sensibles, alinear rutas y revisar reglas de caché. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: cache deception](https://portswigger.net/web-security/web-cache-deception) — contenido privado cacheado.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
