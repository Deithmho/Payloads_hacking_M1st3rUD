# 🗡️ Divulgación de información: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Mapa de fuentes

**Objetivo:** Comprobar exposición de source map y clasificar contenido.

```http
GET /static/app.js.map HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Confirmar formato de mapa, fuentes y datos sensibles; un 200 HTML de SPA no cuenta.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/information-disclosure/exploiting).

### 2. Cabecera sourceMappingURL

**Objetivo:** Detectar referencia pública en el bundle cargado por la aplicación.

```bash
curl -s "https://{ORIGEN}/static/app.js" | rg -o "sourceMappingURL=[^ ]+"
```

**Interpretación:** El enlace puede apuntar a mapa inexistente o inocuo; no publicar secretos extraídos.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/information-disclosure/exploiting).

### 3. Archivo de respaldo conocido

**Objetivo:** Comprobar si una copia de un archivo propio quedó servida.

```http
GET /config.json.bak HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Validar tipo de contenido y procedencia; evitar enumeración masiva y redactar valores.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/information-disclosure/exploiting).

### 4. Metadatos Git

**Objetivo:** Comprobar si el directorio de control de versiones es accesible.

```http
GET /.git/HEAD HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** La cadena ref: confirma exposición parcial; no clonar historia completa sin autorización.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/information-disclosure/exploiting).

### 5. Error de parsing acotado

**Objetivo:** Solicitar error controlado para observar stack traces.

```http
POST /api/v1/test HTTP/1.1
Host: {ORIGEN}
Content-Type: application/json

{
```

**Interpretación:** Información interna en error requiere evaluar sensibilidad y alcance; usar endpoint de prueba.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/information-disclosure).

### 6. Índice de directorio

**Objetivo:** Comprobar si una carpeta pública lista archivos no destinados a usuarios.

```http
GET /uploads/ HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Un listado público puede ser intencional; demostrar acceso a archivo sensible permitido por el alcance.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/information-disclosure/exploiting).

### 7. Robots como pista

**Objetivo:** Revisar rutas declaradas públicamente sin considerarlas hallazgo automático.

```http
GET /robots.txt HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Las rutas de robots no son secretos; validar acceso y datos antes de reportar.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/information-disclosure).

### 8. Verbose API

**Objetivo:** Comprobar si un modo de depuración controlado expone detalles internos.

```http
GET /api/v1/health?debug=true HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** El parámetro debe existir para ser relevante; no deducir exposición de una respuesta genérica.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/information-disclosure).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
