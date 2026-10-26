# 📖 Prompt injection en funciones web con LLM: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una aplicación entrega al modelo contenido de usuario o terceros junto con instrucciones y acceso a herramientas. Texto de menor confianza puede intentar hacerse pasar por instrucciones para desviar una respuesta o llamar una API.

El límite de confianza relevante es **documento, comentario o respuesta de herramienta frente a modelo y orquestador de herramientas**. La aplicación recibe **documento, comentario o respuesta de herramienta** y debería **separar datos de instrucciones y autorizar cada herramienta en backend**. La vulnerabilidad aparece cuando **el orquestador ejecuta una orden extraída de contenido no confiable**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza documento, comentario o respuesta de herramienta en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en modelo y orquestador de herramientas.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el orquestador ejecuta una orden extraída de contenido no confiable.
4. **Observación:** Un documento de prueba induce solo una respuesta marcador; para reportar impacto se requiere una acción no autorizada observada en herramientas de prueba.

## 🧭 Contextos y variantes

**Dónde buscar:** chatbots con RAG, asistentes de soporte, agentes web y analizadores automáticos.

| Variante | Diferencia técnica |
| --- | --- |
| **Directa** | El usuario instruye al modelo por chat. |
| **Indirecta** | La instrucción viaja en un documento o página externa. |
| **Exceso de agencia** | La herramienta ejecuta acciones sin política servidor. |
| **Fuga** | El modelo devuelve datos que el usuario no debería recibir. |

## 🔗 Cadenas y dependencias

La inyección indirecta puede invocar una función API con BFLA; el fallo de autorización en la herramienta es el control decisivo.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Que el modelo repita un marcador no prueba vulnerabilidad. El impacto requiere datos o acción fuera de los permisos del usuario. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar documento, comentario o respuesta de herramienta y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en modelo y orquestador de herramientas.
- Confirmar: Un documento de prueba induce solo una respuesta marcador; para reportar impacto se requiere una acción no autorizada observada en herramientas de prueba.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Dar a herramientas permisos mínimos, autorizar cada llamada, separar contenido no confiable y pedir confirmación para acciones sensibles. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: Web LLM attacks](https://portswigger.net/web-security/llm-attacks) — pruebas de límites entre datos e instrucciones.
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) — clasificación de riesgos API.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
