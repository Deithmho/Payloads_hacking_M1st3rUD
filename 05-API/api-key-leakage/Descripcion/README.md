# 📖 Exposición de API keys y secretos: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un secreto embebido en cliente, repositorio, log o respuesta puede ser leído por quien tenga acceso a ese canal. Debe distinguirse una clave pública de identificación de una credencial con permisos útiles.

El límite de confianza relevante es **un artefacto cliente o respuesta API frente a el sistema que almacena la credencial**. La aplicación recibe **un artefacto cliente o respuesta API** y debería **mantener secretos servidor, usar mínimo privilegio y rotación**. La vulnerabilidad aparece cuando **una clave privada queda accesible a usuarios no autorizados**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un artefacto cliente o respuesta API en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el sistema que almacena la credencial.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si una clave privada queda accesible a usuarios no autorizados.
4. **Observación:** Se identifica tipo, alcance y permiso mediante documentación o una llamada inocua autorizada, sin imprimir ni guardar el valor completo.

## 🧭 Contextos y variantes

**Dónde buscar:** bundles JS, source maps, `.env`, logs, respuestas y repositorios.

| Variante | Diferencia técnica |
| --- | --- |
| **Clave pública** | Identificador diseñado para cliente; no es secreto por ubicación. |
| **Token de servicio** | Permite API con privilegios si sigue vigente. |
| **Credencial histórica** | Puede estar revocada y no tener impacto actual. |

## 🔗 Cadenas y dependencias

Una key expuesta con permiso de escritura puede facilitar cambios en servicios terceros; ese permiso debe verificarse sin operar sobre datos ajenos.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Severidad depende de validez, scopes, cuota y datos. La presencia de una cadena con formato de clave no basta. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un artefacto cliente o respuesta API y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el sistema que almacena la credencial.
- Confirmar: Se identifica tipo, alcance y permiso mediante documentación o una llamada inocua autorizada, sin imprimir ni guardar el valor completo.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Sacar secretos del cliente, rotarlos, limitar scopes, restringir origen/IP cuando aplique y auditar uso. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: información expuesta](https://portswigger.net/web-security/information-disclosure) — prueba de impacto.
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) — clasificación de riesgos API.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
