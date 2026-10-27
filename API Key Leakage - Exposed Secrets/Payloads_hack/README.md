# 🗡️ Exposición de API keys y secretos: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Rutas y artefactos candidatos

```text
/config.json
/static/app.js
/static/app.js.map
/.env
/.env.example
/manifest.json
```

**Cuándo usarlo:** Un 200 puede ser el fallback de SPA; verificar tipo/contenido y nunca copiar valores secretos al informe.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks).


### Nombres de variables que merecen clasificación

```text
apiKey
clientId
clientSecret
accessToken
authorization
secretKey
```

**Cuándo usarlo:** La presencia de un nombre no demuestra fuga: muchas claves de cliente son públicas por diseño.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks).


## 🧭 Payloads por contexto

### Búsqueda local que devuelve solo nombres de archivo

```bash
rg -l -i '(api[_-]?key|client_secret|access_token)' ./dist
rg -l -i '(secret|token|authorization)' ./dist/*.map
git log --all --name-only --pretty=format: | rg -i '(\.env|secret|credential)'
```

**Cuándo usarlo:** Solo sobre una copia autorizada; evitar imprimir o conservar valores de tokens.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks).


## 🔥 Payloads avanzados

### Verificación de alcance sin modificar recursos

```http
GET {RUTA_DOCUMENTADA_DE_IDENTIDAD} HTTP/1.1
Host: {PROVEEDOR_AUTORIZADO}
Authorization: Bearer {CLAVE_CANDIDATA_PROPIA}

GET {RUTA_DOCUMENTADA_DE_IDENTIDAD} HTTP/1.1
Host: {PROVEEDOR_AUTORIZADO}
X-API-Key: {CLAVE_CANDIDATA_PROPIA}
```

**Cuándo usarlo:** Dos solicitudes alternativas: elegir únicamente la cabecera documentada por el proveedor y una ruta de solo lectura. Solo si el programa autoriza comprobar la clave; identificar tipo, restricción y permisos sin exponerla.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks).


## 🔬 Pruebas guiadas por escenario

### 1. Ficheros JS candidatos

**Objetivo:** Buscar nombres de archivos sin volcar valores de credenciales.

```bash
rg -l -i "(api[_-]?key|secret|token|client_secret)" ./dist
```

**Interpretación:** Una coincidencia es candidata; distinguir clave pública de secreto servidor.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/API%20Key%20Leaks/README.md).

### 2. Source map publicado

**Objetivo:** Comprobar si un bundle enlaza código fuente de desarrollo.

```bash
curl -I "https://{ORIGEN}/static/app.js.map"
```

**Interpretación:** Un 200 puede ser fallback SPA; validar Content-Type y mapa real sin descargar secretos masivamente.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/information-disclosure).

### 3. Configuración pública

**Objetivo:** Revisar un endpoint de configuración intencionado para cliente.

```http
GET /config.json HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Clasificar cada clave por restricciones y scopes; una clave de navegador puede ser pública.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/API%20Key%20Leaks/README.md).

### 4. Variables embebidas en HTML

**Objetivo:** Localizar datos de bootstrap sin imprimir valores completos.

```bash
curl -s "https://{ORIGEN}/" | rg -o "(window\.__[A-Z_]+__|apiKey|clientId)" | sort -u
```

**Interpretación:** Solo nombres de campos. Verificar si el valor es secreto antes de informarlo.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/API%20Key%20Leaks/README.md).

### 5. Ruta de identidad inocua

**Objetivo:** Validar vigencia de una credencial solo si el programa lo autoriza.

```http
GET /v1/whoami HTTP/1.1
Host: {PROVEEDOR_AUTORIZADO}
Authorization: Bearer {CLAVE_CANDIDATA}
```

**Interpretación:** No imprimir ni registrar token; detenerse tras scopes/identidad y no modificar recursos.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/API%20Key%20Leaks/README.md).

### 6. Búsqueda en historial Git local

**Objetivo:** Identificar rutas de secretos en repo propio sin mostrar el valor.

```bash
git log --all --name-only --pretty=format: | rg -i "(^|/)(\.env|secrets?|credentials?)(/|\.|$)" | sort -u
```

**Interpretación:** Solo repositorios autorizados. Si existe secreto, rotar y redactar antes de cualquier evidencia pública.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/API%20Key%20Leaks/README.md).

### 7. Restricción por origen

**Objetivo:** Comprobar si una clave de navegador está restringida a la app autorizada.

```http
GET /v1/test-readonly HTTP/1.1
Host: {PROVEEDOR_AUTORIZADO}
Origin: https://{CONTROLLED_HOST}
X-API-Key: {CLAVE_CANDIDATA}
```

**Interpretación:** Una respuesta 200 a curl no prueba uso desde navegador ni falta de restricciones de backend.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/API%20Key%20Leaks/README.md).

### 8. Clave como parámetro URL de prueba

**Objetivo:** Comprobar si una ruta propaga credenciales en Referer o historial.

```http
GET /api/test?api_key=CANARY-{NONCE} HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Usar solo canary. Un secreto real en query puede filtrarse a logs/Referer; no colocarlo en este PoC.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/API%20Key%20Leaks/README.md).

### 9. Contenido de mapa local

**Objetivo:** Localizar mapas propios que mencionan credenciales sin mostrar valores.

```bash
rg -l -i "(authorization|client_secret|api[_-]?key)" ./dist/*.map
```

**Interpretación:** Una coincidencia es candidata; revisar restricciones y redactar antes de compartir evidencia.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/API%20Key%20Leaks/README.md).

### 10. Historial de cambios en repo propio

**Objetivo:** Localizar commits que tocaron archivos de configuración.

```bash
git log --all --oneline -- .env.example config.json
```

**Interpretación:** El nombre del archivo no confirma secreto filtrado. Revisar historial solo si el repositorio está autorizado.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/API%20Key%20Leaks/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
