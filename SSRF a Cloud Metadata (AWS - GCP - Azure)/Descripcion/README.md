# 📖 SSRF hacia metadatos cloud: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Algunos entornos cloud exponen metadatos a cargas de trabajo mediante direcciones de enlace local. Una SSRF desde el proceso correcto podría llegar allí, pero proveedores usan controles distintos como tokens de sesión, cabeceras o límites de salto.

El límite de confianza relevante es **una función fetch del servidor frente a servicio de metadatos del entorno cloud**. La aplicación recibe **una función fetch del servidor** y debería **bloquear egress a metadata y usar identidad de mínimo privilegio**. La vulnerabilidad aparece cuando **el proceso puede solicitar metadata sin restricciones suficientes**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza una función fetch del servidor en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en servicio de metadatos del entorno cloud.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el proceso puede solicitar metadata sin restricciones suficientes.
4. **Observación:** En laboratorio propio se observa acceso a un campo no secreto; en programas reales no consultar credenciales ni tokens sin autorización expresa.

## 🧭 Contextos y variantes

**Dónde buscar:** AWS, GCP, Azure, contenedores y workloads con IAM.

| Variante | Diferencia técnica |
| --- | --- |
| **AWS IMDSv2** | Requiere un token obtenido con PUT y puede impedir SSRF simple. |
| **GCP** | Exige `Metadata-Flavor: Google`. |
| **Azure** | Exige `Metadata: true` y versión de API. |
| **Contenedor** | El camino de red puede estar bloqueado aunque exista SSRF externa. |

## 🔗 Cadenas y dependencias

La cadena SSRF→credenciales→acceso cloud solo es válida si se prueban fetch, acceso a metadata, obtención de credencial y permisos, cada uno por separado.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Potencialmente grave, pero una callback externa o `169.254.169.254` en una URL no confirma acceso a credenciales. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar una función fetch del servidor y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en servicio de metadatos del entorno cloud.
- Confirmar: En laboratorio propio se observa acceso a un campo no secreto; en programas reales no consultar credenciales ni tokens sin autorización expresa.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Bloquear metadata en egress cuando no se use, aplicar protecciones del proveedor y mínimo privilegio IAM. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: SSRF](https://portswigger.net/web-security/ssrf) — variantes y confirmación.
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) — clasificación de riesgos API.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
