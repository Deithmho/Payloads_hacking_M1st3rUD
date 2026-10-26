# 📖 BOLA: autorización rota por objeto: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

En una API, la función puede estar disponible para el usuario, pero el ID enviado apunta a un objeto que no le pertenece. La verificación debe combinar sujeto, acción, objeto y contexto en cada request.

El límite de confianza relevante es **ID de objeto en path, query, header o JSON frente a resolver de objeto API**. La aplicación recibe **ID de objeto en path, query, header o JSON** y debería **verificar política sobre ese objeto concreto**. La vulnerabilidad aparece cuando **se consulta por ID sin filtrar por derechos del principal**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza ID de objeto en path, query, header o JSON en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en resolver de objeto API.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se consulta por ID sin filtrar por derechos del principal.
4. **Observación:** La cuenta A obtiene o cambia un objeto creado por la cuenta B de prueba, con efectos comprobados por B.

## 🧭 Contextos y variantes

**Dónde buscar:** REST, GraphQL, APIs móviles, multi-tenant y rutas anidadas.

| Variante | Diferencia técnica |
| --- | --- |
| **Lectura** | A ve datos de B. |
| **Escritura** | A altera objeto de B. |
| **Relación anidada** | Se valida proyecto pero no documento hijo. |
| **Batch** | Una lista mezcla IDs propios y ajenos sin filtrado por elemento. |

## 🔗 Cadenas y dependencias

BOLA con exposición excesiva puede revelar campos adicionales del objeto ajeno; describir por separado el fallo de política y el exceso de campos.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Desde exposición de un registro de prueba hasta compromiso masivo, pero no enumerar terceros para estimar alcance. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar ID de objeto en path, query, header o JSON y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en resolver de objeto API.
- Confirmar: La cuenta A obtiene o cambia un objeto creado por la cuenta B de prueba, con efectos comprobados por B.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Consultar con filtros de autorización por objeto y tenant, no aceptar IDs como prueba de permiso. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP API1:2023 BOLA](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/) — autorización por objeto.
- [PortSwigger: pruebas API](https://portswigger.net/web-security/api-testing) — descubrimiento de superficie.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
