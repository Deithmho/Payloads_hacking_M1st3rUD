# 📖 Zip Slip: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un extractor usa el nombre de entrada de un ZIP como ruta de salida. Entradas con `../` o rutas absolutas pueden escribir fuera del directorio de extracción si no se valida la ruta canónica.

El límite de confianza relevante es **nombres de archivos dentro de un archivo comprimido frente a extractor del servidor**. La aplicación recibe **nombres de archivos dentro de un archivo comprimido** y debería **resolver cada destino y restringirlo al directorio base**. La vulnerabilidad aparece cuando **se escribe usando la ruta archivada sin normalizar**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza nombres de archivos dentro de un archivo comprimido en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en extractor del servidor.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se escribe usando la ruta archivada sin normalizar.
4. **Observación:** En laboratorio propio, una entrada crea un archivo marcador fuera de la carpeta de extracción y se elimina después.

## 🧭 Contextos y variantes

**Dónde buscar:** importadores, plugins, backups y procesamiento de entregables.

| Variante | Diferencia técnica |
| --- | --- |
| **Traversal relativo** | `../` escapa del destino. |
| **Ruta absoluta** | El archivo declara ubicación raíz. |
| **Symlink** | Un enlace dentro del archivo puede redirigir una escritura posterior. |

## 🔗 Cadenas y dependencias

Si el destino escapado es un directorio ejecutable, Zip Slip puede convertirse en ejecución; no declarar RCE sin observar ejecución del marcador benigno.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede sobrescribir archivos de la aplicación. La prueba se limita a un directorio de laboratorio para evitar corrupción. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar nombres de archivos dentro de un archivo comprimido y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en extractor del servidor.
- Confirmar: En laboratorio propio, una entrada crea un archivo marcador fuera de la carpeta de extracción y se elimina después.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Normalizar cada ruta, rechazar absolutos y traversal, controlar symlinks y extraer con permisos mínimos. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [PortSwigger: file upload](https://portswigger.net/web-security/file-upload) — almacenamiento y ejecución.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
