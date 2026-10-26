# 📖 Configuración insegura de OAuth: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

OAuth delega autorización mediante redirecciones y tokens. La aplicación debe vincular la respuesta al navegador que inició el flujo y limitar exactamente el destino y el público de cada token.

El límite de confianza relevante es **navegador, cliente y servidor de autorización**. La aplicación recibe **redirect_uri, state, code y token** y debería **comparar URI registrada y ligar state/PKCE a la transacción**. La vulnerabilidad aparece cuando **se acepta una redirección abierta o una respuesta no vinculada al inicio**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se inicia un flujo OAuth con una cuenta propia y se captura la autorización.
2. **Procesamiento:** Se observa cómo se genera y guarda `state` y si se usa PKCE.
3. **Ruptura del control:** Se modifica solo `redirect_uri` o se intenta reutilizar una respuesta del propio flujo.
4. **Observación:** Se comprueba destino del código y rechazo de respuestas ajenas.

## 🧭 Contextos y variantes

**Dónde buscar:** SSO, login social, aplicaciones SPA, móviles y servicios con múltiples clientes OAuth.

| Variante | Diferencia técnica |
| --- | --- |
| **Redirect URI laxa** | Comparación por prefijo o comodín permite destino no registrado. |
| **CSRF de login** | Falta de `state` permite vincular una sesión a otra identidad. |
| **Confusión de emisor** | Respuesta de un proveedor se acepta en flujo de otro. |
| **PKCE ausente** | Un código interceptado puede ser reutilizable según el cliente. |

## 🔗 Cadenas y dependencias

Una redirección abierta en un dominio permitido puede hacer que un código salga hacia otra URL; el impacto exige que el código siga siendo canjeable y no esté ligado por PKCE. No basta observar un `Location`.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede llegar a vinculación indebida de cuentas o robo de token. La valoración exige comprobar restricciones de emisor, cliente, código, PKCE y sesión. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Inventariar clientes, redirect URI exactas y proveedores.
- Comprobar `state` nuevo y ligado a cada inicio de flujo.
- Probar cambios inocuos de ruta, puerto y subdominio en `redirect_uri` propio.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Usar coincidencia exacta de URI, `state` impredecible y ligado a sesión, PKCE S256 y validación de emisor y audiencia. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: OAuth](https://portswigger.net/web-security/oauth) — mecanismos y laboratorios.
- [RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700) — seguridad actual de OAuth 2.0.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
