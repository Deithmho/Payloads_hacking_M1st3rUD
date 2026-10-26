# 📖 Remote File Inclusion (RFI): descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una aplicación incluye una ruta remota como código o plantilla. Se diferencia de SSRF porque el contenido remoto se incorpora al motor de ejecución o renderizado, no solo se descarga.

El límite de confianza relevante es **una URL para plantilla o include frente a el mecanismo de inclusión**. La aplicación recibe **una URL para plantilla o include** y debería **prohibir includes remotos y mapear nombres a recursos locales**. La vulnerabilidad aparece cuando **la URL del cliente se usa como fuente de código**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza una URL para plantilla o include en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el mecanismo de inclusión.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si la URL del cliente se usa como fuente de código.
4. **Observación:** Un archivo inocuo en host propio cambia el renderizado previsto; ejecución de código requiere prueba separada.

## 🧭 Contextos y variantes

**Dónde buscar:** aplicaciones PHP legacy, motores de plantillas e importadores inseguros.

| Variante | Diferencia técnica |
| --- | --- |
| **Inclusión ejecutable** | El contenido remoto se interpreta. |
| **Inclusión textual** | Solo se renderiza como dato. |
| **Wrapper** | Un esquema especial altera el origen leído. |

## 🔗 Cadenas y dependencias

Una SSRF que descarga texto y luego lo evalúa puede convertirse en RFI; demostrar el paso de evaluación antes de declarar RCE.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede ser crítico si interpreta código con permisos del servidor; una descarga reflejada sin evaluación es otra clase de riesgo. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar una URL para plantilla o include y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el mecanismo de inclusión.
- Confirmar: Un archivo inocuo en host propio cambia el renderizado previsto; ejecución de código requiere prueba separada.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Desactivar includes remotos, fijar lista de plantillas locales y separar contenido externo de código. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [PortSwigger: SSRF](https://portswigger.net/web-security/ssrf) — variantes y confirmación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
