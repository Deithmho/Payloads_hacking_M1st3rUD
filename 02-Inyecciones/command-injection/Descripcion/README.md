# 📖 Inyección de comandos del sistema: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un valor de request llega a un intérprete de comandos del sistema. Metacaracteres como `;`, `&&` o sustitución de comandos hacen que el shell ejecute una instrucción adicional.

El límite de confianza relevante es **un nombre de host, archivo o parámetro de herramienta frente a un shell invocado por el backend**. La aplicación recibe **un nombre de host, archivo o parámetro de herramienta** y debería **pasar argumentos sin shell y validar formato**. La vulnerabilidad aparece cuando **se concatena la entrada a una línea de comandos**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un nombre de host, archivo o parámetro de herramienta en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en un shell invocado por el backend.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se concatena la entrada a una línea de comandos.
4. **Observación:** Un marcador fijo aparece en la respuesta o en un canal controlado y desaparece en el control negativo.

## 🧭 Contextos y variantes

**Dónde buscar:** diagnósticos de red, conversiones, procesamiento de archivos y utilidades legacy.

| Variante | Diferencia técnica |
| --- | --- |
| **Directa** | La salida del comando vuelve en la respuesta. |
| **Ciega** | Solo se observa tiempo o un efecto lateral. |
| **Separadores** | Distintos shells interpretan sintaxis distinta. |

## 🔗 Cadenas y dependencias

Una carga de archivo puede alimentar el nombre pasado al shell; la ejecución requiere que el backend invoque shell con ese nombre.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede llevar a ejecución bajo permisos del servicio. No usar lectura de secretos ni comandos destructivos para la prueba mínima. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un nombre de host, archivo o parámetro de herramienta y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en un shell invocado por el backend.
- Confirmar: Un marcador fijo aparece en la respuesta o en un canal controlado y desaparece en el control negativo.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Evitar shell, usar APIs con argumentos separados, validar entradas y reducir permisos del proceso. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: command injection](https://portswigger.net/web-security/os-command-injection) — variantes y confirmación.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
