# 📖 XML External Entity (XXE): descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un parser XML con entidades externas habilitadas resuelve una referencia definida en el DTD. La resolución puede leer un recurso o efectuar una solicitud de red desde el servidor.

El límite de confianza relevante es **un cuerpo XML o archivo que se analiza como XML frente a el parser con DTD**. La aplicación recibe **un cuerpo XML o archivo que se analiza como XML** y debería **deshabilitar entidades externas y DTD innecesarios**. La vulnerabilidad aparece cuando **el parser resuelve una entidad del cliente**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un cuerpo XML o archivo que se analiza como XML en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el parser con DTD.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el parser resuelve una entidad del cliente.
4. **Observación:** Un dominio de prueba recibe una solicitud correlacionada o el parser refleja un marcador seguro; no intentar leer archivos ajenos.

## 🧭 Contextos y variantes

**Dónde buscar:** SOAP, SVG, SAML, importadores XML y transformaciones de documentos.

| Variante | Diferencia técnica |
| --- | --- |
| **In-band** | El contenido resuelto vuelve en la respuesta. |
| **Blind/OAST** | Solo se observa una conexión externa. |
| **XInclude** | Una inclusión XML opera aunque no haya DTD controlable. |

## 🔗 Cadenas y dependencias

XXE que provoca una solicitud de red es una forma de SSRF. El acceso a servicios internos necesita verificación separada y autorización explícita.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

De consulta OAST sin datos hasta lectura de archivos o SSRF; severidad ligada al recurso realmente alcanzado. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un cuerpo XML o archivo que se analiza como XML y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el parser con DTD.
- Confirmar: Un dominio de prueba recibe una solicitud correlacionada o el parser refleja un marcador seguro; no intentar leer archivos ajenos.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Desactivar DTD y entidades externas, aislar parsers y limitar acceso a red y sistema de archivos. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

HackerOne cita como ejemplo de informe divulgado el [#312543 de Semrush](https://hackerone.com/reports/312543), XXE en Site Audit con exposición de archivos y directorios. La lectura de archivos es el efecto documentado de ese caso, no una propiedad automática de todos los parsers XML.

## 📚 Fuentes

- [PortSwigger: XXE](https://portswigger.net/web-security/xxe) — variantes y confirmación.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [HackerOne: Semrush, informe 312543](https://hackerone.com/reports/312543) — reporte divulgado citado por HackerOne.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
