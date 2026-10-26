# 📖 Fijación de sesión: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Si el identificador de sesión permanece igual antes y después de autenticarse, quien conoce o impone el identificador previo puede heredar el estado autenticado.

El límite de confianza relevante es **sesión anónima frente a sesión autenticada**. La aplicación recibe **cookie de sesión previa al login** y debería **regenerar el identificador tras elevar privilegios**. La vulnerabilidad aparece cuando **se conserva el mismo identificador durante la transición**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se abre una sesión anónima controlada y se registra la cookie.
2. **Procesamiento:** Se inicia sesión con esa misma sesión.
3. **Ruptura del control:** Se compara el valor de cookie y su validez anterior.
4. **Observación:** Se comprueba si la sesión anónima anterior obtiene acceso autenticado.

## 🧭 Contextos y variantes

**Dónde buscar:** aplicaciones web con cookies, tiendas y portales legacy.

| Variante | Diferencia técnica |
| --- | --- |
| **ID no rotado** | La cookie no cambia al login. |
| **Adopción de ID** | El servidor acepta un identificador elegido por el cliente. |
| **Subdominio** | Una cookie de dominio amplio puede ser fijada desde un subdominio comprometido. |

## 🔗 Cadenas y dependencias

Un subdomain takeover o XSS en un subdominio puede ayudar a fijar una cookie amplia; la toma de cuenta requiere demostrar que el ID preconocido pasa a autenticado.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede producir toma de cuenta de una víctima que use un ID impuesto. La ausencia de rotación es una condición, pero el riesgo explotable depende de poder conocer o fijar ese ID. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Registrar cookie anónima y posterior al login.
- Probar si el ID anónimo sigue siendo válido.
- Revisar alcance `Domain`, `Path`, `Secure`, `HttpOnly` y `SameSite`.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Rotar identificador en login y elevación, invalidar el anterior y limitar cookies al host más estrecho posible. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [PortSwigger: autenticación](https://portswigger.net/web-security/authentication) — mecanismos y laboratorios.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
