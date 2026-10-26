# 📖 CRLF injection: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Si un valor controlado entra en un encabezado HTTP sin eliminar retornos de carro y saltos de línea, puede crear encabezados adicionales o alterar la separación de la respuesta.

El límite de confianza relevante es **un parámetro reflejado en `Location` o cabecera frente a el serializador de HTTP**. La aplicación recibe **un parámetro reflejado en `Location` o cabecera** y debería **rechazar CR y LF antes de escribir encabezados**. La vulnerabilidad aparece cuando **los delimitadores codificados se decodifican y serializan**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un parámetro reflejado en `Location` o cabecera en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el serializador de HTTP.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si los delimitadores codificados se decodifican y serializan.
4. **Observación:** La respuesta contiene una cabecera `X-Prueba` separada que no aparece en el control.

## 🧭 Contextos y variantes

**Dónde buscar:** redirecciones, nombres de archivo descargado y cabeceras de proxy.

| Variante | Diferencia técnica |
| --- | --- |
| **Response splitting** | Se inyecta una línea de encabezado adicional. |
| **Cookie tossing** | Una cabecera Set-Cookie añadida cambia estado en el navegador. |
| **Caché** | Una respuesta alterada puede ser almacenada para otros. |

## 🔗 Cadenas y dependencias

CRLF más caché puede convertir un encabezado propio en contenido servido a otras personas; demostrar caché compartida es un paso separado.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Desde alteración de respuesta propia hasta contaminación de caché. Un eco de `%0d%0a` sin nueva cabecera no es inyección. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un parámetro reflejado en `Location` o cabecera y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el serializador de HTTP.
- Confirmar: La respuesta contiene una cabecera `X-Prueba` separada que no aparece en el control.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Validar valores de encabezado con APIs seguras y rechazar caracteres de control tras decodificación. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [PortSwigger: Host header](https://portswigger.net/web-security/host-header) — enrutamiento y generación de URL.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
