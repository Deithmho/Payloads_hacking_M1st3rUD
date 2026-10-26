# 📖 HTTP Parameter Pollution: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una misma clave aparece varias veces en query o body. Proxy, framework y lógica de negocio pueden seleccionar primero, último o lista, y una validación puede inspeccionar un valor diferente del que usa el sink.

El límite de confianza relevante es **parámetros duplicados frente a parsers HTTP en distintas capas**. La aplicación recibe **parámetros duplicados** y debería **normalizar duplicados con una política única**. La vulnerabilidad aparece cuando **validador y consumidor eligen valores diferentes**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza parámetros duplicados en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en parsers HTTP en distintas capas.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si validador y consumidor eligen valores diferentes.
4. **Observación:** Dos valores marcadores muestran qué valor usa cada capa y si una regla se aplica al mismo valor.

## 🧭 Contextos y variantes

**Dónde buscar:** filtros, firmas, caché, WAF y parámetros de navegación.

| Variante | Diferencia técnica |
| --- | --- |
| **Primero/último** | Cada parser elige posición diferente. |
| **Array** | El framework entrega una lista. |
| **Query/body** | Mismo nombre en fuentes diferentes recibe prioridad distinta. |

## 🔗 Cadenas y dependencias

HPP puede ayudar a saltar un filtro de inyección o control de caché; el bypass se confirma solo si el valor peligroso llega al sink.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Por sí solo es discrepancia de parsing. Severidad depende de un control eludido y efecto demostrado. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar parámetros duplicados y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en parsers HTTP en distintas capas.
- Confirmar: Dos valores marcadores muestran qué valor usa cada capa y si una regla se aplica al mismo valor.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Rechazar parámetros duplicados o definir semántica única antes de validación y uso. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [PortSwigger: pruebas API](https://portswigger.net/web-security/api-testing) — descubrimiento de superficie.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
