# 📖 Mass assignment en APIs: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

En APIs JSON es habitual reutilizar el modelo de salida como entrada. Si el binder acepta cualquier clave, una propiedad marcada como solo lectura en documentación puede persistirse o afectar autorizaciones.

El límite de confianza relevante es **JSON de PATCH/PUT/POST frente a binder y modelo API**. La aplicación recibe **JSON de PATCH/PUT/POST** y debería **usar DTO de escritura y campos permitidos**. La vulnerabilidad aparece cuando **el modelo acepta propiedades reservadas del cliente**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza JSON de PATCH/PUT/POST en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en binder y modelo API.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el modelo acepta propiedades reservadas del cliente.
4. **Observación:** Un campo de solo lectura en un objeto de prueba cambia tras una request y luego altera una decisión efectiva.

## 🧭 Contextos y variantes

**Dónde buscar:** REST, GraphQL mutations, generación automática de CRUD y APIs móviles.

| Variante | Diferencia técnica |
| --- | --- |
| **Top-level** | `role` o `isAdmin` entra en el objeto principal. |
| **Anidado** | Una relación bajo `settings` o `user` también se vincula. |
| **PUT vs PATCH** | Rutas distintas aplican validadores diferentes. |

## 🔗 Cadenas y dependencias

Una ruta de perfil accesible puede almacenar `role`, pero solo hay elevación si la aplicación toma decisiones basadas en ese rol editado.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Depende de propiedad aceptada y efecto. La mera inclusión del campo en la respuesta puede ser reflejo. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar JSON de PATCH/PUT/POST y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en binder y modelo API.
- Confirmar: Un campo de solo lectura en un objeto de prueba cambia tras una request y luego altera una decisión efectiva.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

DTOs de entrada por operación, allowlist de campos, autorización por propiedad y pruebas de persistencia. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: pruebas API](https://portswigger.net/web-security/api-testing) — descubrimiento de superficie.
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) — clasificación de riesgos API.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
