# 📖 Fallos de validación SAML: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

SAML transporta aserciones XML firmadas entre proveedor de identidad y servicio. El servicio debe consumir exactamente el elemento cuya firma validó, para el destinatario y ventana temporal correctos.

El límite de confianza relevante es **XML firmado frente al parser de la aplicación**. La aplicación recibe **SAMLResponse y sus aserciones** y debería **verificar firma, referencia, emisor, audiencia y destinatario**. La vulnerabilidad aparece cuando **el dato consumido difiere del nodo firmado o no se comprueba su contexto**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se captura una respuesta SAML de un tenant de pruebas.
2. **Procesamiento:** Se localizan `Assertion`, `Signature`, `Reference` y `InResponseTo`.
3. **Ruptura del control:** Se altera un atributo propio sin rehacer firma, o se duplica un nodo en laboratorio.
4. **Observación:** Se confirma rechazo y se registra qué nodo usa el servicio.

## 🧭 Contextos y variantes

**Dónde buscar:** SSO empresarial, aplicaciones legacy y pasarelas de federación.

| Variante | Diferencia técnica |
| --- | --- |
| **Signature wrapping** | El parser consume una aserción distinta de la firmada. |
| **Replay** | Una respuesta válida se acepta fuera de su transacción. |
| **Confusión de audiencia** | La aserción para otro servicio es aceptada. |

## 🔗 Cadenas y dependencias

Si una aserción falsificada establece un usuario administrador y el servicio crea sesión, el fallo de validación se convierte en toma de cuenta. Debe demostrarse el cambio de identidad después del login.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede afectar una cuenta o toda la federación. Los ejemplos de XML modificado son pruebas de rechazo, no prueba de explotación hasta obtener sesión con identidad no autorizada. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Examinar referencias de firma y nodos consumidos.
- Cambiar un atributo propio y verificar rechazo.
- Comprobar audiencia, destinatario, expiración e `InResponseTo`.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Usar una biblioteca SAML mantenida, validar el nodo firmado y rechazar XML ambiguo, respuestas duplicadas o fuera de contexto. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) — clasificación de riesgos web.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
