# 📖 Server-Side Request Forgery (SSRF): descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una función que recibe URL realiza la solicitud desde el servidor. Si no restringe destino, esquema y redirecciones, el usuario puede hacer que el backend contacte recursos fuera de los previstos.

El límite de confianza relevante es **una URL de importación o vista previa frente a el cliente HTTP del servidor**. La aplicación recibe **una URL de importación o vista previa** y debería **usar allowlist de destinos y bloquear redes no autorizadas tras resolver DNS**. La vulnerabilidad aparece cuando **se solicita una URL elegida por el usuario**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza una URL de importación o vista previa en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el cliente HTTP del servidor.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se solicita una URL elegida por el usuario.
4. **Observación:** Un host controlado recibe una solicitud con un identificador único; eso prueba salida de red, no acceso interno.

## 🧭 Contextos y variantes

**Dónde buscar:** webhooks, renderizado de imágenes, PDF, integraciones y importadores.

| Variante | Diferencia técnica |
| --- | --- |
| **Con respuesta** | El contenido remoto vuelve al usuario. |
| **Blind** | Solo se observa una conexión OAST. |
| **Redirección/DNS** | El destino final cambia después de la validación. |

## 🔗 Cadenas y dependencias

Una SSRF limitada puede ganar alcance por redirecciones o confusión de parser, como documenta YesWeHack. Probar recursos internos requiere permiso explícito y evidencia separada.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Una simple conexión a host externo puede ser baja; lectura de servicios internos o metadatos sensibles puede ser alta o crítica. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar una URL de importación o vista previa y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el cliente HTTP del servidor.
- Confirmar: Un host controlado recibe una solicitud con un identificador único; eso prueba salida de red, no acceso interno.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Allowlist estricta de esquema y host, resolver y validar IP final, revalidar redirecciones, bloquear redes internas en egress. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

Alex Brumen documentó en [YesWeHack](https://www.yeswehack.com/learn-bug-bounty/syntax-confusion-ambiguous-parsing-exploits) una cadena que empezó con SSRF limitada y lectura ciega de archivos y terminó en lectura arbitraria. El objetivo se mantuvo anónimo; la lección transferible es verificar cada límite de parser y cada paso del flujo, no asumir que toda SSRF llega a archivos.

## 📚 Fuentes

- [PortSwigger: SSRF](https://portswigger.net/web-security/ssrf) — variantes y confirmación.
- [YesWeHack: confusión sintáctica](https://www.yeswehack.com/learn-bug-bounty/syntax-confusion-ambiguous-parsing-exploits) — investigación pública y límites de inferencia.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
