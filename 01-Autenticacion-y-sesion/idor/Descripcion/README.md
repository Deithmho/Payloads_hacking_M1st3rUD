# 📖 IDOR: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

IDOR es una referencia directa a un objeto cuyo acceso no se verifica para la identidad actual. Que el identificador sea un UUID no reemplaza la comprobación de propiedad o política.

El límite de confianza relevante es **usuario autenticado frente a objeto ajeno**. La aplicación recibe **ID de ruta, query o cuerpo** y debería **autorizar la acción sobre el objeto concreto**. La vulnerabilidad aparece cuando **se busca el objeto por ID y se devuelve o modifica sin comprobar permiso**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Las cuentas A y B crean objetos de prueba propios.
2. **Procesamiento:** A solicita su objeto y luego sustituye solo el ID por el de B.
3. **Ruptura del control:** El servicio busca el objeto sin filtrar por propietario o relación.
4. **Observación:** Se compara contenido y código; B verifica cualquier efecto de edición.

## 🧭 Contextos y variantes

**Dónde buscar:** REST, GraphQL, descargas, facturas, chats, documentos y rutas de exportación.

| Variante | Diferencia técnica |
| --- | --- |
| **Lectura** | Se ve un objeto de otra cuenta. |
| **Escritura** | Se modifica un objeto ajeno. |
| **ID anidado** | La política se comprueba para el padre, no para el hijo. |
| **UUID** | La impredecibilidad dificulta descubrimiento, no corrige autorización. |

## 🔗 Cadenas y dependencias

Si se permite mass assignment en un objeto ajeno, IDOR de escritura puede convertirse en escalación. Se requiere verificar qué campos cambian y con qué rol.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

La exposición de un objeto aislado puede ser media o alta; edición o acceso a datos sensibles puede ser crítica. Medir alcance sin enumerar datos de terceros. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Preparar dos cuentas y dos objetos propios.
- Intercambiar un solo identificador por solicitud.
- Probar GET y, con permiso, actualización reversible; verificar desde la otra cuenta.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Aplicar autorización por objeto en cada operación, incluidos hijos, exportaciones y GraphQL; filtrar consultas por principal y política. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

El [informe divulgado de Nextcloud #2705507](https://hackerone.com/reports/2705507) fue clasificado como IDOR en información compartida de Tables; su severidad publicada fue baja, ejemplo de que la etiqueta IDOR no determina el impacto. Un [relato en Medium](https://medium.com/@ssherlock1/my-first-bug-on-hackerone-a-simple-idor-that-taught-me-a-lot-157c7ef46dd7) describe un `organisation_id` de otro tenant, pero no enlaza el reporte original y se usa solo como hipótesis de trabajo.

## 📚 Fuentes

- [OWASP API1:2023 BOLA](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/) — autorización por objeto.
- [PortSwigger: control de acceso](https://portswigger.net/web-security/access-control) — mecanismos y laboratorios.
- [HackerOne: Nextcloud, informe 2705507](https://hackerone.com/reports/2705507) — reporte divulgado sobre acceso a información compartida.
- [Medium: relato de IDOR multi-tenant](https://medium.com/@ssherlock1/my-first-bug-on-hackerone-a-simple-idor-that-taught-me-a-lot-157c7ef46dd7) — relato del investigador; no sustituye al reporte divulgado.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
