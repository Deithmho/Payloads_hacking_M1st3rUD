# 📖 Vulnerabilidades de subida de archivos: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un archivo aportado por cliente pasa por validación de tipo, nombre, contenido, almacenamiento y publicación. Errores en cualquiera de esas fases pueden permitir servir HTML activo, sobrescribir rutas o ejecutar contenido.

El límite de confianza relevante es **archivo, nombre y Content-Type de multipart frente a procesamiento y almacenamiento**. La aplicación recibe **archivo, nombre y Content-Type de multipart** y debería **validar contenido, renombrar y servir desde dominio no ejecutable**. La vulnerabilidad aparece cuando **se confía en metadatos o extensión aportados por cliente**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza archivo, nombre y Content-Type de multipart en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en procesamiento y almacenamiento.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se confía en metadatos o extensión aportados por cliente.
4. **Observación:** Un archivo marcador propio se almacena y sirve con un tipo o ubicación inesperados; no subir web shells en producción.

## 🧭 Contextos y variantes

**Dónde buscar:** avatares, documentos, CSV, imágenes y archivos comprimidos.

| Variante | Diferencia técnica |
| --- | --- |
| **Tipo MIME** | El servidor confía en Content-Type cliente. |
| **Doble extensión** | Servidor y aplicación interpretan extensión diferente. |
| **SVG/HTML** | Contenido activo se sirve bajo origen de la aplicación. |
| **Nombre/ruta** | El nombre controla destino de almacenamiento. |

## 🔗 Cadenas y dependencias

Un SVG activo en origen de la aplicación puede llevar a XSS; una extracción ZIP vulnerable puede llevar a Zip Slip. Cada procesamiento tiene su propia prueba.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Depende de ejecución, mismo origen y ruta accesible. Aceptar un archivo no significa que pueda ejecutarse. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar archivo, nombre y Content-Type de multipart y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en procesamiento y almacenamiento.
- Confirmar: Un archivo marcador propio se almacena y sirve con un tipo o ubicación inesperados; no subir web shells en producción.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Validar magic bytes y esquema, renombrar, almacenar fuera del webroot y servir con `Content-Disposition` y dominio separados. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: file upload](https://portswigger.net/web-security/file-upload) — almacenamiento y ejecución.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
