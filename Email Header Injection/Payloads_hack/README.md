# 🗡️ Email header injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Cc por CRLF

**Objetivo:** Campo de nombre/asunto que se copie literalmente a una cabecera; ambas bandejas son del tester.

```text
Prueba%0D%0ACc:%20{EMAIL_PROPIO_2}
```

**Interpretación:** Confirmar cabecera Cc en fuente cruda del correo y recepción en segunda bandeja; no solo eco HTML.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 2. Bcc por CRLF

**Objetivo:** Usar únicamente destinatario secundario propio.

```text
Prueba%0D%0ABcc:%20{EMAIL_PROPIO_2}
```

**Interpretación:** Una copia Bcc recibida demuestra alteración de destinatarios; borrar correo de prueba.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 3. Reply-To inyectado

**Objetivo:** Evaluar si la app acepta cambiar la dirección de respuesta por cabecera añadida.

```text
Prueba%0D%0AReply-To:%20{EMAIL_PROPIO_2}
```

**Interpretación:** Inspeccionar cabeceras originales; algunos MTA reescriben Reply-To y bloquean el efecto.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 4. Subject adicional

**Objetivo:** Probar sustitución de asunto en mensaje a cuenta propia.

```text
Prueba%0D%0ASubject:%20marcador-123
```

**Interpretación:** Los clientes pueden mostrar el primer o último Subject; revisar fuente y ruta SMTP.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 5. LF aislado

**Objetivo:** Cuando CRLF se filtra pero se sospecha tolerancia de LF solo.

```text
Prueba%0ACc:%20{EMAIL_PROPIO_2}
```

**Interpretación:** Debe crearse una nueva cabecera efectiva; el texto dentro de Subject no basta.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 6. Doble decodificación

**Objetivo:** Solo si hay indicio de dos etapas de URL decode.

```text
Prueba%250D%250ABcc:%20{EMAIL_PROPIO_2}
```

**Interpretación:** El literal %0D%0A en el correo no es inyección; confirmar destinatario de prueba.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 7. Control sin delimitador

**Objetivo:** Sirve para descartar que el segundo correo sea una función legítima del formulario.

```text
Prueba-Bcc-{EMAIL_PROPIO_2}
```

**Interpretación:** El control no debe agregar destinatarios; si lo hace, investigar lógica del formulario.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
