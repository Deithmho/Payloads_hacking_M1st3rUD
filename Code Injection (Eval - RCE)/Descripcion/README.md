# 📖 Code injection / eval: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

La aplicación entrega texto del usuario a `eval`, `exec` o un intérprete embebido. El dato se convierte en instrucciones con los permisos del proceso.

El límite de confianza relevante es **una fórmula o expresión configurable frente a un evaluador de código**. La aplicación recibe **una fórmula o expresión configurable** y debería **parsear un lenguaje restringido o usar datos, nunca eval general**. La vulnerabilidad aparece cuando **se evalúa la entrada como código del lenguaje**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza una fórmula o expresión configurable en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en un evaluador de código.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se evalúa la entrada como código del lenguaje.
4. **Observación:** Una expresión matemática inocua se evalúa y su control literal no, con correlación clara.

## 🧭 Contextos y variantes

**Dónde buscar:** motores de reglas, cálculos dinámicos, plugins y consolas de administración.

| Variante | Diferencia técnica |
| --- | --- |
| **Expresión** | El evaluador ejecuta operaciones simples. |
| **Escape de sandbox** | Requiere acceso a objetos o funciones peligrosas. |
| **Código remoto** | La entrada llega a un intérprete del servidor, no solo al navegador. |

## 🔗 Cadenas y dependencias

Una SSTI puede convertirse en code injection si expone `eval` o llamadas a funciones; demostrar la disponibilidad real de ese sink.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Desde alteración de cálculos hasta ejecución remota. La prueba aritmética no justifica declarar RCE. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar una fórmula o expresión configurable y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en un evaluador de código.
- Confirmar: Una expresión matemática inocua se evalúa y su control literal no, con correlación clara.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Eliminar `eval`, implementar parser de expresiones limitado y aislar procesos cuando se requiera scripting. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) — clasificación de riesgos web.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
