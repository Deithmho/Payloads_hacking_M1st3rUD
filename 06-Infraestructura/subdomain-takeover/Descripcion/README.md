# 📖 Subdomain takeover: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un subdominio sigue apuntando por DNS a un servicio externo cuyo recurso fue eliminado. Si otra persona puede reclamar exactamente ese recurso, puede servir contenido bajo el subdominio de la organización.

El límite de confianza relevante es **CNAME o registro de un subdominio en alcance frente a proveedor SaaS desvinculado**. La aplicación recibe **CNAME o registro de un subdominio en alcance** y debería **retirar DNS o reservar el recurso antes de liberarlo**. La vulnerabilidad aparece cuando **el nombre DNS existe pero el recurso destino es reclamable**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza CNAME o registro de un subdominio en alcance en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en proveedor SaaS desvinculado.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el nombre DNS existe pero el recurso destino es reclamable.
4. **Observación:** La respuesta del proveedor indica recurso ausente y una verificación no intrusiva documenta reclamabilidad; tomar control solo con autorización.

## 🧭 Contextos y variantes

**Dónde buscar:** hosting estático, PaaS, tiendas, helpdesks y CDNs.

| Variante | Diferencia técnica |
| --- | --- |
| **CNAME huérfano** | Alias apunta a recurso eliminado. |
| **A/AAAA huérfano** | IP o virtual host ya no pertenece al dueño. |
| **Wildcard** | Patrón DNS amplía superficie, sin implicar control por sí solo. |

## 🔗 Cadenas y dependencias

Si el subdominio comparte cookies `Domain`, un takeover podría afectar sesión; comprobar alcance y atributos reales de cookies antes de afirmarlo.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Una respuesta 404 del proveedor o firma conocida es candidato, no prueba de control. Impacto depende del recurso reclamable y confianza del subdominio. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar CNAME o registro de un subdominio en alcance y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en proveedor SaaS desvinculado.
- Confirmar: La respuesta del proveedor indica recurso ausente y una verificación no intrusiva documenta reclamabilidad; tomar control solo con autorización.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Inventariar DNS, retirar registros al desmontar servicios y reservar nombres críticos. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) — clasificación de riesgos web.
- [HackTricks: subdomain takeover](https://book.hacktricks.wiki/es/pentesting-web/domain-subdomain-takeover.html) — reclamabilidad y posibles cadenas.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
