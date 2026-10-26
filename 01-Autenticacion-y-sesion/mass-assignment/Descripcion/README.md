# 📖 Mass assignment: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un framework puede enlazar automáticamente todas las claves JSON a propiedades de un modelo. Si la API no define campos editables por operación, el cliente puede influir en propiedades internas como `role` o `ownerId`.

El límite de confianza relevante es **JSON del cliente frente a modelo persistente**. La aplicación recibe **campos adicionales en body** y debería **lista permitida de propiedades editables por rol**. La vulnerabilidad aparece cuando **se persisten campos que la UI nunca expuso**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se obtiene un objeto propio y se identifican propiedades de solo lectura.
2. **Procesamiento:** Se envía una actualización reversible con un campo extra.
3. **Ruptura del control:** El deserializador enlaza ese campo al modelo.
4. **Observación:** Se recupera el objeto y se compara si el campo cambió o fue ignorado.

## 🧭 Contextos y variantes

**Dónde buscar:** REST CRUD, registro de usuarios, actualizaciones de perfil y mutaciones GraphQL.

| Variante | Diferencia técnica |
| --- | --- |
| **Propiedad de rol** | El cliente intenta alterar privilegios. |
| **Propiedad de dueño** | Se reasigna titularidad. |
| **Objeto anidado** | Una clave profunda modifica una relación que no debía editarse. |

## 🔗 Cadenas y dependencias

Con BFLA, un usuario puede llegar a una función de actualización y luego escribir un campo privilegiado; se requieren ambos fallos para el impacto total.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Desde corrupción de metadatos propios hasta elevación. Un campo reflejado en la respuesta sin persistencia ni uso en autorizaciones no demuestra escalación. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Comparar esquema de lectura con formulario de edición.
- Añadir un campo de solo lectura a objeto propio.
- Recuperar el objeto después y probar una acción que dependa del campo.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Usar DTOs de entrada por operación, allowlist de campos y autorización sobre cambios de propiedades sensibles. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: pruebas API](https://portswigger.net/web-security/api-testing) — descubrimiento de superficie.
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) — clasificación de riesgos API.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
