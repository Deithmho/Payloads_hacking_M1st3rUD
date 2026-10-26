# 🗡️ Exposición de API keys y secretos: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Ficheros JS candidatos

**Objetivo:** Buscar nombres de archivos sin volcar valores de credenciales.

```bash
rg -l -i "(api[_-]?key|secret|token|client_secret)" ./dist
```

**Interpretación:** Una coincidencia es candidata; distinguir clave pública de secreto servidor.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks).

### 2. Source map publicado

**Objetivo:** Comprobar si un bundle enlaza código fuente de desarrollo.

```bash
curl -I "https://{ORIGEN}/static/app.js.map"
```

**Interpretación:** Un 200 puede ser fallback SPA; validar Content-Type y mapa real sin descargar secretos masivamente.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/information-disclosure).

### 3. Configuración pública

**Objetivo:** Revisar un endpoint de configuración intencionado para cliente.

```http
GET /config.json HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Clasificar cada clave por restricciones y scopes; una clave de navegador puede ser pública.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks).

### 4. Variables embebidas en HTML

**Objetivo:** Localizar datos de bootstrap sin imprimir valores completos.

```bash
curl -s "https://{ORIGEN}/" | rg -o "(window\.__[A-Z_]+__|apiKey|clientId)" | sort -u
```

**Interpretación:** Solo nombres de campos. Verificar si el valor es secreto antes de informarlo.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks).

### 5. Ruta de identidad inocua

**Objetivo:** Validar vigencia de una credencial solo si el programa lo autoriza.

```http
GET /v1/whoami HTTP/1.1
Host: {PROVEEDOR_AUTORIZADO}
Authorization: Bearer {CLAVE_CANDIDATA}
```

**Interpretación:** No imprimir ni registrar token; detenerse tras scopes/identidad y no modificar recursos.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks).

### 6. Búsqueda en historial Git local

**Objetivo:** Identificar rutas de secretos en repo propio sin mostrar el valor.

```bash
git log --all --name-only --pretty=format: | rg -i "(^|/)(\.env|secrets?|credentials?)(/|\.|$)" | sort -u
```

**Interpretación:** Solo repositorios autorizados. Si existe secreto, rotar y redactar antes de cualquier evidencia pública.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks).

### 7. Restricción por origen

**Objetivo:** Comprobar si una clave de navegador está restringida a la app autorizada.

```http
GET /v1/test-readonly HTTP/1.1
Host: {PROVEEDOR_AUTORIZADO}
Origin: https://{CONTROLLED_HOST}
X-API-Key: {CLAVE_CANDIDATA}
```

**Interpretación:** Una respuesta 200 a curl no prueba uso desde navegador ni falta de restricciones de backend.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
