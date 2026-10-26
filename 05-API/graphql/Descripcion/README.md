# 📖 GraphQL: introspección, inyección y autorización: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

GraphQL expone un esquema y permite combinar campos en una operación. La introspección revela superficie, pero no es por sí sola una vulnerabilidad; cada resolver debe aplicar autorización, límites de coste y tratamiento seguro de argumentos.

El límite de confianza relevante es **query, variables y nombres de campos frente a resolvers y planificador GraphQL**. La aplicación recibe **query, variables y nombres de campos** y debería **autorizar cada campo/objeto y limitar complejidad**. La vulnerabilidad aparece cuando **un resolver confía en argumentos o queda fuera de controles REST**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza query, variables y nombres de campos en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en resolvers y planificador GraphQL.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si un resolver confía en argumentos o queda fuera de controles REST.
4. **Observación:** Una cuenta de prueba consulta un campo o nodo que su rol no debería ver, con comparación de control; la introspección solo sirve para inventario.

## 🧭 Contextos y variantes

**Dónde buscar:** APIs GraphQL públicas, BFFs y federación de servicios.

| Variante | Diferencia técnica |
| --- | --- |
| **Introspección** | Enumera tipos y operaciones si está habilitada. |
| **BOLA en node** | Un ID de otro usuario llega a resolver sin política. |
| **Coste/alias** | Muchas operaciones en una solicitud agotan recursos si no hay límites. |
| **Inyección de argumento** | Un resolver inseguro pasa el valor a SQL, NoSQL o shell. |

## 🔗 Cadenas y dependencias

La introspección ayuda a hallar una mutación; el impacto requiere demostrar BFLA, BOLA o inyección en un resolver específico.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

El esquema público puede ser esperado. Riesgo real depende de datos, acciones y recursos obtenidos sin permiso. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar query, variables y nombres de campos y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en resolvers y planificador GraphQL.
- Confirmar: Una cuenta de prueba consulta un campo o nodo que su rol no debería ver, con comparación de control; la introspección solo sirve para inventario.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Autorizar por resolver y objeto, validar argumentos, limitar profundidad/coste y mantener políticas consistentes con REST. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: GraphQL](https://portswigger.net/web-security/graphql) — introspección y autorización.
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) — clasificación de riesgos API.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
