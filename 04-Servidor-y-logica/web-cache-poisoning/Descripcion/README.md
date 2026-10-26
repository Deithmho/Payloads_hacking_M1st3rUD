# 📖 Web cache poisoning: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una caché agrupa solicitudes por una clave. Si el backend usa una entrada que no figura en esa clave y la respuesta se almacena, contenido influido por una persona se sirve a otras.

El límite de confianza relevante es **un header o parámetro no incluido en clave frente a caché compartida y backend**. La aplicación recibe **un header o parámetro no incluido en clave** y debería **incluir entradas relevantes en clave o no cachear**. La vulnerabilidad aparece cuando **la respuesta varía por una entrada no claveada**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un header o parámetro no incluido en clave en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en caché compartida y backend.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si la respuesta varía por una entrada no claveada.
4. **Observación:** Un marcador inocuo se ve desde una segunda sesión de prueba sin enviarlo; comprobar `Age` o indicadores de caché.

## 🧭 Contextos y variantes

**Dónde buscar:** CDN, proxies, HTML público y endpoints con cabeceras de forwarding.

| Variante | Diferencia técnica |
| --- | --- |
| **Unkeyed header** | Backend refleja una cabecera que caché ignora. |
| **Query ignorada** | La caché descarta un parámetro usado por backend. |
| **Normalización** | Ruta o query se normaliza de forma distinta. |

## 🔗 Cadenas y dependencias

Host header injection o request smuggling puede aportar una entrada envenenada; se necesita demostrar almacenamiento y entrega a un segundo cliente.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede afectar muchos usuarios si la respuesta compartida contiene redirección o HTML activo; no envenenar claves populares durante pruebas. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un header o parámetro no incluido en clave y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en caché compartida y backend.
- Confirmar: Un marcador inocuo se ve desde una segunda sesión de prueba sin enviarlo; comprobar `Age` o indicadores de caché.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Alinear clave y variación de respuesta, desactivar caché en contenido dinámico y validar entradas del backend. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

[YesWeHack](https://www.yeswehack.com/learn-bug-bounty/syntax-confusion-ambiguous-parsing-exploits) describe un desacuerdo de normalización de puerto en PHP que llevó de cache poisoning a XSS persistente. Es un caso divulgado sin identificar la empresa; demuestra por qué hay que comparar la clave y el parseo del backend.

## 📚 Fuentes

- [PortSwigger: cache poisoning](https://portswigger.net/web-security/web-cache-poisoning) — clave de caché y entrada no incluida.
- [PortSwigger Research: HTTP desync](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn) — casos reales publicados.
- [YesWeHack: confusión sintáctica](https://www.yeswehack.com/learn-bug-bounty/syntax-confusion-ambiguous-parsing-exploits) — investigación pública y límites de inferencia.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
