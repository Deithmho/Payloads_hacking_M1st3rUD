# 📖 Path Traversal y LFI: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Cuando una ruta proporcionada por usuario se concatena a un directorio base, segmentos `../` o decodificaciones sucesivas pueden salir del directorio permitido. LFI añade inclusión del archivo en una respuesta o intérprete.

El límite de confianza relevante es **un nombre de archivo o ruta frente a el resolvedor de archivos servidor**. La aplicación recibe **un nombre de archivo o ruta** y debería **resolver ruta canónica y restringir al directorio previsto**. La vulnerabilidad aparece cuando **la ruta final escapa del directorio permitido**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un nombre de archivo o ruta en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en el resolvedor de archivos servidor.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si la ruta final escapa del directorio permitido.
4. **Observación:** Se lee un archivo marcador de prueba colocado fuera de la carpeta esperada; no usar archivos del sistema ni secretos.

## 🧭 Contextos y variantes

**Dónde buscar:** descargas, plantillas, imágenes, logs y visores de documentos.

| Variante | Diferencia técnica |
| --- | --- |
| **Traversal simple** | `../` sale del directorio. |
| **Doble codificación** | Una capa decodifica después de validar. |
| **LFI** | El contenido se incluye o interpreta en vez de descargarse. |

## 🔗 Cadenas y dependencias

La lectura de logs y una inyección previa podrían encadenarse a ejecución si el intérprete incluye el log; demostrar ambos pasos sin dejar persistencia.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Depende del archivo accesible y de si se interpreta. Leer un archivo público por otra ruta puede no tener impacto. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un nombre de archivo o ruta y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en el resolvedor de archivos servidor.
- Confirmar: Se lee un archivo marcador de prueba colocado fuera de la carpeta esperada; no usar archivos del sistema ni secretos.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Resolver ruta real y comprobar pertenencia, usar IDs de archivo y negar rutas arbitrarias; separar almacenamiento de ejecución. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: path traversal](https://portswigger.net/web-security/file-path-traversal) — normalización de rutas.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [PayloadsAllTheThings: directory traversal](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md) — familias de codificación y normalización.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
