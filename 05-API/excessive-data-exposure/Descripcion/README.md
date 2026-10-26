# 📖 Exposición excesiva de datos en API: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una API serializa un objeto con más campos de los necesarios y espera que el frontend los oculte. Cualquier consumidor puede leer la respuesta cruda, incluso si el campo nunca se muestra en la interfaz.

El límite de confianza relevante es **una respuesta JSON accesible frente a serializador de modelo API**. La aplicación recibe **una respuesta JSON accesible** y debería **definir proyección mínima por recurso y rol**. La vulnerabilidad aparece cuando **se expone el modelo interno completo**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza una respuesta JSON accesible en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en serializador de modelo API.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se expone el modelo interno completo.
4. **Observación:** En una cuenta propia aparece un campo sensible o interno que el rol no necesita y cuyo valor tiene relevancia real.

## 🧭 Contextos y variantes

**Dónde buscar:** perfiles, listados, GraphQL, móviles y respuestas de administración reutilizadas.

| Variante | Diferencia técnica |
| --- | --- |
| **Campo sensible** | La respuesta incluye dato de otra persona o secreto. |
| **Metadato interno** | IDs o flags internos pueden ser informativos sin impacto autónomo. |
| **Overfetching GraphQL** | Campos no protegidos pueden solicitarse explícitamente. |

## 🔗 Cadenas y dependencias

Si BOLA permite leer objeto ajeno, la exposición excesiva aumenta la cantidad de datos filtrados; el núcleo del acceso cruzado sigue siendo BOLA.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Severidad depende del dato y quién puede leerlo. Campos públicos omitidos de UI no constituyen automáticamente un hallazgo. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar una respuesta JSON accesible y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en serializador de modelo API.
- Confirmar: En una cuenta propia aparece un campo sensible o interno que el rol no necesita y cuyo valor tiene relevancia real.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Serializar con DTOs y proyecciones por rol, revisar esquemas y no enviar secretos al cliente. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) — clasificación de riesgos API.
- [PortSwigger: pruebas API](https://portswigger.net/web-security/api-testing) — descubrimiento de superficie.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
