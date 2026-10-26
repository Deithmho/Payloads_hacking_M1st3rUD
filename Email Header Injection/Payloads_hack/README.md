# 🗡️ Email header injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Cc y Bcc a buzones propios

```text
Prueba%0d%0aCc:%20{EMAIL_PROPIO_2}
Prueba%0d%0aBcc:%20{EMAIL_PROPIO_2}
Prueba%0aCc:%20{EMAIL_PROPIO_2}
```

**Cuándo usarlo:** Cada línea es un valor de campo, no un mensaje completo. Enviar una sola notificación de prueba a direcciones propias y revisar fuente MIME cruda.

**Fuente:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).


### Control literal y doble codificación

```text
Prueba-Cc-{EMAIL_PROPIO_2}
Prueba%250d%250aCc:%20{EMAIL_PROPIO_2}
Prueba%0d%0aX-Prueba:%20canary-{NONCE}
```

**Cuándo usarlo:** El control separa reflejo de nueva cabecera. Doble codificación solo funciona si hay doble decodificación; X-Prueba evita añadir destinatarios.

**Fuente:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).


## 🧭 Payloads por contexto

### Campo de asunto de formulario

```text
Consulta%0d%0aX-Prueba:%20canary-{NONCE}
Consulta%0d%0aReply-To:%20{EMAIL_PROPIO_2}
```

**Cuándo usarlo:** Probar solo si el asunto se inserta en cabeceras sin API estructurada. Confirmar mensaje crudo y que Reply-To apunta a buzón propio.

**Fuente:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).


### Nombre visible o dirección de remitente

```text
Nombre%0d%0aX-Prueba:%20canary-{NONCE}
Nombre%0d%0aCc:%20{EMAIL_PROPIO_2}
```

**Cuándo usarlo:** Aplicable a campos que el backend coloca en From/Reply-To. Bibliotecas de correo modernas suelen rechazar CR/LF.

**Fuente:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).


## 🔥 Payloads avanzados

### Separación de cabecera y cuerpo

```text
Prueba%0d%0aX-Prueba:%20canary-{NONCE}%0d%0a%0d%0acuerpo-canary-{NONCE}
Prueba%250d%250aX-Prueba:%20canary-{NONCE}%250d%250a%250d%250acuerpo-canary-{NONCE}
```

**Cuándo usarlo:** Solo mensaje de laboratorio hacia buzones propios. Comprobar si el cuerpo quedó alterado; no usar adjuntos ni correos a terceros.

**Fuente:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).


## 🔬 Pruebas guiadas por escenario

### 1. Cc por CRLF

**Objetivo:** Campo de nombre/asunto que se copie literalmente a una cabecera; ambas bandejas son del tester.

```text
Prueba%0D%0ACc:%20{EMAIL_PROPIO_2}
```

**Interpretación:** Confirmar cabecera Cc en fuente cruda del correo y recepción en segunda bandeja; no solo eco HTML.

**Fuente técnica:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 2. Bcc por CRLF

**Objetivo:** Usar únicamente destinatario secundario propio.

```text
Prueba%0D%0ABcc:%20{EMAIL_PROPIO_2}
```

**Interpretación:** Una copia Bcc recibida demuestra alteración de destinatarios; borrar correo de prueba.

**Fuente técnica:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 3. Reply-To inyectado

**Objetivo:** Evaluar si la app acepta cambiar la dirección de respuesta por cabecera añadida.

```text
Prueba%0D%0AReply-To:%20{EMAIL_PROPIO_2}
```

**Interpretación:** Inspeccionar cabeceras originales; algunos MTA reescriben Reply-To y bloquean el efecto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 4. Subject adicional

**Objetivo:** Probar sustitución de asunto en mensaje a cuenta propia.

```text
Prueba%0D%0ASubject:%20marcador-123
```

**Interpretación:** Los clientes pueden mostrar el primer o último Subject; revisar fuente y ruta SMTP.

**Fuente técnica:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 5. LF aislado

**Objetivo:** Cuando CRLF se filtra pero se sospecha tolerancia de LF solo.

```text
Prueba%0ACc:%20{EMAIL_PROPIO_2}
```

**Interpretación:** Debe crearse una nueva cabecera efectiva; el texto dentro de Subject no basta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 6. Doble decodificación

**Objetivo:** Solo si hay indicio de dos etapas de URL decode.

```text
Prueba%250D%250ABcc:%20{EMAIL_PROPIO_2}
```

**Interpretación:** El literal %0D%0A en el correo no es inyección; confirmar destinatario de prueba.

**Fuente técnica:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 7. Control sin delimitador

**Objetivo:** Sirve para descartar que el segundo correo sea una función legítima del formulario.

```text
Prueba-Bcc-{EMAIL_PROPIO_2}
```

**Interpretación:** El control no debe agregar destinatarios; si lo hace, investigar lógica del formulario.

**Fuente técnica:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 8. From inyectado por salto de línea

**Objetivo:** El campo nombre/asunto entra en cabeceras SMTP y el mensaje va solo a una bandeja del tester.

```text
Prueba%0D%0AFrom:%20{EMAIL_PROPIO_2}
```

**Interpretación:** Comparar `From` y `Sender` en fuente cruda; un MTA puede reescribir el remitente y bloquear el efecto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/kb/issues/00200800_smtp-header-injection).

### 9. Destinatario adicional sin salto de línea

**Objetivo:** Solo cuando la aplicación copia un correo de usuario directamente en la lista To; ambas direcciones son propias.

```text
{EMAIL_PROPIO_1},{EMAIL_PROPIO_2}
```

**Interpretación:** La entrega a dos bandejas indica interpretación de lista, no CRLF; confirmar que el contrato permitía solo un destinatario.

**Fuente técnica:** [www.rfc-editor.org](https://www.rfc-editor.org/rfc/rfc5322.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
