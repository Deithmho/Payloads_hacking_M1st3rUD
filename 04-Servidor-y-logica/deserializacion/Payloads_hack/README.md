# 🗡️ Deserialización insegura: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Tipo inesperado

**Objetivo:** Comprobar aceptación de formato, sin gadgets.

```text
{BLOB_SERIALIZADO_PROPIO_CON_CAMPO_INOCUO_CAMBIADO}
```

**Interpretación:** El rechazo seguro no es vulnerabilidad; errores específicos solo ayudan a identificar tecnología.

### 2. Firma alterada

**Objetivo:** Verificar rechazo de una cookie propia modificada.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: state={BLOB_PROPIO_CON_UN_BYTE_CAMBIADO}
```

**Interpretación:** Debe rechazarse o crear sesión anónima; no usar payloads gadget en producción.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
