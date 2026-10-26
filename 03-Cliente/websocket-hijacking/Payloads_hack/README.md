# 🗡️ Cross-Site WebSocket Hijacking: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Origen externo

**Objetivo:** Comparar handshake entre orígenes.

```http
GET /ws HTTP/1.1
Host: {ORIGEN}
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: https://{CONTROLLED_HOST}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Confirmar en navegador si la cookie se envía y si llegan mensajes; curl no reproduce toda la política.

### 2. Origen legítimo

**Objetivo:** Control positivo del mismo canal.

```http
GET /ws HTTP/1.1
Host: {ORIGEN}
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: https://{ORIGEN}
```

**Interpretación:** Comparar códigos y permisos de mensajes con el origen externo.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
