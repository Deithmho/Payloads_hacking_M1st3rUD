# 📖 Configuración de seguridad incorrecta: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una configuración de servidor, CDN o navegador puede ampliar superficie: modo debug, métodos innecesarios, políticas CSP débiles o respuestas sensibles cacheables. Una cabecera ausente no siempre implica impacto explotable.

El límite de confianza relevante es **configuración observable por HTTP frente a servidor, proxy y navegador**. La aplicación recibe **configuración observable por HTTP** y debería **aplicar configuración mínima por recurso**. La vulnerabilidad aparece cuando **un control requerido falta o se aplica a ruta equivocada**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza configuración observable por HTTP en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en servidor, proxy y navegador.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si un control requerido falta o se aplica a ruta equivocada.
4. **Observación:** Se demuestra el efecto de una configuración sobre un flujo concreto, comparando rutas y capas.

## 🧭 Contextos y variantes

**Dónde buscar:** cabeceras de seguridad, TLS, servidores web, CDN y despliegues cloud.

| Variante | Diferencia técnica |
| --- | --- |
| **CSP débil** | Puede permitir ejecución si existe una fuente XSS. |
| **Debug** | Filtra datos o habilita funciones internas. |
| **Método** | PUT/DELETE expuestos importan solo si hacen una acción no autorizada. |
| **Caché** | Una regla sirve datos privados. |

## 🔗 Cadenas y dependencias

Una CSP débil combinada con XSS puede elevar explotación; la política por sí sola no produce XSS. La ausencia de `frame-ancestors` importa si hay clickjacking real.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Se evalúa por consecuencia comprobada; listas automáticas de headers faltantes generan falsos positivos. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar configuración observable por HTTP y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en servidor, proxy y navegador.
- Confirmar: Se demuestra el efecto de una configuración sobre un flujo concreto, comparando rutas y capas.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Configurar por entorno, revisar rutas sensibles, validar políticas en navegador y ejecutar regresiones tras cambios de proxy. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) — clasificación de riesgos web.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
