# 📖 Límites insuficientes de recursos en API: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una API puede aceptar operaciones que consumen tiempo, memoria, cuota o dinero sin límites por usuario y objeto. El problema incluye coste por solicitud, paginación y abuso de operaciones, más allá de un contador de requests.

El límite de confianza relevante es **parámetros de tamaño, paginación o coste frente a procesamiento API y cuotas**. La aplicación recibe **parámetros de tamaño, paginación o coste** y debería **imponer límites de coste, tamaño y frecuencia**. La vulnerabilidad aparece cuando **una solicitud pequeña induce trabajo desproporcionado**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza parámetros de tamaño, paginación o coste en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en procesamiento API y cuotas.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si una solicitud pequeña induce trabajo desproporcionado.
4. **Observación:** En staging o una ventana autorizada, una variación acotada supera el límite documentado sin degradar el servicio.

## 🧭 Contextos y variantes

**Dónde buscar:** GraphQL, exportaciones, búsquedas, subidas y APIs de pago.

| Variante | Diferencia técnica |
| --- | --- |
| **Paginación** | El cliente pide demasiados resultados. |
| **Complejidad GraphQL** | Consultas anidadas consumen recursos. |
| **Coste externo** | Una acción genera SMS, email o API facturable. |
| **Rate limiting** | No se limita frecuencia por identidad. |

## 🔗 Cadenas y dependencias

Alias GraphQL pueden multiplicar una función costosa; el impacto requiere medir consumo o cuota, no solo enviar una query grande.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Desde gasto económico hasta indisponibilidad. Pruebas de carga y DoS requieren autorización específica; no extrapolar con tres requests. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar parámetros de tamaño, paginación o coste y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en procesamiento API y cuotas.
- Confirmar: En staging o una ventana autorizada, una variación acotada supera el límite documentado sin degradar el servicio.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Límites de tamaño y complejidad, cuotas por identidad y recurso, presupuestos de tiempo e idempotencia. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) — clasificación de riesgos API.
- [PortSwigger: GraphQL](https://portswigger.net/web-security/graphql) — introspección y autorización.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
