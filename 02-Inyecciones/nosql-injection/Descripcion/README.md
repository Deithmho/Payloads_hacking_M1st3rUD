# 📖 NoSQL injection: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Si la API inserta JSON del cliente en un filtro MongoDB u otro motor documental sin tipar y limitar operadores, una cadena esperada puede convertirse en una expresión de consulta.

El límite de confianza relevante es **un filtro JSON o parámetro de login frente a el selector NoSQL**. La aplicación recibe **un filtro JSON o parámetro de login** y debería **aceptar tipos escalares y construir filtros servidor**. La vulnerabilidad aparece cuando **se aceptan operadores aportados por el cliente**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un filtro JSON o parámetro de login en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el selector NoSQL.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se aceptan operadores aportados por el cliente.
4. **Observación:** Un par de consultas equivalentes con y sin operador cambia únicamente el objeto de prueba esperado.

## 🧭 Contextos y variantes

**Dónde buscar:** APIs Node.js, filtros de búsqueda, autenticación y endpoints con JSON flexible.

| Variante | Diferencia técnica |
| --- | --- |
| **$ne** | Un operador de desigualdad cambia el conjunto de coincidencias. |
| **$regex** | Una expresión regular altera criterios de búsqueda. |
| **Inyección de sintaxis** | Un valor rompe una expresión construida como texto. |

## 🔗 Cadenas y dependencias

Si la búsqueda de cuenta acepta operadores y después emite sesión, puede volverse bypass de autenticación; un resultado ampliado de búsqueda no demuestra login.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Va de lectura fuera de filtro a autenticación indebida; validar con datos propios y sin enumeración masiva. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un filtro JSON o parámetro de login y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el selector NoSQL.
- Confirmar: Un par de consultas equivalentes con y sin operador cambia únicamente el objeto de prueba esperado.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Validar tipo y esquema, construir consultas con campos permitidos y rechazar operadores no previstos. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: NoSQL injection](https://portswigger.net/web-security/nosql-injection) — variantes y confirmación.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
