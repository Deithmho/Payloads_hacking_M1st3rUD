# 📖 Divulgación de información: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un endpoint de debug, archivo de configuración, `.git` o respuesta de error puede revelar datos internos. La exposición solo es hallazgo cuando el dato tiene sensibilidad o habilita un impacto concreto.

El límite de confianza relevante es **rutas y respuestas públicas frente a servidor web y despliegue**. La aplicación recibe **rutas y respuestas públicas** y debería **excluir artefactos internos y sanear errores**. La vulnerabilidad aparece cuando **un recurso interno se sirve a usuarios no autorizados**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza rutas y respuestas públicas en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en servidor web y despliegue.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si un recurso interno se sirve a usuarios no autorizados.
4. **Observación:** Se documenta un fragmento mínimo redactado y su utilidad real, sin descargar repositorios ni bases completas.

## 🧭 Contextos y variantes

**Dónde buscar:** debug endpoints, source maps, `.env`, `.git`, logs y trazas.

| Variante | Diferencia técnica |
| --- | --- |
| **Secreto** | Credencial vigente con permisos. |
| **Código fuente** | Puede revelar lógica y endpoints; no necesariamente secretos. |
| **Versión** | Dato de tecnología sin impacto autónomo. |
| **Traza** | Rutas internas o consultas pueden ayudar a análisis. |

## 🔗 Cadenas y dependencias

Código fuente expuesto puede revelar una ruta BFLA o una clave; validar cada consecuencia de manera separada y sin usar secretos ajenos.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

La sensibilidad y vigencia del dato determinan severidad. Status 200 o versión visible no bastan. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar rutas y respuestas públicas y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en servidor web y despliegue.
- Confirmar: Se documenta un fragmento mínimo redactado y su utilidad real, sin descargar repositorios ni bases completas.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Excluir archivos de despliegue, desactivar debug, sanear errores y rotar secretos confirmados expuestos. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: información expuesta](https://portswigger.net/web-security/information-disclosure) — prueba de impacto.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
