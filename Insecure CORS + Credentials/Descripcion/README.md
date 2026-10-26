# 📖 CORS con credenciales: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

La combinación de `Access-Control-Allow-Origin` para un origen no confiable y `Access-Control-Allow-Credentials: true` puede permitir a JavaScript leer una respuesta con cookies de sesión. El navegador debe enviar cookies y el endpoint debe devolver datos privados.

El límite de confianza relevante es **`Origin` externo y sesión con cookies frente a política CORS de un endpoint privado**. La aplicación recibe **`Origin` externo y sesión con cookies** y debería **allowlist exacta y credenciales solo donde se requieren**. La vulnerabilidad aparece cuando **se autoriza lectura cruzada con credenciales a un origen ajeno**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza `Origin` externo y sesión con cookies en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en política CORS de un endpoint privado.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se autoriza lectura cruzada con credenciales a un origen ajeno.
4. **Observación:** Una página en origen propio de prueba lee el perfil de una cuenta de prueba; curl sirve solo para inspección preliminar.

## 🧭 Contextos y variantes

**Dónde buscar:** SPAs, APIs con cookies y subdominios con políticas compartidas.

| Variante | Diferencia técnica |
| --- | --- |
| **Reflejo arbitrario** | ACAO copia Origin y ACAC habilita credenciales. |
| **null** | Un origen opaco autorizado puede leer si la cookie se envía. |
| **Sufijo laxo** | Un hostname parecido pasa una comparación incompleta. |

## 🔗 Cadenas y dependencias

Si un subdominio autorizado tiene XSS, puede volverse origen capaz de leer API privada; se requieren ambas condiciones.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Alto si se leen datos sensibles de otra sesión. ACAC sin ACAO válido, o ACAO `*` con credenciales, no permite esa lectura por navegador. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar `Origin` externo y sesión con cookies y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en política CORS de un endpoint privado.
- Confirmar: Una página en origen propio de prueba lee el perfil de una cuenta de prueba; curl sirve solo para inspección preliminar.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Permitir orígenes exactos, evitar confianza en `null`, limitar cookies cross-site y auditar respuestas privadas. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: CORS](https://portswigger.net/web-security/cors) — orígenes, credenciales y lectura.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
