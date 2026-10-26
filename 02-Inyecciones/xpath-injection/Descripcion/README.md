# 📖 XPath injection: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Cuando una aplicación concatena valores a una expresión XPath, operadores y comillas pueden alterar la selección de nodos XML de forma análoga a una inyección SQL.

El límite de confianza relevante es **un filtro de búsqueda XML frente a la expresión XPath**. La aplicación recibe **un filtro de búsqueda XML** y debería **usar variables XPath y tipos esperados**. La vulnerabilidad aparece cuando **se concatena entrada como expresión**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un filtro de búsqueda XML en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en la expresión XPath.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se concatena entrada como expresión.
4. **Observación:** La consulta de un XML de prueba devuelve nodos diferentes con una condición verdadera y falsa.

## 🧭 Contextos y variantes

**Dónde buscar:** aplicaciones legacy, XML de configuración, SAML mal implementado y búsquedas documentales.

| Variante | Diferencia técnica |
| --- | --- |
| **Boolean blind** | El número de nodos cambia por condición. |
| **Error-based** | Un error revela sintaxis del parser. |
| **Consulta alterada** | Se seleccionan nodos fuera del filtro previsto. |

## 🔗 Cadenas y dependencias

Si el XPath decide qué cuenta autenticar, una expresión ampliada podría llevar a autenticación rota; la sesión resultante debe confirmarse aparte.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede revelar información estructurada en XML; la severidad depende de los nodos accesibles. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un filtro de búsqueda XML y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en la expresión XPath.
- Confirmar: La consulta de un XML de prueba devuelve nodos diferentes con una condición verdadera y falsa.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Usar variables enlazadas, validar tipos y limitar acceso del proceso a documentos XML. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
