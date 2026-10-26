# 📖 Server-Side Template Injection (SSTI): descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una plantilla compilada por el servidor incorpora datos del usuario como código de plantilla. Expresiones aparentemente textuales se evalúan en el motor y pueden acceder a objetos del entorno.

El límite de confianza relevante es **texto de plantilla controlable frente a un motor de templates servidor**. La aplicación recibe **texto de plantilla controlable** y debería **renderizar datos como variables y no como fuente de plantilla**. La vulnerabilidad aparece cuando **la entrada se compila como sintaxis del motor**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza texto de plantilla controlable en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en un motor de templates servidor.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si la entrada se compila como sintaxis del motor.
4. **Observación:** Una operación aritmética simple produce el resultado calculado y un control literal permanece sin evaluar.

## 🧭 Contextos y variantes

**Dónde buscar:** emails, PDF, CMS, personalización y generadores de documentos.

| Variante | Diferencia técnica |
| --- | --- |
| **Jinja/Twig** | Delimitadores `{{...}}` con semántica dependiente del motor. |
| **EL/Freemarker** | Delimitadores `${...}`. |
| **Sandbox escape** | Requiere primitives concretas; no se infiere por evaluar aritmética. |

## 🔗 Cadenas y dependencias

SSTI puede llegar a inyección de comandos si el motor expone objetos peligrosos; primero identificar motor y restricciones.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Evaluar `7*7` demuestra interpretación, no ejecución de comandos. El impacto final depende de acceso del motor y sandbox. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar texto de plantilla controlable y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en un motor de templates servidor.
- Confirmar: Una operación aritmética simple produce el resultado calculado y un control literal permanece sin evaluar.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Separar plantilla fija de datos, escapar según contexto y restringir objetos disponibles en el renderizado. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: SSTI](https://portswigger.net/web-security/server-side-template-injection) — variantes y confirmación.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
