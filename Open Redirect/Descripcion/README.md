# 📖 Open redirect: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una aplicación usa un destino aportado por cliente para redirigir sin limitarlo al mismo origen o a una allowlist. Los navegadores siguen el `Location` resultante hacia un sitio no confiable.

El límite de confianza relevante es **next, returnUrl o redirect_uri frente a la respuesta 30x o navegación cliente**. La aplicación recibe **next, returnUrl o redirect_uri** y debería **resolver y validar destino contra lista exacta**. La vulnerabilidad aparece cuando **se acepta una URL externa o relativa a protocolo**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza next, returnUrl o redirect_uri en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en la respuesta 30x o navegación cliente.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se acepta una URL externa o relativa a protocolo.
4. **Observación:** Una request propia devuelve `Location` al host controlado y el navegador llega allí.

## 🧭 Contextos y variantes

**Dónde buscar:** login, logout, enlaces de email, OAuth y navegación de SPAs.

| Variante | Diferencia técnica |
| --- | --- |
| **URL absoluta** | Se acepta `https://otro`. |
| **Protocol-relative** | `//host` hereda esquema actual. |
| **Parser mismatch** | Normalización diferente entre validador y navegador. |

## 🔗 Cadenas y dependencias

Puede facilitar phishing; para robo de código OAuth es indispensable que el proveedor acepte la redirección y que el código no esté protegido por vinculación efectiva.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

A menudo bajo por sí solo; evaluar una cadena demostrada sin asumir token theft. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar next, returnUrl o redirect_uri y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en la respuesta 30x o navegación cliente.
- Confirmar: Una request propia devuelve `Location` al host controlado y el navegador llega allí.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Permitir rutas relativas locales o IDs de destino predefinidos; normalizar y comparar orígenes exactos. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [PortSwigger: OAuth](https://portswigger.net/web-security/oauth) — mecanismos y laboratorios.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
