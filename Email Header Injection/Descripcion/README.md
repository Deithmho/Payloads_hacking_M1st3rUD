# 📖 Email header injection: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una aplicación forma encabezados de un mensaje con texto del usuario. Saltos de línea no filtrados pueden insertar `Cc`, `Bcc` u otros campos en el correo generado.

El límite de confianza relevante es **nombre, asunto o dirección de formulario frente a constructor de mensajes SMTP**. La aplicación recibe **nombre, asunto o dirección de formulario** y debería **usar API estructurada y rechazar CR/LF**. La vulnerabilidad aparece cuando **el texto se concatena a cabeceras de correo**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza nombre, asunto o dirección de formulario en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en constructor de mensajes SMTP.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el texto se concatena a cabeceras de correo.
4. **Observación:** Una copia llega solo a una bandeja controlada, y la cabecera añadida se observa en el mensaje crudo.

## 🧭 Contextos y variantes

**Dónde buscar:** formularios de contacto, invitaciones, soporte y notificaciones.

| Variante | Diferencia técnica |
| --- | --- |
| **Cc/Bcc** | Nueva cabecera agrega destinatario. |
| **Subject** | El asunto se sustituye o extiende. |
| **MIME** | Se altera estructura del mensaje cuando el constructor es débil. |

## 🔗 Cadenas y dependencias

Si el formulario puede enviar correo desde un dominio confiable, la inyección puede amplificar phishing; no probar envíos a terceros.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Desde copias no autorizadas de mensajes propios hasta abuso de remitente; depende de controles de envío y contenido. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar nombre, asunto o dirección de formulario y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en constructor de mensajes SMTP.
- Confirmar: Una copia llega solo a una bandeja controlada, y la cabecera añadida se observa en el mensaje crudo.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Usar biblioteca de correo con campos separados, validar direcciones y bloquear caracteres de control. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
