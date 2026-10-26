# 📖 HTTP Request Smuggling: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Dos parsers HTTP en cadena pueden discrepar sobre dónde termina una request. Una longitud ambigua desincroniza la conexión backend y mezcla solicitudes, con posible impacto sobre otros usuarios.

El límite de confianza relevante es **framing HTTP entre frontend y backend frente a dos parsers de la cadena**. La aplicación recibe **framing HTTP entre frontend y backend** y debería **normalizar o rechazar mensajes ambiguos y usar framing coherente**. La vulnerabilidad aparece cuando **cada capa calcula una longitud distinta**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza framing HTTP entre frontend y backend en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en dos parsers de la cadena.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si cada capa calcula una longitud distinta.
4. **Observación:** En laboratorio se observa una desincronización reproducible con solicitudes propias; en producción se requiere permiso y aislamiento para no afectar a terceros.

## 🧭 Contextos y variantes

**Dónde buscar:** CDN, reverse proxies, gateways HTTP/2→HTTP/1.1 y conexiones reutilizadas.

| Variante | Diferencia técnica |
| --- | --- |
| **CL.TE** | Una capa usa Content-Length y otra Transfer-Encoding. |
| **TE.CL** | Orden opuesto. |
| **H2 downgrade** | La conversión entre protocolos produce ambigüedad. |
| **CL.0** | Backend ignora cuerpo de una solicitud. |

## 🔗 Cadenas y dependencias

Request smuggling puede facilitar cache poisoning o saltar controles de frontend; PortSwigger documentó casos reales. Una respuesta inesperada por keep-alive puede ser falso positivo.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Alto potencial, pero riesgo operativo también alto. No incluir payloads de desync sobre servicios compartidos sin ventana de prueba. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar framing HTTP entre frontend y backend y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en dos parsers de la cadena.
- Confirmar: En laboratorio se observa una desincronización reproducible con solicitudes propias; en producción se requiere permiso y aislamiento para no afectar a terceros.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Rechazar framing ambiguo en edge y backend, alinear protocolos y cerrar conexiones ante errores; probar regresiones en entorno aislado. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

James Kettle publicó casos reales de desincronización y envenenamiento de caché en [HTTP Desync Attacks](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn). El artículo distingue mecanismo, alcance y efectos; no se traslada su impacto a un hallazgo nuevo sin pruebas.

## 📚 Fuentes

- [PortSwigger: request smuggling](https://portswigger.net/web-security/request-smuggling) — desacuerdo de parsers.
- [PortSwigger Research: HTTP desync](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn) — casos reales publicados.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
