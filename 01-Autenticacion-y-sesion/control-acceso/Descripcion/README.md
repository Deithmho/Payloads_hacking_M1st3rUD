# 📖 Control de acceso roto y elevación de privilegios: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Autenticación identifica a quien llama; autorización decide si esa identidad puede ejecutar cada función y sobre qué datos. El control debe repetirse en el backend, no depender de ocultar botones.

El límite de confianza relevante es **rol o atributo del principal frente a función protegida**. La aplicación recibe **ruta, método, rol y objeto** y debería **denegar por defecto según política del servidor**. La vulnerabilidad aparece cuando **una ruta alternativa omite el chequeo o confía en un rol enviado por cliente**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se registran rutas permitidas para roles propios A y B.
2. **Procesamiento:** Se repite una solicitud de rol alto usando una sesión de rol bajo.
3. **Ruptura del control:** Se compara el resultado para rutas y métodos equivalentes.
4. **Observación:** Se comprueba si la acción se realizó o solo devolvió un código engañoso.

## 🧭 Contextos y variantes

**Dónde buscar:** paneles de administración, APIs REST, acciones de exportación y entornos multi-tenant.

| Variante | Diferencia técnica |
| --- | --- |
| **Horizontal** | Acceso a recursos de un par. |
| **Vertical** | Usuario común ejecuta función administrativa. |
| **Contextual** | La acción solo debería permitirse en cierto estado del flujo. |

## 🔗 Cadenas y dependencias

BFLA puede combinarse con un endpoint de invitaciones y mass assignment para crear un rol elevado. El reporte debe distinguir acceso al endpoint, cambio de rol y privilegio efectivo.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Depende de la función: lectura limitada hasta administración total. Un endpoint `200` sin datos ni efecto no prueba elevación. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Construir matriz rol × ruta × método.
- Comparar cada función con sesiones de prueba de menor y mayor privilegio.
- Buscar acciones ocultas en tráfico UI, no solo rutas `/admin`.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Centralizar políticas por función y objeto, negar por defecto y cubrir todos los métodos y transportes con pruebas de regresión. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: control de acceso](https://portswigger.net/web-security/access-control) — mecanismos y laboratorios.
- [OWASP API5:2023 BFLA](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/) — autorización por función.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
