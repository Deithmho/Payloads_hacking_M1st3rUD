# 📖 Deserialización insegura: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un programa reconstruye objetos a partir de datos no confiables. Algunas bibliotecas ejecutan métodos de inicialización o gadgets durante la reconstrucción, antes de que una validación posterior pueda protegerlos.

El límite de confianza relevante es **un blob serializado en cookie, cuerpo o archivo frente a el deserializador del backend**. La aplicación recibe **un blob serializado en cookie, cuerpo o archivo** y debería **no deserializar objetos arbitrarios de clientes**. La vulnerabilidad aparece cuando **se acepta una estructura de objeto no confiable**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un blob serializado en cookie, cuerpo o archivo en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el deserializador del backend.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se acepta una estructura de objeto no confiable.
4. **Observación:** Una estructura benigna manipulada causa una diferencia de tipo verificable; no concluir ejecución por errores de parser.

## 🧭 Contextos y variantes

**Dónde buscar:** sesiones, colas, importaciones y RPC legacy.

| Variante | Diferencia técnica |
| --- | --- |
| **Manipulación lógica** | Campos deserializados alteran estado sin gadget. |
| **Gadget chain** | Métodos existentes ejecutan acciones durante reconstrucción. |
| **Firma** | Una firma ausente o inválida permite alterar el blob; su presencia no asegura uso seguro de objetos. |

## 🔗 Cadenas y dependencias

Un archivo subido puede alcanzar un parser vulnerable. Para declarar RCE hay que observar un efecto inocuo específico causado por el gadget.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede abarcar manipulación de sesión o ejecución de código. No probar gadgets que borren archivos o envíen datos. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un blob serializado en cookie, cuerpo o archivo y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el deserializador del backend.
- Confirmar: Una estructura benigna manipulada causa una diferencia de tipo verificable; no concluir ejecución por errores de parser.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Usar formatos de datos simples con esquema, no clases arbitrarias; firmar tokens y actualizar bibliotecas. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: deserialización](https://portswigger.net/web-security/deserialization) — límite de confianza.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
